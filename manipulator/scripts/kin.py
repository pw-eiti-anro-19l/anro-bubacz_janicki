#!/usr/bin/env python
import rospy
from sensor_msgs.msg import JointState
from tf2_msgs.msg import TFMessage
from std_msgs.msg import String
from os import system

pub = rospy.Publisher('tf', TFMessage, queue_size = 1)


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "%s", data.name[1])
    pub.publish([])





def listener():
    rospy.init_node('kin', anonymous = True)


    rospy.Subscriber("joint_states", JointState, callback)

    rospy.spin()


        

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass


        

