#opened 11/3/16
#Which Fear Replication
#Unlabeled Trial Run 1
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
#---------------------------------------------------------
#Set up---------------------------------------------------
#---------------------------------------------------------
#
#----Get subject ID----
gui = psychopy.gui.Dlg()
gui.addField("Subject ID:")
gui.show()
subj_id = gui.data[0]
print subj_id
#
#----Create file path for experiment timing data----
data_path = "UL_Run1_onsets"+str(subj_id)+".csv";
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

#----Declare experiment variables
n_trials=36;   #Number of stimulus items presented per block
n_IDs=6;
n_blocks=4;
Unlabeled_list = ["Face 1-1.bmp", "Face 1-2.bmp", "Face 1-3.bmp", "Face 1-4.bmp", "Face 1-5.bmp", "Face 1-6.bmp"];
X=np.zeros((n_blocks,n_trials));   #Create blank vector to store timing data
cl = psychopy.core.Clock(); #clock for keeping track of timing
#
#----Open experiment window
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
#Begin picture loop
for i in range(0,n_blocks):
    #Begin block
    #Show fixation for first 18 seconds
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(18)
    for j in range(0,n_IDs):
        shuffle(Unlabeled_list)
        for k in range(0,n_IDs):
            tr=k+(j*6)  #trial index within block
            #show fixation for 300 milliseconds
            fixation_text.draw()
            win.flip()
            psychopy.core.wait(.3)
            #show face for 200 milliseconds
            filename="/Users/whalenlab/desktop/Experiments/WhichFear_Replication/WhichFear_Version1/UL_Stim/"+ Unlabeled_list[k]
            print filename
            img = psychopy.visual.ImageStim(
                win=win,
                image=filename,
                units="pix"
            )
            
            size_x = img.size[0]
            size_y = img.size[1]
            img.size = [size_x*1.5, size_y*1.5]#scale image
            img.draw()
            t=cl.getTime()    #record time right before face stimulus is presented
            win.flip()
            psychopy.core.wait(.2)
            X[i,tr]=t   #store timing of trial onset
#Show final fixation
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