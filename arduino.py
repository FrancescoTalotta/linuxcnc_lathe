#!/usr/bin/python
import serial
import hal
import sys
import time

PORT = "/dev/ttyACM0"
ser = serial.Serial(PORT, 115200, timeout=0)

#Now we create the HAL component and its pins
## HAL_IN  arduino can read from linuxCNC
## HAL_OUT arduino can write to linuxCNC
#
c = hal.component("arduino")
c.newpin("spindle_rev",hal.HAL_BIT,hal.HAL_IN)
c.newpin("vacuum_pump",hal.HAL_BIT,hal.HAL_IN)
c.newpin("servo_tool",hal.HAL_BIT,hal.HAL_IN)
c.newpin("enable_A",hal.HAL_BIT,hal.HAL_IN)
c.newpin("run_A_axis",hal.HAL_BIT,hal.HAL_IN)
c.newpin("probe_3d",hal.HAL_BIT,hal.HAL_IN)
c.newpin("A_axis_speed",hal.HAL_S32,hal.HAL_IN)
#c.newpin("temperature",hal.HAL_FLOAT,hal.HAL_OUT)

time.sleep(1)
c.ready()

spindle_rev  =c['spindle_rev']
vacuum_pump  =c['vacuum_pump']
servo_tool   =c['servo_tool']
enable_A     =c['enable_A']
run_A_axis   =c['run_A_axis']
probe_3d     =c['probe_3d']
A_axis_speed =c['A_axis_speed']

spindle_rev_old='False'
vacuum_pump_old='False'
servo_tool_old='False'
enable_A_old='False'
A_axis_speed_old=0
run_A_axis_old='False'
probe_3d_old='False'
#temperature_old=0

try:
  while 1:
    time.sleep(.01)
# Spindle REV 
    spindle_rev=c['spindle_rev']
    if spindle_rev!=spindle_rev_old:
       spindle_rev_old=spindle_rev
       if spindle_rev==False:
          ser.write("F")
       elif spindle_rev==True:
          ser.write("E")
# Vacuum Pump
    vacuum_pump=c['vacuum_pump']
    if vacuum_pump!=vacuum_pump_old:
       vacuum_pump_old=vacuum_pump
       if vacuum_pump==False:
          ser.write("B")
       elif vacuum_pump==True:
          ser.write("A")
# Servo Tool
    servo_tool=c['servo_tool']
    if servo_tool!=servo_tool_old:
       servo_tool_old=servo_tool
       if servo_tool==False:
          ser.write("L")
       elif servo_tool==True:
          ser.write("U")
# Enable A
    enable_A=c['enable_A']
    if enable_A!=enable_A_old:
       enable_A_old=enable_A
       if enable_A==False:
          ser.write("C")
       elif enable_A==True:
          ser.write("D")
# A Axis Speed
    A_axis_speed=c['A_axis_speed']
    if A_axis_speed!=A_axis_speed_old:
       A_axis_speed_old=A_axis_speed
       ser.write(A_axis_speed)
# Run A Axis
    run_A_axis=c['run_A_axis']
    if run_A_axis!=run_A_axis_old:
       run_A_axis_old=run_A_axis
       if run_A_axis==False:
          ser.write("G")
       elif run_A_axis==True:
          ser.write("H")
# 3D Probe
    probe_3d=c['probe_3d']
    if probe_3d!=probe_3d_old:
       probe_3d_old=probe_3d
       if probe_3d==False:
          ser.write("M")
       elif probe_3d==True:
          ser.write("I")

# Temperature
    #while ser.inWaiting():
       #temp = ser.read(5)
       #c['temperature']=float(temp)

except KeyboardInterrupt:
    raise SystemExit 
