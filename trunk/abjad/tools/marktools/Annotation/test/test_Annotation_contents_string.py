from abjad import *


def test_Annotation_contents_string_01( ):
   '''Annotation contents string is read / write.
   '''

   annotation = marktools.Annotation('annotation contents')
   assert annotation.contents_string == 'annotation contents'
   
   annotation.contents_string = 'new annotation contents'
   assert annotation.contents_string == 'new annotation contents'
