import smbus
import time
import numpy
import threading

bus = smbus.SMBus(1)

IODIRA = 0x00
IODIRB = 0x01
GPIOA = 0x12
GPIOB = 0x13
OLATA = 0x14
GPPUA = 0x0C
GPPUB = 0x0D
bus.write_byte_data(0x23, IODIRA, 0x00) #1 = inputs. #0 = outputs.
bus.write_byte_data(0x23, IODIRB, 0xFF)

bus.write_byte_data(0x23, GPPUA, 0xFF)
bus.write_byte_data(0x23, GPPUB, 0xFF)

bus.write_byte_data(0x21, IODIRA, 0x00) #1 = inputs. #0 = outputs.
bus.write_byte_data(0x21, IODIRB, 0xFF)

bus.write_byte_data(0x21, GPPUA, 0xFF)
bus.write_byte_data(0x21, GPPUB, 0xFF)

lives = 3
leftBoard = 0
middleBoard = 0
rightAboveBoard = 0
rightUnderBoard = 0
ballInGutter = 0
ballInHole = 0
mcpInBinary = [0,0,0,0,0,0,0,0]



#This function restarts itself after 30 seconds. Every 30 seconds, the leftboard, middleboard, rightaboveboard and rightunderboard will activate.
def ActivateBoards():
    threading.Timer(30.0, ActivateBoards).start()
    
    currentMcpRead = bus.read_byte_data(0x23, GPIOB)
    
    bus.write_byte_data(0x23, IODIRA, currentMcpRead - 15)
    
ActivateBoards()

#This function reads the sensor value. Then converts the sensor(decimal) value into a 8 bit binary array of 0 and 1's.
#returns the mcp value in binary array.
def ConvertMcpValuesIntoBinary(address, GPIO, mcpValue):
    teller = 7
    mcpValue = bus.read_byte_data(address, GPIO)
    print(mcpValue)
    for x in range(0,8):
        if mcpValue % 2 == 1:
            mcpInBinary[teller] = 1
            mcpValue = (mcpValue -1) / 2
        else:
            mcpInBinary[teller] = 0
            mcpValue = mcpValue/2

        teller = teller -1
        
    return mcpInBinary

#The MCP0x21 control is very easy. The solenoids respond directly upon touching a switch. MCPA are connected to the solenoids and MCPB are connected to the switches.
#The output data becomes the same as the input data. mcpA value turns into mcpB.
def Mcp0x21Control():
    mcpBValue = bus.read_byte_data(0x21, GPIOB)
    bus.write_byte_data(0x21, IODIRA, (0+mcpBValue))
    mcpAValue = bus.read_byte_data(0x21, GPIOA)


while True:
    
    mpcDecimalValue = bus.read_byte_data(0x23, GPIOB)
    mcp0x23BPinInBinary = ConvertMcpValuesIntoBinary(0x23, GPIOB, mpcDecimalValue)
    #The binary array are linked to the variables to recognize which switch has been hit on the field.
    leftBoard = mcp0x23BPinInBinary[7]
    middleBoard = mcp0x23BPinInBinary[6]
    rightAboveBoard = mcp0x23BPinInBinary[5]
    rightUnderBoard = mcp0x23BPinInBinary[4]
    ballInGutter = mcp0x23BPinInBinary[3]
    ballInHole = mcp0x23BPinInBinary[2]
    
    #When ball is in the gutter the value will turn 0, because the switch is being touched.
    if ballInGutter == 0:
        lives = lives - 1
        time.sleep(2)
        bus.write_byte_data(0x23, IODIRA, mpcDecimalValue)
        
    #If the ballInGutter = 1, it means it is still waiting to be grounded. The BallInGutter gets grounded when a switch has been hit.
    #1 means switch not hit.
    if ballInGutter == 1:
        bus.write_byte_data(0x23, IODIRA, mpcDecimalValue)
        
    Mcp0x21Control()



    