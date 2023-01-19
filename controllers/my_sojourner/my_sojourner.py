"""Controller name: my_sojourner"""

# Import libraries.
from controller import Motor, Robot
from datetime import timedelta
from math import asin, pi

# Define a constant that refers to the robot instance.
ROBOT = Robot()

# Define constants for the controller.
TIME_STEP = int(ROBOT.getBasicTimeStep())

# Define constanst for the robot.
VELOCITY_MODIFIER = 0.6
ROBOT_HEIGHT = 0.3
JOINT_COUNT = 14

# Define constants for the joints list.
BACK_LEFT_BOGIE = 0
FRONT_LEFT_BOGIE = 1
FRONT_LEFT_ARM = 2
BACK_LEFT_ARM = 3
FRONT_LEFT_WHEEL = 4
MIDDLE_LEFT_WHEEL = 5
BACK_LEFT_WHEEL = 6
BACK_RIGHT_BOGIE = 7
FRONT_RIGHT_BOGIE = 8
FRONT_RIGHT_ARM = 9
BACK_RIGHT_ARM = 10
FRONT_RIGHT_WHEEL = 11
MIDDLE_RIGHT_WHEEL = 12
BACK_RIGHT_WHEEL = 13

# Define the joints constants.
JOINTS = [None] * JOINT_COUNT
JOINTS[BACK_LEFT_BOGIE] = ROBOT.getDevice("BackLeftBogie")
JOINTS[FRONT_LEFT_BOGIE] = ROBOT.getDevice("FrontLeftBogie")
JOINTS[FRONT_LEFT_ARM] = ROBOT.getDevice("FrontLeftArm")
JOINTS[BACK_LEFT_ARM] = ROBOT.getDevice("BackLeftArm")
JOINTS[FRONT_LEFT_WHEEL] = ROBOT.getDevice("FrontLeftWheel")
JOINTS[MIDDLE_LEFT_WHEEL] = ROBOT.getDevice("MiddleLeftWheel")
JOINTS[BACK_LEFT_WHEEL] = ROBOT.getDevice("BackLeftWheel")
JOINTS[BACK_RIGHT_BOGIE] = ROBOT.getDevice("BackRightBogie")
JOINTS[FRONT_RIGHT_BOGIE] = ROBOT.getDevice("FrontRightBogie")
JOINTS[FRONT_RIGHT_ARM] = ROBOT.getDevice("FrontRightArm")
JOINTS[BACK_RIGHT_ARM] = ROBOT.getDevice("BackRightArm")
JOINTS[FRONT_RIGHT_WHEEL] = ROBOT.getDevice("FrontRightWheel")
JOINTS[MIDDLE_RIGHT_WHEEL] = ROBOT.getDevice("MiddleRightWheel")
JOINTS[BACK_RIGHT_WHEEL] = ROBOT.getDevice("BackRightWheel")

# Define a constant that refers to the range finder on the robot.
RANGE_FINDER = ROBOT.getDevice("RangeFinder")

# Define a constant that refers to the camera on the robot.
CAMERA = ROBOT.getDevice("Camera")

# Define method to move laterally.
def move_4_wheels(velocity):
    JOINTS[FRONT_LEFT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[MIDDLE_LEFT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[BACK_LEFT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[FRONT_RIGHT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[MIDDLE_RIGHT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[BACK_RIGHT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    
    JOINTS[MIDDLE_RIGHT_WHEEL].setAvailableTorque(0.0)
    JOINTS[MIDDLE_LEFT_WHEEL].setAvailableTorque(0.0)

# Define method to move perpendicularly.
def move_6_wheels(velocity):
    JOINTS[MIDDLE_RIGHT_WHEEL].setAvailableTorque(2.0)
    JOINTS[MIDDLE_LEFT_WHEEL].setAvailableTorque(2.0)
    
    JOINTS[FRONT_LEFT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[MIDDLE_LEFT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[BACK_LEFT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[FRONT_RIGHT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[MIDDLE_RIGHT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[BACK_RIGHT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)

# Define method to turn right.
def turn_right():
    JOINTS[FRONT_LEFT_ARM].setPosition(0.4)
    JOINTS[FRONT_RIGHT_ARM].setPosition(0.227)
    JOINTS[BACK_RIGHT_ARM].setPosition(-0.227)
    JOINTS[BACK_LEFT_ARM].setPosition(-0.4)

# Define method to turn left.
def turn_left():
    JOINTS[FRONT_LEFT_ARM].setPosition(-0.227)
    JOINTS[FRONT_RIGHT_ARM].setPosition(-0.4)
    JOINTS[BACK_RIGHT_ARM].setPosition(0.4)
    JOINTS[BACK_LEFT_ARM].setPosition(0.227)

# Define method to turn straight.
def turn_straight():
    JOINTS[FRONT_LEFT_ARM].setPosition(0.0)
    JOINTS[FRONT_RIGHT_ARM].setPosition(0.0)
    JOINTS[BACK_RIGHT_ARM].setPosition(0.0)
    JOINTS[BACK_LEFT_ARM].setPosition(0.0)

# Define method to turn around.
def turn_around(velocity):
    JOINTS[FRONT_LEFT_ARM].setPosition(-0.87)
    JOINTS[FRONT_RIGHT_ARM].setPosition(0.87)
    JOINTS[BACK_RIGHT_ARM].setPosition(-0.87)
    JOINTS[BACK_LEFT_ARM].setPosition(0.87)
    
    JOINTS[FRONT_LEFT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[MIDDLE_LEFT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[BACK_LEFT_WHEEL].setVelocity(velocity * VELOCITY_MODIFIER)
    JOINTS[FRONT_RIGHT_WHEEL].setVelocity(-velocity * VELOCITY_MODIFIER)
    JOINTS[MIDDLE_RIGHT_WHEEL].setVelocity(-velocity * VELOCITY_MODIFIER)
    JOINTS[BACK_RIGHT_WHEEL].setVelocity(-velocity * VELOCITY_MODIFIER)

    JOINTS[MIDDLE_RIGHT_WHEEL].setAvailableTorque(0.0)
    JOINTS[MIDDLE_LEFT_WHEEL].setAvailableTorque(0.0)

# Define main flow.
if __name__ == "__main__":
    # Set the initial position of a select number of JOINTS.
    JOINTS[FRONT_LEFT_WHEEL].setPosition(float("inf"))
    JOINTS[MIDDLE_LEFT_WHEEL].setPosition(float("inf"))
    JOINTS[BACK_LEFT_WHEEL].setPosition(float("inf"))
    JOINTS[FRONT_RIGHT_WHEEL].setPosition(float("inf"))
    JOINTS[MIDDLE_RIGHT_WHEEL].setPosition(float("inf"))
    JOINTS[BACK_RIGHT_WHEEL].setPosition(float("inf"))

    # Enable the RANGE_FINDER.
    RANGE_FINDER.enable(TIME_STEP)
    
    # Get the width and height of the rangefinder view.
    RANGE_IMAGE_WIDTH = RANGE_FINDER.getWidth()
    RANGE_IMAGE_HEIGHT = RANGE_FINDER.getHeight()

    # Define angle per pixel.
    ANGLE_PER_PIXEL = 180 / RANGE_IMAGE_HEIGHT

    # Enable the CAMERA and the recognition module.
    CAMERA.enable(TIME_STEP)
    CAMERA.recognitionEnable(TIME_STEP)

    # Define the baseline number of recognition objects.
    recognition_object_count = 0

    # Start moving the robot.
    move_6_wheels(1.0)

    # Values to ensure the smoothness of decisions.
    MAX_DECISION_SKIP_COUNT = 15
    has_decided = False
    decision_skip_count = 0

    # Define working loop of the robot.
    while ROBOT.step(TIME_STEP) != -1:
        # Get the range image
        range_image = RANGE_FINDER.getRangeImage()
        
        # Initialize distance values of different areas within the range image.
        left_distance = middle_distance = right_distance = 100
        
        # Initialize angle values of different areas within the range image.
        max_left_angle = max_middle_angle = max_right_angle = 90
        
        for pixel_column_index in range(RANGE_IMAGE_WIDTH):
            # Get distance to the object in front.
            distance = RANGE_FINDER.rangeImageGetDepth(range_image, RANGE_IMAGE_WIDTH, pixel_column_index, RANGE_IMAGE_HEIGHT//2)

            # Get the shortest distance from each area within the range image.
            if(pixel_column_index < RANGE_IMAGE_WIDTH/3):
                if(distance < left_distance):
                    left_distance = distance
            elif(pixel_column_index > 2 * RANGE_IMAGE_WIDTH/3):
                if(distance < right_distance):
                    right_distance = distance
            else:
                if(distance < middle_distance):
                    middle_distance = distance

            # Get the distance to the floor in front.
            distance = RANGE_FINDER.rangeImageGetDepth(range_image, RANGE_IMAGE_WIDTH, pixel_column_index, 3 * RANGE_IMAGE_HEIGHT//4)

            # Get angle to the floor in front.
            angle = 0
            side_ratio = ROBOT_HEIGHT/distance

            # If the triangle is not an isoscelese triangle.
            if(side_ratio >= -1 and side_ratio <= 1):
                angle = 180 - 45 - asin(side_ratio) * 180/pi
            # If the triangle is an isosceles triangle.
            else:
                angle = 45
        
            # Get the biggest angle (deepest chasm).
            if(pixel_column_index < RANGE_IMAGE_WIDTH/3):
                if(angle > max_left_angle):
                    max_left_angle = angle
            elif(pixel_column_index > 2 * RANGE_IMAGE_WIDTH/3):
                if(angle > max_right_angle):
                    max_right_angle = angle
            else:
                if(angle > max_middle_angle):
                    max_middle_angle = angle

        # If the robot has made a decision allow the robot to partially fulfill that decision
        if(not has_decided):
            # Decide movement based on distance of objects and elevation (angle).
            if((middle_distance <= 1 and right_distance <= 1 and left_distance < 1) or (max_middle_angle >= 125 and max_right_angle >= 125 and max_left_angle >= 125)):
                turn_around(1.0)
            elif((right_distance < 1) or (max_right_angle >= 125)):
                turn_left()
                move_4_wheels(1.0)
            elif((left_distance < 1) or (max_left_angle >= 125)):
                turn_right()
                move_4_wheels(1.0)
            elif((middle_distance > 1 and right_distance > 1 and left_distance > 1) and (max_middle_angle < 125 and max_right_angle < 125 and max_left_angle < 125)):
                turn_straight()
                move_6_wheels(1.0)
            
            # Indicate the robot has made a decision.
            has_decided = True
        else:
            # After a certain amount of decision points.
            if(decision_skip_count == MAX_DECISION_SKIP_COUNT):
                # Indicate the decision can be renewed.
                has_decided = False

                # Reset the decision count.
                decision_skip_count = 0
            else:
                # Increment the decision count.
                decision_skip_count += 1
    
        # Capture image if there is any meaningful object.
        if(CAMERA.hasRecognition()):
            # Get the number of recognition object in the current image.
            current_recognition_object_count = CAMERA.getRecognitionNumberOfObjects()
            
            # Check whether the current image has already been captured.
            if(current_recognition_object_count != recognition_object_count):
                # Update the recognition object count.
                recognition_object_count = current_recognition_object_count
            
                # Save the image.
                CAMERA.saveImage(f"{str(timedelta(seconds = ROBOT.getTime()))}.png", 100)
                
                # Log the recognition objects in the recognition image.
                objects = CAMERA.getRecognitionObjects()
                for object in objects:
                    print(type(object))