org   100h   

%macro print_msg 1 
	mov ah, 9       
	mov dx, %1 
	int 21h         
%endmacro


start:
	mov si, 81h ; start of command line arguments

parse_arg:
	call skip_space
	mov al, [si] ; first character
	cmp al, '1'
	je text_25x80
	cmp al, '2'
	je text_25x40
	cmp al, '3'
	je graph_320x200
	cmp al, '4'
	je graph_320x200_p2
	cmp al, '5'
	je graph_640x200

exit:
	mov   ax,4C00h
	int   21h

skip_space:
	cmp byte [si], 0x20 
	je .skip
	ret
.skip:
	inc si
	jmp skip_space

text_25x80:
	mov  si, textt       ;Offset address of the register-table
	mov  bl, 00000001b   ;80x25 text mode
	mov  cl, 00000000b 
	call crtc_prog
	print_msg text_msg_25x80  
	jmp  exit

text_25x40:
	mov  si, textt       ;Offset address of the register-table
	mov  bl, 00000000b   ;40x25 text mode
	mov  cl, 00000000b 
	call crtc_prog
	print_msg text_msg_25x40  
	jmp exit 

graph_320x200:
	mov  si, graphict    ;Offset address of the register-table
	mov  bl, 00000010b   ;Graphics mode 320x200
	mov  cl, 00100000b   ;Color palette #1
	call crtc_prog
	print_msg graph_msg_320x200  
	jmp exit 

graph_320x200_p2:
	mov  si, graphict    ;Offset address of the register-table
	mov  bl, 0000010b    ;Graphics mode 320x200
	mov  cl, 00000000b   ;Color palette #2 
	call crtc_prog
	print_msg graph_msg_320x200_p2  
	jmp exit 

graph_640x200:
	mov  si, graphict    ;Offset address of the register-table
	mov  bl, 00010000b   ;Graphics mode 640x200
	call crtc_prog
	print_msg graph_msg_640x200  
	jmp exit

setmode:
	mov  dx, word [CONTROL_REG]   ;Address of the display control register
	mov  al,bl
	out  dx,al                    ;Send mode to control register
	ret

crtc_prog:
	call setmode            ;
	call setcol             ;Set color palette
	mov  cx,14              ;14 registers are set 
	xor  bh,bh              ;Start with register 0 
vcp1:
	lodsb                   ;Get register value from table 
	mov  ah,al              ;Register value to AH
	mov  al,bh              ;Number of the register to AL
	call setvk              ;Transmit value to controller 
	inc  bh                 ;Address next register 
	loop vcp1               ;Set additional registers 

	or bl,8                 ;Bit 3 = 1: screen on 
	call setmode
	ret                     ;Back to caller

setvk:
	mov  dx, word [ADDRESS_6845]   ;Address of the index register
	out  dx,al                     ;Send number of the register 
	jmp  short $+2                 ;Short I/O pause
	inc  dx                        ;Address of the index register
	mov  al,ah                     ;Content to AL
	out  dx,al                     ;Set new content 
	ret                            ;Back to caller

setcol:   
	mov  dx, word [CCHOICE_REG]  ;Address of the color selection register
	mov  al,cl
	out  dx,al                   ;Output color value 
	ret                          ;Back to caller



section .data
	;Custom CGA card I/O (e.g. 0x3D4 -> 0x394)
	CONTROL_REG  dw  0x0398          ;Control register port address
	CCHOICE_REG  dw  0x0399          ;Color select register port address
	ADDRESS_6845 dw  0x0394          ;6845 address register
	DATA_6845    dw  0x0395          ;6845 data register
	
	graphict              db 0x38,0x28,0x2D,0x0A,0x7F,0x06,0x64,0x70,0x02,0x01,0x06,0x07,0x00,0x00  
	textt                 db 0x71,0x50,0x5A,0x0A,0x1F,0x06,0x19,0x1C,0x02,0x07,0x06,0x07,0x00,0x00
	text_msg_25x80        db 'Text Mode - 25x80$'
	text_msg_25x40        db 'Text Mode - 25x40$'
	graph_msg_320x200     db 'Graphics Mode - 320x200 (color palette #1)$'
	graph_msg_320x200_p2  db 'Graphics Mode - 320x200 (color palette #2)$'
	graph_msg_640x200     db 'Graphics Mode - 640x200$'

	