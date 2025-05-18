#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Int16MultiArray

def marble_coordinates():
    pub = rospy.Publisher('marble_coordinates', Int16MultiArray, queue_size=10)
    rospy.init_node('marble_coordinates_out', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():

	marble_array = Int16MultiArray()
	marble_array.data = [10,20,2,13,18,1]
	


        pub.publish(marble_array)
        rate.sleep()

if __name__ == '__main__':
    try:
        marble_coordinates()
    except rospy.ROSInterruptException:
        pass
