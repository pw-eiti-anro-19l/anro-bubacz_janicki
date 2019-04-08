#!/usr/bin/env python
import rospy
from math import pow, sqrt, atan2
from std_msgs.msg import String
from rospkg import RosPack

rospack = RosPack()

prefix = """<?xml version="1.0" ?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">\n"""
postfix = """</robot>"""

def create_df_xacro():
    #rospy.init_node('dh_parameters_maker', anonymous=True)
    dh_in = open(rospack.get_path('manipulator') + "/DH_params.txt","r")
    dh_out = open(rospack.get_path('manipulator') + "/urdf/dh_parameters.xacro", "w")
    
    dh_out.write(prefix)

    dh_lines = dh_in.readlines()

    i=1;
    for line in dh_lines:
        words = line.split()
        print (i)
        dh_out.write("""\t<xacro:property name="a""" + str(i-1) + """\"    \tvalue=\"""" + str(words[0]) + """\"\t/>\n""") 
        dh_out.write("""\t<xacro:property name="alpha""" + str(i-1) + """\"\tvalue=\"""" + """${""" + str(words[1])+ "}" + """\"\t/>\n""")
        dh_out.write("""\t<xacro:property name="d""" + str(i) + """\"    \tvalue=\"""" + str(words[2]) + """\"\t/>\n""")
        dh_out.write("""\t<xacro:property name="L""" + str(i) + """\"    \tvalue=\"""" + str(sqrt(pow(float(words[0]),2) + pow(float(words[2]),2))) + """\"\t/>\n""")
        dh_out.write("""\t<xacro:property name="phi""" + str(i) + """\"    \tvalue=\"""" + str(atan2(float(words[0]),float(words[2]))) + """\"\t/>\n\n""")
        i=i+1

    dh_in.close()
    dh_out.write(postfix)
    dh_out.close()

if __name__ == '__main__':
    try:
        create_df_xacro()
    except rospy.ROSInterruptException:
        pass