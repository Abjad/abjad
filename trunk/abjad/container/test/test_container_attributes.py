from abjad import *


def test_container_attributes_01( ):
   '''
   Container implements five public attributes.
   '''

   t = Container(scale(4))

   r'''
        c'8
        d'8
        e'8
        f'8
   '''

   assert t.format == "\tc'8\n\td'8\n\te'8\n\tf'8"
   assert t.leaves == t._music
   assert t.next is None
   assert t.parallel == False
   assert t.prev is None
