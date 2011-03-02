from abjad.tools.spannertools.Spanner import Spanner
from _StaffLinesSpannerFormatInterface import _StaffLinesSpannerFormatInterface


class StaffLinesSpanner(Spanner):
   '''Abjad staff lines spanner.

   Staff lines spanner handles changing either the line-count
   or the line-positions property of the StaffSymbol grob,
   as well as automatically stopping and restarting the staff
   so that the change may take place.

   Return staff lines spanner.
   '''

   def __init__(self, arg = 5, music = None):
      Spanner.__init__(self, music)
      if isinstance(arg, int) and 0 < arg:
         self._lines = arg
      elif isinstance(arg, (tuple, list)) \
      and all([isinstance(x, (int, float)) for x in arg]):
         self._lines = arg
      else:
         raise ValueError('StaffLinesSpanner requires either an int, ' + \
            'or a list/tuple of ints and/or floats.')
      self._format = _StaffLinesSpannerFormatInterface(self)

   @apply
   def lines( ):
      def fget(self):
         return self._lines
      def fset(self, arg):
         if isinstance(arg, int) and 0 < arg:
            self._lines = arg
         elif isinstance(arg, (tuple, list)) \
         and all([isinstance(x, (int, float)) for x in arg]):
            self._lines = arg
         else:
            raise ValueError('StaffLinesSpanner requires either an int, ' + \
               'or a list/tuple of ints and/or floats.')
      return property(**locals( ))
