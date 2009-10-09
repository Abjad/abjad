from abjad.pitch import Pitch


class PitchRange(object):
   '''Model a range of pitches.

   All the magic is in the implementation of __contains__.

   Tests are all made by pitch number.
   '''

   def __init__(self, start = None, stop = None):
      self.start = start
      self.stop = stop
   
   ## OVERLOADS ##

   def __contains__(self, arg):
      try:
         pitch = Pitch(arg)
      except (KeyError, ValueError):
         return False
      if self.start is None and self.stop is None:
         return True
      elif self.start is None:
         if self._include_stop:
            return pitch <= self._stop_pitch
         else:
            return pitch < self._stop_pitch
      elif self.stop is None:
         if self._include_start:
            return self._start_pitch <= pitch
         else:
            return self._start_pitch < pitch
      else:
         if self._include_start:
            if self._include_stop:
               return self._start_pitch <= pitch <= self._stop_pitch
            else:
               return self._start_pitch <= pitch < self._stop_pitch
         else:
            if self._include_stop:
               return self._start_pitch < pitch <= self._stop_pitch
            else:
               return self._start_pitch < pitch < self._stop_pitch

   def __repr__(self):
      return '%s(%s, %s)' % (
         self.__class__.__name__, self.start, self.stop)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _include_start(self):
      if self.start is None:
         return True
      return self.start[1] == 'inclusive'

   @property
   def _include_stop(self):
      if self.stop is None:
         return True
      return self.stop[1] == 'inclusive'

   @property
   def _start_pitch(self):
      if self.start is None:
         return None
      return self.start[0]

   @property
   def _stop_pitch(self):
      if self.stop is None:
         return None
      return self.stop[0]

   ## PUBLIC ATTRIBUTES ##
   
   @apply
   def start( ):
      def fget(self):
         return self._start
      def fset(self, arg):
         if arg is None:
            self._start = arg
         else:
            assert len(arg) == 2
            pitch, containment = arg
            assert containment in ('inclusive', 'exclusive')
            pitch = Pitch(pitch)
            self._start = (pitch, containment)
      return property(**locals( ))

   @apply
   def stop( ):
      def fget(self):
         return self._stop
      def fset(self, arg):
         if arg is None:
            self._stop = arg
         else:
            assert len(arg) == 2
            pitch, containment = arg
            assert containment in ('inclusive', 'exclusive')
            pitch = Pitch(pitch)
            self._stop = (pitch, containment)
      return property(**locals( ))
