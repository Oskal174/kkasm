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

## kkasm examples
* test.kkasm - simple code with random operations.
* game.kkasm - simple game using video memory.

### Assembly
`python examples\game.kkasm game.bin`

### Start
Bin files may launch with using special emulator of my own processor architecture. 

Github project with this emulator: https://github.com/Oskal174/kkasm_emulator
