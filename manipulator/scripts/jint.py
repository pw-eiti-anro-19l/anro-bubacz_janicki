#!/usr/bin/env python
import rospy, numpy
from manipulator.srv import *
from sensor_msgs.msg import JointState
from std_msgs.msg import String, Header



pose0 = numpy.array([0.0, 0.0, 0.0])
pose_max = numpy.array([3.14, 3.14,3.14])
pose_min = numpy.array([-3.14, -3.14, -3.14])
v_max = numpy.array([0.2, 0.2, 0.5])
a = numpy.array([0.05, 0.05, 0.1])
current_pose = pose0
dt = 0.1                #100Hz

eps = 0.001            #accuracy


pub = rospy.Publisher('joint_states', JointState, queue_size = 1)
pose = JointState()
pose.name = ['base_link__link_01', 'link_01__link_02', 'link_02__link_03']
pose.header = Header()

def count_acceleration(current_target, points, prev_pose):
    global v_max, a
    is_triangular = 0
    l = numpy.abs((points[current_target] - prev_pose))
    conditions = numpy.divide(v_max**2,a)
    t1 = l>conditions
    t2 = conditions>l
    max_times = numpy.multiply((numpy.divide(v_max, a) + numpy.divide(l, v_max)), t1) + numpy.multiply(2*numpy.sqrt((numpy.divide(l,a))), t2)
    #x = max(max_times)
    a_temp = [0,0,0]
    t_id = numpy.argmax(max_times)
    if(t1[t_id]):
        t_a = v_max[t_id]/a[t_id]
        t_j = max_times[t_id] - 2*t_a
        a_temp[t_id] = a[t_id]
        a_temp[:t_id] = numpy.divide(l[:t_id],(t_a**2+t_a*t_j))
        a_temp[t_id:] = numpy.divide(l[t_id:],(t_a**2+t_a*t_j))
        is_triangular = 0
    else:
        t_a = numpy.sqrt(l[t_id]/a[t_id])
        t_j = 0
        a_temp[t_id] = a[t_id]
        a_temp[:t_id] = 2*numpy.divide(l[:t_id],t_a**2)
        a_temp[t_id:] = 2*numpy.divide(l[t_id:],t_a**2)
        is_triangular = 1
    ret = {'t_a':t_a, 'a_temp':a_temp, 'shape':is_triangular}
    return ret 

def handle_command(request):
    global pose0
    global pose_max
    global pose_min
    global current_pose
    rate = rospy.Rate(10)   #100Hz
    executable = True
    progress = 0
    err_msg = ""
    pose.position = list(current_pose)
    time = numpy.array(request.time)
    points = numpy.array(request.check_points).reshape(-1,3)
    mode = request.mode

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
        total_time = sum(time)
        current_time = 0
        current_target = 0

        #trapezy
        if mode == 1:
            #print points[current_target]
            data = count_acceleration(current_target, points, prev_pose)
            t_a = data['t_a']
            a_temp = data['a_temp']
            is_triangular = data['shape']
            #print current_pose
            v = numpy.array([0.,0.,0.])
            a = numpy.array([0.,0.,0.])
            t_i = 0

            while (current_target < time.shape[0] and executable):
                if t_i < t_a:
                    a = a_temp
                elif t_i < t_a + t_j:
                    a = numpy.array([0.,0.,0.])
                else:
                    a = -a_temp
                v += a
                t_i += dt
                next_pose = current_pose + v*dt
                if (sum(next_pose>pose_max) + sum(next_pose<pose_min)) == 0:
                    current_pose =  next_pose
                    #print current_pose
                else:
                    executable = False
                    err_msg = "Extrapolated through point outside work area"
                current_time += dt
                if numpy.linalg.norm(current_pose - points[current_target]) < eps:
                    print "finished phase"
                    current_target += 1
                    prev_pose = current_pose
                    if not(current_target == time.shape[0]):
                        data = count_acceleration(current_target, points, prev_pose)
                        t_a = data['t_a']
                        a_temp = data['a_temp']
                        is_triangular = data['shape']
                        t_i = 0
                pose.header.stamp = rospy.Time.now()
                pose.position = list(current_pose)
                print t_i
                print current_pose
                print t_a
                pub.publish(pose)
                rate.sleep()
        #liniowe
        if mode == 2:
            v = (points[current_target] - prev_pose)/time[current_target]
            print current_pose
            while (progress < 1 and current_target < time.shape[0] and executable):
                if (sum((current_pose + dt * v)>pose_max) + sum((current_pose + dt * v)<pose_min)) == 0:
                    current_pose +=  v*dt
                    print current_pose
                else:
                    executable = False
                    err_msg = "Extrapolated through point outside work area"
                current_time += dt
                progress += dt/total_time
                if numpy.linalg.norm(current_pose - points[current_target]) < eps:
                    print "finished phase"
                    current_target += 1
                    prev_pose = current_pose
                    if not(current_target == time.shape[0]):
                        v = (points[current_target] - prev_pose)/time[current_target]
                pose.header.stamp = rospy.Time.now()
                pose.position = list(current_pose)
                pub.publish(pose)
                rate.sleep()

    else:
        pose.header.stamp = rospy.Time.now()
        pub.publish(pose)
    return jint_control_srvResponse(executable, err_msg)



    


def jint():
    rospy.init_node('jint', anonymous = True)
    s = rospy.Service('jint_control_srv', jint_control_srv, handle_command)
    rospy.spin()

        

if __name__ == '__main__':
    try:
        jint()
    except rospy.ROSInterruptException:
        pass


