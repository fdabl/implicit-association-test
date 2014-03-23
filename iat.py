# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import random
import functools
import helpers as help
from psychopy import visual, event, core, gui

# create all the basic objects (window, fixation-cross, feedback)
win = visual.Window(size=(900, 600), units='pix', color='black')
fixCross = visual.TextStim(win, text='+', height=30)
posFeedback = visual.TextStim(win, text='O', color='green', height=30)
negFeedback = visual.TextStim(win, text='X', color='red', height=30)

win.setMouseVisible(False)

# Experiment Setup up
title = 'Impliziter Assoziations Test'
questions = {'VPN-Code': '', 'Geschlecht': ['m', 'w']}
posnegMap = {'pos': 'f', 'neg': 'h'}
selfotherMap = {'self': 'f', 'other': 'h'}

# partially apply the helper functions to suite our needs
draw = functools.partial(help.draw, win)
showInstruction = functools.partial(help.showInstruction, win)
join = lambda l, r, s: '{l}{s}{r}'.format(l=l, s=' ' * s, r=r)

posneg = visual.TextStim(win, text=join('Positiv', 'Negativ', 22),
                         height=22, pos=(0, -100))
selfother = visual.TextStim(win, text=join('Selbst', 'Fremd', 22),
                            height=22, pos=(0, -100))

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


def Experiment(dimension, responseMap, *selection):
    data = []

    selectedStim = help.filterStimuli(stimuli, 'response', *selection)
    random.shuffle(selectedStim)
    dimension.setAutoDraw(True)

    for stimulus in selectedStim:
        content = stimulus['content']
        rightAnswer = stimulus['response']
        ISI = help.jitterISI(minimum=0.5, maximum=1.5)
        curStim = visual.TextStim(win, text=content, height=40)
        timer.reset()
        draw(curStim)
        userAnswer = event.waitKeys(keyList=responseMap.values(), maxWait=TIMEOUT)
        choseWisely = help.equals(userAnswer, rightAnswer, responseMap)
        if choseWisely:
            RT = timer.getTime()
            draw(posFeedback, feedbackTime)
        else:
            RT = 9999
            draw(negFeedback, feedbackTime)
        data.append([ISI, content, int(RT != 9999), RT])
        draw(fixCross, ISI)
    dimension.setAutoDraw(False)
    return data


def main():
    # Instruction Setup
    info = help.getInput(title, questions).values()
    header = ['ISI', 'Content', 'corrAns', 'RT']
    showInstruction(text=instruction)

    # run experimental conditions
    PosNeg = Experiment(posneg, posnegMap, 'pos', 'neg')
    SelfOther = Experiment(selfother, selfotherMap, 'self', 'other')

    # Save Data to CSV
    experimentData.extend([info, header])
    experimentData.extend(PosNeg)
    experimentData.extend(SelfOther)
    help.saveData('data.csv', experimentData)

main()
