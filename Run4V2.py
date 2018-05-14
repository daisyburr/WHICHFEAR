#opened 12/12/16
#Which Fear Replication
#Labeled Trial Run 4 Version 2
#(In V1, this is R2)
#---------------------------------------------------------
#Experiment description: [insert description here]
#---------------------------------------------------------
import os
import serial
import sys
import numpy as np
import psychopy.gui
import psychopy.visual
import psychopy.event
import psychopy.core
from psychopy import data, logging, sound
from psychopy.constants import *  # things like STARTED, FINISHED
from random import randint
from random import shuffle
import time
#----------------------------------------------------
#Set up----------------------------------------------
#----------------------------------------------------
#
#----Get subject ID----
gui = psychopy.gui.Dlg()
gui.addField("Subject ID:")
gui.show()
subj_id = gui.data[0]
print subj_id
#
#----Create file path for experiment timing data----
data_path = "Run2V2_onsets"+str(subj_id)+".csv";
while os.path.exists(data_path): #if path exists, rename it to avoid overwriting data
    print "CHECK SUBJECT NUMBER"
    subj_id = subj_id+"000"
    data_path = "timing"+str(subj_id)+".csv"
#
#----Configuration for USB serial input for scanner trigger
serial_settings = {
    #'mount': '/dev/tty.USA19H141P1.1',   # May need to change per computer
    'mount': '/dev/tty.USA19H142P1.1',   # May need to change per computer
    #'mount': '/dev/tty.tty.KeySerial1',   # May need to change per computer
    'baud': 115200,
    'timeout': .00001
}
fmri_settings = {
    'sync': '5',         # character to use as the sync timing event
}

#
#----Declare experiment variables
n_trials=36;   #Number of stimulus items
n_IDs=6;
n_blocks=6;
ForYou_list = ["Face 1-1.bmp", "Face 1-2.bmp", "Face 1-3.bmp", "Face 1-4.bmp", "Face 1-5.bmp", "Face 1-6.bmp"];
OfYou_list =["Face 2-1.bmp", "Face 2-2.bmp", "Face 2-3.bmp", "Face 2-4.bmp", "Face 2-5.bmp", "Face 2-6.bmp"];
FromYou_list = ["Face 3-1.bmp", "Face 3-2.bmp", "Face 3-3.bmp", "Face 3-4.bmp", "Face 3-5.bmp", "Face 3-6.bmp"];
X=np.zeros((n_blocks,n_trials));   #Create blank vector to store timing data
cl = psychopy.core.Clock(); #clock for keeping track of timing
#
#----Open experiment window----
win = psychopy.visual.Window(
    size=[1280, 800],
    units="pix",
    fullscr=True,
    color=[-1, -1, -1]
)
#
#----Declare image and text variables
welcome_text = psychopy.visual.TextStim(
    win=win,
    text="Waiting for scanner...",
    color=[1, 1, 1],
    height=35
)
#
fixation_text = psychopy.visual.TextStim(
    win=win,
    text="+",
    color=[1,1,1],
    height=35
)
#
ofyou_text = psychopy.visual.TextStim(
    win=win,
    text="These people are afraid OF YOU",
    color=[1, 1, 1],
    height=40,
    wrapWidth=1000
)
#
foryou_text = psychopy.visual.TextStim(
    win=win,
    text="These people are afraid FOR YOU",
    color=[1, 1, 1],
    height=40,
    wrapWidth=1000
)
#
fromyou_text = psychopy.visual.TextStim(
    win=win,
    text="These people are afraid AND NEED HELP FROM YOU",
    color=[1, 1, 1],
    height=40,
    wrapWidth=1000
)
#
finish_text = psychopy.visual.TextStim(
    win=win,
    text="Please wait...",
    color=[1, 1, 1],
    height=35,
    wrapWidth=1000
)
#---------------------------------------------------------
#----Show welcome screen while waiting for scanner trigger
#---------------------------------------------------------
#welcome_text.draw()
#win.flip()
#psychopy.event.waitKeys()
#
ser = serial.Serial(
    serial_settings['mount'],
    serial_settings['baud'],
    timeout = serial_settings['timeout']
)
ser.flushInput()
trigger = ''
while trigger != fmri_settings['sync']:
    welcome_text.draw()
    win.flip()
    trigger = ser.read()
ser.close()
#
#---------------------------------------------------------
#----Begin experiment blocks------------------------------
#---------------------------------------------------------
#Set clock to 0 at beginning of experiment
cl.reset(0)
#
#----Block 1 of 6 "FROM YOU"----
#
#Show first fixation for 12.9 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(12.9)
#
#Show instructions for 2 seconds
fromyou_text.draw()
win.flip()
psychopy.core.wait(2)
#
#Show fixation after instructions for 3.1 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(3.1)
#
#Begin picture loop
for i in range(0,n_IDs):
    shuffle(FromYou_list)
    for j in range(0,n_IDs):
        tr=j+(i*6)  #trial index within block
        #show fixation for 300 milliseconds
        fixation_text.draw()
        win.flip()
        psychopy.core.wait(.3)
        #show image for 200 milliseconds
        filename3="FromYouV2_Stim/"+ FromYou_list[j]
        img = psychopy.visual.ImageStim(
            win=win,
            image=filename3,
            units="pix"
        )
        size_x = img.size[0]
        size_y = img.size[1]
        img.size = [size_x*1.5, size_y*1.5]   #scale image
        img.draw()
        t=cl.getTime()    #record time right before face stimulus is presented
        win.flip()
        psychopy.core.wait(.2)
        X[0,tr]=t   #store timing of trial onset
        print tr
#
#----Block 2 of 6 "OF YOU"----
#
#Show first fixation for 12.4 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(12.4)
#
#Show instructions for 2 seconds
ofyou_text.draw()
win.flip()
psychopy.core.wait(2)
#
#Show fixation after instructions for 3.6 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(3.6)
#
#Begin picture loop
for i in range(0,n_IDs):
    shuffle(OfYou_list)
    for j in range(0,n_IDs):
        tr=j+(i*6)  #trial index within block
        #show fixation for 300 milliseconds
        fixation_text.draw()
        win.flip()
        psychopy.core.wait(.3)
        #show face stimulus for 200 milliseconds
        filename1="OfYouV2_Stim/"+ OfYou_list[j]
        img = psychopy.visual.ImageStim(
            win=win,
            image=filename1,
            units="pix"
        )
        size_x = img.size[0]
        size_y = img.size[1]
        img.size = [size_x*1.5, size_y*1.5]   #scale image
        img.draw()
        t=cl.getTime()    #record time right before face stimulus is presented
        win.flip()
        psychopy.core.wait(.2)
        X[1,tr]=t   #store timing of trial onset
        print tr
#
#----Block 3 of 6 "FOR YOU"----
#
#Show first fixation for 13.5 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(13.5)
#
#Show instructions for 2 seconds
foryou_text.draw()
win.flip()
psychopy.core.wait(2)
#
#Show fixation after instructions for 2.5 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(2.5)
#
#Begin picture loop
for i in range(0,n_IDs):
    shuffle(ForYou_list)
    for j in range(0,n_IDs):
        tr=j+(i*6)  #trial index within block
        #Show fixation for 300 milliseconds
        fixation_text.draw()
        win.flip()
        psychopy.core.wait(.3)
        #Show face for 200 milliseconds
        filename2="ForYouV2_Stim/"+ ForYou_list[j]
        img = psychopy.visual.ImageStim(
            win=win,
            image=filename2,
            units="pix"
        )
        size_x = img.size[0]
        size_y = img.size[1]
        img.size = [size_x*1.5, size_y*1.5]   #scale image
        img.draw()
        t=cl.getTime()    #record time right before face stimulus is presented
        win.flip()
        psychopy.core.wait(.2)
        X[2,tr]=t   #store timing of trial onset
        print tr
#
#----Block 4 of 6 "FROM YOU"----
#
#Show initial fixation for 13.1 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(13.1)
#Show instructions for 2 seconds
fromyou_text.draw()
win.flip()
psychopy.core.wait(2)
#Show fixation for 2.9 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(2.9)
#Begin picture loop
for i in range(0,n_IDs):
    shuffle(FromYou_list)
    for j in range(0,n_IDs):
        tr=j+(i*6)  #trial index within block
        #Show fixation for 300 milliseconds
        fixation_text.draw()
        win.flip()
        psychopy.core.wait(.3)
        #Show image for 200 milliseconds
        filename3="FromYouV2_Stim/"+ FromYou_list[j]
        img = psychopy.visual.ImageStim(
            win=win,
            image=filename3,
            units="pix"
        )
        size_x = img.size[0]
        size_y = img.size[1]
        img.size = [size_x*1.5, size_y*1.5]   #scale image?
        img.draw()
        t=cl.getTime()    #record time right before face stimulus is presented
        win.flip()
        psychopy.core.wait(.2)
        X[3,tr]=t   #store timing of trial onset
        print tr
#
#----Block 5 of 6 "For You"----
#
#Show initial fixation for 13.3 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(13.3)
#
#Show instructions for 2 seconds
foryou_text.draw()
win.flip()
psychopy.core.wait(2)
#
#Show fixation after instructions for 2.7 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(2.7)
#
#Begin picture loop
for i in range(0,n_IDs):
    shuffle(ForYou_list)
    for j in range(0,n_IDs):
        tr=j+(i*6)  #trial index within block
        #show fixation for 300 milliseconds
        fixation_text.draw()
        win.flip()
        psychopy.core.wait(.3)
        #show face stimulus for 200 milliseconds
        filename2="ForYouV2_Stim/"+ ForYou_list[j]
        img = psychopy.visual.ImageStim(
            win=win,
            image=filename2,
            units="pix"
        )
        size_x = img.size[0]
        size_y = img.size[1]
        img.size = [size_x*1.5, size_y*1.5]   #scale image
        img.draw()
        t=cl.getTime()    #record time right before face stimulus is presented
        win.flip()
        psychopy.core.wait(.2)
        X[4,tr]=t   #store timing of trial onset
        print tr
#
#----Block 6 of 6 "Of YOU"----
#
#Show first fixation for 12.7 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(12.7)
#
#Show instructions for 2 seconds
ofyou_text.draw()
win.flip()
psychopy.core.wait(2)
#
#Show fixation after instructions for 3.3 seconds
fixation_text.draw()
win.flip()
psychopy.core.wait(3.3)
#
#Begin picture loop
for i in range(0,n_IDs):
    shuffle(OfYou_list)
    for j in range(0,n_IDs):
        tr=j+(i*6)  #trial index within block
        #Show fixation for 300 milliseconds
        fixation_text.draw()
        win.flip()
        psychopy.core.wait(.3)
        #Show face stimulus for 200 milliseconds
        filename1="OfYouV2_Stim/"+ OfYou_list[j]
        img = psychopy.visual.ImageStim(
            win=win,
            image=filename1,
            units="pix"
        )
        size_x = img.size[0]
        size_y = img.size[1]
        img.size = [size_x*1.5, size_y*1.5]   #scale image
        img.draw()
        t=cl.getTime()    #record time right before face stimulus is presented
        win.flip()
        psychopy.core.wait(.2)
        X[5,tr]=t   #store timing of trial onset
        print tr
#
#----Show last fixation----
fixation_text.draw()
win.flip()
psychopy.core.wait(30)
print cl.getTime() #print how long the experiment took
#
#---------------------------------------------------------
#----Save the timing data---------------------------------
#---------------------------------------------------------
np.savetxt(
    data_path,
    X,
    delimiter=","
)
#
#---------------------------------------------------------
#----Show finish screen-----------------------------------
#---------------------------------------------------------
finish_text.draw()
win.flip()
psychopy.event.waitKeys()    