# Xilinx RAM COE Generator
## Overview
This third party python script with no dependency other than native python package is used to generate Xilinx *.coe files for RAM data initializing

Xilinx RAM COE files aka coefficient files is used to initiate the data associated with their addresses inside Block RAM or other types of RAM.

The reference for Xilinx *.coe files can be found here at [COE File Syntax](https://www.xilinx.com/support/documentation/sw_manuals/xilinx11/cgn_r_coe_file_syntax.htm) on Xilinx support website.

## Motivation 
Although it is possible to use one RAM controller for each data with large FPGA setup, saving multiple data on single RAM usually costs us less resource requirement and provides routing simplicity thus decreasing development time. However, this usually comes with the expenses of doing [Memory Mapping](https://en.wikipedia.org/wiki/Memory_map) on available variables.

The *coe files is read and write in linear fashion, ie. it will start from address 0x0 all the ways until 0x100000 (your end). Therefore, saving a series of data starting from arbitary addresses (eg. 0x1A32) usually is a hard task as we might need to count the data manually.

Besides, data collision in same address is also possible as chucks of data might overlap with each other 

This python script is use to translate addresses and data specified by the input file, then arrange them to generate *.coe files

## Using it
* Clone or download the repository
* Update the config.ini files
* Write your own input file using the syntax specified at the following section
* run `python xilinx-coe-generator.py`

## Available setting in config.ini

Default setting values is defined in the `[default]` section, user can overwrite the setting in `[user]` section
```ini
; value in USER section overwrite the default config value
[USER]
INPUT_FILE = example/my_new_file.txt

; The value in DEFAULT section shall be left untouched
[DEFAULT]
; The input file name written with defined syntax
INPUT_FILE = example/normal.txt
; The file name for output coe file
OUTPUT_FILE = output.coe

; the maximum range for each bit, 16 for hex
ACCEPT_RADIX = 16
; maximum size of the targetted RAM
MAX_SIZE = 150000
; default data for the remaining data of RAM
DEFAULT_DATA = 0
; number of datas in each line of coe output, wont affect Xilinx RAM but affect our readability
NUM_DATA_EACH = 10
```

This will cause the script to take "example/my_new_file.txt" as input, then follow default value for other variables.

## Documentation
This python script is developed on python 3.7.1 on Ubuntu 18.04 LTS

### Accepted syntaxes for input files
Here are 4 of the syntaxes acceptable for this script   
The spaces in between ` = ` or ` * ` is optional.
```
0x[address] = [data] * [number of repeat]
0x[address] = [data]
[data] * [number of repeat]
[data]
```
In the following sections, please note that we will be using w/ "0x" for address, w/o "0x" for data. Both are in hexadecimal.


Syntax:
```
0x[address] = [data]
```

Eg. Saving data `0xAB3432` into address `0x123AB` shall be
```
0x123AB = AB3432 
```

### Saving chucks of data
To save this chuck of data one after another 

|Address|Data|
|---|---|
|0x10|0x20|
|0x11|0x21|
|...|...|
|0x1F|0x2F|

Shall be written like this in input file
```
0x10 = 20
21
22
...
2F
```

### Saving repetitive data
One can use " * " as indicator for repetitive data. Notes that \[ number of repeat \] is in decimal of base 10

Syntax:
```
0x[address] = [data] * [number of repeat]
```

Eg. saving 12 data with value of `0xABC` in address range of `0x110 to 0x11C`
```
0x110 = ABC * 12
```

|Address|Data|
|---|---|
|0x110|0xABC|
|0x111|0xABC|
|...|...|
|0x11B|0xABC|

### Using two types of syntax together
It is also possible to generate repeative values after assigning address on previous line.
```
0x100 = 1102321C
20932123
32212CDA * 3
BC312212
```

Will result in

|Address|Data|
|---|---|
|0x100|0x1102321C|
|0x101|0x20932123|
|0x102|0x32212CDA|
|0x103|0x32212CDA|
|0x104|0x32212CDA|
|0x105|0xBC312212|


## Using examples

Will be added in the future

## To do list
* [ ] Accepting comment in input file
* [ ] Adding more example
* [ ] Adding command line interface (CLI) support
* [ ] Adding Collision alert. ie. warning for saving multiple data on same address
* [ ] Reading files directly as binary

## Disclaimer
Although the contributor of this project had made every attempt to ensure the best possible accuracy of this script. However, this python script is provided "as is" without warranty of any kind. The contributor does not take any responsibility or liability for the damage of lost caused by the usage of this script.

By using this script, you are hereby agree to the condition stated in the disclaimer section of this project.

## Wrapping up!
This project is maintained as side project of an undergraduate. So updates might come a bit occasionally 

For any issues, please submit an [issues](https://github.com/kooltzh/xilinx-coe-generator/issues) or contact the author at kooltzh@gmail.com

## Contributing
Have all the fun forking the repository, check out, then submit your new feature as pull request,   
I will be more than happy to accept it :D