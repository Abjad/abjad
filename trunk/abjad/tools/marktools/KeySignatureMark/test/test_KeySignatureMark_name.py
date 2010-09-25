from abjad import *


def test_KeySignature_name_01( ):

   assert marktools.KeySignatureMark('e', 'major').name == 'E major'
   assert marktools.KeySignatureMark('E', 'major').name == 'E major'

   assert marktools.KeySignatureMark('e', 'minor').name == 'e minor'
   assert marktools.KeySignatureMark('E', 'minor').name == 'e minor'
