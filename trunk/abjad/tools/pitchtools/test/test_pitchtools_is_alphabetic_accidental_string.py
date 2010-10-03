from abjad import *


def test_pitchtools_is_alphabetic_accidental_string_01( ):

   assert pitchtools.is_alphabetic_accidental_string('')
   assert pitchtools.is_alphabetic_accidental_string('s')
   assert pitchtools.is_alphabetic_accidental_string('ss')
   assert pitchtools.is_alphabetic_accidental_string('f')
   assert pitchtools.is_alphabetic_accidental_string('ff')
   assert pitchtools.is_alphabetic_accidental_string('qs')
   assert pitchtools.is_alphabetic_accidental_string('tqs')
   assert pitchtools.is_alphabetic_accidental_string('qf')
   assert pitchtools.is_alphabetic_accidental_string('tqf')


def test_pitchtools_is_alphabetic_accidental_string_02( ):

   assert pitchtools.is_alphabetic_accidental_string('!')
   assert pitchtools.is_alphabetic_accidental_string('s!')
   assert pitchtools.is_alphabetic_accidental_string('ss!')
   assert pitchtools.is_alphabetic_accidental_string('f!')
   assert pitchtools.is_alphabetic_accidental_string('ff!')
   assert pitchtools.is_alphabetic_accidental_string('qs!')
   assert pitchtools.is_alphabetic_accidental_string('tqs!')
   assert pitchtools.is_alphabetic_accidental_string('qf!')
   assert pitchtools.is_alphabetic_accidental_string('tqf!')
