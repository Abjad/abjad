from abjad.tools import iterate


def measures_color_nonbinary(expr, color = 'red'):
   '''Color all nonbinary mesures in 'expr'.
      Useful when giving presentations or explaining transforms.

      The usual LilyPond color names are these:

      black       white          red         green
      blue        cyan           magenta     yellow
      grey        darkred        darkgreen   darkblue
      darkcyan    darkmagenta    darkyellow 
   
      Additional color names appear in appendix B.5 of the LilyPond LM.'''

   from abjad.measure.measure import _Measure
   for measure in iterate.naive(expr, _Measure):
      if measure.meter.effective.nonbinary:
         measure.beam.color = color
         measure.dots.color = color
         measure.meter.color = color
         measure.meter.promote('color', 'Staff')
         measure.notehead.color = color
         measure.stem.color = color
