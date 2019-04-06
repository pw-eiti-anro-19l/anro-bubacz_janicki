#!/usr/bin/env python
import rospy
from math import pow, sqrt, atan2
from std_msgs.msg import String
import rospkg
rospack = rospkg.RosPack()

prefix = """<?xml version="1.0" ?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">\n"""
postfix = """</robot>"""


#    <xacro:property name="a0"               value="0"           />
 #   <xacro:property name="a1"               value="0"           />
  #  <xacro:property name="a2"               value="0"           />
   # <xacro:property name="alpha0"           value="0"           />
    #<xacro:property name="alpha1"           value="${pi/2.0}"   />
    #<xacro:property name="alpha2"           value="${pi/2.0}"   />
    #<xacro:property name="d1"               value="0"           />
    #<xacro:property name="d2"               value="${L01}"      />
    #<xacro:property name="d3"               value="${L02}"      />

if __name__ == '__main__':
    try:
        DH_file = open(rospack.get_path('manipulator')+"/DH_params.txt","r")
        out = open(rospack.get_path('manipulator')+"/urdf/dh.xacro", "w")
        out.write(prefix)
        DH_lines = DH_file.readlines()
        i=1;
        for line in DH_lines:
            words = line.split()
            print (i)
            out.write("""\t<xacro:property name="a""" + str(i-1) + """\"    \tvalue=\"""" + str(words[0]) + """\"\t/>\n""") 
            out.write("""\t<xacro:property name="alpha""" + str(i-1) + """\"\tvalue=\"""" + """${""" + str(words[1])+ "}" + """\"\t/>\n""")
            out.write("""\t<xacro:property name="d""" + str(i) + """\"    \tvalue=\"""" + str(words[2]) + """\"\t/>\n\n""")
            sumaKwadratow = sqrt(pow(float(words[0]),2) + pow(float(words[2]),2))

            out.write("""\t<xacro:property name="L""" + str(i) + """\"    \tvalue=\"""" + str(sumaKwadratow) + """\"\t/>\n\n""")
            out.write("""\t<xacro:property name="phi""" + str(i) + """\"    \tvalue=\"""" + str(atan2(float(words[0]),float(words[2]))) + """\"\t/>\n\n""")
            i=i+1

        DH_file.close()
        out.write(postfix)
        out.close()
    except rospy.ROSInterruptException:
        pass