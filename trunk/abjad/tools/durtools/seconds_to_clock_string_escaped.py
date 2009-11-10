from abjad.rational import Rational


def seconds_to_clock_string_escaped(total_seconds):
   r'''Format ``seconds`` as ``m'ss"`` string 
   rounded to the nearest second. Escape the seconds indicator
   for output as LilyPond markup. ::

      abjad> t = Note(0, (1, 4))
      abjad> durtools.seconds_to_clock_string(117, escape = True)
      '1\'57\\"'
      abjad> clock_string = _
      abjad> t.markup.up.append('"%s"' % clock_string)
      abjad> print t.format
      c'4 ^ \markup { "1'57\"" }
   '''

   assert isinstance(total_seconds, (int, float, Rational))
   if total_seconds < 0:
      raise ValueError('total seconds must be positive.')

   minutes = int(total_seconds / 60)
   seconds = str(int(total_seconds - minutes * 60)).zfill(2)
   clock_string = "%s'%s\\\"" % (minutes, seconds)

   return clock_string
