from abjad.core import Fraction


def numeric_seconds_to_escaped_clock_string(seconds):
   r'''Format rounded `seconds`.

   Escape the seconds indicator for output as LilyPond markup. ::

      abjad> t = Note(0, (1, 4))
      abjad> durtools.numeric_seconds_to_clock_string(117)
      '1\'57\\"'
      abjad> clock_string = _
      abjad> markuptools.Markup('"%s"' % clock_string, 'up')(t)
      abjad> print t.format
      c'4 ^ \markup { "1'57\"" }

   .. versionchanged:: 1.1.2
      renamed ``durtools.seconds_to_clock_string_escaped( )`` to
      ``durtools.numeric_seconds_to_escaped_clock_string( )``.
   '''

   assert isinstance(seconds, (int, float, Fraction))
   if seconds < 0:
      raise ValueError('total seconds must be positive.')

   minutes = int(seconds / 60)
   remaining_seconds = str(int(seconds - minutes * 60)).zfill(2)
   clock_string = "%s'%s\\\"" % (minutes, remaining_seconds)

   return clock_string
