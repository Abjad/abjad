from abjad import *


### TEST INIT EMPTY CONTAINER ###

def test_empty_container( ):
   t = Container([ ])
   assert repr(t) == '( )'
   assert t.format == ''
   assert len(t) == 0
   assert t._parent == None
   assert t.duration == t.duration.prolated == 0
   # empty containers are allowed but not well-formed;
   # so we do not check( ) here
   

def test_typical_container( ):
   t = Container(Note(0, (1, 4)) * 4)
   assert repr(t) == "(c'4, c'4, c'4, c'4)"
   assert t.format == "\tc'4\n\tc'4\n\tc'4\n\tc'4"
   assert len(t) == 4
   assert t._parent == None
   assert t.duration == t.duration.prolated == 1
   assert check(t, ret = True)

### TEST CONTENT MODIFYING FUNCTIONS ###

def test_pop_01( ):
   '''Components can be poped. Poped components are fractured correctly.'''
   t = Staff(Voice(Note(0, (1,8)) * 8)* 2)
   Beam(t)
   v = t[1]
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t\\new Voice {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}" 
   '''
   \new Staff {
           \new Voice {
                   c'8 [
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
           }
           \new Voice {
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8 ]
           }
   }
   '''
   assert v.format == "\\new Voice {\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ]\n}"

   '''
   \new Voice {
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8 ]
   }
   '''
   x = t.pop( )
   assert t.format =="\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
   '''
   \new Staff {
           \new Voice {
                   c'8 [
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8 ]
           }
   }
   '''
   assert v.format == "\\new Voice {\n\tc'8 [\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ]\n}"
   '''
   \new Voice {
           c'8 [
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8 ]
   }
   '''
   assert x.format == v.format
   assert x == v
   assert id(x) == id(v)

def test_remove_01( ):
   '''Components can be removed. Spanners are fractured appropriately.'''
   t = Staff(Voice(Note(0, (1,8)) * 8)* 2)
   Beam(t)
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t\\new Voice {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}" 
   '''
   \new Staff {
           \new Voice {
                   c'8 [
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
           }
           \new Voice {
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8 ]
           }
   }
   '''
   t.remove(0)
   assert t.format =="\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
   '''
   \new Staff {
           \new Voice {
                   c'8 [
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8 ]
           }
   }
   '''
