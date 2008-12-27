from abjad import *


def test_tempo_01( ):
   '''Tempo works on staves.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t.tempo = (1, 8), 38
   assert t.format == "\\new Staff {\n\t\\tempo 8=38\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   r'''
   \new Staff {
           \tempo 8=38
           c'8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_tempo_02( ):
   '''Tempo works on empty staves.'''
   t = Staff([ ])
   t.tempo = (1, 8), 38
   assert t.format == '\\new Staff {\n\t\\tempo 8=38\n}'
   r'''
   \new Staff {
           \tempo 8=38
   }
   '''


def test_tempo_03( ):
   '''Tempo works on pure containers.'''
   t = Container([Note(n, (1, 8)) for n in range(8)])
   t.tempo = (1, 8), 38
   assert t.format == "\t\\tempo 8=38\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8"
   r'''
        \tempo 8=38
        c'8
        cs'8
        d'8
        ef'8
        e'8
        f'8
        fs'8
        g'8
   '''


def test_tempo_04( ):
   '''Tempo works on notes.'''
   t = Note(0, (1, 4))
   t.tempo = (1, 8), 38
   assert t.format == "\\tempo 8=38\nc'4"
   r'''
   \tempo 8=38
   c'4
   '''


def test_tempo_05( ):
   '''Tempo works on chords.'''
   t = Chord([2, 3, 4], (1, 4))
   t.tempo = (1, 8), 38
   assert t.format == "\\tempo 8=38\n<d' ef' e'>4"
   r'''
   \tempo 8=38
   <d' ef' e'>4
   '''


def test_tempo_06( ):
   '''Tempo accepts durations.'''
   t = Note(0, (1, 4))
   t.tempo = Rational(1, 8), 38
   assert t.format == "\\tempo 8=38\nc'4"
   r'''
   \tempo 8=38
   c'4
   '''


def test_tempo_07( ):
   '''None clears tempo.'''
   t = Note(0, (1, 4))
   t.tempo = Rational(1, 8), 38
   t.tempo = None
   assert t.format == "c'4"
   '''
   c'4
   '''
