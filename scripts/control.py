#!/usr/bin/env python
from rospy import Publisher, ROSInterruptException, init_node, Rate, is_shutdown, get_param
from geometry_msgs.msg import Twist
from os import system


def display(keys):
	print 'Press button and accept with enter:'
	print keys['fwd'],' to move forward'
	print keys['bwd'],' to move backward'
	print keys['rht'],' to move right'
	print keys['lft'],' to move left'
	print 'Press <q> to quit'


def get_move(keys):
	key = ''
	while key == '':
		key = raw_input('')
		move = Twist()
		if key == keys["fwd"]:
			move.linear.x = 1.0
		elif key == keys["bwd"]:
			move.linear.x = -1.0
		elif key == keys["rht"]:
			move.angular.z = -0.5
		elif key == keys["lft"]:
			move.angular.z = 0.5
		elif key == 'q':
			move = 'quit'
		else:
			return None
		return move




def step():
	publisher = Publisher('turtle1/cmd_vel', Twist, queue_size = 10)
	init_node('control')
	rate = Rate(100)

	
	while not is_shutdown():
		keys = {
		"fwd": get_param('fwd'),
		"bwd": get_param('bwd'),
		"rht": get_param('rht'),
		"lft": get_param('lft')
		}
		system('clear')
		display(keys)
		move = get_move(keys)
		if move == 'quit':
			return True
			break
		if move is not None:
			publisher.publish(move)
		rate.sleep()
		

if __name__ == '__main__':
	try:
		step()
	except ROSInterruptException:
		pass


		

