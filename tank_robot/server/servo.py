#!/usr/bin/env python3
# File name   : servo.py
# Description : Control Motor
# Product     : RaspTank  
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/12/27
from __future__ import division
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)



#def config():
#L11
L11_MAX=330
L11_MIN=138
L11_ST1=300
#L12
# 0deg - 310
# min - 90deg - 100
# max - -115 - 530
#$ currently using ST1-3
L12_MAX=520
L12_MIN=100
L12_ST1=300
L12_ST2=100
L12_ST3=510
#L13
# 0deg - 240
# max - -60deg - 380
# min - 70deg - 100
#$ currently using ST1-3
L13_MAX=380
L13_MIN=110
L13_ST1=220
L13_ST2=380
L13_ST3=110
#L14
# min - 0deg - 125
# max - -180 - 570
#$ currently using ST1-3
L14_MAX=570
L14_MIN=125
L14_ST1=570
L14_ST2=570
L14_ST3=570
#L15
# clamped - 470
# better clamp - 450
# really open - 200
# good open - 300
#$ currently using ST1-4
L15_MAX=463
L15_MIN=300
L15_ST1=463
L15_ST2=463
L15_ST3=463
L15_ST4=300
#config()


def camera_ang(direction, ang=10):
	global L11_ST1
	org_pos = L11_ST1
	if ang == 0:
		ang=4
	if direction == 'lookdown':
		if org_pos < L11_MAX:
			org_pos+=ang
		else:
			org_pos = L11_MAX
	elif direction == 'lookup':
		if org_pos > L11_MIN:
			org_pos-=ang
		else:
			org_pos = L11_MIN
	elif direction == 'home':
		org_pos = L11_MAX
	else:
		pass
	#print(ang)
	#print(org_pos)
	L11_ST1 = org_pos
	pwm.set_pwm(11,0,org_pos)





class Arm:
	def __init__(self):
		self.L12_angle = 0
		self.L13_angle = 0
		self.L14_angle = 0
		#
		self.start_position() 

	def start_position(self):
		self.L12_pos = L12_ST1
		self.L13_pos = L13_ST1
		self.L14_pos = L14_ST1
		self.L15_pos = L15_ST1
		pwm.set_pwm(12,0,L12_ST1)
		pwm.set_pwm(13,0,L13_ST1)
		pwm.set_pwm(14,0,L14_ST1)
		pwm.set_pwm(15,0,L15_ST1)
		camera_ang('home',None) # might as well put it here

	def destroy(self):
		clean_all()


	## lower-level functions

	def _step_pos(self, current_pos, target_pos, num_steps):
		step = (target_pos-current_pos)/num_steps
		return step

	def _move_joint_within_bounds(self, direction, step, joint_num, current_pos, max_pos, min_pos):
		print('_move_joint_within_bounds')
		if direction == 'pos':
			target_pos = current_pos + step
			if target_pos > max_pos:
				current_pos = max_pos
				pwm.set_pwm(joint_num,0,max_pos)
			else:
				current_pos = target_pos
				pwm.set_pwm(joint_num,0,target_pos)
		elif direction == 'neg':
			target_pos = current_pos - step
			if target_pos < min_pos:
				current_pos = min_pos
				pwm.set_pwm(joint_num,0,min_pos)
			else:
				current_pos = target_pos
				pwm.set_pwm(joint_num,0,target_pos)

		return current_pos

	def move_L12(self, direction, step=20):
		self.L12_pos = self._move_joint_within_bounds(direction, step, 12, self.L12_pos, L12_MAX, L12_MIN)

	def move_L13(self, direction, step=20):
		self.L13_pos = self._move_joint_within_bounds(direction, step, 13, self.L13_pos, L13_MAX, L13_MIN)

	def move_L14(self, direction, step=20):
		self.L14_pos = self._move_joint_within_bounds(direction, step, 14, self.L14_pos, L14_MAX, L14_MIN)

	def move_L15(self, direction, step=20):
		self.L15_pos = self._move_joint_within_bounds(direction, step, 15, self.L15_pos, L15_MAX, L15_MIN)

	def print_servo_pos(self):
		print('L12:{} L13:{} L14:{} L15:{}'.format(self.L12_pos,self.L13_pos,self.L14_pos,self.L15_pos))

	## mid-level functions

	def tuck_in(self):
		num_steps = 40 
		L12_step = self._step_pos(self.L12_pos, L12_ST2, num_steps)
		L13_step = self._step_pos(self.L13_pos, L13_ST2, num_steps)
		L14_step = self._step_pos(self.L14_pos, L14_ST2, num_steps)
		#L15_step = _step_pos(self.L15_pos, L15_ST2, num_steps)
		for i in range(num_steps):
			self.L12_pos += L12_step
			self.L13_pos += L13_step
			self.L14_pos += L14_step
			pwm.set_pwm(12,0,int(self.L12_pos))
			pwm.set_pwm(13,0,int(self.L13_pos))
			pwm.set_pwm(14,0,int(self.L14_pos))
			#pwm.set_pwm(15,0,self.L15_pos)
			#time.sleep(0.05)

	def reach_out(self):
		num_steps = 40 
		L12_step = self._step_pos(self.L12_pos, L12_ST3, num_steps)
		L13_step = self._step_pos(self.L13_pos, L13_ST3, num_steps)
		L14_step = self._step_pos(self.L14_pos, L14_ST3, num_steps)
		#L15_step = _step_pos(self.L15_pos, L15_ST3, num_steps)
		for i in range(num_steps):
			self.L12_pos += L12_step
			self.L13_pos += L13_step
			self.L14_pos += L14_step 
			pwm.set_pwm(12,0,int(self.L12_pos))
			pwm.set_pwm(13,0,int(self.L13_pos))
			pwm.set_pwm(14,0,int(self.L14_pos))
			#pwm.set_pwm(15,0,self.L15_pos)
			#time.sleep(0.05)

	def clamp(self):
		pwm.set_pwm(15,0,L15_ST1)
		self.L15_pos = L15_ST1

	def loosen(self):
		pwm.set_pwm(15,0,L15_ST4)
		self.L15_pos = L15_ST4


	## higher-level functions

	def reach_out_clamp_and_tuck_in(self):
		self.loosen()
		self.reach_out()
		self.clamp()
		self.tuck_in()






def clean_all():
	pwm.set_pwm(0, 0, 0)
	pwm.set_pwm(1, 0, 0)
	pwm.set_pwm(2, 0, 0)
	pwm.set_pwm(3, 0, 0)
	pwm.set_pwm(4, 0, 0)
	pwm.set_pwm(5, 0, 0)
	pwm.set_pwm(6, 0, 0)
	pwm.set_pwm(7, 0, 0)
	pwm.set_pwm(8, 0, 0)
	pwm.set_pwm(9, 0, 0)
	pwm.set_pwm(10, 0, 0)
	pwm.set_pwm(11, 0, 0)
	pwm.set_pwm(12, 0, 0)
	pwm.set_pwm(13, 0, 0)
	pwm.set_pwm(14, 0, 0)
	pwm.set_pwm(15, 0, 0)
	print("Set all pwm to 0")


if __name__ == '__main__':

	try:
		arm = Arm()

	except KeyboardInterrupt:
		clean_all()



