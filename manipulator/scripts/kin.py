#!/usr/bin/env python
import rospy, numpy
from math import sin, cos
from sensor_msgs.msg import JointState
from visualization_msgs.msg import Marker
from tf2_msgs.msg import TFMessage
from std_msgs.msg import String
from os import system

pub = rospy.Publisher('visualization_marker', Marker, queue_size = 1)
robot = rospy.get_param('manipulator_params')
tool = rospy.get_param('tool_vec')
v0 = numpy.array([[tool['x']], [tool['y']], [tool['z']],[1]])

def T_DH(DHparam):
	th = float(DHparam['theta'])
	a  = float(DHparam['a'])
	d  = float(DHparam['d'])
	al = float(DHparam['alpha'])
	T = numpy.array([[cos(th), -sin(th)*cos(al), sin(th)*sin(al), a*cos(th)],
		[sin(th), cos(th)*cos(al), -cos(th)*sin(al), a*sin(th)],
		[0, sin(al), cos(al), d],
		[0, 0, 0, 1]])
	return T


def callback(data):
    #rospy.loginfo(data.position)
    marker = Marker()
    marker.header.frame_id = "base_link"
    marker.header.stamp = rospy.Time()
    marker.ns = "ns1"
    marker.id = 0
    marker.type = marker.SPHERE
    marker.action = marker.ADD
    marker.pose.orientation.w = 1.0
    marker.scale.x = 0.3
    marker.scale.y = 0.3
    marker.scale.z = 0.3
    marker.color.a = 1.0 
    marker.color.g = 1.0

    params = {}
    v = v0
    for joint in reversed(robot):
    	params['a'] = joint['a']
    	params['theta'] = joint['theta']
    	params['d'] = joint['d']
    	params['alpha'] = joint['alpha']
    	params[joint['move']] += data.position[joint['joint_number'] - 1]
    	T = T_DH(params)
    	v = T.dot(v)
    	#rospy.loginfo(v)
    marker.pose.position.x = v[0]
    marker.pose.position.y = v[1]
    marker.pose.position.z = v[2]
    pub.publish(marker)





def listener():
    rospy.init_node('kin', anonymous = True)


    rospy.Subscriber("joint_states", JointState, callback)

    rospy.spin()


        

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass


        

