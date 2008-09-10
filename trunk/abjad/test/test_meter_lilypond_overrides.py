from abjad import *


def test_meter_lilypond_overrides_01( ):
   '''Abjad Meters format arbitrary LilyPond TimeSignature overrides.'''
   t = Measure((4, 4), Note(0, (1, 4)) * 4)
   t.meter.transparent = True
   assert t.format == "\t\\once \\override Staff.TimeSignature #'transparent = ##t\n\t\\time 4/4\n\tc'4\n\tc'4\n\tc'4\n\tc'4"
   '''
   \once \override Staff.TimeSignature #'transparent = ##t
   \time 4/4
   c'4
   c'4
   c'4
   c'4
   '''


def test_meter_lilypond_overrides_02( ):
   '''Abjad Meters format arbitrary LilyPond TimeSignature overrides.'''
   t = Measure((4, 4), Note(0, (1, 4)) * 4)
   t.meter.color = 'red'
   assert t.format == "\t\\once \\override Staff.TimeSignature #'color = #red\n\t\\time 4/4\n\tc'4\n\tc'4\n\tc'4\n\tc'4"
   '''
   \once \override Staff.TimeSignature #'color = #red
   \time 4/4
   c'4
   c'4
   c'4
   c'4
   '''
