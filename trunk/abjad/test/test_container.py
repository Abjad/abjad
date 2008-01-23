from abjad import *


### TEST INIT EMPTY CONTAINER ###

def test_empty_container( ):
   t = Container([ ])
   assert repr(t) == '( )'
   assert t.format == ''
   assert len(t) == 0
   assert t._parent == None
   assert t.duration == t.duratum == Duration(0)
   # empty containers are allowed but not well-formed;
   # so we do not check( ) here
   

def test_typical_container( ):
   t = Container(Note(0, (1, 4)) * 4)
   assert repr(t) == "(c'4, c'4, c'4, c'4)"
   assert t.format == "\tc'4\n\tc'4\n\tc'4\n\tc'4"
   assert len(t) == 4
   assert t._parent == None
   assert t.duration == t.duratum == Duration(1)
   assert check(t, ret = True)

