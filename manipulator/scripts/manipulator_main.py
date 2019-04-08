#!/usr/bin/env python
import rospy
from rospkg import RosPack

rospack = RosPack()

prefix = """<?xml version="1.0"?>

<robot name="my_manipulator" xmlns:xacro="http://www.ros.org/wiki/xacro">
    <xacro:include filename="$(find manipulator)/urdf/templates.xacro" />
    <xacro:include filename="$(find manipulator)/urdf/base_and_limits.xacro" />
    <xacro:include filename="$(find manipulator)/urdf/dh_parameters.xacro"  />

    <my_link_box name="${l00}" origin_rpy="0 0 0" origin_xyz="0 0 ${base_height_half}" size="${base_size} ${base_height}" />\n"""
postfix = """</robot>"""

def create_main_xacro():
    #rospy.init_node('dh_parameters_maker', anonymous=True)
    dh_in = open(rospack.get_path('manipulator') + "/DH_params.txt","r")
    dh_out = open(rospack.get_path('manipulator') + "/urdf/manipulator_main.xacro", "w")
    

    dh_out.write(prefix)


    dh_lines = dh_in.readlines()
    i=0
    for line in dh_lines:
        if(i!=0):
            dh_out.write("""\t<my_link_cylinder name="${l0""" + str(i) + """}" origin_xyz="${a""" + str(i) + """/2} 0 ${d""" + str(i+1) + """/2}" origin_rpy="0 ${phi""" + str(i+1) + """} 0" radius="${R0""" + str(i) + """}" length="${L""" + str(i+1) + """}"/>\n""") 
        i=i+1

    #CHWYTAKKKKK
    dh_out.write("""\t<my_link_box name="${l0""" + str(i) + """}" origin_xyz="${gripper_height_half} 0 0" origin_rpy="0 0 0" size="${gripper_size} ${gripper_height}"/>\n""") 

    dh_out.write("\n\n\n")

    i=0
    for line in dh_lines:
        #if(i!= len(dh_lines)-1):
        dh_out.write("""<my_joint name="${l0""" + str(i) + "}__${l0" + str(i+1) + """}" type=\"${type""" + str(i) + "}" + """\"\norigin_rpy=\"${alpha""" + str(i) + """} 0 0" origin_xyz="${a""" + str(i) + """} 0 ${d"""+ str(i+1) + """}"\nparent = "${l0""" + str(i) + """}" child = "${l0""" + str(i+1) + """}"/>\n\n""")
        i=i+1

    print("SUCCESS: " + str(i-1) + " rows")
    dh_out.write(postfix)
    dh_out.close()
    dh_in.close()

if __name__ == '__main__':
    try:
        create_main_xacro()
    except rospy.ROSInterruptException:
        pass