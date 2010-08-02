from abjad import *


def test_TempoInterface_01( ):
   '''Tempo interface works on nonempty staves.'''

   t = Staff(macros.scale(4))
   t.tempo.forced = tempotools.TempoIndication(Rational(1, 8), 38)

   r'''
   \new Staff {
           \tempo 8=38
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t[0].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[1].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[2].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[3].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t.format == "\\new Staff {\n\t\\tempo 8=38\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_TempoInterface_02( ):
   '''Tempo interface works on empty staves.'''

   t = Staff([ ])
   t.tempo.forced = tempotools.TempoIndication(Rational(1, 8), 38)

   r'''
   \new Staff {
           \tempo 8=38
   }
   '''

   assert t.format == '\\new Staff {\n\t\\tempo 8=38\n}'

   

def test_TempoInterface_03( ):
   '''Tempo interface works on pure containers.'''

   t = Container(macros.scale(4))
   t.tempo.forced = tempotools.TempoIndication(Rational(1, 8), 38)
   t[2].tempo.forced = tempotools.TempoIndication(Rational(1, 8), 42)

   r'''
   {
      \tempo 8=38
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t[0].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[1].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 38)
   assert t[2].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 42)
   assert t[3].tempo.effective == tempotools.TempoIndication(Rational(1, 8), 42)
   assert t.format == "{\n\t\\tempo 8=38\n\tc'8\n\td'8\n\t\\tempo 8=42\n\te'8\n\tf'8\n}"


def test_TempoInterface_04( ):
   '''Tempo interface works on notes.'''

   t = Note(0, (1, 4))
   t.tempo.forced = tempotools.TempoIndication(Rational(1, 8), 38)

   r'''
   \tempo 8=38
   c'4'''

   assert t.format == "\\tempo 8=38\nc'4"


def test_TempoInterface_05( ):
   '''Tempo interface works on chords.'''

   t = Chord([2, 3, 4], (1, 4))
   t.tempo.forced = tempotools.TempoIndication(Rational(1, 8), 38)

   r'''
   \tempo 8=38
      <d' ef' e'>4'''

   assert t.format == "\\tempo 8=38\n<d' ef' e'>4"


def test_TempoInterface_06( ):
   '''Tempo interface accepts durations.'''

   t = Note(0, (1, 4))
   t.tempo.forced = tempotools.TempoIndication(Rational(1, 8), 38)

   r'''
   \tempo 8=38
      c'4'''

   assert t.format == "\\tempo 8=38\nc'4"


def test_TempoInterface_07( ):
   '''None clears tempo.'''

   t = Note(0, (1, 4))
   t.tempo.forced = tempotools.TempoIndication(Rational(1, 8), 38)
   t.tempo.forced = None

   '''
   c'4
   '''

   assert t.format == "c'4"
