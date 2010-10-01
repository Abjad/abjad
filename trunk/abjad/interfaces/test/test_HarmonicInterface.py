from abjad import *


def test_HarmonicInterface_01( ):
   '''Add a natural harmonic.'''

   t = Note(0, (1, 4))
   marktools.LilyPondCommandMark('flageolet', 'right')(t)
   assert t.format == "c'4 \\flageolet"


def test_HarmonicInterface_02( ):
   '''Add and then remove natural harmonic.'''

   t = Note(0, (1, 4))
   marktools.LilyPondCommandMark('flageolet', 'right')(t)
   marktools.detach_lilypond_command_marks_attached_to_component(t, 'flageolet')
   assert t.format == "c'4"
