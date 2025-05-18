#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
	for i in range(0,len(data.data),3):
		print(data.data[i],data.data[i+1],data.data[i+2])
	print() #new line

def listener():
    rospy.init_node('marble_coordinates_in', anonymous=True)

    rospy.Subscriber("marble_coordinates", Int16MultiArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

