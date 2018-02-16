#  Author(s):  Anton Deguet
#  Created on: 2018-02-15

# (C) Copyright 2018 Johns Hopkins University (JHU), All Rights Reserved.

# --- begin cisst license - do not edit ---

# This software is provided "as is" under an open source license, with
# no warranty.  The complete license can be found in license.txt and
# http://www.cisst.org/cisst/license.txt.

# --- end cisst license ---

import inspect
import threading
import math

import rospy
import numpy
import PyKDL

# we should probably not import the symbols and put them in current namespace
from tf import transformations
from tf_conversions import posemath
from std_msgs.msg import String, Bool, Float32, Empty, Float64MultiArray
from geometry_msgs.msg import TransformStamped, Vector3, Quaternion, WrenchStamped, TwistStamped
from sensor_msgs.msg import JointState, Joy

class utils:
    def add_internals(class_instance):
        print ('checking if object has __crtk__')
        if not class_instance.hasattr("__crtk__"):
            class_instance.setattr("__crtk__", {})

    def add_servoed_js(class_instance, ros_namespace):
        print ('adding servoed js')
        utils.add_internal(class_instance)
        print ('added servoed js')



# # from code import InteractiveConsole
# # from imp import new_module

# #class Console(InteractiveConsole):
# #    def __init__(self, names=None):
# #        names = names or {}
# #        names['console'] = self
# #        InteractiveConsole.__init__(self, names)
# #        self.superspace = new_module('superspace')
# #
# #    def enter(self, source):
# #        source = self.preprocess(source)
# #        self.runcode(source)
# #
# #    @staticmethod
# #    def preprocess(source):
# #        return source

# class arm(object):
#     """Simple arm API wrapping around ROS messages
#     """

#     # initialize the arm
#     def __init__(self, arm_name, ros_namespace = '/dvrk/'):
#         # base class constructor in separate method so it can be called in derived classes
#         self.__init_arm(arm_name, ros_namespace)


#     def __init_arm(self, arm_name, ros_namespace = '/dvrk/'):
#         """Constructor.  This initializes a few data members.It
#         requires a arm name, this will be used to find the ROS
#         topics for the arm being controlled.  For example if the
#         user wants `PSM1`, the ROS topics will be from the namespace
#         `/dvrk/PSM1`"""
#         # data members, event based
#         self.__arm_name = arm_name
#         self.__ros_namespace = ros_namespace
#         self.__arm_current_state = ''
#         self.__arm_current_state_event = threading.Event()
#         self.__arm_desired_state = ''
#         self.__goal_reached = False
#         self.__goal_reached_event = threading.Event()

#         # continuous publish from dvrk_bridge
#         self.__servoed_jp = numpy.array(0, dtype = numpy.float)
#         self.__servoed_jf = numpy.array(0, dtype = numpy.float)
#         self.__servoed_cp = PyKDL.Frame()
#         self.__servoed_cp_local = PyKDL.Frame()
#         self.__measured_jp = numpy.array(0, dtype = numpy.float)
#         self.__measured_jv = numpy.array(0, dtype = numpy.float)
#         self.__measured_jf = numpy.array(0, dtype = numpy.float)
#         self.__measured_cp = PyKDL.Frame()
#         self.__measured_cp_local = PyKDL.Frame()
#         self.__measured_cv = numpy.zeros(6, dtype = numpy.float)
#         self.__measured_cf = numpy.zeros(6, dtype = numpy.float)
#         self.__jacobian_spatial = numpy.ndarray(0, dtype = numpy.float)
#         self.__jacobian_body = numpy.ndarray(0, dtype = numpy.float)

#         self.__sub_list = []
#         self.__pub_list = []

#         # publishers
#         frame = PyKDL.Frame()
#         self.__full_ros_namespace = self.__ros_namespace + self.__arm_name
#         self.__set_arm_desired_state_pub = rospy.Publisher(self.__full_ros_namespace
#                                                            + '/set_desired_state',
#                                                            String, latch = True, queue_size = 1)
#         self.__servo_jp_pub = rospy.Publisher(self.__full_ros_namespace
#                                               + '/servo_jp',
#                                               JointState, latch = True, queue_size = 1)
#         self.__move_jp_pub = rospy.Publisher(self.__full_ros_namespace
#                                              + '/move_jp',
#                                              JointState, latch = True, queue_size = 1)
#         self.__servo_cp_pub = rospy.Publisher(self.__full_ros_namespace
#                                               + '/servo_cp',
#                                               TransformStamped, latch = True, queue_size = 1)
#         self.__move_cp_pub = rospy.Publisher(self.__full_ros_namespace
#                                              + '/move_cp',
#                                              TransformStamped, latch = True, queue_size = 1)
#         self.__servo_jf_pub = rospy.Publisher(self.__full_ros_namespace
#                                               + '/servo_jf',
#                                               JointState, latch = True, queue_size = 1)
#         self.__servo_cf_body_pub = rospy.Publisher(self.__full_ros_namespace
#                                                    + '/servo_cf',
#                                                    WrenchStamped, latch = True, queue_size = 1)
#         self.__servo_cf_orientation_absolute_pub = rospy.Publisher(self.__full_ros_namespace
#                                                                    + '/set_wrench_body_orientation_absolute',
#                                                                    Bool, latch = True, queue_size = 1)
#         self.__servo_cf_spatial_pub = rospy.Publisher(self.__full_ros_namespace
#                                                       + '/servo_cf',
#                                                       WrenchStamped, latch = True, queue_size = 1)
#         self.__set_gravity_compensation_pub = rospy.Publisher(self.__full_ros_namespace
#                                                               + '/set_gravity_compensation',
#                                                               Bool, latch = True, queue_size = 1)
#         self.__pub_list = [self.__set_arm_desired_state_pub,
#                            self.__servo_jp_pub,
#                            self.__move_jp_pub,
#                            self.__servo_cp_pub,
#                            self.__move_cp_pub,
#                            self.__servo_jf_pub,
#                            self.__servo_cf_body_pub,
#                            self.__servo_cf_orientation_absolute_pub,
#                            self.__servo_cf_spatial_pub,
#                            self.__set_gravity_compensation_pub]
#         # subscribers
#         self.__sub_list = [rospy.Subscriber(self.__full_ros_namespace + '/current_state',
#                                             String, self.__arm_current_state_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/desired_state',
#                                           String, self.__arm_desired_state_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/goal_reached',
#                                           Bool, self.__goal_reached_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/servoed_js',
#                                           JointState, self.__servoed_js_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/servoed_cp',
#                                           TransformStamped, self.__servoed_cp_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/local/servoed_cp',
#                                           TransformStamped, self.__servoed_cp_local_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/measured_js',
#                                           JointState, self.__measured_js_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/measured_cp',
#                                           TransformStamped, self.__measured_cp_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/local/measured_cp',
#                                           TransformStamped, self.__measured_cp_local_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/measured_cv',
#                                           TwistStamped, self.__measured_cv_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/measured_cf',
#                                           WrenchStamped, self.__measured_cf_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/jacobian_spatial',
#                                           Float64MultiArray, self.__jacobian_spatial_cb),
#                            rospy.Subscriber(self.__full_ros_namespace + '/jacobian_body',
#                                           Float64MultiArray, self.__jacobian_body_cb)]

#         # create node
#         if not rospy.get_node_uri():
#             rospy.init_node('arm_api', anonymous = True, log_level = rospy.WARN)
#         else:
#             rospy.logdebug(rospy.get_caller_id() + ' -> ROS already initialized')


#     def __arm_current_state_cb(self, data):
#         """Callback for arm current state.

#         :param data: the current arm state"""
#         self.__arm_current_state = data.data
#         self.__arm_current_state_event.set()


#     def __arm_desired_state_cb(self, data):
#         """Callback for arm desired state.

#         :param data: the desired arm state"""
#         self.__arm_desired_state = data.data


#     def __goal_reached_cb(self, data):
#         """Callback for the goal reached.

#         :param data: the goal reached"""
#         self.__goal_reached = data.data
#         self.__goal_reached_event.set()


#     def __servoed_js_cb(self, data):
#         """Callback for the joint desired position.

#         :param data: the `JointState <http://docs.ros.org/api/sensor_msgs/html/msg/JointState.html>`_desired"""
#         self.__servoed_jp.resize(len(data.position))
#         self.__servoed_jf.resize(len(data.effort))
#         self.__servoed_jp.flat[:] = data.position
#         self.__servoed_jf.flat[:] = data.effort


#     def __servoed_cp_cb(self, data):
#         """Callback for the cartesian desired position.

#         :param data: the cartesian position desired"""
#         self.__servoed_cp = TransformFromMsg(data.transform)


#     def __servoed_cp_local_cb(self, data):
#         """Callback for the cartesian desired position.

#         :param data: the cartesian position desired"""
#         self.__servoed_cp_local = TransformFromMsg(data.transform)


#     def __measured_js_cb(self, data):
#         """Callback for the current joint position.

#         :param data: the `JointState <http://docs.ros.org/api/sensor_msgs/html/msg/JointState.html>`_current"""
#         self.__measured_jp.resize(len(data.position))
#         self.__measured_jv.resize(len(data.velocity))
#         self.__measured_jf.resize(len(data.effort))
#         self.__measured_jp.flat[:] = data.position
#         self.__measured_jv.flat[:] = data.velocity
#         self.__measured_jf.flat[:] = data.effort


#     def __measured_cp_cb(self, data):
#         """Callback for the current cartesian position.

#         :param data: The cartesian position current."""
#         self.__measured_cp = TransformFromMsg(data.transform)


#     def __measured_cp_local_cb(self, data):
#         """Callback for the current cartesian position.

#         :param data: The cartesian position current."""
#         self.__measured_cp_local = TransformFromMsg(data.transform)


#     def __measured_cv_cb(self, data):
#         """Callback for the current twist in body frame.

#         :param data: Twist."""
#         self.__measured_cv[0] = data.twist.linear.x
#         self.__measured_cv[1] = data.twist.linear.y
#         self.__measured_cv[2] = data.twist.linear.z
#         self.__measured_cv[3] = data.twist.angular.x
#         self.__measured_cv[4] = data.twist.angular.y
#         self.__measured_cv[5] = data.twist.angular.z


#     def __measured_cf_cb(self, data):
#         """Callback for the current wrench in body frame.

#         :param data: Wrench."""
#         self.__measured_cf[0] = data.wrench.force.x
#         self.__measured_cf[1] = data.wrench.force.y
#         self.__measured_cf[2] = data.wrench.force.z
#         self.__measured_cf[3] = data.wrench.torque.x
#         self.__measured_cf[4] = data.wrench.torque.y
#         self.__measured_cf[5] = data.wrench.torque.z

#     def __jacobian_spatial_cb(self, data):
#         """Callback for the Jacobian in spatial frame.

#         :param data: Jacobian."""
#         jacobian = numpy.asarray(data.data)
#         jacobian.shape = data.layout.dim[0].size, data.layout.dim[1].size
#         self.__jacobian_spatial = jacobian

#     def __jacobian_body_cb(self, data):
#         """Callback for the Jacobian in spatial frame.

#         :param data: Jacobian."""
#         jacobian = numpy.asarray(data.data)
#         jacobian.shape = data.layout.dim[0].size, data.layout.dim[1].size
#         self.__jacobian_body = jacobian

#     def __set_desired_state(self, state, timeout = 5):
#         """Set state with block.

#         :param state: the desired arm state
#         :param timeout: the amount of time you want to wait for arm to change state
#         :return: whether or not the arm state has been successfuly set
#         :rtype: Bool"""
#         if (self.__arm_desired_state == state):
#             return True
#         self.__arm_current_state_event.clear()
#         self.__set_arm_desired_state_pub.publish(state)
#         self.__arm_current_state_event.wait(timeout)
#         # if the state is not changed return False
#         if (self.__arm_current_state != state):
#             rospy.logfatal(rospy.get_caller_id() + ' -> failed to reach state ' + state)
#             return False
#         return True


#     def name(self):
#         return self.__arm_name


#     def home(self):
#         """This method will provide power to the arm and will home
#         the arm."""
#         # if we already received a state
#         if (self.__arm_current_state == 'READY'):
#             return
#         self.__arm_current_state_event.clear()
#         self.__set_arm_desired_state_pub.publish('READY')
#         counter = 10 # up to 10 transitions to get ready
#         while (counter > 0):
#             self.__arm_current_state_event.wait(20) # give up to 20 secs for each transition
#             if (self.__arm_current_state != 'READY'):
#                 self.__arm_current_state_event.clear()
#                 counter = counter - 1
#             else:
#                 counter = -1
#         if (self.__arm_current_state != 'READY'):
#             rospy.logfatal(rospy.get_caller_id() + ' -> failed to reach state READY')


#     def shutdown(self):
#         """Stop providing power to the arm."""
#         self.__set_desired_state('UNINITIALIZED', 20)


#     def get_arm_current_state(self):
#         """Get the arm current state.
#         :returns: the arm current state
#         :rtype: string"""
#         return self.__arm_current_state


#     def get_arm_desired_state(self):
#         """Get the arm desired state.
#         :returns: the arm desired state
#         :rtype: string"""
#         return self.__arm_desired_state


#     def measured_cp(self):
#         """Get the :ref:`current cartesian position <currentvdesired>` of the arm.

#         :returns: the current position of the arm in cartesian space
#         :rtype: `PyKDL.Frame <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_"""
#         return self.__measured_cp


#     def measured_cp_local(self):
#         """Get the :ref:`current cartesian position <currentvdesired>` of the arm.

#         :returns: the current position of the arm in cartesian space
#         :rtype: `PyKDL.Frame <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_"""
#         return self.__measured_cp_local


#     def measured_cv(self):
#         """Get the current cartesian velocity of the arm.  This
#         is based on the body jacobian, both linear and angular are
#         rotated to be defined in base frame.

#         :returns: the current position of the arm in cartesian space
#         :rtype: geometry_msgs.TwistStamped"""
#         return self.__measured_cv


#     def measured_cf_body(self):
#         """Get the current cartesian force applied on arm.  This is
#         based on the body jacobian, both linear and angular are
#         rotated to be defined in base frame if the flag
#         wrench_body_orientation_absolute is set to True.  See method
#         set_wrench_body_orientation_absolute.

#         :returns: the current force applied to the arm in cartesian space
#         :rtype: geometry_msgs.WrenchStamped"""
#         return self.__measured_cf


#     def measured_jp(self):
#         """Get the :ref:`current joint position <currentvdesired>` of
#         the arm.

#         :returns: the current position of the arm in joint space
#         :rtype: `JointState <http://docs.ros.org/api/sensor_msgs/html/msg/JointState.html>`_"""
#         return self.__measured_jp


#     def measured_jv(self):
#         """Get the :ref:`current joint velocity <currentvdesired>` of
#         the arm.

#         :returns: the current position of the arm in joint space
#         :rtype: `JointState <http://docs.ros.org/api/sensor_msgs/html/msg/JointState.html>`_"""
#         return self.__measured_jv


#     def get_current_joint_effort(self):
#         """Get the :ref:`current joint effort <currentvdesired>` of
#         the arm.

#         :returns: the current position of the arm in joint space
#         :rtype: `JointState <http://docs.ros.org/api/sensor_msgs/html/msg/JointState.html>`_"""
#         return self.__measured_jf

#     def get_jacobian_spatial(self):
#         """Get the :ref:`jacobian spatial` of the arm.

#         :returns: the jacobian spatial of the arm
#         :rtype: `numpy.ndarray <https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html>`_"""
#         return self.__jacobian_spatial

#     def get_jacobian_body(self):
#         """Get the :ref:`jacobian body` of the arm.

#         :returns: the jacobian body of the arm
#         :rtype: `numpy.ndarray <https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html>`_"""
#         return self.__jacobian_body

#     def servoed_cp(self):
#         """Get the :ref:`desired cartesian position <currentvdesired>` of the arm.

#         :returns: the desired position of the arm in cartesian space
#         :rtype: `PyKDL.Frame <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_"""
#         return self.__servoed_cp


#     def servoed_cp_local(self):
#         """Get the :ref:`desired cartesian position <currentvdesired>` of the arm.

#         :returns: the desired position of the arm in cartesian space
#         :rtype: `PyKDL.Frame <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_"""
#         return self.__servoed_cp_local


#     def servoed_jp(self):
#         """Get the :ref:`desired joint position <currentvdesired>` of
#         the arm.

#         :returns: the desired position of the arm in joint space
#         :rtype: `JointState <http://docs.ros.org/api/sensor_msgs/html/msg/JointState.html>`_"""
#         return self.__servoed_jp


#     def servoed_jf(self):
#         """Get the :ref:`desired joint effort <currentvdesired>` of
#         the arm.

#         :returns: the desired effort of the arm in joint space
#         :rtype: `JointState <http://docs.ros.org/api/sensor_msgs/html/msg/JointState.html>`_"""
#         return self.__servoed_jf


#     def get_joint_number(self):
#         """Get the number of joints on the arm specified.

#         :returns: the number of joints on the specified arm
#         :rtype: int"""
#         joint_num = len(self.__servoed_jp)
#         return joint_num


#     def __check_input_type(self, input, type_list):
#         """Check if the data input is a data type that is located in type_list

#         :param input: The data type that needs to be checked.
#         :param type_list : A list of types to check input against.
#         :returns: whether or not the input is a type in type_list
#         :rtype: Bool"""
#         found = False
#         # check the input against all input_type
#         for i in range (len(type_list)):
#             if (type(input) is type_list[i]):
#                   return True
#         # not of type_list print state for this error inside
#         if (found == False):
#             print 'Error in ', inspect.stack()[1][3], 'input is of type', input, 'and is not one of:'
#             message = ''
#             # skip_length
#             i = 0
#             while i < len(type_list):
#                 message += ' '
#                 message += str(type_list[i])
#                 i += 1
#             print message
#         return False


#     def dmove(self, delta_input, interpolate = True, blocking = True):
#         """Incremental motion in cartesian space.

#         :param delta_input: the incremental motion you want to make
#         :param interpolate: see  :ref:`interpolate <interpolate>`
#         """
#         # is this a legal translation input
#         if (self.__check_input_type(delta_input, [PyKDL.Vector, PyKDL.Rotation, PyKDL.Frame])):
#             if (type(delta_input) is PyKDL.Vector):
#                 return self.__dmove_translation(delta_input, interpolate, blocking)
#             elif (type(delta_input) is PyKDL.Rotation):
#                 return self.__dmove_rotation(delta_input, interpolate, blocking)
#             elif (type(delta_input) is PyKDL.Frame):
#                 return self.__dmove_frame(delta_input, interpolate, blocking)


#     def __dmove_translation(self, delta_translation, interpolate = True, blocking = True):
#         """Incremental translation (using PYKDL Vector) in cartesian space.

#         :param delta_translation: the incremental translation you want to make based on the current position, this is in terms of a  `PyKDL.Vector <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""
#         # convert into a Frame
#         delta_rotation = PyKDL.Rotation.Identity()
#         delta_frame = PyKDL.Frame(delta_rotation, delta_translation)
#         return self.__dmove_frame(delta_frame, interpolate, blocking)


#     def __dmove_rotation(self, delta_rotation, interpolate = True, blocking = True):
#         """Incremental rotation (using PyKDL Rotation) in cartesian plane.

#         :param delta_rotation: the incremental `PyKDL.Rotation <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_ based upon the current position
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""
#         # convert into a Frame
#         delta_vector = PyKDL.Vector(0.0, 0.0, 0.0)
#         delta_frame = PyKDL.Frame(delta_rotation, delta_vector)
#         return self.__dmove_frame(delta_frame, interpolate, blocking)


#     def __dmove_frame(self, delta_frame, interpolate = True, blocking = True):
#         """Incremental move (using PyKDL Frame) in cartesian plane.

#         :param delta_frame: the incremental `PyKDL.Frame <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_ based upon the current position
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""
#         # add the incremental move to the current position, to get the ending frame
#         end_frame = delta_frame * self.__servoed_cp
#         return self.__move_frame(end_frame, interpolate, blocking)


#     def move(self, abs_input, interpolate = True, blocking = True):
#         """Absolute translation in cartesian space.

#         :param abs_input: the absolute translation you want to make
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""
#         # is this a legal translation input
#         if (self.__check_input_type(abs_input, [PyKDL.Vector, PyKDL.Rotation, PyKDL.Frame])):
#             if (type(abs_input) is PyKDL.Vector):
#                 return self.__move_translation(abs_input, interpolate, blocking)
#             elif (type(abs_input) is PyKDL.Rotation):
#                 return self.__move_rotation(abs_input, interpolate, blocking)
#             elif (type(abs_input) is PyKDL.Frame):
#                 return self.__move_frame(abs_input, interpolate, blocking)


#     def __move_translation(self, abs_translation, interpolate = True, blocking = True):
#         """Absolute translation in cartesian space.

#         :param abs_translation: the absolute translation you want to make based on the current position, this is in terms of a  `PyKDL.Vector <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""
#         # convert into a Frame
#         abs_rotation = self.__servoed_cp.M
#         abs_frame = PyKDL.Frame(abs_rotation, abs_translation)
#         return self.__move_frame(abs_frame, interpolate, blocking)


#     def __move_rotation(self, abs_rotation, interpolate = True, blocking = True):
#         """Absolute rotation in cartesian space.

#         :param abs_rotation: the absolute `PyKDL.Rotation <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""
#         # convert into a Frame
#         abs_vector = self.__servoed_cp.p
#         abs_frame = PyKDL.Frame(abs_rotation, abs_vector)
#         return self.__move_frame(abs_frame, interpolate, blocking)


#     def __move_frame(self, abs_frame, interpolate = True, blocking = True):
#         """Absolute move by PyKDL.Frame in Cartesian space.

#         :param abs_frame: the absolute `PyKDL.Frame <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""
#         # move based on value of interpolate
#         if (interpolate):
#             return self.__move_cartesian_goal(abs_frame, blocking)
#         else:
#             return self.__move_cartesian_direct(abs_frame)


#     def __move_cartesian_direct(self, end_frame):
#         """Move the arm to the end position by passing the trajectory generator.

#         :param end_frame: the ending `PyKDL.Frame <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_
#         :returns: true if you had successfully move
#         :rtype: Bool"""
#         # set in position cartesian mode
#         end_position = TransformToMsg(end_frame)
#         # go to that position directly
#         self.__servo_cp_pub.publish(end_position)
#         return True


#     def __move_cartesian_goal(self, end_frame, blocking):
#         """Move the arm to the end position by providing a goal for trajectory generator.

#         :param end_frame: the ending `PyKDL.Frame <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_
#         :returns: true if you had succesfully move
#         :rtype: Bool"""
#         # set in position cartesian mode
#         end_position= TransformToMsg(end_frame)
#         # go to that position by goal
#         if blocking:
#             return self.__set_position_goal_cartesian_publish_and_wait(end_position)
#         else:
#             self.__move_cp_pub.publish(end_position)
#         return True


#     def __set_position_goal_cartesian_publish_and_wait(self, end_position):
#         """Wrapper around publisher/subscriber to manage events for cartesian coordinates.

#         :param end_position: the ending `PyKDL.Frame <http://docs.ros.org/diamondback/api/kdl/html/python/geometric_primitives.html>`_
#         :returns: returns true if the goal is reached
#         :rtype: Bool"""
#         self.__goal_reached_event.clear()
#         # the goal is originally not reached
#         self.__goal_reached = False
#         # recursively call this function until end is reached
#         self.__move_cp_pub.publish(end_position)
#         self.__goal_reached_event.wait(20) # 1 minute at most
#         if not self.__goal_reached:
#             return False
#         return True


#     def dmove_joint(self, delta_pos, interpolate = True, blocking = True):
#         """Incremental move in joint space.

#         :param delta_pos: the incremental amount in which you want to move index by, this is in terms of a numpy array
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""
#         if ((not(type(delta_pos) is numpy.ndarray))
#              or (not(delta_pos.dtype == numpy.float64))):
#             print "delta_pos must be an array of floats"
#             return False
#         if (not(delta_pos.size ==  self.get_joint_number())):
#             print "delta_pos must be an array of size", self.get_joint_number()
#             return False

#         abs_pos = numpy.array(self.__servoed_jp)
#         abs_pos = abs_pos+ delta_pos
#         return self.__move_joint(abs_pos, interpolate, blocking)


#     def dmove_joint_one(self, delta_pos, indices, interpolate = True, blocking = True):
#         """Incremental index move of 1 joint in joint space.

#         :param delta_pos: the incremental amount in which you want to move index by, this is a float
#         :param index: the joint you want to move, this is an integer
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""
#         if (type(delta_pos) is float and type(indices) is int):
#             return self.dmove_joint_some(numpy.array([delta_pos]), numpy.array([indices]), interpolate, blocking)
#         else:
#             return False


#     def dmove_joint_some(self, delta_pos, indices, interpolate = True, blocking = True):
#         """Incremental index move of a series of joints in joint space.

#         :param delta_pos: the incremental amount in which you want to move index by, this is a numpy array corresponding to the number of indices
#         :param indices: the joints you want to move, this is a numpy array of indices
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""

#         # check if delta is an array
#         if ((not(type(delta_pos) is numpy.ndarray))
#              or (not(delta_pos.dtype == numpy.float64))):
#             print "delta_pos must be an array of floats"
#             return False

#         # check the length of the delta move
#         if ((not(type(indices) is numpy.ndarray))
#             or (not(indices.dtype == numpy.int64))):
#             print "indices must be an array of integers"
#             return False

#         if ((not(indices.size == delta_pos.size))
#             or (indices.size > self.get_joint_number())):
#             print "size of delta_pos and indices must match and be less than", self.get_joint_number()
#             return False

#         for i in range(indices.size):
#             if (indices[i] > self.get_joint_number()):
#                 print "all indices must be less than", self.get_joint_number()
#                 return False

#         abs_pos = numpy.array(self.__servoed_jp)
#         for i in range(len(indices)):
#             abs_pos[indices[i]] = abs_pos[indices[i]] + delta_pos[i]

#         # move accordingly
#         return self.__move_joint(abs_pos, interpolate, blocking)


#     def move_joint(self, abs_pos, interpolate = True, blocking = True):
#         """Absolute move in joint space.

#         :param abs_pos: the absolute position in which you want to move, this is a numpy array
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""

#         if ((not(type(abs_pos) is numpy.ndarray))
#             or (not(abs_pos.dtype == numpy.float64))):
#             print "abs_pos must be an array of floats"
#             return False
#         if (not(abs_pos.size == self.get_joint_number())):
#             print "abs_pos must be an array of size", self.get_joint_number()
#             return False

#         return self.__move_joint(abs_pos, interpolate, blocking)


#     def move_joint_one(self, abs_pos, joint_index, interpolate = True, blocking = True):
#         """Absolute index move of 1 joint in joint space.

#         :param value: the absolute amount in which you want to move index by, this is a list
#         :param index: the joint you want to move, this is a list
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""
#         if ((type(abs_pos) is float) and (type(joint_index) is int)):
#             return self.move_joint_some(numpy.array([abs_pos]), numpy.array([joint_index]), interpolate, blocking)
#         else:
#             return False


#     def move_joint_some(self, abs_pos, indices, interpolate = True, blocking = True):
#         """Absolute index move of a series of joints in joint space.

#         :param value: the absolute amount in which you want to move index by, this is a list
#         :param index: the joint you want to move, this is a list
#         :param interpolate: see  :ref:`interpolate <interpolate>`"""

#         if ((not(type(abs_pos) is numpy.ndarray))
#             or (not(abs_pos.dtype == numpy.float64))):
#             print "delta_pos must be an array of floats"
#             return False

#         # check the length of the delta move
#         if ((not(type(indices) is numpy.ndarray))
#             or (not(indices.dtype == numpy.int64))):
#             print "indices must be an array of integers"
#             return False

#         if ((not(indices.size == abs_pos.size))
#             or (indices.size > self.get_joint_number())):
#             print "size of delta_pos and indices must match and be less than", self.get_joint_number()
#             return False

#         for i in range(indices.size):
#             if (indices[i] > self.get_joint_number()):
#                 print "all indices must be less than", self.get_joint_number()
#                 return False

#         abs_pos_result = numpy.array(self.__servoed_jp)
#         for i in range(len(indices)):
#             abs_pos_result[indices[i]] = abs_pos[i]

#         # move accordingly
#         return self.__move_joint(abs_pos_result, interpolate, blocking)


#     def __move_joint(self, abs_joint, interpolate = True, blocking = True):
#         """Absolute move by vector in joint plane.

#         :param abs_joint: the absolute position of the joints in terms of a numpy array
#         :param interpolate: if false the trajectory generator will be used; if true you can bypass the trajectory generator"""
#         if (interpolate):
#             return self.__move_joint_goal(abs_joint, blocking)
#         else:
#             return self.__move_joint_direct(abs_joint)

#     def __move_joint_direct(self, end_joint):
#         """Move the arm to the end vector by passing the trajectory generator.

#         :param end_joint: the list of joints in which you should conclude movement
#         :returns: true if you had succesfully move
#         :rtype: Bool"""
#         # go to that position directly
#         joint_state = JointState()
#         joint_state.position[:] = end_joint.flat
#         self.__servo_jp_pub.publish(joint_state)
#         return True


#     def __move_joint_goal(self, end_joint, blocking):
#         """Move the arm to the end vector by bypassing the trajectory generator.

#         :param end_joint: the list of joints in which you should conclude movement
#         :returns: true if you had succesfully move
#         :rtype: Bool"""
#         joint_state = JointState()
#         joint_state.position[:] = end_joint.flat
#         if blocking:
#             return self.__set_position_goal_joint_publish_and_wait(joint_state)
#         else:
#             self.__move_jp_pub.publish(joint_state)
#         return True


#     def __set_position_goal_joint_publish_and_wait(self, end_position):
#         """Wrapper around publisher/subscriber to manage events for joint coordinates.

#         :param end_position: there is only one parameter, end_position which tells us what the ending position is
#         :returns: whether or not you have successfully moved by goal or not
#         :rtype: Bool"""
#         self.__goal_reached_event.clear()
#         self.__goal_reached = False
#         self.__move_jp_pub.publish(end_position)
#         self.__goal_reached_event.wait(20) # 1 minute at most
#         if not self.__goal_reached:
#             return False
#         return True


#     def servo_jf(self, effort):
#         if ((not(type(effort) is numpy.ndarray))
#             or (not(effort.dtype == numpy.float64))):
#             print "effort must be an array of floats"
#             return False
#         if (not(effort.size == self.get_joint_number())):
#             print "effort must be an array of size", self.get_joint_number()
#             return False
#         joint_state = JointState()
#         joint_state.effort[:] = effort.flat
#         self.__servo_jf_pub.publish(joint_state)
#         return True


#     def servo_cf_spatial(self, force):
#         """Apply a wrench with force only (spatial), torque is null

#         :param force: the new force to set it to
#         """
#         w = WrenchStamped()
#         w.wrench.force.x = force[0]
#         w.wrench.force.y = force[1]
#         w.wrench.force.z = force[2]
#         w.wrench.torque.x = 0.0
#         w.wrench.torque.y = 0.0
#         w.wrench.torque.z = 0.0
#         self.__servo_cf_spatial_pub.publish(w)


#     def servo_cf_body_orientation_absolute(self, absolute):
#         """Apply body wrench using body orientation (relative/False) or reference frame (absolute/True)"""
#         m = Bool()
#         m.data = absolute
#         self.__servo_cf_orientation_absolute_pub.publish(m)


#     def servo_cf(self, force):
#         "Apply a wrench with force only (body), torque is null"
#         w = WrenchStamped()
#         w.wrench.force.x = force[0]
#         w.wrench.force.y = force[1]
#         w.wrench.force.z = force[2]
#         w.wrench.torque.x = 0.0
#         w.wrench.torque.y = 0.0
#         w.wrench.torque.z = 0.0
#         self.__servo_cf_body_pub.publish(w)


#     def set_gravity_compensation(self, gravity_compensation):
#         "Turn on/off gravity compensation in cartesian effort mode"
#         g = Bool()
#         g.data = gravity_compensation
#         self.__set_gravity_compensation_pub.publish(g)

# # Unregister all publishers and subscribers for this instance
#     def unregister(self, verbose=False):
#         for sub in self.__sub_list:
#             sub.unregister()
#         if verbose:
#             print 'Unregistered {} subs for {}'.format(self.__sub_list.__len__(), self.__arm_name)

#         for pub in self.__pub_list:
#             pub.unregister()
#         if verbose:
#             print 'Unregistered {} pubs for {}'.format(self.__pub_list.__len__(), self.__arm_name)

# # to and from pose message
# def TransformFromMsg(t):
#     """
#     :param p: input pose
#     :type p: :class:`geometry_msgs.msg.Pose`
#     :return: New :class:`PyKDL.Frame` object

#     Convert a pose represented as a ROS Pose message to a :class:`PyKDL.Frame`.
#     """
#     return PyKDL.Frame(PyKDL.Rotation.Quaternion(t.rotation.x,
#                                      t.rotation.y,
#                                      t.rotation.z,
#                                      t.rotation.w),
#                  PyKDL.Vector(t.translation.x,
#                         t.translation.y,
#                         t.translation.z))

# def TransformToMsg(f):
#     """
#     :param f: input pose
#     :type f: :class:`PyKDL.Frame`

#     Return a ROS Pose message for the Frame f.

#     """
#     m = TransformStamped()
#     t = m.transform()
#     t.rotation.x, t.rotation.y, t.rotation.z, t.rotation.w = f.M.GetQuaternion()
#     t.translation.x = f.p[0]
#     t.translation.y = f.p[1]
#     t.translation.z = f.p[2]
#     return m
