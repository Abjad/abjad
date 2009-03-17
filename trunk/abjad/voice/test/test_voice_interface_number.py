from abjad import *
import py.test


def test_voice_interface_number_01( ):
   '''Voice number defaults to None.'''

   t = Voice(run(4))

   assert t[0].voice.number is None
   assert t.format == "\\new Voice {\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_voice_interface_number_02( ):
   '''Voice number can be set on leaves.'''

   t = Voice(run(4))
   t[0].voice.number = 1

   assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_voice_interface_number_03( ):
   '''Voice number can be set to 1, 2, 3, 4, or None.
      Anyhing else will throw a ValueError exception.'''

   t = Voice(run(4))
   t[0].voice.number = 1
   assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   t[0].voice.number = 2
   assert t.format == "\\new Voice {\n\t\\voiceTwo\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   t[0].voice.number = 3
   assert t.format == "\\new Voice {\n\t\\voiceThree\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   t[0].voice.number = 4
   assert t.format == "\\new Voice {\n\t\\voiceFour\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   t[0].voice.number = None
   assert t.format == "\\new Voice {\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"
   assert py.test.raises(ValueError, 't[0].voice.number = 23')


def test_voice_interface_number_04( ):
   '''Voice number can be set on a Voice container.'''

   t = Voice(run(4))
   t.voice.number = 1
   assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_voice_interface_number_05( ):
   '''Voice number can be set on a Voice container and 
      on one of the leaves contained in it.'''

   t = Voice(run(4))
   t.voice.number = 1
   t[1].voice.number = 2
   assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\t\\voiceTwo\n\tc'8\n\tc'8\n\tc'8\n}"
