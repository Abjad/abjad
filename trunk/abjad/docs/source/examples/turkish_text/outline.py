# -*- encoding: utf-8 -*-
from abjad import *


source = u"""Taraf'ın Türkiye'nin saygın gazetelerinden olduğunun anımsatıldığı dilekçede."""
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

def vowel_to_duration_numerator(vowel):
    vowel = vowel.lower()
    treatment_pair = vowel_treatments[vowel]
    duration_numerator = treatment_pair[0]
    return duration_numerator

def vowel_to_pitch(vowel):
    vowel = vowel.lower()
    treatment_pair = vowel_treatments[vowel]
    pitch = treatment_pair[-1]
    return pitch

consonant_treatments = {
    'b':    ()
        }
