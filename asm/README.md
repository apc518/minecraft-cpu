## Overview
- This instruction set is designed for a CPU with exactly two 8-bit working registers.
- Opcodes are three bits, and other bits can either indicate a register, indicate an immediate value, or indicate a more specific function.

## Spec
```
comm: 000 r ffff (commutative operations)
        funct:
        0000: zero (set to 0)
        0010: and
        0011: nand
        0100: xor
        0101: xnor
        0110: or
        0111: nor
        1000: add
addi: 001 r r iii (add immediate)
move: 010 r ----  (copy)
not:  011 r r --- (invert bits)
jump: 100 f iiii
        funct:
        0: jeq (jump if equal)
        1: jneq (jump if not equal)
sb:   101 r iiii  (store byte)
lb:   110 r iiii  (load byte)
dr:   111 r ----  (display register)
noop: 001 0 0 000 (addi $r0, $r0, 0)
```

## Advantage of having just 2 registers
With only two working registers, commutative operations don't need to specify their origins, clearing up two bits in the instruction (nice!).
Additionally, specifying a register only takes 1 bit, which is very useful with only 8 bits of real estate for instructions.

## Possible Future Work
dr (display register) could be subsumed by the move instruction, as it's kind of "moving" or copying a register to the display.
In that case, move would look like this: `move: 010 r rr --`. We'd need two bits to represent the destination register since there would be three options. But the origin register would still only ever be $r0 or $r1, so that can stay as 1 bit

If the above change was made to dr, then 111 could be used for something else, probably non-commutative arithmetic such as subtraction.
So it might look like:
non-commutative: 111 r r r ff
        funct:
        00: sub
        01: ??
        10: ??
        11: ??