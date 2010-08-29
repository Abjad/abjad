from abjad import *
import math
#from abjad.tools import template
from abjad.tools.scoretools.make_empty_piano_score import make_rigid_measures_with_full_measure_spacer_skips_empty_piano_score


def desordre_build(pitches):
   '''Returns a complete PianoStaff with Ligeti music!'''
   assert len(pitches) == 2
   #piano = make_empty_piano_score( )[0]
   piano = scoretools.PianoStaff([ ])
   ## set tempo indication...
   spannertools.TempoSpanner(piano, tempotools.TempoIndication(Rational(1, 1), 60))
   ## build music...
   for hand in pitches:
      seq = staff_build(hand)
      piano.append(seq)
   ## set clef and key to lower staff...
   marktools.ClefMark('bass')(piano[1])
   marktools.KeySignatureMark('b', 'major')(piano[1])
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
   result = DynamicMeasure([ ])
   for seq in pitches:
      result.append(desordre_cell(seq))
   ## make denominator 8
   if marktools.get_effective_time_signature(result).denominator == 1:
      result.denominator = 8
   return result


def desordre_cell(pitches):
   '''Returns a parallel container encapsulating a Ligeti "cell".'''
   Pitch.accidental_spelling = 'sharps'
   notes = [Note(p, (1, 8)) for p in pitches]
   spannertools.BeamSpanner(notes)
   spannertools.SlurSpanner(notes)
   notes[0].dynamics.mark = 'f'
   notes[1].dynamics.mark = 'p'
   v_lower = Voice(notes)
   v_lower.name = 'rh_lower'
   #v_lower.voice.number = 2
   v_lower.misc.voice_two = None

   n = int(math.ceil(len(pitches) / 2.))
   chord = Chord([pitches[0], pitches[0] + 12], (n, 8))
   chord.articulations.append('>')
   v_higher = Voice([chord])
   v_higher.name = 'rh_higher'
   #v_higher.voice.number = 1
   v_higher.misc.voice_one = None
   p = Container([v_lower, v_higher])
   p.parallel = True
   ## make all 1/8 beats breakable
   for n in v_lower.leaves[:-1]:
      n.bar_line.kind = ''
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
      elif line.startswith('##'):
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


