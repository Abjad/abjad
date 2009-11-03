from abjad import *
import math
from abjad.tools import template


def desordre_build(pitches):
   piano = template.piano( )
   piano[1].formatter.opening.append(r'\key b \major')
   for i, hand in enumerate(pitches):
      seq = multimeasure_build(hand)
      piano[i].extend(seq)
   return piano


def multimeasure_build(pitches):
   result = [ ]
   for seq in pitches:
      measure = measure_build(seq)
      result.append(measure)
   return result


def measure_build(pitches):
   result = DynamicMeasure([ ])
   for seq in pitches:
      result.append(desordre_run(seq))
   ## make denominator 4
   if result.meter.effective.denominator == 1:
      result.denominator = 4
   return result


def desordre_run(pitches):
   Pitch.accidental_spelling = 'sharps'
   notes = [Note(p, (1, 8)) for p in pitches]
   Beam(notes)
   Slur(notes)
   notes[0].dynamics.mark = 'f'
   notes[1].dynamics.mark = 'p'
   v_lower = Voice(notes)
   v_lower.name = 'rh_lower'
   v_lower.voice.number = 2

   n = int(math.ceil(len(pitches) / 2.))
   chord = Chord([pitches[0], pitches[0] + 12], (n, 8))
   chord.articulations.append('>')
   v_higher = Voice([chord])
   v_higher.name = 'rh_higher'
   v_higher.voice.number = 1
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


