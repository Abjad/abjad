from abjad.core import _Immutable
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


class PitchRange(_Immutable):
   r""".. versionadded:: 1.1.2

   Abjad model of pitch range::

      abjad> pitchtools.PitchRange(-12, 36)
      PitchRange((NamedChromaticPitch('c'), 'inclusive'), (NamedChromaticPitch("c''''"), 'inclusive'))

   Init from pitch numbers, pitch instances or other pitch range objects.

   Pitch ranges implement all six Python rich comparators.

   Pitch ranges are immutable.
   """

   def __init__(self, *args):
      if len(args) ==0:
         object.__setattr__(self, '_start', None)
         object.__setattr__(self, '_stop', None)
      elif len(args) == 1:
         assert isinstance(args[0], type(self))
         if args[0].start_pitch_is_included_in_range:
            indicator = 'inclusive'
         else:
            indicator = 'exclusive'
         start = (args[0].start_pitch, indicator)
         object.__setattr__(self, '_start', start)
         assert isinstance(args[0], type(self))
         if args[0].stop_pitch_is_included_in_range:
            indicator = 'inclusive'
         else:
            indicator = 'exclusive'
         stop = (args[0].stop_pitch, indicator)
         object.__setattr__(self, '_stop', stop)
      else:
         assert len(args) == 2
         start, stop = args
         if start is None:
            start = start
         elif isinstance(start, (int, long, float)):
            pitch = NamedChromaticPitch(start)
            start = (pitch, 'inclusive')
         else:
            assert len(start) == 2
            pitch, containment = start
            assert containment in ('inclusive', 'exclusive')
            pitch = NamedChromaticPitch(pitch)
            start = (pitch, containment)
         object.__setattr__(self, '_start', start)
         if stop is None:
            stop = stop
         elif isinstance(stop, (int, long, float)):
            pitch = NamedChromaticPitch(stop)
            stop = (pitch, 'inclusive')
         else:
            assert len(stop) == 2
            pitch, containment = stop
            assert containment in ('inclusive', 'exclusive')
            pitch = NamedChromaticPitch(pitch)
            stop = (pitch, containment)
         object.__setattr__(self, '_stop', stop)
   
   ## OVERLOADS ##

   def __contains__(self, arg):
      if isinstance(arg, (int, long, float)):
         pitch = NamedChromaticPitch(arg)
         return self._contains_pitch(pitch)
      elif isinstance(arg, NamedChromaticPitch):
         return self._contains_pitch(arg)
      else:
         pitches = list_named_chromatic_pitches_in_expr(arg)
         if pitches:
            return all([self._contains_pitch(x) for x in pitches])
      return False

   def __eq__(self, arg):
      if isinstance(arg, PitchRange):
         if self._start == arg._start:
            if self._stop == arg._stop:
               return True
      return False

   def __ge__(self, arg):
      try:
         pitch = NamedChromaticPitch(arg)
         if self.start_pitch is None:
            return False
         return pitch <= self.start_pitch
      except (TypeError, ValueError):
         return False

   def __gt__(self, arg):
      try:
         pitch = NamedChromaticPitch(arg)
         if self.start_pitch is None:
            return False
         return pitch < self.start_pitch
      except (TypeError, ValueError):
         return False

   def __le__(self, arg):
      try:
         pitch = NamedChromaticPitch(arg)
         if self.stop_pitch is None:
            return False
         return self.stop_pitch <= pitch
      except (TypeError, ValueError):
         return False

   def __lt__(self, arg):
      try:
         pitch = NamedChromaticPitch(arg)
         if self.stop_pitch is None:
            return False
         return self.stop_pitch < pitch
      except (TypeError, ValueError):
         return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s, %s)' % (self.__class__.__name__, self._start, self._stop)

   ## PRIVATE METHODS ##

   def _contains_pitch(self, pitch):
      if self._start is None and self._stop is None:
         return True
      elif self._start is None:
         if self.stop_pitch_is_included_in_range:
            return pitch <= self.stop_pitch
         else:
            return pitch < self.stop_pitch
      elif self._stop is None:
         if self.start_pitch_is_included_in_range:
            return self.start_pitch <= pitch
         else:
            return self.start_pitch < pitch
      else:
         if self.start_pitch_is_included_in_range:
            if self.stop_pitch_is_included_in_range:
               return self.start_pitch <= pitch <= self.stop_pitch
            else:
               return self.start_pitch <= pitch < self.stop_pitch
         else:
            if self.stop_pitch_is_included_in_range:
               return self.start_pitch < pitch <= self.stop_pitch
            else:
               return self.start_pitch < pitch < self.stop_pitch

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def start_pitch(self):
      r'''Read-only start pitch of range::

         abjad> pitch_range = pitchtools.PitchRange(-12, 36)
         abjad> pitch_range.start_pitch
         NamedChromaticPitch('c')

      Return pitch.
      '''
      if self._start is None:
         return None
      return self._start[0]

   @property
   def start_pitch_is_included_in_range(self):
      '''True when start pitch is included in range. Otherwise false::

         abjad> pitch_range = pitchtools.PitchRange(-12, 36)
         abjad> pitch_range.start_pitch_is_included_in_range
         True

      Return boolean.
      '''
      if self._start is None:
         return True
      return self._start[1] == 'inclusive'

   @property
   def stop_pitch(self):
      r"""Read-only stop pitch of range::

         abjad> pitch_range = pitchtools.PitchRange(-12, 36)
         abjad> pitch_range.stop_pitch
         NamedChromaticPitch("c''''")

      Return pitch.
      """ 
      if self._stop is None:
         return None
      return self._stop[0]

   @property
   def stop_pitch_is_included_in_range(self):
      '''True when stop pitch is included in range. Otherwise false::

         abjad> pitch_range = pitchtools.PitchRange(-12, 36)
         abjad> pitch_range.stop_pitch_is_included_in_range
         True

      Return boolean.
      '''
      if self._stop is None:
         return True
      return self._stop[1] == 'inclusive'
