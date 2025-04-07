'''Controlling Mouse:
# This script demonstrates how to control the mouse using the `pynput` library in Python.
# Use case: You can simulate user interactions, which can be useful for automated testing or red team operations.
# Install the library: pip install pynput or py -m pip install pynput 

## ❌IMPORTANT❌: THIS SCRIPT IS FOR EDUCATIONAL PURPOSES ONLY. USE RESPONSIBLY AND ETHICALLY ##
'''

from pynput.mouse import Controller, Button # import the Controller class from the mouse module


mouse = Controller() # create an instance of the Controller class
mouse.position = (400, 600) # set mouse position (x, y) (0, 0) is the top left corner of the screen
#mouse.click(Button.left) # click the left mouse button
#mouse.click(Button.right) # click the right mouse button
#mouse.scroll(0, -2) # scroll up 2 units (positive value) or down (-ve value)

print(mouse.position) #print the position of the mouse to the console
#print(mouse.scroll(0, -2)) # print the scroll value to the console

    


  

