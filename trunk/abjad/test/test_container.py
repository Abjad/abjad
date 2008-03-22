from abjad import *


def test_container_01( ):
   '''Empty container.'''
   t = Container([ ])
   assert repr(t) == '( )'
   assert t.format == ''
   assert len(t) == 0
   assert t._parent == None
   assert t.duration == t.duration.prolated == 0
   # empty containers are allowed but not well-formed;
   # so we do not check( ) here
   

def test_container_02( ):
   '''Typical container.'''
   t = Container(Note(0, (1, 4)) * 4)
   assert repr(t) == "(c'4, c'4, c'4, c'4)"
   assert t.format == "\tc'4\n\tc'4\n\tc'4\n\tc'4"
   assert len(t) == 4
   assert t._parent == None
   assert t.duration == t.duration.prolated == 1
   assert check(t, ret = True)


def test_container_03( ):
   '''Container parallel boolean property.'''
   t = Container(Note(0, (1, 4)) * 8)
   assert not t.parallel
   t.brackets = 'double-angle'
   assert t.parallel
