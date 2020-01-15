from Adafruit_MCP230xx import Adafruit_MCP230XX as Chip
from gpiozero import LED
from time import sleep
import math
from pynput.mouse import Listener
from pygame.time import Clock
from threading import Thread
chip = Chip(busnum = 1, address = 0x20, num_gpios = 16)

class led:
	def __init__(self, pin):
		self.pin = pin
		chip.config(pin, Chip.OUTPUT)
		
	def on(self):
		chip.output(self.pin, 1)
		
	def off(self):
		chip.output(self.pin, 0)

def factory(pin):
	if pin > 1 and pin < 28:
		return LED(pin)
	if pin > 27 and pin < 44:
		return led(pin-28)
	raise ValueError('pin index out of range')

table = {-1: '0000000', 0: '1110111', 1: '0010010', 2: '1011101', 3: '1011011', 4: '0111010', 5: '1101011', 6: '1101111', 7: '1010010', 8: '1111111', 9: '1111010'}

class Digit:
	def __init__(self, pins):
		self.pins = [factory(x) for x in pins]
		self.setVal(8)
		
	def setVal(self, val):
		s = table[val]
		for x in range(len(s)):
			if s[x] == '1':
				self.pins[x].on()
			else:
				self.pins[x].off()

class Number:
	def __init__(self, pins):
		self.digits = [Digit(row) for row in pins]
	
	def setVal(self, val):
		if val < -1 or val >= 10**len(self.digits):
			raise ValueError('number out of range')
		if val == -1:
			for dig in self.digits:
				dig.setVal(-1)
		else:
			s = ('{0:0' + str(len(self.digits)) + 'd}').format(val)
			print(s)
			i = 0
			for x in s:
				self.digits[i].setVal(int(x))
				i += 1

d1 = [20,19,16,21,13,26,6]
d2 = [11,5,14,10,7,8,12]
d3 = [41,35,43,9,25,40,42]
d4 = [31,28,30,34,29,33,32]

num = Number([d1,d2,d3,d4])
state = 0

class Countdown(Thread):
	def __init__(self, num):
		super(Countdown, self).__init__()
		self.num = num
		self.counting = True
		self.alive = True

	def run(self):
		clock = Clock()
		val = self.num
		while val >= 0 and self.counting:
			num.setVal(val)
			val -= 1
			clock.tick(17)
		while self.alive:
			num.setVal(0)
			clock.tick(5)
			num.setVal(-1)
			clock.tick(5)

countdown = Countdown(4000)

def on_click(x,y,button,pressed):
	if str(button) == 'Button.right' and pressed:
		print('killing listener')
		return False
	if str(button) == 'Button.left' and pressed:
		global state, countdown
		state += 1
		if state  == 0:
			num.setVal(8888)
		elif state  == 1:
			num.setVal(4000)
		elif state == 2:
			countdown.start()
		elif state == 3:
			countdown.counting = False
		elif state == 4:
			countdown.alive = False
		else:
			return False

def getNum():
	return num

if __name__ == '__main__':
	
	with Listener(on_click=on_click) as listener:
		while listener.running:
			print('state: ' + str(state))
			sleep(.5)


