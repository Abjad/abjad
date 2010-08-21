from abjad import *
import py.test


#def test_VoiceInterface_number_01( ):
#   '''Voice number defaults to None.'''
#
#   t = Voice(notetools.make_repeated_notes(4))
#
#   assert t[0].voice.number is None
#   assert t.format == "\\new Voice {\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_VoiceInterface_number_02( ):
   '''Voice number can be set on leaves.'''

   t = Voice(notetools.make_repeated_notes(4))
   #t[0].voice.number = 1
   t[0].misc.voice_one = None

   assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_VoiceInterface_number_03( ):
   '''Voice number can be set to 1, 2, 3, 4, or None.
   Anyhing else will throw a ValueError exception.
   '''

   t = Voice(notetools.make_repeated_notes(4))
   #t[0].voice.number = 1
   t[0].misc.voice_one = None
   assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   #t[0].voice.number = 2
   del(t[0].misc.voice_one)
   t[0].misc.voice_two = None
   assert t.format == "\\new Voice {\n\t\\voiceTwo\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   #t[0].voice.number = 3
   del(t[0].misc.voice_two)
   t[0].misc.voice_three = None 
   assert t.format == "\\new Voice {\n\t\\voiceThree\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   #t[0].voice.number = 4
   del(t[0].misc.voice_three)
   t[0].misc.voice_four = None
   assert t.format == "\\new Voice {\n\t\\voiceFour\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   #t[0].voice.number = None
   del(t[0].misc.voice_four)
   assert t.format == "\\new Voice {\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"
   #assert py.test.raises(ValueError, 't[0].voice.number = 23')


def test_VoiceInterface_number_05( ):
   '''Voice number can be set on a Voice container and 
   on one of the leaves contained in it.
   '''

   t = Voice(notetools.make_repeated_notes(4))
   #t.voice.number = 1
   #t[1].voice.number = 2
   t.misc.voice_one = None
   t[1].misc.voice_two = None
   assert t.format == "\\new Voice {\n\t\\voiceOne\n\tc'8\n\t\\voiceTwo\n\tc'8\n\tc'8\n\tc'8\n}"
