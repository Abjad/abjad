from abjad import *


def test_ScaleDegree__init_by_number_01( ):

   degree = tonalharmony.ScaleDegree(2)
   assert degree.accidental == pitchtools.Accidental('')
   assert degree.number == 2


def test_ScaleDegree__init_by_number_02( ):
   '''Init from other scale degree instance.'''

   degree = tonalharmony.ScaleDegree(2)
   new = tonalharmony.ScaleDegree(degree)

   assert degree is not new
   assert new.number == 2
