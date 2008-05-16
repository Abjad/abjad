from abjad import *

### EMBED ### # *insert* without fracturing spanners.

def test_embed_01( ):
   '''Components with one spanner can embed a Leaf. '''
   t = Staff(Note(0, (1, 8)) * 8)
   Beam(t)
   t.embed(2, Rest((1,8)))
   assert check(t)
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
   assert check(t)
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
   assert check(t)
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
   assert check(t)
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

def test_embed_05( ):
   '''Components with a spanner can embed a list of Components.'''
   t = Staff(Note(0, (1, 8)) * 8)
   Beam(t)
   t.embed(2, [Note(i, (1,32)) for i in range(4)])
   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 [\n\tc'8\n\tc'32\n\tcs'32\n\td'32\n\tef'32\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ]\n}"
   '''
   \new Staff {
        c'8 [
        c'8
        c'32
        cs'32
        d'32
        ef'32
        c'8
        c'8
        c'8
        c'8
        c'8
        c'8 ]
   }
   ''' 
