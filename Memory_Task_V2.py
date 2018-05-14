#Opened November 8, 2016
#Which Fear Replication
#Memory Task
import os
import sys
import numpy as np
import psychopy.gui
import psychopy.visual
import psychopy.event
import psychopy.core
from random import randint
from random import shuffle

#----Get subject ID----
gui = psychopy.gui.Dlg()
gui.addField("Subject ID:")
gui.show()
subj_id = gui.data[0]
print subj_id
#
def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))
#
#----Create file path for response data----
data_path = "V2_MTresponses"+str(subj_id)+".csv";
while os.path.exists(data_path): #if path exists, rename it to avoid overwriting data
    print "CHECK SUBJECT NUMBER"
    subj_id = subj_id+"000"
    data_path = "V2_MTresponses"+str(subj_id)+".csv"
#
#
#
#
#----Declare experiment variables--------------
#
cl = psychopy.core.Clock();  #declare clock for tracking RT---DO WE WANT TO DO RT?

n_trials=60;   #Number of stimulus items
n_blocks=1;
n_vars=5;    #variables: subj_id, trial#, photoID, response, RT

Memory_Stim= ["FromYou01.bmp", "FromYou02.bmp", "FromYou03.bmp", "FromYou04.bmp", "FromYou05.bmp", "FromYou06.bmp", "FromYou07.bmp", "FromYou08.bmp", "FromYou09.bmp", "FromYou10.bmp", "FromYou11.bmp", "FromYou12.bmp", "FromYou13.bmp", "FromYou14.bmp", "FromYou15.bmp", "FromYou16.bmp", "FromYou17.bmp", "FromYou18.bmp", "FromYou19.bmp", "FromYou20.bmp", "ForYou21.bmp", "ForYou22.bmp", "ForYou23.bmp", "ForYou24.bmp", "ForYou25.bmp", "ForYou26.bmp", "ForYou27.bmp", "ForYou28.bmp", "ForYou29.bmp", "ForYou30.bmp", "ForYou31.bmp", "ForYou32.bmp", "ForYou33.bmp", "ForYou34.bmp", "ForYou35.bmp", "ForYou36.bmp", "ForYou37.bmp", "ForYou38.bmp", "ForYou39.bmp", "ForYou40.bmp", "OfYou41.bmp", "OfYou42.bmp", "OfYou43.bmp", "OfYou44.bmp", "OfYou45.bmp", "OfYou46.bmp", "OfYou47.bmp", "OfYou48.bmp", "OfYou49.bmp", "OfYou50.bmp", "OfYou51.bmp", "OfYou52.bmp", "OfYou53.bmp", "OfYou54.bmp", "OfYou55.bmp", "OfYou56.bmp", "OfYou57.bmp", "OfYou58.bmp", "OfYou59.bmp", "OfYou60.bmp"];
shuffle(Memory_Stim);   #Randomize trial order
X=np.zeros((n_trials,n_vars));   #Create blank vector to store data

#
#
#----------------------------------------------------
#
#
#
#----Open experiment window----
win = psychopy.visual.Window(
    size=[1280, 800],
    units="pix",
    fullscr=True,
    color=[-1, -1, -1]
)
#
open_text="Welcome. Press any key to begin...";
text = psychopy.visual.TextStim(
    win=win,
    text=open_text,
    color=[1, 1, 1],
    height=35
)
text.draw()
win.flip()
psychopy.event.waitKeys() 
#
#
#-----Instruction Page---------#GO OVER THIS--text is not quite right...
instruction_text="You are going to see groups of 3 faces.\n\nAll will be faces you just saw in the scanner.\n\nPlease put these faces in the appropriate context from the experiment.\n\n2 = This person is afraid AND NEEDS HELP FROM YOU\n\n3 = This person is afraid FOR YOU\n\n4 = This person is afraid OF YOU\n\n\n\nThe experiment will begin shortly...";
text = psychopy.visual.TextStim(
    win=win,
    text=instruction_text,
    color=[1, 1, 1],
    height=35,
    wrapWidth=1000,
    alignHoriz='center',
    pos=(0,-3),
    alignVert='center'
)
text.draw()
win.flip()
psychopy.event.waitKeys()

question_pos=300

#-----Begin picture blocks---#
for i in range (0,n_trials):
    filename = "Memory_Stim/" + Memory_Stim[i]
    
    #----draw trial text----
    txtline1 = "Which sentence group are these faces from?";
    text_line1 = psychopy.visual.TextStim(
        win=win,
        text=txtline1,
        color=[1, 1, 1],
        pos=(0,question_pos),
        alignHoriz='center',
        height=40,
        wrapWidth=1200
    )
    
    
    rspline1 = "2 = This person is afraid AND NEEDS HELP FROM YOU\n3 = This person is afraid FOR YOU\n4 = This person is afraid OF YOU"
    response_line1 = psychopy.visual.TextStim(
        win=win,
        text=rspline1,
        color=[1, 1, 1],
        pos=(0,-question_pos+50),
        alignHoriz='center',
        height=35,
        wrapWidth=1200
    )
    
    
    
    img = psychopy.visual.ImageStim(
        win=win,
        image=filename,
        units="pix",
        pos=(0,20)
    )
    size_x = img.size[0]
    size_y = img.size[1]
    if  get_num(Memory_Stim[i]) <= 20:         
        img.size = [size_x * 1.2, size_y * 1.2]   #scale image
    elif get_num(Memory_Stim[i]) >= 41:
        img.size = [size_x * 1.2, size_y * 1.2]
    else:
        img.size = [size_x * 1, size_y * 1]
    
    img.draw()
    text_line1.draw()
    response_line1.draw()
    #---display trial----
    win.flip()
    #---collect response----
    cl.reset(0) #Set clock to 0 at beginning of trial
    keys = psychopy.event.waitKeys(keyList=["2","3","4"],timeStamped=cl)
    X[i,0] = subj_id;
    X[i,1] = i+1;
    X[i,2] = get_num(Memory_Stim[i]);
    X[i,3] = keys[0][0];
    X[i,4] = keys[0][1];
    print X[i]
#----Save data----
np.savetxt(
    data_path,
    X,
    delimiter=",",
    fmt='%.0i',
    header="Subject ID, Trial#, Stim ID, Response, RTime"
)

#------End Screen-----#
End_text="You have finished with this portion.\n\n\n\nPlease inform your experimenter that you are ready to proceed"
text = psychopy.visual.TextStim(
    win=win,
    text=End_text,
    color=[1, 1, 1],
    height=35,
    wrapWidth=1000,
    alignHoriz='center',
    pos=(0,-3)
)
text.draw()
win.flip()
psychopy.event.waitKeys()
