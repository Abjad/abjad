from abjad import *
import py.test
py.test.skip('fix me.')


def test_TempoInterface_01( ):
   '''Tempo interface works on staves.
   '''

   t = Staff(macros.scale(4))
   #t.tempo.forced = tempotools.TempoIndication(Rational(1, 8), 38)
   #t[2].tempo.forced = tempotools.TempoIndication(Rational(1, 8), 42)
   marktools.TempoMark(Rational(1, 8), 38)(t)
   marktools.TempoMark(Rational(1, 8), 42)(t, t[2])

   r'''
   \new Staff {
      \tempo 8=38
      c'8
      d'8
      \tempo 8=42
      e'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t[0].tempo.effective == marktools.TempoMark(Rational(1, 8), 38)
   assert t[1].tempo.effective == marktools.TempoMark(Rational(1, 8), 38)
   assert t[2].tempo.effective == marktools.TempoMark(Rational(1, 8), 42)
   assert t[3].tempo.effective == marktools.TempoMark(Rational(1, 8), 42)
   assert t.format == "\\new Staff {\n\t\\tempo 8=38\n\tc'8\n\td'8\n\t\\tempo 8=42\n\te'8\n\tf'8\n}"



def test_TempoInterface_02( ):
   '''Tempo interface works on chords.
   '''

   t = Staff([Chord([2, 3, 4], (1, 4))])
   marktools.TempoMark(Rational(1, 8), 38)(t, t[0])

   r'''
   \new Staff {
      \tempo 8=38
      <d' ef' e'>4
   }
   '''

   assert t.format == "\\new Staff {\n\t\\tempo 8=38\n\t<d' ef' e'>4\n}"


def test_TempoInterface_03( ):
   '''Tempo interface accepts durations.'''

   staff = Staff([Note(0, (1, 4))])
   #t.tempo.forced = tempotools.TempoIndication(Rational(1, 8), 38)
   marktools.TempoMark(Rational(1, 8), 38)(staff, staff[0])

   r'''
   \new Staff {
      \tempo 8=38
      c'4
   }
   '''

   assert staff.format == "\\new Staff {\n\t\\tempo 8=38\n\tc'4\n}"


def test_TempoInterface_04( ):
   '''Detach tempo mark.
   '''

   staff = Staff([Note(0, (1, 4))])
   tempo = marktools.TempoMark(Rational(1, 8), 38)(staff, staff[0])
   tempo.detach_mark_from_context_and_start_component( )
   

   r'''
   \new Staff {
      c'4
   }
   '''

   assert staff.format == "\\new Staff {\n\tc'4\n}"
