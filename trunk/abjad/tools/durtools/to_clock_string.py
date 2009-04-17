from abjad.rational.rational import Rational


def to_clock_string(minutes):
   '''Format h'mm'' clock string from rational duration.'''

   assert isinstance(minutes, (int, float, Rational))
   if minutes < 0:
      raise ValueError('clock time must be positive.')

   truncated_minutes = int(minutes)
   seconds = str(int(round(minutes * 60)) % 60).zfill(2)
   clock_string = "%s'%s''" % (truncated_minutes, seconds)

   return clock_string
