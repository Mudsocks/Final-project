#=====================
#finalproject.py
#by Ahmed Ben Mabrouk
#This expirment tests you response time and accuracy of pressing the arrow keys.
#It can effectively be used to test and train your fingers for better
# typing control for applications such as video games.
#=====================

#=====================
#IMPORT MODULES
#=====================
#-import numpy and/or numpy functions *
import numpy as np
#-import psychopy functions
from psychopy import core, gui, visual, event, monitors
#-import file save functions
import csv
#-(import other functions as necessary: os...)
import os
from datetime import datetime
import random
import pandas as pd

#=====================
#PATH SETTINGS
#=====================
#-define the main directory where you will keep all of your experiment files
main_dir = os.getcwd()
#-define the directory where you will save your data
data_dir = os.path.join(main_dir,'data')
#-check that these directories exist
if not os.path.isdir(main_dir):
    raise Exception("Could not find the main directory!")
if not os.path.isdir(data_dir):
    raise Exception("Could not find the data directory!")


#=====================
#COLLECT PARTICIPANT INFO
#=====================
#-create a dialogue box that will collect current participant number, age, gender, 
    #handedness
exp_info = {'subject_nr':0, 'age':0, 'handedness':('right','left','ambi'), 
            'gender':('male','female','other','prefer not to say')}
my_dlg = gui.DlgFromDict(dictionary=exp_info)
#get date and time
now = datetime.now()
dt_string = now.strftime("%d.%m.%Y_%H.%M.%S")
#-create a unique filename for the data
filename = str(exp_info['subject_nr']) + '_' + dt_string + '.csv'


#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
#-number of trials and blocks *
nTrials = 10
nBlocks = 3
totalTrials = nTrials*nBlocks
#-stimulus names (and stimulus extensions, if images) *
keyList=["left", "right","up","down"]
correct_keys = []

#=====================
#PREPARE CONDITION LISTS
#=====================
#-check if files to be used during the experiment (e.g., images) exist
if not os.path.isdir(data_dir):
    raise Exception("Could not find the data directory!")
#-create counterbalanced list of all conditions *

#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
#create an empty list for block and trial numbers
blockNumbers = [0]*totalTrials
trialNumbers = [0]*totalTrials
#-create an empty list for correct responses (e.g., "on this trial, a response of X is 
    #correct") *
correct_responses = [0]*totalTrials
#-create an empty list for participant responses (e.g., "on this trial, response was a 
    #X") *
responses = [0]*totalTrials
#-create an empty list for response accuracy collection (e.g., "was participant 
    #correct?") *
responseTimes = [0]*totalTrials
#-create an empty list for response time collection *
accuracies = [0]*totalTrials

#=====================
#CREATION OF WINDOW AND STIMULI
#=====================
#-define the monitor settings using psychopy functions
mon = monitors.Monitor('myMonitor', width=35.56, distance=60)
mon.setSizePix([1920, 1080])
#-define the window (size, color, units, fullscreen mode) using psychopy functions
win = visual.Window(
fullscr=False,
monitor=mon,
size=(600,600),
color='grey',
units='pix'
)
#-define experiment start text unsing psychopy functions
instructText = visual.TextStim(win, text='Press the correct direction when shown a direction up, down, left or right.Press a key to continue.')
#-define block and trial (start)/end text using psychopy functions
blockStartText = visual.TextStim(win, text='New block starting. Press a key to begin set of ' + str(nTrials) + ' trials.')
trialStartText = visual.TextStim(win, text='Wait...')
#-define stimuli using psychopy functions
leftText = visual.TextStim(win, text='<-')
rightText = visual.TextStim(win, text='->')
upText = visual.TextStim(win, text='/\\')
downText = visual.TextStim(win, text='\/')
pressedText = visual.TextStim(win, text='Response Time recorded!')
#-create response time clock
trial_timer = core.Clock()


#=====================
#START EXPERIMENT
#=====================
#-present start message text
instructText.draw()
win.flip()
#-allow participant to begin experiment with button press
event.waitKeys()
#=====================
#BLOCK SEQUENCE
#=====================
#-for loop for nBlocks *
for block in range(nBlocks):
    #-present block start message
    blockStartText.draw()
    win.flip()
    event.waitKeys()
    
    #=====================
    #TRIAL SEQUENCE
    #=====================    
    #-for loop for nTrials *
    for trial in range(nTrials):
        #starting trial, set up variable based on trial and block number we will use to save results
        overallTrial = block * nTrials + trial
        blockNumbers[overallTrial] = block + 1
        trialNumbers[overallTrial] = trial + 1

        
        #=====================
        #START TRIAL
        #=====================
        #-set stimuli and stimulus properties for the current trial
        trialStartText.draw()
        win.flip()

        

        #-randomize time for prompt to show
        wait_time = random.uniform(0.25,3)
        print('wait time ' +  str(wait_time))
        core.wait(wait_time)

        #-randomize which key to draw and save it to correct keys list
        random_key = random.choice(keyList)
        correct_keys.append(random_key)

        #draw the corect stimuli depending on which random key was chosen
        if random_key == 'left':
            leftText.draw()
        elif random_key == 'right':
            rightText.draw()
        elif random_key == 'up':
            upText.draw()
        elif random_key == 'down':
            downText.draw()
        win.flip()

        #reset timer and wait for input
        trial_timer.reset()
        input_keys = event.waitKeys(keyList=["left", "right","up","down"])

        #-collect subject response time for that trial
        #record response time and add to response time results array
        responseTimes[overallTrial] = trial_timer.getTime()

        #-collect subject response for that trial
        #add the inputted key to the data list
        responses[overallTrial] = input_keys[0]

        #-collect accuracy for that trial
        #check if the inputted key was the one shown and add correctness to results
        if input_keys[0] == random_key:
            accuracies[overallTrial] = 'Correct'
        else:
            accuracies[overallTrial] = 'InCorrect'

        #-draw stimulus
        pressedText.draw()
        win.flip()
        #-wait time (stimulus duration)
        core.wait(1)

        # Print the info after the current trial has finished
        print(
            'Block: ',
            block + 1,
            ', Trial: ',
            trial + 1,
            ', Correct key: ',
            correct_keys[trial],
            ', Response: ',
            responses[overallTrial],
            ', Accuracy: ',
            accuracies[overallTrial],
            ', Response Time: ',
            responseTimes[overallTrial]
        )

        
#======================
# END OF EXPERIMENT
#======================        
#-create panda data frame for saving to cvs
df = pd.DataFrame(data={
"Block Number": blockNumbers,
"Trial Number": trialNumbers,
"Response": responses,
"Accuracy": accuracies,
"Response Time": responseTimes
})
#-write data to a file
df.to_csv(os.path.join(data_dir, filename), sep=',', index=False)
#-close window
win.close()
#-quit experiment
quit()