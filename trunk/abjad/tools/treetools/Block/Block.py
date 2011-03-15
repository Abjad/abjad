from abjad.tools.treetools.BoundedInterval import BoundedInterval


class Block(BoundedInterval):
   '''An abstract block of musical material occupying some amount of time.'''

   __slots__ = ('_data', '_high', '_low', )

   def __init__(self, *args, **kwargs):
      if len(args) == 1 and isinstance(args[0], BoundedInterval):
         start_offset = args[0].low
         duration = args[0].high - args[0].low
         data = args[0].data
      elif len(args) == 2:
         start_offset, duration, data = args[0], args[1], None
         if 'data' in kwargs:
            data = kwargs['data']
      elif len(args) == 3:
         start_offset, duration, data = args
      else:
         raise ValueError('unknown argument combinations.')
      BoundedInterval.__init__(self, start_offset, start_offset + duration, data)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s, %s, data = %s)' % \
         (self.__class__.__name__, \
         repr(self.start_offset), \
         repr(self.duration), \
         repr(self.data))

   ## PUBLIC ATTRIBUTES ##

   @property
   def start_offset(self):
      return self.low

   @property
   def stop_offset(self):
      return self.high

   @property
   def duration(self):
      return self.high - self.low
