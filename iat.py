# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import random
import functools
import helpers as help
from psychopy import visual, event, core, gui


# get user data before setup, since Dlg does not work in fullscreen
title = 'Impliziter Assoziations Test'
questions = {'VPN-Code': '', 'Geschlecht': ['m', 'w']}
info = help.getInput(title, questions).values()

# create all the basic objects (window, fixation-cross, feedback)
win = visual.Window(size=(900, 700), units='norm', color='black', fullscr=True)
fixCross = visual.TextStim(win, text='+', height=0.1)
negFeedback = visual.TextStim(win, text='X', color='red', height=0.1)
win.setMouseVisible(False)

# partially apply the helper functions to suite our needs
draw = functools.partial(help.draw, win)
wrapdim = functools.partial(help.wrapdim, win, height=0.08)
showInstruction = functools.partial(help.showInstruction, win)

# Response Mappings
allRes = ('self', 'other', 'pos', 'neg')
posnegMap = {'pos': 'e', 'neg': 'i'}
negposMap = {'neg': 'e', 'pos': 'i'}
selfotherMap = {'self': 'e', 'other': 'i'}
otherselfMap = {'other': 'e', 'self': 'i'}
negoposelfMap = dict(negposMap.items() + otherselfMap.items())
selfnegopoMap = dict(negposMap.items() + selfotherMap.items())

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
stimuli = help.getStimuli('stimuli.csv')

ISI = 0.5
TIMEOUT = 1.5
feedbackTime = 1
instruction = '''
This is a Implicit Association Task.
Have Fun!

Start by pressing Space.
'''


def experiment(anchors, responseMap, selection, trialName, trials=20):
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


def wrap(*args):
    return functools.partial(experiment, *args)


allTrials = {
    'otherSelf': wrap(otherself, otherselfMap, allRes[:2], 'otherSelf'),
    'negPos': wrap(negpos, negposMap, allRes[2:], 'negativePos'),
    'negOPself': wrap(negopoself, negoposelfMap, allRes, 'negOPself'),
    'negOPself40': wrap(negopoself, negoposelfMap, allRes, 'negOPself40'),
    'selfOther': wrap(selfother, selfotherMap, allRes[:2], 'selfOther'),
    'selfNOpos': wrap(selfnegopo, selfnegopoMap, allRes, 'selfNOpos'),
    'selfNOpos40': wrap(selfnegopo, selfnegopoMap, allRes, 'selfNOpos40')
}


def callTrials(pause, **functions):
    for function in functions:
        function()
        pause()


def main():
    '''There are only two hard things in Computer Science:
    cache invalidation and naming things.
    -- Phil Karlton
    '''
    # Instruction Setup
    showInstruction(text=instruction, height=0.1)
    text = 'Chill. Continue with Space'
    pause = lambda text: showInstruction(text=text, height=0.1)
    header = ['ISI', 'Content', 'corrAns', 'RT', 'trialName']

    if random.randint(0, 1):
        callTrials(pause,
                   allTrials['otherSelf'](),
                   allTrials['negPos'](),
                   allTrials['negOPself'](),
                   allTrials['negOPself40'](trials=40),
                   allTrials['selfOther'](trials=40),
                   allTrials['selfNOpos'](),
                   allTrials['selfNOpos40'](trials=40),
                   )
    else:
        callTrials(pause,
                   allTrials['selfOther'](),
                   allTrials['negPos'](),
                   allTrials['selfNOpos'](),
                   allTrials['selfNOpos40'](trials=40),
                   allTrials['otherSelf'](trials=40),
                   allTrials['negOPself'](),
                   allTrials['negOPself40'](trials=40),
                   )

    ## Save Data to CSV
    experimentData.extend([info, header])
    everything = (otherSelf + negPos + negOPself + negOPself40 +
                  selfOther + selfNOpos + selfNOpos40)

    experimentData.extend(everything)
    help.saveData('data.csv', experimentData)

main()
