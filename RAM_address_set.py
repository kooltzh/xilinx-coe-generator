import re

with open('setRAM.txt') as fp:
    lines = fp.read().split("\n")
    
fp.close()

fp = open('testing1.coe', 'w')

fp.write('memory_initialization_radix=16;\n')
fp.write('memory_initialization_vector=')

target = 0

maxsize = 150000
wordArray = []

for i in range(0, maxsize):
    wordArray.append(0)

for line in lines:
    reObj = re.search('0x([0-9a-fA-F]+) ?= ?(.+)', line)
    if reObj:
        if target != 0:
            print('stop at 0x', format(target-1, '02X'))
        target = int(reObj.group(1), 16)
        print('printing at 0x',reObj.group(1))
        #seeking to there. 
        wordArray[target] = reObj.group(2)
        target = target + 1
    else:
        reObj = re.search('([0-9a-fA-F]+)', line)
        if reObj:
            wordArray[target] = reObj.group(1)
            target = target + 1

current = 0
for item in wordArray:
    if current == 9:
        fp.write("%s\n" % item)
        current = 0
    else: 
        fp.write("%s " % item)
        current = current + 1

fp.close()
#int(re.group(0), 16)