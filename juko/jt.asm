org   100h     

start:
    ; parse first argument
    mov si, 81h ; start of command line arguments
    call skip_space
    call parse_hex
    mov [arg1], al ; store first byte

    ; parse second argument
    add si, 3 ; move to start of second argument
    call skip_space
    call parse_hex
    mov [arg2], al ; store second byte

    ; write to TD3300A port
    call write_port

exit:
    mov   ax,4C00h
    int   21h

parse_hex:
    mov al, [si] ; first character
    cmp al, 'a'
    jl .digit
    sub al, 'a' - 10
    jmp .store

.digit:
    sub al, '0'

.store:
    shl al, 4 ; shift the high nibble into place
    mov bl, [si+1] ; second caracter 
    cmp bl, 'a'
    jl .digit2
    sub bl, 'a' - 10
    jmp .store2

.digit2:
    sub bl, '0'

.store2:
    or al, bl ; combine the high and low nibbles
    ret

skip_space:
    cmp byte [si], 0x20 
    je .skip
    ret

.skip:
    inc si
    jmp skip_space

; TD3300A
write_port:
    xor dx,dx
    mov dl, byte [arg1]
    mov bl, byte [arg2]
    cli
    in al,dx
    mov al, bl
    out dx, al 
    sti
    sti
    ret

section .bss
    arg1 resb 1
    arg2 resb 1