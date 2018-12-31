import re
from shutil import copyfile

## All available setting here
# input and output files path and name
SETTING_FILE = 'setRAM_test.txt'
OUTPUT_FILE = 'output_test.coe'

# customization
ACCEPT_RADIX = 16 # the maximum range for each bit, 16 for hex
MAX_SIZE = 150000 # maximum size of the targetted RAM 
DEFAULT_VALUE = 0 # default value for the remaining value of RAM
NUM_VALUE_EACH = 10 # number of values in each line of coe output, wont affect Xilinx IP but affect our debug

## end of setting

try:
    with open(SETTING_FILE) as fp:
        lines = fp.read().split("\n")
except IOError:
    print("Error: the SETTING_FILE does not exist.. exiting..")

try:
    with open(OUTPUT_FILE) as fp:
        pass
    copyfile(OUTPUT_FILE, '{}.bak'.format(OUTPUT_FILE))
except:
    pass

try:
    fp = open(OUTPUT_FILE, 'w')
except IOError:
    print("Cannot open the OUTPUT_FILE for write.. exiting..")

fp.write('memory_initialization_radix={};\n'.format(ACCEPT_RADIX))
fp.write('memory_initialization_vector=')

addr = 0

wordArray = [DEFAULT_VALUE]*(MAX_SIZE-1)

for line in lines:
    reObj = re.search('0x([0-9a-fA-F]+) *?= *?([0-9a-fA-F]+) *?\* *?([0-9]+) *?$', line)
    if reObj:
        if addr != 0:
            print('stopped at 0x{:02X}'.format(addr-1))
        addr = int(reObj.group(1), 16)
        print('Start at 0x{}, '.format(reObj.group(1)), end='')
        # seeking to there. 
        numEnd = int(reObj.group(3))
        for i in range(0, numEnd):
            wordArray[addr] = reObj.group(2)
            addr+=1
            i+=1
    else:
        reObj = re.search('0x([0-9a-fA-F]+) *?= *?([0-9a-fA-F]+) *?$', line)
        if reObj:
            if addr != 0:
                print('stopped at 0x{:02X}'.format(addr-1))
            addr = int(reObj.group(1), 16)
            print('Start at 0x{}, '.format(reObj.group(1)), end='')
            # seeking to there. 
            wordArray[addr] = reObj.group(2)
            addr+=1
        else:
            reObj = re.search('([0-9a-fA-F]+)', line)
            if reObj:
                wordArray[addr] = reObj.group(1)
                addr+=1
print('stopped at 0x{:02X}'.format(addr-1))

current = 0
for word in wordArray:
    if current == 9:
        fp.write("{}\n".format(word))
        current = 0
    else: 
        fp.write("{} ".format(word))
        current = current + 1

fp.close()
