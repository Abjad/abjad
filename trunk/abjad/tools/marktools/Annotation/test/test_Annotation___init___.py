from abjad import *


def test_Annotation___init____01( ):
   '''Initialize annotation with string.
   '''

   annotation = marktools.Annotation('foo')
   assert annotation.contents == 'foo'
