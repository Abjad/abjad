from abjad import *


def test_ChordClass_quality_pair_01( ):

   cc = tonalharmony.ChordClass('c', 'major', 'triad', 'root')
   assert cc.quality_pair == ('major', 'triad')

   cc = tonalharmony.ChordClass('c', 'minor', 'triad', 'root')
   assert cc.quality_pair == ('minor', 'triad')


def test_ChordClass_quality_pair_02( ):

   cc = tonalharmony.ChordClass('c', 'dominant', 'seventh', 'root')
   assert cc.quality_pair == ('dominant', 'seventh')

   cc = tonalharmony.ChordClass('c', 'diminished', 'seventh', 'root')
   assert cc.quality_pair == ('diminished', 'seventh')
