#!/usr/bin/env python
import rospy
import rospkg
rospack = rospkg.RosPack()

prefix = """<?xml version="1.0"?>

<robot name="my_manipulator" xmlns:xacro="http://www.ros.org/wiki/xacro">

    <xacro:property name="limit_effort"     value="1000.0"  />
    <xacro:property name="limit_lower"      value="${-pi}"  />
    <xacro:property name="limit_upper"      value="${pi}"   />
    <xacro:property name="limit_velocity"   value="0.5"     />
    
    <xacro:property name="base_size"        value="1.5 1.5" />
    <xacro:property name="base_height"      value="0.1"     />
    <xacro:property name="base_height_half" value="${base_height/2.0}" />  

    <xacro:property name="l00"          value="base_link"           />\n"""

postfix = """</robot>"""

STARTING_RADIUS = 0.3
LINK_RADIUS_DECREMENTATION = 0.05
MINIMUM_RADIUS = 0.1

def countRadius(link_number):
    currentRadius = STARTING_RADIUS - link_number * LINK_RADIUS_DECREMENTATION
    if currentRadius <=  MINIMUM_RADIUS:
        return MINIMUM_RADIUS
    else:
        return currentRadius

def create_main_xacro():
    #rospy.init_node('dh_parameters_maker', anonymous=True)
    dh_in = open(rospack.get_path('manipulator')+"/DH_params.txt","r")
    dh_out = open(rospack.get_path('manipulator')+"/urdf/base_and_limits.xacro", "w")

    dh_out.write(prefix)

    dh_lines = dh_in.readlines()
    i=0
    for line in dh_lines:
        if i!=0:
            dh_out.write("""\t<xacro:property name="l0""" + str(i) + """"          value="link_0""" + str(i) + """"             />\n""")
        i=i+1

    dh_out.write("\n\n")

    i=0
    for line in dh_lines:
        if i!=0:
            dh_out.write("""\t<xacro:property name="R0""" + str(i) + """"          value=\"""" + str(countRadius(i)) + """"             />\n""")
        i=i+1
        

    dh_out.write(postfix)
    dh_out.close()
    dh_in.close()

if __name__ == '__main__':
    try:
        create_main_xacro()
    except rospy.ROSInterruptException:
        pass