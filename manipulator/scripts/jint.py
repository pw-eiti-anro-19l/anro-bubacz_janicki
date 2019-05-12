#!/usr/bin/env python
import rospy, numpy
from manipulator.srv import jint_control_srv
from sensor_msgs.msg import JointState
from std_msgs.msg import String, Header



pose0 = numpy.array([0.0, 0.0, 0.0])
pose_max = numpy.array([3.14, 3.14,3.14])
pose_min = numpy.array([-3.14, -3.14, -3.14])
current_pose = pose0
dt = 0.1                #10Hz

eps = 0.0001            #accuracy

pub = rospy.Publisher('joint_states', JointState, queue_size = 1)
pose = JointState()
pose.name = ['base_link__link_01', 'link_01__link_02', 'link_02__link_03']
pose.header = Header()

def handle_command(request):
    rate = rospy.Rate(10)   #10Hz
    executable = True
    progress = 0
    err_msg = ""
    pose.position = list(current_pose)
    time = numpy.array(request.time)
    points = numpy.array(request.check_points).reshape(-1,3)

    if not(time.shape[0] == points.shape[0]):
        err_msg = "Uncomprehensive data (unequal number of times and points)"
        executable = False

    if min(time) <= 0:
        err_msg = "Invalid times expected (t=<0)"
        executable = False

    p_av = 0
    for p in points:
        p_av += sum(p>pose_max) + sum(p<pose_min)
    if p_av > 0:
        err_msg = "Invalid checkpoints (out of work area)"
        executable = False

    #extrapolacja
    if executable:
            
        progress = 0
        prev_pose = current_pose
        total_t = sum(time)
        curent_time = 0
        current_target = 0
        #liniowa
        if mode == 1:

            while (progress < 1 and current_target < time.shape[0] and executable):

                v = (points[current_target] - prev_pose)*dt/time[current_target]
                if (sum(current_pose + dt * v<pose_max) + sum(current_pose + dt * v>pose_min)) == 0:
                    current_pose += dt * v
                else:
                    executable = False
                    err_msg = "Extrapolated through point outside work area"
                current_time += dt
                progress += dt/total_time
                if numpy.linalg.norm(current_pose - points[current_target]) < eps:
                    current_target += 1
                    prev_pose = current_pose
                pose.header.stamp = rospy.Time.now()
                pose.position = list(current_pose)
                pub.publish(pose)
                rate.sleep()
    else:
        pose.header.stamp = rospy.Time.now()
        pub.publish(pose)



    


def jint():
    rospy.init_node('jint', anonymous = True)
    s = rospy.Service('jint_control_srv', jint_control_srv, handle_command)
    rospy.spin()

        

if __name__ == '__main__':
    try:
        jint()
    except rospy.ROSInterruptException:
        pass


