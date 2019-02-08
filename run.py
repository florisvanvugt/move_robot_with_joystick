


import time
import robot.interface as robot
#import robot.dummy as robot
import pygame

conf = {}

robot.load()

print("Loaded")


def init_pygame():
    pygame.init()
    if True:
        joystick_count = pygame.joystick.get_count()
        if joystick_count==0:
            print("## ERROR: no joystick found!")
            sys.exit(0) # this is problematic!
        if joystick_count>1:
            print("## ERROR: multiple joystick.  Unsure which to use.")
            sys.exit(0)
        
        conf['joystick'] = pygame.joystick.Joystick(0)
        conf['joystick'].init()




ROBOT_SCALE = .00025 # the sensitivity of changes in the robot (don't make this high, warning warning warning!)

UPDATE_PERIOD_T = .0025 # how often we update the target position

MINX,MAXX= -.4,.4
MINY,MAXY= -.1,.25

init_pygame()


# Start out in the center of the workspace
x,y = 0,0

print("Moving into position.")

robot.move_to(x,y,3.)
while not robot.move_is_done():
    pass

robot.stay_at(x,y)

print("In position now")

next_tick_t = time.time()

keep_going = True

i = 0

dx,dy = 0,0 # we get this from the joystick later
while keep_going:

    if time.time()>next_tick_t:
        
        x += ROBOT_SCALE*dx
        y -= ROBOT_SCALE*dy

        # Snap to edges if we pass them!
        if x<MINX: x=MINX
        if x>MAXX: x=MAXX
        if y<MINY: y=MINY
        if y>MAXY: y=MAXY
        
        i+=1
        if i>100:
            print("%.3f %.3f"%(x,y))
            i=0

        if True: # actually write this to the robot (this is the scary part)
            robot.wshm('plg_p1x',x)
            robot.wshm('plg_p1y',y)
        
        next_tick_t += UPDATE_PERIOD_T
        # Update the robot position
    
    evs = pygame.event.get()
    for ev in evs:
        if ev.type==pygame.JOYAXISMOTION:
            joystick = conf['joystick']
            dx,dy = [ joystick.get_axis( i ) for i in range(2) ] # get the first two axes
        if ev.type==pygame.JOYBUTTONDOWN:
            keep_going = False


robot.unload()

