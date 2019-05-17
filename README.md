# kkasm - KuzminykhKirill Assembler
This is a simple assembler with own assembly language developed for training purposes.

## Usage
`python kkasm_CISC.py <src_filename> <out_filename>`

## Architecture
CISC - complex instruction set computer. 

## Command format
```
|------|-----|-----|-----|----|
|ОПКОД | РА1 | РА2 | ОП1 | ОП2|
|  1   |  1  | 1   |  4  |  4 |
|------|-----|-----|-----|----|

Command size:
* With no operands  - 1 byte
* With one operand  - 7 bytes
* With two operands - 11 bytes
```
