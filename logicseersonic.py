import sys
import os
import json
os.chdir(sys.path[0])

from time import sleep
from seersoniciapdev import CSeerSonicIapDev
from seersonicchardev import CSeerSonicCharDev
from iapdev import CIapDev

try:
    with open('..\\User\\ipconfig.json', 'r') as f:
        data = json.load(f)
        f.close()
    F4K_ip = data['inet addr']

except:
    F4K_ip = '192.168.192.4'

if(2 == len(sys.argv)):
    bin_file = sys.argv[1]
    #*.gyro.bin
    tail2 = bin_file[-7:-4]
    if tail2 != '.ss':
        print('not the firmware for seer controller, press enter to continue...')
        input()
        sys.exit()
else:
    bin_file = '../Output/Project.bin'

BOOTLOADER_START_ADDR = 0x08000000
BOOTPARAM_ADDR = 0x08007800
APP_START_ADDR = 0x08008000
chardev = CSeerSonicCharDev((F4K_ip, 15003), (F4K_ip, 15003))
# chardev = CSeerSonicCharDev(('127.0.0.1', 9999), ('127.0.0.1', 9999))
udpIapDev = CSeerSonicIapDev(chardev)
# udpIapDev.resetBoard()
udpIapDev.setforwardmode()
# udpIapDev.resettargetboard()
udpIapDev.settargetboardbootloader()
FWV = udpIapDev.getbootloaderversion()
print('firmware version V%X.%X' % (FWV >> 4, FWV & 0xF))
# udpIapDev.loadbin(bin_file, APP_START_ADDR)
udpIapDev.loaduint32(0xaaaa5555, BOOTPARAM_ADDR)
udpIapDev.jumpToAddress(APP_START_ADDR)
udpIapDev.resetforwardmode()

os.system('pause')
sys.exit()
