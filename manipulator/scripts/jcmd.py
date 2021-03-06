#!/usr/bin/env python
import rospy, numpy
from manipulator.srv import jint_control_srv
from sensor_msgs.msg import JointState
from std_msgs.msg import String, Header



def jcmd():
    cp = [0.0, 0.0, 3, 1.2, 0.0, 0.2, 1.2, 0.3, 0.2]
    t = [3, 2, 2]
    mode = 1
    rospy.wait_for_service('jint_control_srv')
    try:
        cntrl = rospy.ServiceProxy('jint_control_srv', jint_control_srv)
        resp = cntrl(cp, t, mode)
        print "executable = %d, err_msg = %s"%(resp.executable, resp.err_msg)
    except:
        pass


if __name__ == '__main__':
    try:
        jcmd()
    except rospy.ROSInterruptException:
        pass


        

