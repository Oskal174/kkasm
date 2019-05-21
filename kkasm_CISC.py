# (c) Kuzminykh Kirill, 2015 (МК-301)

import re
import os
import sys

# Dict with all opcodes
cops = {}

# Segments
DataSeg = re.compile('\s*\.data\s*$')
CodeSeg = re.compile('\s*\.code\s*$')

# Operations
# With no operands
nop = re.compile('nop')						 
cops['nop'] = b'\x00'	 
ret = re.compile('ret')
cops['ret'] = b'\x01' 
hlt = re.compile('hlt')
cops['hlt'] = b'\x02'
get = re.compile('get')
cops['get'] = b'\x1D'
rand = re.compile('rand')
cops['rand'] = b'\x1E'
wait = re.compile('wait')
cops['wait'] = b'\x1F'

# With one operand
inc = re.compile('inc')
cops['inc'] = b'\x03'
dec = re.compile('dec')
cops['dec'] = b'\x04'
pop = re.compile('pop')
cops['pop'] = b'\x05'
push = re.compile('push')
cops['push'] = b'\x06'
comIn = re.compile('in')
cops['in'] = b'\x07'
out = re.compile('out')
cops['out'] = b'\x08'

# With two operand
mov = re.compile('mov')				
cops['mov'] = b'\x09'	
add = re.compile('add')			
cops['add'] = b'\x0A'			
sub = re.compile('sub')		
cops['sub'] = b'\x0B'			
mul = re.compile('mul')		
cops['mul'] = b'\x0C'			
div = re.compile('div')		
cops['div'] = b'\x0D'
comAnd = re.compile('and')
cops['and'] = b'\x0E'
comOr = re.compile('or')
cops['or'] = b'\x0F'
comXor = re.compile('xor')
cops['xor'] = b'\x10'
cmp = re.compile('cmp')
cops['cmp'] = b'\x11'
shl = re.compile('shl')
cops['shl'] = b'\x12'
shr = re.compile('shr')
cops['shr'] = b'\x13'
lea = re.compile('lea')
cops['lea'] = b'\x14'

# Jump commands		
jmp = re.compile('jmp')
cops['jmp'] = b'\x15'	
ja = re.compile('ja')
cops['ja'] = b'\x16'		
jae = re.compile('jae')
cops['jae'] = b'\x17'	  
jb = re.compile('jb')
cops['jb'] = b'\x18'		
jbe = re.compile('jbe')
cops['jbe'] = b'\x19'	
je = re.compile('je')
cops['je'] = b'\x1A'		
jne = re.compile('jne')
cops['jne'] = b'\x1B'	

# Call
call = re.compile('call')
cops['call'] = b'\x1C'

# Endfile label
LabelEnd = re.compile('\s*end\s*$')
cops['end'] = b'\x20'

# Memory addressing modes
# Registers
RegDword 	= re.compile('r[0-9]{1,2}$')	#0001
RegWord		= re.compile('rw[0-9]{1,2}$')	#0010
RegByte 	= re.compile('rb[0-9]{1,2}$')	#0011

# Dereference registers (ex. byte ptr [eax])
RegDwordMem 	= re.compile('DwordPtr\[r[0-9]{1,2}\]$')	#0100
RegWordMem 		= re.compile('WordPtr\[r[0-9]{1,2}\]$')		#0101
RegByteMem 		= re.compile('BytePtr\[r[0-9]{1,2}\]$')		#0110

# Variables in .data segment
Var 		= re.compile('[a-zA-Z_]\w*$')					#1000
VarDword 	= re.compile('DwordPtr\[[a-zA-Z_]\w*\]$')		#1001
VarWord		= re.compile('WordPtr\[[a-zA-Z_]\w*\]$')		#1010
VarByte		= re.compile('BytePtr\[[a-zA-Z_]\w*\]$')		#1011

# Raw memory (ex. 0xFFFFFFFF)
MemDword 	= re.compile('DwordPtr\[0x[0-9A-Fa-f]+\]$')			#1100
MemWord 	= re.compile('WordPtr\[0x[0-9A-Fa-f]+\]$')			#1101
MemByte		= re.compile('BytedPtr\[0x[0-9A-Fa-f]+\]$')			#1110

# Constants
ConstDec		= re.compile('[0-9]+$')			#0111
ConstBin		= re.compile('[0-1]+b$')		#0111
ConstHex		= re.compile('[0-9a-fA-F]+h$') 	#0111

# Goto label
label 			= re.compile('[a-zA-Z_]\w*\:+$')	#1111

# Commands in data segment
# Deposite dword
dd = re.compile('[a-zA-Z_]\w*\s+dd\s+0?x?[0-9a-fA-Fhb\?]+\s*$')
cops['dd'] = b'\x30'

#--------------------------------|
#Functions:						 |
#--------------------------------|


def ErrorExit():
	global CurrentLine
	global LineCount
	global FileOUT
	
	print('ERROR in:', LineCount, '  ' + CurrentLine)
	
	FileIN.close()
	FileOUT.close()
	sys.exit(1)


# Defines memory addressing mode by type of operand
def RACheck(op):
	if RegDword.match(op):
		return '0001'
	elif RegWord.match(op):
		return '0010'
	elif RegByte.match(op):
		return '0011'
	elif RegDwordMem.match(op):
		return '0100'
	elif RegWordMem.match(op):
		return '0101'
	elif RegByteMem.match(op):
		return '0110'
	elif Var.match(op):
		return '1000'
	elif VarDword.match(op):
		return '1001'
	elif VarWord.match(op):
		return '1010'
	elif VarByte.match(op):
		return '1011'
	elif ConstDec.match(op):
		return '0111'
	elif ConstBin.match(op):
		return '0111'
	elif ConstHex.match(op):
		return '0111'	
	elif label.match(op):
		return '1111'


def StructFileCheck(line):
	global DataFlag
	global CodeFlag
	global EndFlag
	
	if DataSeg.match(line):
		DataFlag = 1
	if CodeSeg.match(line):
		CodeFlag = 1
	if LabelEnd.match(line):
		EndFlag = 1


#
def DeleteSpaces(line):
	tempstr = re.compile('^\s*')
	line = tempstr.sub('', line)
	tempstr = re.compile('\s*$')
	line = tempstr.sub('', line)
	tempstr = re.compile('\s+')
	line = tempstr.sub(' ', line)
	tempstr = re.compile('\s*,\s*')
	line = tempstr.sub(',', line)
	tempstr = re.compile('\[\s*')
	line = tempstr.sub('[', line)
	tempstr = re.compile('\s*\]')
	line = tempstr.sub(']', line)
	# Delete comments
	tempstr = re.compile('\s*;.*$')
	line = tempstr.sub('', line)
	
	return line

#-----------------------------------------------------|	
# Processing commands in jump label calculat		  |
#-----------------------------------------------------|


# функция обработки однооперандной команды для вычисления метки	
def OneOpCommandParsLabel(line):
	global ByteCount
	
	#отделение операнда:
	#убрать переносы из строки
	line = line.replace('\n', '')
	#разделить строку по пробелу. на выходе - массив строк
	parts = line.split(' ')
	
	#ищем операнд
	if len(parts) == 1:
		ErrorExit()
	elif len(parts) == 2:
		Op1 = parts[1]
	
	#узнать режим адресации операнда
	Op1RA = RACheck(Op1)

	#изменить счетчик в зависимости от РА
	ByteCount += 2
	
	if Op1RA == '0001' or Op1RA == '0010' or Op1RA == '0011' or Op1RA == '0100' or Op1RA == '0101' or Op1RA == '0110':
		ByteCount += 1
	else:
		ByteCount += 4
	
	return


#Функция обработки двухоперандной команыд для вычисления метки
def TwoOpCommandParsLabel(line):
	global ByteCount
	
	#отделение операндов:
	#убрать переносы из строки
	line = line.replace('\n', '')
	#заменить запятую на пробел
	line = line.replace(',', ' ')
	#разделить строку по пробелу. на выходе - массив строк
	parts = line.split(' ')
	
	#ищем операнды
	if len(parts) == 1:
		ErrorExit()
	elif len(parts) == 3:
		Op1 = parts[1]
		Op2 = parts[2]
	
	#узнать режим адресации операндов
	Op1RA = RACheck(Op1)
	Op2RA = RACheck(Op2)
	
	#изменить счетчик в зависимости от РА
	ByteCount += 2
	if Op1RA == '0001' or Op1RA == '0010' or Op1RA == '0011' or Op1RA == '0100' or Op1RA == '0101' or Op1RA == '0110':
		ByteCount += 1
	else:
		ByteCount += 4
	if Op2RA == '0001' or Op2RA == '0010' or Op2RA == '0011' or Op2RA == '0100' or Op2RA == '0101' or Op2RA == '0110':
		ByteCount += 1
	else:
		ByteCount += 4
		
	return
	

#функция обработки метки
def LabelCommandPars(line):
	global Labels
	global ByteCount
	
	#убрать двоеточие
	line = line.replace(':', '')
	#убрать символ переноса строки
	line = line.replace('\n', '')
	
	#проверка, что метка уже определена
	for element in Labels:
		if element[0] == line:
			print('label redefined')
			ErrorExit()
	
	#добавляем ее в список	
	Labels.append([line, ByteCount])
	
	return


#функция вычисления меток	
EmptyLine = re.compile('^\s*$')
def ParsingLabels(line):
	global DataFlag
	global CodeFlag
	global ByteCount
	
	#убрать лишние пробелы в строке
	line = DeleteSpaces(line)
	
	#если строка пуста(они не учитываютя в смещении)
	if EmptyLine.match(line) or line == '':
		return
	
	#если найден сегмент кода
	if CodeSeg.match(line):
		CodeFlag = 1
		return
		
	#если найдена метка end
	if LabelEnd.match(line):
		CodeFlag = 0
		ByteCount += 1
		return
	
	#обработка сегмента кода
	if CodeFlag == 1:
		#поиск и обработка каждой команды
		#безоперандные
		if nop.match(line):
			ByteCount += 1
			return
		elif ret.match(line):
			ByteCount += 1
			return
		elif hlt.match(line):
			ByteCount += 1
			return
		elif get.match(line):
			ByteCount += 1
			return
		elif wait.match(line):
			ByteCount += 1
			return
			
		#однооперандные
		elif inc.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif dec.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif pop.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif push.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif comIn.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif out.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
			
		#двухоперандные
		elif mov.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif add.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif sub.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif mul.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif div.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif comAnd.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif comOr.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif comXor.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif cmp.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif shl.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif shr.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif lea.match(line):
			#TwoOpCommandParsLabel(line)
			ByteCount += 11
			return
		elif rand.match(line):
			ByteCount += 11
			return
			
		#команды переходов
		elif jmp.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif ja.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif jae.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif jb.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif jbe.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif je.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif jne.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
		elif call.match(line):
			#OneOpCommandParsLabel(line)
			ByteCount += 7
			return
			
		#обработка метки	
		elif label.match(line):
			LabelCommandPars(line)
			return
		else:
			print('unknown command')
			ErrorExit()


#функция обработки операнда
def OpToBytes(op, ra):
	global Labels
	global Vars
	
	#если это регистр
	if ra == '0001' or ra == '0010' or ra == '0011' or ra == '0100' or ra == '0101' or ra == '0110':
		#проверить, что такой регистр существует
		#убрать все лишнее
		temp = re.compile('DwordPtr')
		op = temp.sub('', op)
		temp = re.compile('WordPtr')
		op = temp.sub('', op)
		temp = re.compile('BytePtr')
		op = temp.sub('', op)
		op = op.replace('[', '')
		op = op.replace(']', '')
		op = op.replace('r', '')
		op = op.replace('w', '')
		op = op.replace('b', '')
		
		#перевести оставшийся номер регистра из строки в целое слово
		op = int(op)
		if op > 31:
			print('unknown register')
			ErrorExit()
		else:
			#возращаем op, конвертированный в байтовую строку длины 4(4 байта)
			#return op.to_bytes(1, byteorder='big')
			return op.to_bytes(4, byteorder='little')
	
	#если это метка
	elif ra == '1111':
		#убрать двоеточие
		op = op.replace(':', '')
		#ищем метку
		for element in Labels:
			if element[0] == op:
				#если нашли, возвращаем смещение метки, конвертированное в байтовую строку длины 4(4байта)
				return element[1].to_bytes(4, byteorder='little')
		else:
			print('unknown label: ' + op)
			ErrorExit()
			
	#если это переменная
	elif ra == '1000' or ra == '1001' or ra == '1010' or ra == '1011':
		#убрать все лишнее
		temp = re.compile('DwordPtr')
		op = temp.sub('', op)
		temp = re.compile('WordPtr')
		op = temp.sub('', op)
		temp = re.compile('BytePtr')
		op = temp.sub('', op)
		op = op.replace('[', '')
		op = op.replace(']', '')
		
		#найти в списке переменных и вернуть значение переменной в байтовой строке
		for element in Vars:
			if element[0] == op:
				#запомнить значение, в списке Vars они хранятся как строки
				value = element[1]
				
				#проверить какого типа значение и перевести его из строки в число
				if ConstDec.match(value):
					value = int(value, 10)
				elif ConstHex.match(value):
					value = value.replace('h', '')
					value = int(value, 16)
				elif ConstBin.match(value, 2):
					value = value.replace('b', '')
					value = int(value, 2)
				
				#вернуть значение в байтовой строке
				return value.to_bytes(4, byteorder='little')
		else:
			print('unknown var: ' + op)
			ErrorExit()
	
	#если это память(прямой адрес в памяти)
	elif ra == '1100' or ra == '1101' or ra == '1110':
		#убрать все лишнее
		temp = re.compile('DwordPtr')
		op = temp.sub('', op)
		temp = re.compile('WordPtr')
		op = temp.sub('', op)
		temp = re.compile('BytePtr')
		op = op.replace('[', '')
		op = op.replace(']', '')
		
		#вернуть адрес, перведенный в байтовую строку длины 4
		return int(op, 16).to_bytes(4, byteorder='little')
	
	#если это константы:
	#десятичная
	elif ra == '0111' and ConstDec.match(op):
		#возращаем целое слово как байтовую строку длины 4
		return int(op).to_bytes(4, byteorder='little')
	
	#двоичная
	elif ra == '0111' and ConstBin.match(op):
		#убрать лишнее
		value = op.replace('b', '')
		#возращаем целое слово как байтовую строку длины 4
		return int(value, 2).to_bytes(4, byteorder='little')
		
	#шестнадцатеричная
	elif ra == '0111' and ConstHex.match(op):
		#убрать лишнее
		value = op.replace('h', '')
		#возращаем целое слово как байтовую строку длины 4
		return int(value, 16).to_bytes(4, byteorder='little')

		
#--------------------------------------|
#Функции обработки для ассемблирования |		
#--------------------------------------|

#		
#функция обработки безооперандной команды
#
def NonOpCommdandPars(line, OpName):
	return 0
	
#
#функция обработки однооперандной команды
#
def OneOpCommandPars(line, OpName):
	#отделение операнда:
	#убрать переносы из строки
	line = line.replace('\n', '')
	#разделить строку по пробелу. на выходе - массив строк
	parts = line.split(' ')
	
	#ищем операнд
	if len(parts) == 1:
		ErrorExit()
	elif len(parts) == 2:
		Op1 = parts[1]
	
	#узнать режим адресации операнда
	Op1RA = RACheck(Op1)
	RA1 = int(Op1RA, 2).to_bytes(1, byteorder='big')
	
	RA2 = b'\x00'
	
	#перевести первый операнд в байты
	Op1InBytes = OpToBytes(Op1, Op1RA)
	
	#возврат: байтовая строка: ОпКод + РА1 + РА2 + ОП1
	return cops[OpName] + RA1 + RA2 + Op1InBytes

#	
#функция обработки двухоперандной команды
#
def TwoOpCommandPars(line, OpName):
	#отделение операндов:
	#убрать переносы из строки
	line = line.replace('\n', '')
	#заменить запятую на пробел
	line = line.replace(',', ' ')
	#разделить строку по пробелу. на выходе - массив строк
	parts = line.split(' ')
	
	#ищем операнды
	if len(parts) == 1:
		ErrorExit()
	elif len(parts) == 3:
		Op1 = parts[1]
		Op2 = parts[2]
	
	#узнать режим адресации операндов
	Op1RA = RACheck(Op1)
	RA1 = int(Op1RA, 2).to_bytes(1, byteorder='big')
	Op2RA = RACheck(Op2)
	RA2 = int(Op2RA, 2).to_bytes(1, byteorder='big')
	
	#перевести операнды в байты
	Op1InBytes = OpToBytes(Op1, Op1RA)
	Op2InBytes = OpToBytes(Op2, Op2RA)
	
	#возврат: байтовая строка: ОпКод + РА1 + PA2 + ОП1 + ОП2 
	return cops[OpName] + RA1 + RA2 + Op1InBytes + Op2InBytes

#	
#Функция обработки команд перехода jump
#
def JumpCommandPars(line, OpName):
	#отделить команду и метку:
	#убрать символ переноса строки
	line = line.replace('\n', '')
	#разделить строку по пробелу
	parts = line.split(' ')

	if len(parts) != 2:
		print('syntax error')
		ErrorExit
	
	#берем метку
	Op1 = parts[1]
	
	#определяем режим адрессации операнда
	Op1RA = RACheck(Op1)
	RA1 = int(Op1RA, 2).to_bytes(1, byteorder='big')
	#второй операнд отсутствует
	Op2RA = '0000'
	RA2 = int(Op2RA, 2).to_bytes(1, byteorder='big')
	
	#проверить, что op1 это метка
	if Op1RA != '1111':
		print('syntax error')
		ErrorExit()
	
	#перевести в байты первый операнд
	Op1InBytes = OpToBytes(Op1, Op1RA)
	
	#возврат: байтовая строка: ОпКод + РА1 + РА2 + ОП1
	return cops[OpName] + RA1 + RA2 + Op1InBytes

#	
#функция обработки команды dd
#
def ddCommandPars(line):
	global Vars
	
	#удалить символ переноса строки
	line = line.replace('\n', '')
	#разделить по пробелам
	parts = line.split(' ')

	if len(parts) != 3:
		print('syntax error')
		ErrorExit()
		
	#отделяем имя и значение переменной	
	VarName = parts[0]
	VarValue = parts[2]
	
	#проверить, что переменная не переопределена
	for elem in Vars:
		if elem[0] == VarName:
			print('syntax error: using var')
			ErrorExit()
	
	#вычисляем РА значения
	RA = RACheck(VarValue)
	
	#проверяем, что это константа
	if RA != '0111':
		print('syntax error in dd')
		ErrorExit()
		
	#добавить пару [переменная, значение] в список переменных
	Vars.append([VarName, VarValue])	
	
	return b''

#	
#главная функция ассемблирования текста,
#переводит каждую строку в .asm файле в байтовую последовательность
#
def Assembly(line):
	global DataFlag
	global CodeFlag
	
	#удалить лишние пробелы
	line = DeleteSpaces(line)
	
	#если строка пуста, она пропускается
	if line == '' or line == '\n' or EmptyLine.match(line):
		return b''
	
	#найден сегмент данных
	if DataSeg.match(line):
		DataFlag = 1
		CodeFlag = 0
		return b''
	
	#найден сегмент кода
	if CodeSeg.match(line):
		DataFlag = 0
		CodeFlag = 1
		return b''
		
	#найдена метка end
	if LabelEnd.match(line):
		CodeFlag = 0
		return cops['end']
		
	#обработка сегмента данных
	if DataFlag == 1:
		#обработка и перевод в байтовую последовательность каждой команды
		if dd.match(line):
			ddCommandPars(line)
			return b''
		else:
			print('unknown command in data segment')
			ErrorExit()
	
	#обработка сегмента кода
	if CodeFlag == 1:
		#обработка и перевод в байтовую последовательность каждой команды
		#безоперандные
		if nop.match(line):
			return cops['nop']
		elif ret.match(line):
			return cops['ret']
		elif hlt.match(line):
			return cops['hlt']
		elif get.match(line):
			return cops['get']
		elif wait.match(line):
			return cops['wait']
		
		#однооперандные
		elif inc.match(line):
			return OneOpCommandPars(line, 'inc')
		elif dec.match(line):
			return OneOpCommandPars(line, 'dec')
		elif pop.match(line):
			return OneOpCommandPars(line, 'pop')
		elif push.match(line):
			return OneOpCommandPars(line, 'push')
		elif comIn.match(line):
			return OneOpCommandPars(line, 'in')
		elif out.match(line):
			return OneOpCommandPars(line, 'out')
		elif call.match(line):
			return OneOpCommandPars(line, 'call')
			
		#двухоперандные	
		elif mov.match(line):
			return TwoOpCommandPars(line, 'mov')
		elif add.match(line):
			return TwoOpCommandPars(line, 'add')
		elif sub.match(line):
			return TwoOpCommandPars(line, 'sub')
		elif mul.match(line):
			return TwoOpCommandPars(line, 'mul')
		elif div.match(line):
			return TwoOpCommandPars(line, 'div')
		elif comAnd.match(line):
			return TwoOpCommandPars(line, 'comAnd')
		elif comOr.match(line):
			return TwoOpCommandPars(line, 'comOr')
		elif comXor.match(line):
			return TwoOpCommandPars(line, 'comXor')
		elif cmp.match(line):
			return TwoOpCommandPars(line, 'cmp')
		elif shl.match(line):
			return TwoOpCommandPars(line, 'shl')
		elif shr.match(line):
			return TwoOpCommandPars(line, 'shr')
		elif lea.match(line):
			return TwoOpCommandPars(line, 'lea')
		elif rand.match(line):
			return TwoOpCommandPars(line, 'rand')
			
		#команды переходов	
		elif jmp.match(line):
			return JumpCommandPars(line, 'jmp')
		elif ja.match(line):
			return JumpCommandPars(line, 'ja')
		elif jae.match(line):
			return JumpCommandPars(line, 'jae')
		elif jb.match(line):
			return JumpCommandPars(line, 'jb')
		elif jbe.match(line):
			return JumpCommandPars(line, 'jbe')
		elif je.match(line):
			return JumpCommandPars(line, 'je')
		elif jne.match(line):
			return JumpCommandPars(line, 'jne')
			
		#если встречена метка(она не переводится в байтовую строку)
		elif label.match(line):
			return b''
		else:
			print('unknowm command in code segment')
			ErrorExit()


#-----------------------------------------------------------------------|			
#MAIN:																	|
#-----------------------------------------------------------------------|
if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: <src file> <output file>')
		sys.exit(0)
		
	FileIN = open(sys.argv[1], 'r')
	FileOUT = open(sys.argv[2], 'wb')

	# First step
	# Checking file structure (segments and endfile label)
	DataFlag = 0
	CodeFlag = 0
	EndFlag = 0
	for line in FileIN:
		StructFileCheck(line)
	if DataFlag == 0 or CodeFlag == 0 or EndFlag == 0:
		print('error in struct of file')
		sys.exit(1)

	print('File struct check: success')
		
	# Second step
	FileIN.seek(0)
	# Caculation jump labels in code segment
	DataFlag 	= 0
	CodeFlag 	= 0

	Labels = []
	# Offset in bytes
	ByteCount = 0 
	
	LineCount = 0
	CurrentLine = ''
	for line in FileIN:
		CurrentLine = line
		LineCount += 1
		ParsingLabels(line)

	print('Parsing Labels: success')
		
	# Third step
	# Assembling code, translate in bytes sequences
	FileIN.seek(0)
	DataFlag = 0
	CodeFlag = 0

	# Adding special signature to the binary file
	FileOUT.write(b'\x4B') # K
	FileOUT.write(b'\x41') # A
	FileOUT.write(b'\x53') # S
	FileOUT.write(b'\x4D') # M

	Vars = []
	LineCount = 0
	CurrentLine = ''
	for line in FileIN:
		CurrentLine = line
		LineCount += 1
		#print(LineCount, ' ' + CurrentLine)
		FileOUT.write(Assembly(line))

	FileOUT.close()

	print('Assembly: success')
	print('Vars list:\n', Vars, '\nLabel list:\n', Labels, '\n')

	print('BIN file:\n')
	FileOUT = open(sys.argv[2], 'rb')
	for line in FileOUT:
		print(line)
