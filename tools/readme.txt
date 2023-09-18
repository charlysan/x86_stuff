cga.asm
------

Tool that can be used to initialized a CGA card

cga.com
------

The above program compiled using nasm:

   nasm -f bin -o cga.com cga.asm


Usage:
- First arg: MODE

Supported modes:
    1: Text mode - 25x80
    2: Text mode - 25x40
    3: Graphics mode - 320x200 - Color palette #1
    4: Graphics mode - 320x200 - Color palette #2
    5: Graphics mode - 640x200

Example:
   Graphics mode 320x200 (color palette #1): CGA.com 3
