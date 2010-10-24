def _invert_quality_indicator(intervals, inversion):
   from abjad.tools import listtools
   if isinstance(inversion, int):
      #self.rotate(-inversion) 
      intervals = listtools.rotate_iterable(intervals, -inversion)
      rotation = -inversion
   elif inversion == 'root':
      rotation = 0
   elif inversion == 'first':
      #self.rotate(-1)
      intervals = listtools.rotate_iterable(intervals, -1)
      rotation = -1
   elif inversion == 'second':
      #self.rotate(-2)
      intervals = listtools.rotate_iterable(intervals, -2)
      rotation = -2
   elif inversion == 'third':
      #self.rotate(-3)
      intervals = listtools.rotate_iterable(intervals, -3)
      rotation = -3
   elif inversion == 'fourth':
      #self.rotate(-4)
      intervals = listtools.rotate_iterable(intervals, -4)
      rotation = -4
   else:
      raise ValueError('unknown inversion indicator: %s' % inversion)
   return intervals, rotation
