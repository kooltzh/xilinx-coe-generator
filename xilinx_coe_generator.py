import re
from shutil import copyfile
import configparser

# Loading available config
config = configparser.ConfigParser()
config.read('config.ini')

if 'USER' in config:
    allSetting = config['USER']
    INPUT_FILE = allSetting.get('INPUT_FILE')
    OUTPUT_FILE = allSetting.get('OUTPUT_FILE')
    ACCEPT_RADIX = allSetting.get('ACCEPT_RADIX')
    MAX_SIZE = allSetting.getint('MAX_SIZE')
    DEFAULT_DATA = allSetting.get('DEFAULT_DATA')
    NUM_VALUE_EACH = allSetting.getint('NUM_VALUE_EACH')
else: 
    print('Error: Please make sure that config.ini is accessible and both [USER] and [DEFAULT] sections exist in it.. Exiting..')
    exit()

## end of setting

try:
    with open(INPUT_FILE) as fp:
        lines = fp.read().split("\n")
except IOError:
    print("Error: The INPUT_FILE does not exist.. exiting..")
    exit()

try:
    with open(OUTPUT_FILE) as fp:
        pass
    copyfile(OUTPUT_FILE, '{}.bak'.format(OUTPUT_FILE))
except:
    pass

try:
    fp = open(OUTPUT_FILE, 'w')
except IOError:
    print("Error: Cannot open the OUTPUT_FILE for write.. exiting..")
    exit()

numLines = 1
addr = 0
wordArray = [DEFAULT_DATA]*(MAX_SIZE-1)

for line in lines:
    line = line.strip()
    reObj = re.search('^0x([0-9a-fA-F]+) *?= *?([0-9a-fA-F]+) *?\* *?([0-9]+)$', line)
    if reObj:
        if addr != 0:
            print('stop at 0x{:02X}'.format(addr-1)) #because add 1 after saving ram
        addr = int(reObj.group(1), 16)
        print('Start at 0x{}, '.format(reObj.group(1)), end='')
        # seeking to there. 
        numEnd = int(reObj.group(3))
        for i in range(0, numEnd):
            wordArray[addr] = reObj.group(2)
            addr+=1
            i+=1
    else:
        reObj = re.search('^0x([0-9a-fA-F]+) *?= *?([0-9a-fA-F]+)$', line)
        if reObj:
            if addr != 0:
                print('stop at 0x{:02X}'.format(addr-1))
            addr = int(reObj.group(1), 16)
            print('Start at 0x{}, '.format(reObj.group(1)), end='')
            # seeking to there. 
            wordArray[addr] = reObj.group(2)
            addr+=1
        else:
            reObj = re.search('^([0-9a-fA-F]+) *?\* *?([0-9]+)$', line)
            if reObj:
                numEnd = int(reObj.group(2))
                for i in range(0, numEnd):
                    wordArray[addr] = reObj.group(1)
                    addr+=1
            else:
                reObj = re.search('^([0-9a-fA-F]+)$', line)
                if reObj:
                    wordArray[addr] = reObj.group(1)
                    addr+=1
                else:
                    print('Warning: The syntax \"{}\" at line {} is not accepted'.format(line, numLines))
    numLines+=1
print('stop at 0x{:02X}'.format(addr-1))

fp.write(
"""; This coe file is generated using third party script 
; maintained at the github repository
; By using this script, you are considered
; as accepted the disclaimer and MIT license specified on
; https://github.com/kooltzh/xilinx-coe-generator

""")
fp.write('memory_initialization_radix={};\n'.format(ACCEPT_RADIX))
fp.write('memory_initialization_vector=')

current = 0
for word in wordArray:
    if current == 9:
        fp.write("{}\n".format(word))
        current = 0
    else: 
        fp.write("{} ".format(word))
        current = current + 1

fp.write(";")
fp.close()
