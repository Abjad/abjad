from abjad.NamedPitch import NamedPitch
from abjad.tools.pitchtools.get_pitches import get_pitches


class PitchRange(object):
   '''.. versionadded:: 1.1.2

   Model a range of pitches.

   All the magic is in the implementation of __contains__.

   Tests are all made by pitch number.
   '''

   def __init__(self, start = None, stop = None):
      self.start = start
      self.stop = stop
   
   ## OVERLOADS ##

   def __contains__(self, arg):
      if isinstance(arg, (int, long, float)):
         pitch = NamedPitch(arg)
         return self._contains_pitch(pitch)
      elif isinstance(arg, NamedPitch):
         return self._contains_pitch(arg)
      else:
         pitches = get_pitches(arg)
         if pitches:
            return all([self._contains_pitch(x) for x in pitches])
      return False

   def __eq__(self, arg):
      if isinstance(arg, PitchRange):
         if self.start == arg.start:
            if self.stop == arg.stop:
               return True
      return False

   def __ne__(self, arg):
      return not self == arg

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

   ## PRIVATE METHODS ##

   def _contains_pitch(self, pitch):
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

   ## PUBLIC ATTRIBUTES ##
   
   @apply
   def start( ):
      def fget(self):
         return self._start
      def fset(self, arg):
         if arg is None:
            self._start = arg
         elif isinstance(arg, (int, long, float)):
            pitch = NamedPitch(arg)
            self._start = (pitch, 'inclusive')
         else:
            assert len(arg) == 2
            pitch, containment = arg
            assert containment in ('inclusive', 'exclusive')
            pitch = NamedPitch(pitch)
            self._start = (pitch, containment)
      return property(**locals( ))

   @apply
   def stop( ):
      def fget(self):
         return self._stop
      def fset(self, arg):
         if arg is None:
            self._stop = arg
         elif isinstance(arg, (int, long, float)):
            pitch = NamedPitch(arg)
            self._stop = (pitch, 'inclusive')
         else:
            assert len(arg) == 2
            pitch, containment = arg
            assert containment in ('inclusive', 'exclusive')
            pitch = NamedPitch(pitch)
            self._stop = (pitch, containment)
      return property(**locals( ))
