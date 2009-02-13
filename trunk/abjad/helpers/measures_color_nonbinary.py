from abjad.helpers.iterate import iterate


def measures_color_nonbinary(expr, color = 'red'):
   '''Color all nonbinary mesures in expr.
      Useful when giving presentations or explaining transforms.
      
      TODO: Give URL of list of valid LilyPond color names here.'''

   for measure in iterate(expr, '_Measure'):
      if measure.meter.effective.nonbinary:
         measure.beam.color = color
         measure.dots.color = color
         measure.meter.color = color
         measure.meter.promote('color', 'Staff')
         measure.notehead.color = color
         measure.stem.color = color
