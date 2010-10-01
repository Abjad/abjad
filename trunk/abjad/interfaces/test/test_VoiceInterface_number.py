from abjad import *


def test_VoiceInterface_number_02( ):
   '''Voice number can be set on leaves.'''

   t = Voice(notetools.make_repeated_notes(4))
   marktools.LilyPondCommandMark('voiceOne')(t[0])

   assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_VoiceInterface_number_03( ):
   '''Voice number can be set to 1, 2, 3, 4, or None.
   Anyhing else will throw a ValueError exception.
   '''

   t = Voice(notetools.make_repeated_notes(4))
   marktools.LilyPondCommandMark('voiceOne')(t[0])
   assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   marktools.detach_lilypond_command_marks_attached_to_component(t[0], 'voiceOne')
   marktools.LilyPondCommandMark('voiceTwo')(t[0])
   assert t.format == "\\new Voice {\n\t\\voiceTwo\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   marktools.detach_lilypond_command_marks_attached_to_component(t[0], 'voiceTwo')
   marktools.LilyPondCommandMark('voiceThree')(t[0])
   assert t.format == "\\new Voice {\n\t\\voiceThree\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   marktools.detach_lilypond_command_marks_attached_to_component(t[0], 'voiceThree')
   marktools.LilyPondCommandMark('voiceFour')(t[0])
   assert t.format == "\\new Voice {\n\t\\voiceFour\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   marktools.detach_lilypond_command_marks_attached_to_component(t[0], 'voiceFour')
   assert t.format == "\\new Voice {\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_VoiceInterface_number_04( ):
   '''Voice number can be set on a Voice container and on one of the leaves contained in it.
   '''

   t = Voice(notetools.make_repeated_notes(4))
   marktools.LilyPondCommandMark('voiceOne')(t)
   marktools.LilyPondCommandMark('voiceTwo')(t[1])
   assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\t\\voiceTwo\n\tc'8\n\tc'8\n\tc'8\n}"
