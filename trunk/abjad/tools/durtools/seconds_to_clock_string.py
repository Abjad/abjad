from abjad.rational.rational import Rational


def seconds_to_clock_string(total_seconds):
   '''Format h'mm'' clock string from numeric seconds.'''

   assert isinstance(total_seconds, (int, float, Rational))
   if total_seconds < 0:
      raise ValueError('total seconds must be positive.')

   minutes = int(total_seconds / 60)
   seconds = str(int(total_seconds - minutes * 60)).zfill(2)
   clock_string = "%s'%s''" % (minutes, seconds)

   return clock_string
