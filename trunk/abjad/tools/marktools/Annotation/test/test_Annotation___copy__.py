from abjad import *
import copy


def test_Annotation___copy___01( ):
   '''Annotation copy copies annotation contents.
   '''

   dictionary = { }
   annotation_1 = marktools.Annotation(dictionary)
   annotation_2 = copy.copy(annotation_1)
   assert annotation_1 == annotation_2
   assert annotation_1 is not annotation_2
   assert annotation_1.contents == annotation_2.contents == dictionary
   assert annotation_1.contents is not annotation_2.contents is not dictionary
