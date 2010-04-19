from abjad.tools.tonalharmony.ScaleDegree import ScaleDegree
import re


class SuspensionIndicator(object):
   '''.. versionadded:: 1.1.2

   Indicator of 9-8, 7-6, 4-3, 2-1 and other types of
   suspension typical of, for example, the Bach chorales.

   Value object that can not be changed after instantiation.
   '''

   def __init__(self, *args):
      if len(args) == 0:
         self._init_empty( )
      elif len(args) == 1 and args[0] in (None, ''):
         self._init_empty( )
      elif len(args) == 1 and isinstance(args[0], type(self)):
         self._init_by_reference(*args)
      elif len(args) == 1 and isinstance(args[0], str):
         self._init_by_symbolic_string(*args)
      elif len(args) == 1 and isinstance(args[0], tuple):
         self._init_by_pair(*args)
      elif len(args) == 2:
         self._init_by_start_and_stop(*args)
      else:
         raise ValueError('can not initialize suspension indicator.')

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.start == arg.start:
            if self.stop == arg.stop:
               return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      if self.start is not None and self.stop is not None:
         return '%s(%s, %s)' % (type(self).__name__, self.start, self.stop)
      else:
         return '%s( )' % type(self).__name__

   def __str__(self):
      if self.start is not None and self.stop is not None:
         return '%s-%s' % (self.start, self.stop)
      else:
         return ''

   ## PRIVATE ATTRIBUTES ##

   _symbolic_string_regex = re.compile(r'([#|b]?\d+)-([#|b]?\d+)')
   
   ## PRIVATE METHODS ##

   def _init_by_pair(self, pair):
      start, stop = pair
      self._init_by_start_and_stop(start, stop)
      
   def _init_by_reference(self, suspension_indicator):
      start, stop = suspension_indicator.start, suspension_indicator.stop
      self._init_by_start_and_stop(start, stop)

   def _init_by_start_and_stop(self, start, stop):
      start = ScaleDegree(start)
      stop = ScaleDegree(stop)
      self._start = start
      self._stop = stop

   def _init_by_symbolic_string(self, symbolic_string):
      groups = self._symbolic_string_regex.match(symbolic_string).groups( )
      start, stop = groups
      start = ScaleDegree(start)
      self._start = start
      stop = ScaleDegree(stop)
      self._stop = stop

   def _init_empty(self):
      self._start = None
      self._stop = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def chord_name_string(self):
      if self.is_empty:
         return ''
      return 'sus%s' % self.start

   @property
   def figured_bass_string(self):
      if self.is_empty:
         return ''
      return '%s-%s' % (self.start, self.stop)

   @property
   def is_empty(self):
      return self.start is None and self.stop is None

   @property
   def start(self):
      return self._start

   @property
   def stop(self):
      return self._stop

   @property
   def title_string(self):
      if self.is_empty:
         return ''
      start = self.start.title_string
      stop = self.stop.title_string
      return '%s%sSuspension' % (start, stop)
