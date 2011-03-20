from abjad import *


def test_Comment_contents_string_01( ):
   '''Comment contents string is read / write.
   '''

   comment = marktools.Comment('contents string')
   assert comment.contents_string == 'contents string'

   comment.contents_string = 'new contents string'
   assert comment.contents_string == 'new contents string'
