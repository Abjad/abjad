from abjad import *
import py.test
py.test.skip( )


def test_ChromaticInterval___init___01( ):
   '''Init from positive number.'''

   i = pitchtools.ChromaticInterval(3)
   assert i.interval_number == 3


def test_ChromaticInterval___init___02( ):
   '''Init from negative number.'''

   i = pitchtools.ChromaticInterval(-3)
   assert i.interval_number == -3


def test_ChromaticInterval___init___03( ):
   '''Init from other chromatic interval.'''

   i = pitchtools.ChromaticInterval(3)
   j = pitchtools.ChromaticInterval(i)
   assert i.interval_number == j.interval_number == 3
   assert i is not j
   

def test_ChromaticInterval___init___04( ):
   '''Init from diatonic interval.'''

   diatonic_interval = pitchtools.DiatonicInterval('perfect', 4)
   i = pitchtools.ChromaticInterval(diatonic_interval)
   assert i.interval_number == 5
