from abjad import *
from abjad.tools import durtools


def test_durtools_is_lilypond_duration_name_01( ):

   assert durtools.is_lilypond_duration_name(r'\breve')
   assert durtools.is_lilypond_duration_name(r'\longa')
   assert durtools.is_lilypond_duration_name(r'\maxima')


def test_durtools_is_lilypond_duration_name_02( ):

   assert not durtools.is_lilypond_duration_name('breve')
   assert not durtools.is_lilypond_duration_name('foo')
   assert not durtools.is_lilypond_duration_name(12)
