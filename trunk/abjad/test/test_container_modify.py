from abjad import *

### TEST CONTENT MODIFYING FUNCTIONS ###

### INSERT ###

# pending... #


### EMBED ### # *insert* without fracturing spanners.

def test_embed_01( ):
   '''Components with one spanner can embed a Leaf. '''
   t = Staff(Note(0, (1, 8)) * 8)
   Beam(t)
   t.embed(2, Rest((1,8)))
   assert check(t, ret = True)
   assert t.format == "\\new Staff {\n\tc'8 [\n\tc'8\n\tr8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ]\n}"
   '''
   \new Staff {
           c'8 [
           c'8
           r8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8 ]
   }
   '''

def test_embed_02( ):
   '''Components with one spanner can embed a container.'''
   t = Staff(Note(0, (1, 8)) * 8)
   Beam(t)
   t.embed(2, Voice(Note(1, (1,16)) * 4))
   assert check(t, ret = True)
   assert t.format =="\\new Staff {\n\tc'8 [\n\tc'8\n\t\\new Voice {\n\t\tcs'16\n\t\tcs'16\n\t\tcs'16\n\t\tcs'16\n\t}\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ]\n}" 
   '''
   \new Staff {
           c'8 [
           c'8
           \new Voice {
                   cs'16
                   cs'16
                   cs'16
                   cs'16
           }
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8 ]
   }
   '''

def test_embed_03( ):
   '''Components with two spanner can embed a Leaf. '''
   t = Staff(Note(0, (1, 8)) * 8)
   Beam(t)
   Trill(t)
   t.embed(2, Rest((1,8)))
   assert check(t, ret = True)
   assert t.format == "\\new Staff {\n\tc'8 [ \\startTrillSpan\n\tc'8\n\tr8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ] \\stopTrillSpan\n}"
   '''
   \new Staff {
           c'8 [ \startTrillSpan
           c'8
           r8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8 ] \stopTrillSpan
   }
   '''

def test_embed_04( ):
   '''Components with two spanners can embed a Container.'''
   t = Staff(Note(0, (1, 8)) * 8)
   Beam(t)
   Trill(t)
   t.embed(2, Voice(Note(1, (1,16)) * 4))
   assert check(t, ret = True)
   assert t.format =="\\new Staff {\n\tc'8 [ \\startTrillSpan\n\tc'8\n\t\\new Voice {\n\t\tcs'16\n\t\tcs'16\n\t\tcs'16\n\t\tcs'16\n\t}\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ] \\stopTrillSpan\n}"
   '''
   \new Staff {
           c'8 [ \startTrillSpan
           c'8
           \new Voice {
                   cs'16
                   cs'16
                   cs'16
                   cs'16
           }
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8 ] \stopTrillSpan
   }
   ''' 
   
### POP ###

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

## REMOVE ##

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
