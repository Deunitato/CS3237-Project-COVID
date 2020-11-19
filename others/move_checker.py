import random
import time

'''
Works by constantly adding into buffer of size 3 and checking if all is a slash or all is a stab, 
and sends the result to MQTT

- if stable, it'll continue
- else it will sleep for 0.5s
'''
moves = ['stable', 'slash', 'stab']
move_buffer = [0, 0, 0]
counter = 0
moves2 = ['stable', 'stable', 'stable']

while(True):
    move_buffer[counter] = moves[random_move]
    counter = counter + 1

    if(counter == 3):
        counter = 0

    if(move_buffer[:-1] == move_buffer[1:] and move_buffer[0] != 'stable'):
        print("3 Moves")
        print(move_buffer[0])
        time.sleep(0.5)

    time.sleep(0.1) 