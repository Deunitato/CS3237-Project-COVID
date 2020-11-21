# -*- coding: utf-8 -*-
"""
TI CC2650 SensorTag
-------------------

Adapted by Ashwin from the following sources:
 - https://github.com/IanHarvey/bluepy/blob/a7f5db1a31dba50f77454e036b5ee05c3b7e2d6e/bluepy/sensortag.py
 - https://github.com/hbldh/bleak/blob/develop/examples/sensortag.py

"""
import asyncio
import datetime
import platform
import struct
import time
import json
import numpy as np

from tensorflow import keras
from bleak import BleakClient
from MQTTDATA import Publisher
import Discover as discover

MAC_DICTIONARY = {"CC:78:AB:7F:1E:02": 1, "F0:F8:F2:86:BD:80" : 2}

model2 = keras.models.load_model('1DCNN-test/modelTest')
mqtt_pub = Publisher("data/moves", "18.140.67.252", 1883, "charlotte", "charlotteiscool")

reading = np.zeros((1,20,6))
class Service:
    """
    Here is a good documentation about the concepts in ble;
    https://learn.adafruit.com/introduction-to-bluetooth-low-energy/gatt

    In TI SensorTag there is a control characteristic and a data characteristic which define a service or sensor
    like the Light Sensor, Humidity Sensor etc

    Please take a look at the official TI user guide as well at
    https://processors.wiki.ti.com/index.php/CC2650_SensorTag_User's_Guide
    """

    def __init__(self):
        self.data_uuid = None
        self.ctrl_uuid = None
        self.period_uuid = None

    async def read(self, client):
        raise NotImplementedError()


class Sensor(Service):

    def callback(self, sender: int, data: bytearray):
        raise NotImplementedError()

    async def enable(self, client, *args):
        # start the sensor on the device
        write_value = bytearray([0x01])
        await client.write_gatt_char(self.ctrl_uuid, write_value)
        write_value = bytearray([0x0A]) # check the sensor period applicable values in the sensor tag guide mentioned above
        await client.write_gatt_char(self.period_uuid, write_value)

        return self

    async def read(self, client):
        val = await client.read_gatt_char(self.data_uuid)
        return self.callback(1, val)


class MovementSensorMPU9250SubService:

    def __init__(self):
        self.bits = 0

    def enable_bits(self):
        return self.bits

    def cb_sensor(self, data):
        raise NotImplementedError


class MovementSensorMPU9250(Sensor):
    GYRO_XYZ = 7
    ACCEL_XYZ = 7 << 3
    MAG_XYZ = 1 << 6
    ACCEL_RANGE_2G  = 0 << 8
    ACCEL_RANGE_4G  = 1 << 8
    ACCEL_RANGE_8G  = 2 << 8
    ACCEL_RANGE_16G = 3 << 8

    def __init__(self, MAC_ADDRESS):
        super().__init__()
        self.data_uuid = "f000aa81-0451-4000-b000-000000000000"
        self.ctrl_uuid = "f000aa82-0451-4000-b000-000000000000"
        self.ctrlBits = 0
        self.MAC_ADDRESS = MAC_ADDRESS

        self.sub_callbacks = []

    def register(self, cls_obj: MovementSensorMPU9250SubService):
        self.ctrlBits |= cls_obj.enable_bits()
        self.sub_callbacks.append(cls_obj.cb_sensor)

    async def start_listener(self, client, *args):
        # start the sensor on the device
        await client.write_gatt_char(self.ctrl_uuid, struct.pack("<H", self.ctrlBits))

        # listen using the handler
        await client.start_notify(self.data_uuid, self.callback)

    def callback(self, sender: int, data: bytearray):
        global model2,reading
        resultLabel = ["stable","slash","stab"]
        unpacked_data = struct.unpack("<hhhhhhhhh", data)
        dataDict = {}
        for cb in self.sub_callbacks:
            value = cb(unpacked_data)
            dataDict.update(value)
        #print("[MovementSensor] Final dict:", dataDict)
        rowData = np.array([float(dataDict["accelX"]),float(dataDict["accelY"]),
            float(dataDict["accelZ"]),float(dataDict["gyroX"]),
            float(dataDict["gyroY"]),float(dataDict["gyroZ"])])
        reading = np.delete(reading,0,1)
        reading = np.hstack((reading,[[rowData]]))
        result = model2.predict(reading)
        y= np.argmax(result,axis=1)
        #print(resultLabel[int(y)])
        #mqtt_pub.publish(json.dumps(dataDict))
        msgDict = {"player": MAC_DICTIONARY[self.MAC_ADDRESS], "prediction": resultLabel[int(y)]}
        print(msgDict)
        mqtt_pub.publish(json.dumps(msgDict))


class AccelerometerSensorMovementSensorMPU9250(MovementSensorMPU9250SubService):
    def __init__(self):
        super().__init__()
        self.bits = MovementSensorMPU9250.ACCEL_XYZ | MovementSensorMPU9250.ACCEL_RANGE_4G
        self.scale = 8.0/32768.0 # TODO: why not 4.0, as documented? @Ashwin Need to verify

    def cb_sensor(self, data):
        '''Returns (x_accel, y_accel, z_accel) in units of g'''
        rawVals = data[3:6]
        valueTup = tuple([ v*self.scale for v in rawVals ])
        dictValue = {"accelX" : valueTup[0] , "accelY": valueTup[1], "accelZ": valueTup[2]}
        #print("[MovementSensor] Accelerometer:", dictValue)
        return dictValue


class GyroscopeSensorMovementSensorMPU9250(MovementSensorMPU9250SubService):
    def __init__(self):
        super().__init__()
        self.bits = MovementSensorMPU9250.GYRO_XYZ
        self.scale = 500.0/65536.0

    def cb_sensor(self, data):
        '''Returns (x_gyro, y_gyro, z_gyro) in units of degrees/sec'''
        rawVals = data[0:3]
        valueTup = tuple([ v*self.scale for v in rawVals ])
        dictValue = {"gyroX" : valueTup[0] , "gyroY": valueTup[1], "gyroZ": valueTup[2]}
        #print("[MovementSensor] Gyroscope:", dictValue)
        return dictValue



async def run(address):
    async with BleakClient(address) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))

        acc_sensor = AccelerometerSensorMovementSensorMPU9250()
        gyro_sensor = GyroscopeSensorMovementSensorMPU9250()

        movement_sensor = MovementSensorMPU9250(address)
        movement_sensor.register(acc_sensor)
        movement_sensor.register(gyro_sensor)
        await movement_sensor.start_listener(client)



        while True:
            # set according to your period in the sensors; otherwise sensor will return same value for all the readings
            # till the sensor refreshes as defined in the period
            await asyncio.sleep(0.1)  # slightly less than 100ms to accommodate time to print results
            #print("Tick Tock")


if __name__ == "__main__":
    """
    To find the address, once your sensor tag is blinking the green led after pressing the button, run the discover.py
    file which was provided as an example from bleak to identify the sensor tag device
    """

    import os
    import sys

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    discover.main()
    add = discover.getSensorAdd()
    if add == "00":
        print("ERROR: Cannot find device!")
        sys.exit()
    print("DEVICE FOUND: " + add + "\n")
    address = (
        add
        if platform.system() != "Darwin"
        else "6FFBA6AE-0802-4D92-B1CD-041BE4B4FEB9"
    )
    mqtt_pub.run()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address))
    loop.run_forever()
