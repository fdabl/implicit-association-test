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
posFeedback = visual.TextStim(win, text='O', color='green', height=0.1)
negFeedback = visual.TextStim(win, text='X', color='red', height=0.1)

# Response Mappings
posnegMap = {'pos': 'e', 'neg': 'i'}
selfotherMap = {'self': 'e', 'other': 'i'}
allMap = dict(posnegMap.items() + selfotherMap.items())

# partially apply the helper functions to suite our needs
draw = functools.partial(help.draw, win)
wrapdim = functools.partial(help.wrapdim, win)
showInstruction = functools.partial(help.showInstruction, win)

coords = [
    ('Positiv', (-0.4, -0.3)),
    ('Negativ', (+0.4, -0.3)),
    ('Selbst', (-0.4, -0.3)),
    ('Fremd', (+0.4, -0.3))
]

# create textstim with text=key and pos=value
pos, neg, self, other = wrapdim(coords, height=0.08)

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


def adjust(dimensions):
    adj = dimensions[0].pos[0] - 0.1
    first, second = dimensions[-2], dimensions[-1]
    first.setPos((first.pos[0], adj))
    second.setPos((second.pos[0], adj))


def experiment(dimensions, responseMap, selection, trials=20):
    data = []
    if len(dimensions) > 2:
        adjust(dimensions)

    help.autodraw(dimensions)
    selectedStim = help.filterStimuli(stimuli, 'response', *selection) * 2
    randomStim = sorted(selectedStim, key=lambda x: random.random())[:trials]

    for stimulus in randomStim:
        content = stimulus['content']
        rightAnswer = stimulus['response']
        ISI = help.jitterISI(minimum=0.5, maximum=1.5)
        curStim = visual.TextStim(win, text=content, height=0.1)
        timer.reset()
        draw(curStim)
        rightKeys = responseMap.values()
        userAnswer = event.waitKeys(keyList=rightKeys, maxWait=TIMEOUT)
        choseWisely = help.equals(userAnswer, rightAnswer, responseMap)
        if choseWisely:
            RT = timer.getTime()
            draw(posFeedback, feedbackTime)
        else:
            RT = 9999
            draw(negFeedback, feedbackTime)
            draw(curStim)
            event.waitKeys(keyList=responseMap[rightAnswer])
            draw(posFeedback, feedbackTime)
        data.append([ISI, content, int(RT != 9999), RT])
        draw(fixCross, ISI)
    help.autodraw(dimensions, draw=False)
    return data


def main():
    '''There are only two hard things in Computer Science:
    cache invalidation and naming things.
    -- Phil Karlton
    '''
    # Instruction Setup
    showInstruction(text=instruction, height=0.1)
    text = 'Chill. Continue with Space'
    pause = lambda text: showInstruction(text=text, height=0.1)
    header = ['ISI', 'Content', 'corrAns', 'RT']

    allRes = ('self', 'other', 'pos', 'neg')
    negopoself = [neg, other, pos, self]
    selfnegopo = [self, neg, other, pos]

    # Step 1 and Step 2
    otherSelf = experiment([other, self], selfotherMap, allRes[:2])
    pause(text)
    negPos = experiment([neg, pos], posnegMap, allRes[2:])
    pause(text)

    # Step 3 and Step 4
    negOPself = experiment(negopoself, allMap, allRes)
    pause(text)
    negOPself40 = experiment(negopoself, allMap, allRes, trials=40)
    pause(text)

    # Step 5
    selfOther = experiment([self, other], selfotherMap, allRes[2:])
    pause(text)

    # Step 6 and 7
    selfNOpos = experiment(selfnegopo, allMap, allRes)
    pause(text)
    selfNOpos40 = experiment(selfnegopo, allMap, allRes, trials=40)

    # Save Data to CSV
    experimentData.extend([info, header])
    everything = (otherSelf + negPos + nOPself + nOPself40 +
                  selfOther + selfNOpos + selfNOpos40)

    experimentData.extend(everything)
    help.saveData('data.csv', experimentData)

main()
