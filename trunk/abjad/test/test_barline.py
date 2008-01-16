from abjad import *


### TEST LEAF BARLINE ###

def test_leaf_barline_01( ):
   t = Note(0, (1, 4))
   t.barline = 'final'
   assert t.format == 'c\'4\n\\bar "|."'


### TEST CONTAINER BARLINE ###

def test_container_barline_01( ):
   t = Staff([ ])
   t.barline = 'final'
   assert t.format == '\\new Staff {\n\t\\bar "|."\n}' 
