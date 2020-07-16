#!/usr/bin/env python3
# File name   : move.py
# Description : Control Motor
# Product     : RaspTank  
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/12/27
import time
import RPi.GPIO as GPIO
import ultra


# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

Motor_A_EN    = 7
Motor_B_EN    = 11

Motor_A_Pin1  = 8
Motor_A_Pin2  = 10
Motor_B_Pin1  = 13
Motor_B_Pin2  = 12

Dir_forward   = 0
Dir_backward  = 1

left_forward  = 0
left_backward = 1

right_forward = 0
right_backward= 1

pwn_A = 0
pwm_B = 0

def motorStop():#Motor stops
	GPIO.output(Motor_A_Pin1, GPIO.LOW)
	GPIO.output(Motor_A_Pin2, GPIO.LOW)
	GPIO.output(Motor_B_Pin1, GPIO.LOW)
	GPIO.output(Motor_B_Pin2, GPIO.LOW)
	GPIO.output(Motor_A_EN, GPIO.LOW)
	GPIO.output(Motor_B_EN, GPIO.LOW)


def setup():#Motor initialization

	global pwm_A, pwm_B
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Motor_A_EN, GPIO.OUT)
	GPIO.setup(Motor_B_EN, GPIO.OUT)
	GPIO.setup(Motor_A_Pin1, GPIO.OUT)
	GPIO.setup(Motor_A_Pin2, GPIO.OUT)
	GPIO.setup(Motor_B_Pin1, GPIO.OUT)
	GPIO.setup(Motor_B_Pin2, GPIO.OUT)
	
	motorStop()

	try:
		pwm_A = GPIO.PWM(Motor_A_EN, 1000)
		pwm_B = GPIO.PWM(Motor_B_EN, 1000)
	except:
		pass


def motor_right(status, direction, speed):#Motor 2 positive and negative rotation
	if status == 0: # stop
		GPIO.output(Motor_B_Pin1, GPIO.LOW)
		GPIO.output(Motor_B_Pin2, GPIO.LOW)
		GPIO.output(Motor_B_EN, GPIO.LOW)
	else:
		if direction == Dir_backward:
			GPIO.output(Motor_B_Pin1, GPIO.HIGH)
			GPIO.output(Motor_B_Pin2, GPIO.LOW)
			pwm_B.start(100)
			pwm_B.ChangeDutyCycle(speed)
		elif direction == Dir_forward:
			GPIO.output(Motor_B_Pin1, GPIO.LOW)
			GPIO.output(Motor_B_Pin2, GPIO.HIGH)
			pwm_B.start(0)
			pwm_B.ChangeDutyCycle(speed)


def motor_left(status, direction, speed):#Motor 1 positive and negative rotation
	if status == 0: # stop
		GPIO.output(Motor_A_Pin1, GPIO.LOW)
		GPIO.output(Motor_A_Pin2, GPIO.LOW)
		GPIO.output(Motor_A_EN, GPIO.LOW)
	else:
		if direction == Dir_forward:#
			GPIO.output(Motor_A_Pin1, GPIO.HIGH)
			GPIO.output(Motor_A_Pin2, GPIO.LOW)
			pwm_A.start(100)
			pwm_A.ChangeDutyCycle(speed)
		elif direction == Dir_backward:
			GPIO.output(Motor_A_Pin1, GPIO.LOW)
			GPIO.output(Motor_A_Pin2, GPIO.HIGH)
			pwm_A.start(0)
			pwm_A.ChangeDutyCycle(speed)
	return direction


def move(speed, direction, turn, radius=0.6, CRASH_OVERRIDE=False):   # 0 < radius <= 1  
	speed = 100
	if direction == 'forward':
		if turn == 'left':
			motor_left(0, left_backward, int(speed*radius))
			motor_right(1, right_forward, speed)
		elif turn == 'right':
			motor_left(1, left_forward, speed)
			motor_right(0, right_backward, int(speed*radius))
		else:
			if CRASH_OVERRIDE:
				ultradist = round(ultra.checkdist(),2)
				if ultradist < 0.5:
					motorStop()
			else:
				motor_left(1, left_forward, 100)
				motor_right(1, right_forward, 100)				
	elif direction == 'backward':
		if turn == 'left':
			motor_left(0, left_forward, int(speed*radius))
			motor_right(1, right_backward, speed)
		elif turn == 'right':
			motor_left(1, left_backward, speed)
			motor_right(0, right_forward, int(speed*radius))
		else:
			motor_left(1, left_backward, speed)
			motor_right(1, right_backward, speed)
	elif direction == 'no':
		if turn == 'left':
			motor_left(1, left_backward, 100)
			motor_right(1, right_forward, 100)
		elif turn == 'right':
			motor_left(1, left_forward, 100)
			motor_right(1, right_backward, 100)
		else:
			motorStop()
	else:
		pass


## The following functions added by PHIL

# attempt to move in a square ad infinitum
def move_in_square():
	speed_set = 100 # doesn't look like this affects it ..
	while True:
		move(speed_set, 'forward', '')
		time.sleep(1)
		move(speed_set, 'no', 'right')
		time.sleep(1)

def roomba_pattern():
	speed_set = 100
	BUFFER_DISTANCE = 0.5 # meters
	while True:
		move(speed_set, 'forward', '')
		ultradist = round(ultra.checkdist(),2)
		while ultradist > BUFFER_DISTANCE:
			time.sleep(0.5)
			ultradist = round(ultra.checkdist(),2)
		move(speed_set, 'no', 'right')
		time.sleep(1) # or random


## end user added functions



def destroy():
	motorStop()
	GPIO.cleanup()             # Release resource


if __name__ == '__main__':
	try:
		setup()
		
		#move(100, 'no', 1)
		#time.sleep(2.5)
		#move(-100, 'no', 1)
		#time.sleep(2.5)
		#move(100, 'left', 0.6)
		#time.sleep(5)
		#print('1')
		
		#move(100, 'right', 0.6)
		#time.sleep(5)
		#move(0, 'left', 1)
		#time.sleep(5)

		move_in_square()

		#roomba_pattern()

	except KeyboardInterrupt:
		destroy()

