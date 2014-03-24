# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import random
import functools
import helpers as help
from psychopy import visual, event, core, gui


# get user data before setup, since Dlg does not work in fullscreen
title = 'Impliziter Assoziations Test'
questions = {'Pbn': '', 'Geschlecht': ['m', 'w']}
info = help.getInput(title, questions) or core.quit()

# create all the basic objects (window, fixation-cross, feedback)
win = visual.Window(units='norm', color='black', fullscr=True)
fixCross = visual.TextStim(win, text='+', height=0.1)
negFeedback = visual.TextStim(win, text='X', color='red', height=0.1)
win.setMouseVisible(False)

# partially apply the helper functions to suite our needs
draw = functools.partial(help.draw, win)
wrapdim = functools.partial(help.wrapdim, win, height=0.08)
showInstruction = functools.partial(help.showInstruction, win)

# Response Mappings
# you can change the keybindings and allRes to fit your IAT constraints
keybindings = ['e', 'i']
allRes = ['self', 'other', 'pos', 'neg']
allMappings = help.getResponseMappings(allRes, keybindings=keybindings)
negoposelfMap, selfnegopoMap = allMappings[-2:]
selfotherMap, otherselfMap, posnegMap, negposMap = allMappings[:4]

pos, neg, self, other = ['Positiv', 'Negativ', 'Selbst', 'Fremd']
leftup, rightup = (-0.4, -0.3), (+0.4, -0.3)
leftdown, rightdown = (-0.4, -0.4), (+0.4, -0.4)

# this could be implemented better, naming is pretty hard
otherself = wrapdim({other: leftup, self: rightup})
negpos = wrapdim({neg: leftup, pos: rightup})
selfother = wrapdim({self: leftup, other: rightup})
selfnegopo = wrapdim({self: leftup, neg: leftdown,
                      other: rightup, pos: rightdown})
negopoself = wrapdim({neg: leftup, other: leftdown,
                      pos: rightup, self: rightdown})

experimentData = []
timer = core.Clock()
# you can easily change the stimuli by changing the csv
stimuli = help.getStimuli('stimuli.csv')

TIMEOUT = 1.5
feedbackTime = 1
instruction = '''
This is a Implicit Association Task.
Have Fun!

Start by pressing Space.
'''


def experiment(anchors, responseMap, selection, trialName, trials=1):
    data = []

    help.autodraw(anchors)
    selectedStimuli = help.filterStimuli(stimuli, 'response', *selection) * 2
    unique = help.filterDoubles(selectedStimuli)
    randomStim = sorted(unique, key=lambda x: random.random())[:trials]

    for stimulus in randomStim:
        content = stimulus['content']
        rightAnswer = responseMap[stimulus['response']]
        ISI = help.jitterISI(minimum=0.5, maximum=1.5)
        curStim = visual.TextStim(win, text=content, height=0.1)
        timer.reset()
        draw(curStim)
        rightKeys = responseMap.values() + ['escape']
        userAnswer = event.waitKeys(keyList=rightKeys) or []
        choseWisely = help.equals(userAnswer, rightAnswer)
        if choseWisely:
            RT = timer.getTime()
        elif 'escape' in userAnswer:
            core.quit()
        else:
            RT = 9999
            draw(negFeedback, feedbackTime)
            draw(curStim)
            event.waitKeys(keyList=[rightAnswer])
        data.append([ISI, content, int(RT != 9999), RT, trialName])
        draw(fixCross, ISI)

    help.autodraw(anchors, draw=False)
    return data


def wrap(*args, **kwargs):
    return functools.partial(experiment, *args, **kwargs)


allTrials = {
    'otherSelf': wrap(otherself, otherselfMap, allRes[:2], 'otherSelf'),
    'negPos': wrap(negpos, negposMap, allRes[2:], 'negativePos'),
    'negOPself': wrap(negopoself, negoposelfMap, allRes, 'negOPself'),
    'negOPself1': wrap(negopoself, negoposelfMap, allRes, 'negOPself1'),
    'selfOther': wrap(selfother, selfotherMap, allRes[:2], 'selfOther'),
    'selfNOpos': wrap(selfnegopo, selfnegopoMap, allRes, 'selfNOpos'),
    'selfNOpos1': wrap(selfnegopo, selfnegopoMap, allRes, 'selfNOpos1')
}


def main():
    '''There are only two hard things in Computer Science:
    cache invalidation and naming things.
    -- Phil Karlton
    '''
    # Instruction Setup
    showInstruction(text=instruction, height=0.1)
    header = ['ISI', 'Content', 'corrAns', 'RT', 'trialName']

    # after a trial, you can call showInstruction
    # to show a instruction for the next block
    order = random.randint(0, 1)
    if order:
        otherSelf = allTrials['otherSelf']()
        negPos = allTrials['negPos']()
        negOPself = allTrials['negOPself']()
        negOPself1 = allTrials['negOPself1'](trials=1)
        selfOther = allTrials['selfOther'](trials=1)
        selfNOpos = allTrials['selfNOpos']()
        selfNOpos1 = allTrials['selfNOpos1'](trials=1)

    else:
        selfOther = allTrials['selfOther']()
        negPos = allTrials['negPos']()
        selfNOpos = allTrials['selfNOpos']()
        selfNOpos1 = allTrials['selfNOpos1'](trials=1)
        otherSelf = allTrials['otherSelf'](trials=1)
        negOPself = allTrials['negOPself']()
        negOPself1 = allTrials['negOPself1'](trials=1)

    ## Save Data to CSV
    experimentData.extend([info.values(), header])
    everything = (otherSelf + negPos + negOPself + negOPself1 +
                  selfOther + selfNOpos + selfNOpos1)

    experimentData.extend(everything)
    file = '{0}_{1}.csv'.format(info['Pbn'], order)
    help.saveData(file, experimentData)

main()
