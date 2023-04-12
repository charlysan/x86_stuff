jt.asm
------

Juko Tool (beta) source 
CLI Tool that can be used to write to TD3300A registers.

jt.com
------

Juko Tool (beta) compiled using NASM:

   nasm -f bin -o jp.com jp.asm


Usage:
- First arg: register number in hex format (e.g. 90)
- Second arg: value to be written in hex format (e.g. 03)

Example:
   Enable Turbo Mode: jt 90 00
   Disable Turbo Mode: jt 90 03

