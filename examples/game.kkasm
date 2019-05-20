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

main:

call isWin:
;hlt
wait
get

;base hop
rand r16, 4h
cmp r16, 0h
je baseMoveDown:
cmp r16, 1h
je baseMoveLeft:
cmp r16, 2h
je baseMoveRight:
cmp r16, 3h
je baseMoveUp:

playerHop:
;player hop
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

cmp r28, 0h
je main:

jmp endprog:

;----------------------------------------------------------------------
playerMoveLeft:
call playerDelete:
sub r3, 5h
call playerDraw:

jmp main:

;-----------------------
playerMoveDown:
call playerDelete:
sub r4, 5h
call playerDraw:

jmp main:

;-----------------------
playerMoveRight:
call playerDelete:
add r3, 5h
call playerDraw:

jmp main:

;-----------------------
playerMoveUp:
call playerDelete:
add r4, 5h
call playerDraw:

jmp main:

;----------------------------------------------------------------------
baseMoveLeft:
call baseDelete:
sub r23, 10h
call baseDraw:

jmp playerHop:

;-----------------------
baseMoveDown:
call baseDelete:
sub r24, 10h
call baseDraw:

jmp playerHop:

;-----------------------
baseMoveRight:
call baseDelete:
add r23, 10h
call baseDraw:

jmp playerHop:

;-----------------------
baseMoveUp:
call baseDelete:
add r24, 10h
call baseDraw:

jmp playerHop:

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
mov r2, r1
;get start of base
mov r6, r24
mul r6, 200h
add r6, r23

add r2, r6

;draw base
mov r10, 0 ;i
cycle5i:
	mov r11, 0 ;j
		cycle5j:
			mov r6, r10
			mul r6, 200h
			add r6, r11
			
			add r6, r2
			cmp BytePtr[r6], 50
			je endprog:
			;mov BytePtr[r6], 200
			
			inc r11
			cmp r11, r5
			jne cycle5j:

	inc r10
	cmp r10, r5
	jne cycle5i:

ret
;----------------------------------------------------------------------
endprog:
end