from abjad import *


def test_Annotation___init___01( ):
   '''Initialize annotation with dictionary.
   '''

   dictionary = { }
   annotation = marktools.Annotation(dictionary)
   assert annotation.contents_string == dictionary
   assert annotation.contents_string is not dictionary
   

