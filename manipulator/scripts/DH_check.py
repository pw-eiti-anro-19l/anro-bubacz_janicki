#!/usr/bin/env python
import rospy
from math import pow, sqrt, atan2
from std_msgs.msg import String
from rospkg import RosPack

rospack = RosPack()

### Only prismatic & revolute joints

# Order of parameters in file
def read_robot():
    names = ['a', 'd','alpha','theta']

    ### File structure:
    ### a_i d_i alpha_i theta_i
    ### all of above have to be real numbers
    ### joint movement representation: <parameter>+<name> or <name>+<parameter> or <name>
    ### no spaces, parameter is real number start position, name is only-letters word
    ### for revolute joint <theta_i>+<name> eg.: 2 1 0.3 th+3
    ### for prismatic joint <d_i>+<name> eg 2 d 0.1 0.14
    # Load D-H parameters
    f = open(rospack.get_path('manipulator') + "/scripts/DH.txt", 'r')
    # Robot structure
    robot = []
    # number of joint
    joint = 0
    for x in f:
        # Dict for joint
        robot.append({})
        # Params from file
        spl = x.split()
        # count of only number records in line
        count_num = 0
        # count of name/name-value pairs
        count_par = 0
        # index of parameter (vide 'names')
        parameter = 0
        for param in spl:
            # check if single number
            if param.replace('.','',1).isdigit():
                count_num += 1
                robot[joint].update({names[parameter]:param})
            else:
                # check if single name
                if param.isalpha():
                    count_par += 1
                    robot[joint].update({names[parameter]:0})
                    robot[joint].update({'move':names[parameter]})
                else:
                    # check if name-value pair
                    pars = param.split("+",1)
                    if len(pars) == 2:
                        if pars[0].isalpha() and pars[1].replace('.','',1).isdigit():
                            count_par += 1
                            robot[joint].update({names[parameter]:pars[1]})
                            robot[joint].update({'move':names[parameter]})
                        if pars[1].isalpha() and pars[0].replace('.','',1).isdigit():
                            count_par += 1
                            robot[joint].update({names[parameter]:pars[0]})
                            robot[joint].update({'move':names[parameter]})
            parameter += 1
        # check if 5th clas joint
        if count_num == 3 and count_par == 1:
            robot[joint].update({'valid':True})
        else:
            robot[joint].update({'valid':False})
        if robot[joint]['valid']:
            # check if prismatic/revolute joint
            if robot[joint]['move'] == names[1]:
                robot[joint].update({'type':'prismatic'})
            elif robot[joint]['move'] == names[3]:
                robot[joint].update({'type':'revolute'})
            else:
                robot[joint].update({'valid':False})
        if not robot[joint]['valid']:
            # remove obstolete data if invalid joint
            robot.remove(robot[joint])
            robot.append({'valid':False})
        robot[joint].update({'joint_number':(joint+1)})
        # print(robot[joint])
        joint += 1

    ### Convert to ROS structures
    ### Only if whole structure is valid
    ###

    valid = True
    for joint in robot:
        if not joint['valid']:
            valid = False
            return False
        else:
            return robot


prefix = """<?xml version="1.0" ?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">\n"""
postfix = """</robot>"""


#def write_params():



def create_df_xacro(robot):
    #rospy.init_node('dh_parameters_maker', anonymous=True)
    dh_in = open(rospack.get_path('manipulator') + "/DH_params.txt","r")
    dh_out = open(rospack.get_path('manipulator') + "/urdf/dh_parameters.xacro", "w")
    
    dh_out.write(prefix)


    i=1;
    for joint in robot:
        # print (i)
        dh_out.write("""\t<xacro:property name="a""" + str(i-1) + """\"    \tvalue=\"""" + str(robot[i-1]['a']) + """\"\t/>\n""") 
        dh_out.write("""\t<xacro:property name="alpha""" + str(i-1) + """\"\tvalue=\"""" + """${""" + str(robot[i-1]['alpha'])+ "}" + """\"\t/>\n""")
        dh_out.write("""\t<xacro:property name="d""" + str(i) + """\"    \tvalue=\"""" + str(robot[i-1]['d']) + """\"\t/>\n""")
        dh_out.write("""\t<xacro:property name="L""" + str(i) + """\"    \tvalue=\"""" + str(sqrt(pow(float(robot[i-1]['a']),2) + pow(float(robot[i-1]['d']),2))) + """\"\t/>\n""")
        dh_out.write("""\t<xacro:property name="phi""" + str(i) + """\"    \tvalue=\"""" + str(atan2(float(robot[i-1]['a']),float(robot[i-1]['d']))) + """\"\t/>\n""")
        dh_out.write("""\t<xacro:property name="type""" + str(i-1) + """\"    \tvalue=\"""" + str(robot[i-1]['type']) + """\"\t/>\n\n""")
        i=i+1

    dh_in.close()
    dh_out.write(postfix)
    dh_out.close()

if __name__ == '__main__':
    try: 
        robot = read_robot()
    except rospy.ROSInterruptException:
        pass
    try:
        if not robot == False:
            create_df_xacro(robot)
    except rospy.ROSInterruptException:
        pass