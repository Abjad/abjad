from abjad import *


def test_ScaleDegree_name_01( ):

   assert tonalharmony.ScaleDegree(1).name == 'tonic'
   assert tonalharmony.ScaleDegree(2).name == 'superdominant'
   assert tonalharmony.ScaleDegree(3).name == 'mediant'
   assert tonalharmony.ScaleDegree(4).name == 'subdominant'
   assert tonalharmony.ScaleDegree(5).name == 'dominant'
   assert tonalharmony.ScaleDegree(6).name == 'submediant'
   assert tonalharmony.ScaleDegree(7).name == 'leading tone'
