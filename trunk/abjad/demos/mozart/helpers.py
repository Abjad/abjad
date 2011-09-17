from abjad import *
from abjad.demos.mozart.measures import measures
import random


def choose_mozart_measures( ):
    chosen_measures = [ ]
    for i, choices in enumerate(measures):
        if i == 7: # get both alternative endings
            chosen_measures.extend(choices)
        else:
            choice = random.choice(choices)
            chosen_measures.append(choice)
    return chosen_measures    


def build_one_mozart_measure(measure_dict):
    # parse the contents of a measure definition dictionary
    treble = iotools.parse_lilypond_input_string(measure_dict['t'])
    bass = iotools.parse_lilypond_input_string(measure_dict['b'])
    return treble, bass

    
def build_mozart_piano_staff( ):
    treble_staff = Staff([ ])
    bass_staff = Staff([ ])

    # select the measures to use
    choices = choose_mozart_measures( )

    # create and populate the volta containers
    treble_volta = Container([ ])
    bass_volta = Container([ ])
    for choice in choices[:7]:
        treble, bass = build_one_mozart_measure(choice)
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
        treble, bass = build_one_mozart_measure(choice)
        treble_alternative.append(treble)
        bass_alternative.append(bass)

    # add marks to the alternative containers
    marktools.LilyPondCommandMark('alternative', 'before')(treble_alternative)
    marktools.LilyPondCommandMark('alternative', 'before')(bass_alternative)
    treble_staff.append(treble_alternative)
    bass_staff.append(bass_alternative)

    # create the remaining measures
    for choice in choices[9:]:
        treble, bass = build_one_mozart_measure(choice)
        treble_staff.append(treble)
        bass_staff.append(bass)

    # add meter
    contexttools.TimeSignatureMark((3, 8))(treble_staff)

    # add bass clef
    contexttools.ClefMark('bass')(bass_staff)

    # add the final double bar line to each final measure
    marktools.LilyPondCommandMark('bar "|."', 'closing')(treble_staff[-1])
    marktools.LilyPondCommandMark('bar "|."', 'closing')(bass_staff[-1])

    # combine into a PianoStaff
    piano_staff = scoretools.PianoStaff([treble_staff, bass_staff])

    # add an instrument name via contexttools.InstrumentMark
    contexttools.InstrumentMark('Katzenklavier', 'kk.',
        target_context = scoretools.PianoStaff)(piano_staff)

    return piano_staff


def build_mozart_lily(piano_staff):

    # wrap the PianoStaff with a LilyPondFile
    lily = lilypondfiletools.make_basic_lilypond_file(piano_staff)

    # create some markup to use in our header block
    title = markuptools.Markup('\\bold \\sans "Ein Musikalisches Wuerfelspiel"')
    composer = schemetools.SchemeString("W. A. Mozart (maybe?)")

    # change various settings
    lily.global_staff_size = 12
    lily.header_block.title = title
    lily.header_block.composer = composer
    lily.layout_block.ragged_right = True
    lily.paper_block.markup_system_spacing__basic_distance = 20
    lily.paper_block.paper_width = 180

    return lily
