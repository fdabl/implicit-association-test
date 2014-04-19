# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import csv
import random
import itertools
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


def invert(d):
    return {k: v for k, v in zip(d.keys(), reversed(d.values()))}


def getResponseMappings(dimensions, keybindings=['e', 'i']):
    '''dimensions is a list of the all possible responses.
    Maps them to the keybindings accordingly.'''
    selfOther = {k: v for k, v in zip(dimensions[:2], keybindings)}
    posNeg = {k: v for k, v in zip(dimensions[2:], keybindings)}
    otherSelf = invert(selfOther)
    negPos = invert(posNeg)
    negopoself = dict(negPos.items() + otherSelf.items())
    selfnegopo = dict(negPos.items() + selfOther.items())
    return (selfOther, otherSelf, posNeg, negPos, negopoself, selfnegopo)


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


def equals(keypress, rightAnswer):
    '''event.waitKeys() returns a list of keys or None
    if maxWait has timed out. This functions checks if
    the pressed key matches the right answer accodring
    to a certain response mapping.'''
    try:
        userAnswer = keypress[0]
        return userAnswer == rightAnswer
    except (TypeError, IndexError):
        return False


def jitterISI(minimum=1, maximum=3, steps=20):
    '''Compute the ISI according to a minimum and a maximum.'''
    rank = (maximum - minimum) / float(steps)
    ISI = minimum + (rank * random.randint(0, steps))
    return ISI


def wrapdim(win, mapping, **kwargs):
    '''Returns a list with visual.TextStim name and pos
    set according to a mapping dictionary.'''
    stimuli = []
    for name, coord in mapping.items():
        stim = visual.TextStim(win, text=name, pos=coord, **kwargs)
        stimuli.append(stim)
    return stimuli


def autodraw(stimList, draw=True):
    map(lambda stim: stim.setAutoDraw(draw), stimList)


def filterDoubles(stimuli):
    unique = []
    for s1, s2 in zip(stimuli, stimuli[1:]):
        if s1 != s2:
            unique.append(s1)
    return unique


def deneigh(stimuli):
    '''Fear not! The complexity of this
    bogosort like algorithm does not approach
    infinity when using a reasonable amount of trials.'''
    while not all(s1 != s2 for s1, s2 in zip(stimuli, stimuli[1:])):
        random.shuffle(stimuli)
    return stimuli


def compensate(stimuli, trials):
    '''Randomly adds more Stimuli if there are not enough
    as needed by the amount of trials.'''
    diff = trials - len(stimuli)
    if diff > 0:
        more = [random.choice(stimuli) for _ in range(diff)]
        return stimuli + more
    return stimuli


def isImage(string):
    images = ['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG']
    return string.rsplit('.', 1)[-1] in images


def getImages(path):
    '''Get all images that a at the top level of a directory.'''
    images = filter(lambda x: isImage(x), os.listdir(path))
    return [os.path.join(path, image) for image in images]


def orderSpec(array, order):
    '''Order an array according to another array that
    specifies the needed order.'''
    return [array[x] for x in map(lambda x: x - 1, order)]


def runExperiment(pause, instructionOrder, blockOrder):
    '''pause is a function that is called between each block.
    instructionOrder and blockOrder a self explanatory. izip_longest
    is need, if there is not an instruction after each block.'''
    data = []
    trialCount = 0
    mapping = itertools.izip_longest(instructionOrder, blockOrder)

    for instr, block in mapping:
        trialCount += 1
        if instr is None:
            continue
        elif isImage(instr):
            pause(image=instr)
        else:
            pause(text=instr)

        current = block(trials=40) if trialCount == 5 else block()
        data.extend(current)

    return data
