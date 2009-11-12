from abjad.rational import Rational


def seconds_to_clock_string_escaped(seconds):
   r'''Format rounded `seconds`.

   Escape the seconds indicator for output as LilyPond markup. ::

      abjad> t = Note(0, (1, 4))
      abjad> durtools.seconds_to_clock_string(117)
      '1\'57\\"'
      abjad> clock_string = _
      abjad> t.markup.up.append('"%s"' % clock_string)
      abjad> print t.format
      c'4 ^ \markup { "1'57\"" }
   '''

   assert isinstance(seconds, (int, float, Rational))
   if seconds < 0:
      raise ValueError('total seconds must be positive.')

   minutes = int(seconds / 60)
   remaining_seconds = str(int(seconds - minutes * 60)).zfill(2)
   clock_string = "%s'%s\\\"" % (minutes, remaining_seconds)

   return clock_string
