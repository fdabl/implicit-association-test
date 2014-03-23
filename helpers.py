# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import random
from psychopy import visual, event, core, gui


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def getStimuli(path):
    '''Provided a path to a CSV File, creates a dictionary.
    The headers end up being the keys in the dictionary.
    The length of the dictionary equals the number of lines
    in the CSV File.'''
    stimuli = []
    with open(path, 'r') as csvfile:
        file = unicode_csv_reader(csvfile)
        header = next(file)
        for line in file:
            stim = {k: v for k, v in zip(header, line)}
            stimuli.append(stim)
    return stimuli


def getInput(title, questions):
    '''Given an experiment title and a dictionary
    specifying the questions, returns a dictionary where
    question maps to the given answer.'''
    info = gui.DlgFromDict(dictionary=questions, title=title)
    mapping = {k: v for k, v in zip(questions.keys(), info.data)}
    return mapping if info.OK else False


def saveData(path, trials):
    '''Provided a path to the CSV File and a list
    of lists, writes the data in the list to the file.
    Each list maps to a line in the CSV File.'''
    with open(path, 'w') as csvfile:
        file = csv.writer(csvfile)
        for trial in trials:
            file.writerow([unicode(i).encode('utf-8') for i in trial])


def draw(win, stim, time=None):
    '''Abstraction for drawing. Time is optional, since
    one could also want to stop the drawing as a function
    of User Input, e.g. event.waitKeys().'''
    stim.draw()
    win.flip()
    if time:
        core.wait(time)


def showInstruction(win, stopkeys=['space'], text=None, image=None, **kwargs):
    '''Given an Image or some Text, shows the Instruction page until
    the User presses - per default - space. This default can be changed
    by providing a list as keyword argument, e.g.
    stopkeys=['escape', 'space', 'f'].'''
    if text:
        instruction = visual.TextStim(win, text=text, **kwargs)
    elif image:
        instruction = visual.ImageStim(win, image=image, **kwargs)
    else:
        raise Exception('Need either Text or an Image as Instruction!')
    instruction.draw()
    win.flip()
    event.waitKeys(keyList=stopkeys)


def filterStimuli(stimuli, key, *args):
    '''Abstraction for filtering a list of dictionaries by
    key: value pairs.'''
    return [stim for stim in stimuli if stim[key] in args]


def equals(keypress, associate, resmap):
    '''event.waitKeys() returns a list of keys or None
    if maxWait has timed out. This functions checks if
    the pressed key matches the right answer accodring
    to a certain response mapping.'''
    try:
        check = keypress[0]
        inverted = {v: k for k, v in resmap.items()}
        return inverted[check] == associate
    except TypeError:
        return False


def jitterISI(minimum=1, maximum=3, steps=20):
    '''Compute the ISI according to a minimum and a maximum.
    It follows a gaussian distribution, with the peak at
    (minimum + maximum) / 2.'''
    rank = (maximum - minimum) / float(steps)
    ISI = minimum + (rank * random.randint(0, steps))
    return ISI


def wrapdim(win, coords, **kwargs):
    dimensions = []
    for name, quadrant in coords:
        stim = visual.TextStim(win, text=name, pos=quadrant, **kwargs)
        dimensions.append(stim)
    return dimensions


def autodraw(stimList, draw=True):
    map(lambda stim: stim.setAutoDraw(draw), stimList)
