from abjad import *
from abjad.tools.scoretools.make_empty_piano_score import make_empty_piano_score
import math


def desordre_build(pitches):
    '''Returns a complete PianoStaff with Ligeti music!'''
    assert len(pitches) == 2
    #piano = make_empty_piano_score( )[0]
    piano = scoretools.PianoStaff([ ])
    # set tempo indication...
    contexttools.TempoMark(Duration(1, 1), 60)(piano)
    # build music...
    for hand in pitches:
        seq = staff_build(hand)
        piano.append(seq)
    # set clef and key to lower staff...
    contexttools.ClefMark('bass')(piano[1])
    contexttools.KeySignatureMark('b', 'major')(piano[1])
    return piano


def staff_build(pitches):
    '''Returns a Staff containing DynamicMeasures.'''
    result = Staff([ ])
    for seq in pitches:
        measure = measure_build(seq)
        result.append(measure)
    return result


def measure_build(pitches):
    '''Returns a DynamicMeasure containing Ligeti "cells".'''
    result = measuretools.DynamicMeasure([ ])
    for seq in pitches:
        result.append(desordre_cell(seq))
    # make denominator 8
    if contexttools.get_effective_time_signature(result).denominator == 1:
        result.denominator = 8
    return result


def desordre_cell(pitches):
    '''Returns a parallel container encapsulating a Ligeti "cell".'''
    pitchtools.NamedChromaticPitch.accidental_spelling = 'sharps'
    notes = [Note(p, (1, 8)) for p in pitches]
    spannertools.BeamSpanner(notes)
    spannertools.SlurSpanner(notes)
    contexttools.DynamicMark('f')(notes[0])
    contexttools.DynamicMark('p')(notes[1])
    v_lower = Voice(notes)
    v_lower.name = 'rh_lower'
    marktools.LilyPondCommandMark('voiceTwo')(v_lower)

    n = int(math.ceil(len(pitches) / 2.))
    chord = Chord([pitches[0], pitches[0] + 12], (n, 8))
    marktools.Articulation('>')(chord)
    v_higher = Voice([chord])
    v_higher.name = 'rh_higher'
    marktools.LilyPondCommandMark('voiceOne')(v_higher)
    p = Container([v_lower, v_higher])
    p.is_parallel = True
    # make all 1/8 beats breakable
    for n in v_lower.leaves[:-1]:
        marktools.BarLine('')(n)
    return p


def load_desordre_pitches(file):
    result = [ ]
    f = open(file, 'r')
    lines = f.read( )
    lines = lines.splitlines( )
    f.close( )
    for line in lines:
        if len(line) == 0:
            pass
        elif line.startswith('###'):
            hand = [ ]
            result.append(hand)
        else:
            runs = [ ]
            runs_char = line.split('@')
            for run in runs_char:
                run = run.split(',')
                run = [int(n) for n in run]
                runs.append(run)
            hand.append(runs)
    return result
