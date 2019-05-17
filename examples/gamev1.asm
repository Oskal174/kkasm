.data
.code
;video mem start
mov r1, 6000h
;player and base size
mov r5, 25h

;base x start
rand r23, 200h
;base y start
rand r24, 100h
call baseDraw:

;player x start
mov r3, 50h
;player y start
mov r4, 50h
call playerDraw:

;global index
mov r16, 0

main:

call isWin:
hlt
get

cmp r16, 125
jne nextHop:
	;new base state
	call baseDelete:
	rand r23, 200h
	rand r24, 100h
	call baseDraw:
	
	mov r16, 0
	
nextHop:
inc r16

;left
cmp r28, 25h
je playerMoveLeft:
;down
cmp r28, 26h
je playerMoveDown:
;right
cmp r28, 27h
je playerMoveRight:
;up
cmp r28, 28h
je playerMoveUp:


jmp endprog:

;----------------------------------------------------------------------
playerMoveLeft:
call playerDelete:
sub r3, 1h
call playerDraw:

jmp main:

;-----------------------
playerMoveDown:
call playerDelete:
sub r4, 1h
call playerDraw:

jmp main:

;-----------------------
playerMoveRight:
call playerDelete:
add r3, 1h
call playerDraw:

jmp main:

;-----------------------
playerMoveUp:
call playerDelete:
add r4, 1h
call playerDraw:

jmp main:

;----------------------------------------------------------------------
playerDraw:
mov r2, r1
;get start of player
mov r6, r4
mul r6, 200h
add r6, r3

add r2, r6

;draw palyer
mov r10, 0 ;i
cycle1i:
	mov r11, 0 ;j
		cycle1j:
			mov r6, r10
			mul r6, 200h
			add r6, r11
			
			add r6, r2
			mov BytePtr[r6], 50
			
			inc r11
			cmp r11, r5
			jne cycle1j:

	inc r10
	cmp r10, r5
	jne cycle1i:

ret

;----------------------------------------------------------------------
baseDraw:
mov r2, r1
;get start of base
mov r6, r24
mul r6, 200h
add r6, r23

add r2, r6

;draw base
mov r10, 0 ;i
cycle3i:
	mov r11, 0 ;j
		cycle3j:
			mov r6, r10
			mul r6, 200h
			add r6, r11
			
			add r6, r2
			mov BytePtr[r6], 200
			
			inc r11
			cmp r11, r5
			jne cycle3j:

	inc r10
	cmp r10, r5
	jne cycle3i:

ret

;----------------------------------------------------------------------
baseDelete:
mov r2, r1
;get start of base
mov r6, r24
mul r6, 200h
add r6, r23

add r2, r6

;draw base
mov r10, 0 ;i
cycle4i:
	mov r11, 0 ;j
		cycle4j:
			mov r6, r10
			mul r6, 200h
			add r6, r11
			
			add r6, r2
			mov BytePtr[r6], 255
			
			inc r11
			cmp r11, r5
			jne cycle4j:

	inc r10
	cmp r10, r5
	jne cycle4i:

ret

;----------------------------------------------------------------------
playerDelete:
mov r2, r1
;get start of player
mov r6, r4
mul r6, 200h
add r6, r3

add r2, r6

;delete palyer
mov r10, 0 ;i
cycle2i:
	mov r11, 0 ;j
		cycle2j:
			mov r6, r10
			mul r6, 200h
			add r6, r11
			
			add r6, r2
			mov BytePtr[r6], 255
			
			inc r11
			cmp r11, r5
			jne cycle2j:

	inc r10
	cmp r10, r5
	jne cycle2i:

ret

;----------------------------------------------------------------------
isWin:
cmp r3, r23
je nextStep:
ret

	nextStep:
	cmp r4, r24
	je endprog:
ret

;----------------------------------------------------------------------
endprog:
end