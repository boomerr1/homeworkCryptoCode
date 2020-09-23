from oracle import *
import sys

if len(sys.argv) < 2:
    print("Usage: python sample.py <filename>")
    sys.exit(-1)

f = open(sys.argv[1])
data = f.read()
f.close()

ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]

def find_padding(data):
    ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]
    for i in range(len(ctext)-1):
        ctext[i] = ctext[i]^1
        Oracle_Connect()
        rc = Oracle_Send(ctext, 3)
        # 1 means succeeded, 0 or -1 means error
        if rc != 1:
            print(i)
            return
        Oracle_Disconnect()
    return

# find_padding(data)
# This function returns 21. This means that in block 3 all the characters until the last 12 last characters are text and the rest padding.

def first_block(data):
    IV = [0]*16
    resultlist = []
    ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]
    for current_searched in range(15, -1, -1):
        for i in range(31, current_searched, -1):
            ctext[i] = (ctext[i]^(16-current_searched))^(16-current_searched+1)
        for j in range(256):
            IV[current_searched] = j
            Oracle_Connect()
            rc = Oracle_Send(IV+ctext[:16], 2)
            if rc == 1:
                resultlist.append(j)
                break
            Oracle_Disconnect()
    return resultlist

first_block(data)

def second_block(data):
    counter = 0
    resultlist = []
    ctext = [(int(data[i:i+2],16)) for i in range(0, len(data), 2)]
    for current_searched in range(20, 15, -1):
        for i in range(31, current_searched, -1):
            ctext[i] = (ctext[i]^(31-current_searched))^(31-current_searched+1)
        for j in range(256):
            ctext[current_searched] = j
            Oracle_Connect()
            rc = Oracle_Send(ctext, 3)
            if rc == 1:
                resultlist.append(j)
                counter += 1
                break
            Oracle_Disconnect()
    return resultlist

# print(second_block(data))
# second_block(ctext) gives: [97,233,231,31,208] with the 11 other characters being the padding value 11. 

# final = []
# for block_num, (c1, c2) in enumerate(zip(blocks, blocks[1:])):
#     IV = [0] * 16
#     P = [0] * 16
#     for i in range(15,-1,-1):
#         print(i)
#         for b in range(0,256):
#             firstpart = c1[:i]
#             padingbt = 16-i
#             suffix = [padingbt ^ value for value in IV[i+1:]]
#             evil_c1 = firstpart + [b] + suffix
#             Oracle_Connect()
#             rc = Oracle_Send(evil_c1+c2, 2)
#             if rc == 1:
#                 IV[i] = evil_c1[i] ^ padingbt
#                 P[i] = c1[i] ^ IV[i]
#                 print(chr(c1[i] ^ IV[i]))
#                 break
#             Oracle_Disconnect()
#     final+=P
#     print(final)
# print(final)

# This code takes a really long time after finding block 1, because it then can't find block 2 and 3.


