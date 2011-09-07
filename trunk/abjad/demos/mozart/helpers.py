from abjad import *
from abjad.demos.mozart.measures import measures
import random


def choose_measures( ):
    chosen_measures = [ ]
    for i, choices in enumerate(measures):
        if i == 7: # get both alternative endings
            chosen_measures.extend(choices)
        else:
            choice = random.choice(choices)
            chosen_measures.append(choice)
    return chosen_measures    


def build_measure(measure_dict):
    # parse the contents of a measure definition dictionary
    treble = iotools.parse_lilypond_input_string(measure_dict['t'])
    bass = iotools.parse_lilypond_input_string(measure_dict['b'])
    return treble, bass

    
def build_score( ):
    treble_staff = Staff([ ])
    bass_staff = Staff([ ])

    # select the measures to use
    choices = choose_measures( )

    # create and populate the volta containers
    treble_volta = Container([ ])
    bass_volta = Container([ ])
    for choice in choices[:7]:
        treble, bass = build_measure(choice)
        treble_volta.append(treble)
        bass_volta.append(bass)

    # add marks to the volta containers
    marktools.LilyPondCommandMark('repeat volta 2', 'before')(treble_volta)
    marktools.LilyPondCommandMark('repeat volta 2', 'before')(bass_volta)
    treble_staff.append(treble_volta)
    bass_staff.append(bass_volta)

    # create and populate the alternative ending containers
    treble_alternative = Container([ ])
    bass_alternative = Container([ ])
    for choice in choices[7:9]:
        treble, bass = build_measure(choice)
        treble_alternative.append(treble)
        bass_alternative.append(bass)

    # add marks to the alternative containers
    marktools.LilyPondCommandMark('alternative', 'before')(treble_alternative)
    marktools.LilyPondCommandMark('alternative', 'before')(bass_alternative)
    treble_staff.append(treble_alternative)
    bass_staff.append(bass_alternative)

    # create the remaining measures
    for choice in choices[9:]:
        treble, bass = build_measure(choice)
        treble_staff.append(treble)
        bass_staff.append(bass)

    # add meter
    contexttools.TimeSignatureMark((3, 8))(treble_staff)

    # add bass clef
    contexttools.ClefMark('bass')(bass_staff)

    # add the final double bar line to each final measure
    marktools.LilyPondCommandMark('bar "|."', 'closing')(treble_staff[-1])
    marktools.LilyPondCommandMark('bar "|."', 'closing')(bass_staff[-1])

    # combine into a PianoStaff and return
    return scoretools.PianoStaff([treble_staff, bass_staff])
