from abjad.measure.measure import _Measure
from abjad.tools import iterate
from abjad.tools import overridetools


def color_nonbinary(expr, color = 'red'):
   '''Color all nonbinary mesures in 'expr'.
      Useful when giving presentations or explaining transforms.

      The usual LilyPond color names are these:

      black       white          red         green
      blue        cyan           magenta     yellow
      grey        darkred        darkgreen   darkblue
      darkcyan    darkmagenta    darkyellow 
   
      Additional color names appear in appendix B.5 of the LilyPond LM.'''

   for measure in iterate.naive_forward(expr, _Measure):
      if measure.meter.effective.nonbinary:
         measure.beam.color = color
         measure.dots.color = color
         measure.meter.color = color
         overridetools.promote(measure.meter, 'color', 'Staff')
         measure.note_head.color = color
         measure.stem.color = color
