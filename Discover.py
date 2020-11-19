"""
Scan/Discovery
--------------

Example showing how to scan for BLE devices.

Updated on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>

"""

import asyncio
from bleak import discover

sensorMacadd = "00"

async def run():
    global sensorMacadd
    devices = await discover()
    for d in devices:
        #print(d)
        if "CC2650 SensorTag" in d.name:
            sensorMacadd = d.address
            print(d.address)

def getSensorAdd():
    global sensorMacadd
    return sensorMacadd

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

if __name__ == '__main__':
    main()
