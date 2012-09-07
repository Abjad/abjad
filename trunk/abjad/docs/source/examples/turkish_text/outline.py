# -*- encoding: utf-8 -*-
from abjad import *


input_text = u"""Taraf'ın Türkiye'nin saygın gazetelerinden olduğunun anımsatıldığı dilekçede."""
other = u"ÜÖ"
even_more_other = u"Ü"

vowel_treatments = {
     'a':   (2, pitchtools.NamedChromaticPitch("G4")),
     'i':   (2, pitchtools.NamedChromaticPitch("E4")),
    u'ı':   (1, pitchtools.NamedChromaticPitch("E4")),
     'u':   (2, pitchtools.NamedChromaticPitch("C4")),
    u'ü':   (4, pitchtools.NamedChromaticPitch("C4")),
     'e':   (2, pitchtools.NamedChromaticPitch("A3")),
     'o':   (2, pitchtools.NamedChromaticPitch("F3")),
    u'ö':   (4, pitchtools.NamedChromaticPitch("F3")), 
}

def letter_to_duration_numerator(letter):
    letter = letter.lower()
    try:
        treatment_pair = consonant_treatments[letter]
    except KeyError:
        treatment_pair = vowel_treatments[letter]
    duration_numerator = treatment_pair[0]
    return duration_numerator

def letter_to_pitch(letter):
    letter = letter.lower()
    try:
        treatment_pair = consonant_treatments[letter]
    except KeyError:
        treatment_pair = vowel_treatments[letter]
    pitch = treatment_pair[-1]
    return pitch

consonant_treatments = {
    'b':    (2, pitchtools.NamedChromaticPitch("G4")),
    'c':    (3, pitchtools.NamedChromaticPitch("G4")),
   u'ç':    (3, pitchtools.NamedChromaticPitch("G4")),
    'd':    (2, pitchtools.NamedChromaticPitch("G4")),
    'f':    (3, pitchtools.NamedChromaticPitch("E4")),
    'g':    (2, pitchtools.NamedChromaticPitch("E4")),
   u'ğ':    (0, pitchtools.NamedChromaticPitch("E4")),
    'h':    (3, pitchtools.NamedChromaticPitch("E4")),
    'k':    (1, pitchtools.NamedChromaticPitch("C4")),
    'l':    (4, pitchtools.NamedChromaticPitch("C4")),
    'm':    (4, pitchtools.NamedChromaticPitch("C4")),
    'n':    (4, pitchtools.NamedChromaticPitch("C4")),
    'p':    (2, pitchtools.NamedChromaticPitch("A3")),
    'r':    (2, pitchtools.NamedChromaticPitch("A3")),
    's':    (4, pitchtools.NamedChromaticPitch("A3")),
   u'ş':    (4, pitchtools.NamedChromaticPitch("A3")),
    't':    (1, pitchtools.NamedChromaticPitch("A3")),
    'v':    (3, pitchtools.NamedChromaticPitch("F3")),
    'y':    (3, pitchtools.NamedChromaticPitch("F3")),
    'z':    (4, pitchtools.NamedChromaticPitch("F3")),
}




def make_score(input_text):
