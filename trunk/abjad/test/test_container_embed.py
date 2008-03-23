from abjad import *

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
