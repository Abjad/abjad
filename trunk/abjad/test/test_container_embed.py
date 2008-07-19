from abjad import *
from py.test import raises

### EMBED ### # *insert* without fracturing spanners.

def test_embed_01( ):
   '''Containers with one spanner can embed a Leaf. '''
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
   '''Containers with one spanner can embed a container.'''
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
   '''Containers with two parallel spanners can embed a Leaf. '''
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
   '''Containers with two parallel spanners can embed a Container.'''
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
   '''Containers with a spanner can embed a list of Components.'''
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

def test_embed_06( ):
   '''Containers with two sequential spanners can embed a Leaf.'''
   t = Staff(Note(0, (1, 8)) * 8)
   b1 = Beam(t[0:4])
   b2 = Beam(t[4:])
   t.embed(2, Rest((1,8)))
   assert set(b1._leaves).intersection(b2._leaves) == set([ ])
   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 [\n\tc'8\n\tr8\n\tc'8\n\tc'8 ]\n\tc'8 [\n\tc'8\n\tc'8\n\tc'8 ]\n}"

   '''
   \new Staff {
        c'8 [
        c'8
        r8
        c'8
        c'8 ]
        c'8 [
        c'8
        c'8
        c'8 ]
   }
   '''
 
def test_embed_08( ):
   '''Containers with two sequential spanners in parallel with a
   third spanner can embed a Leaf.'''
   t = FixedDurationTuplet((2, 4), [Note(n, (1, 8)) for n in range(6, 12)])
   v = Voice([Note(n, (1, 8)) for n in range(6)])
   v.append(t)
   Beam(v)
   v.spanners.get()[0].fracture(4, 'right')
   Trill(v)
   v.embed(3, Rest((1,32)))
   assert check(v)
   assert v.format =="\\new Voice {\n\tc'8 [ \\startTrillSpan\n\tcs'8\n\td'8\n\tr32\n\tef'8\n\te'8 ]\n\tf'8 [\n\t\\times 2/3 {\n\t\tfs'8\n\t\tg'8\n\t\taf'8\n\t\ta'8\n\t\tbf'8\n\t\tb'8 ] \\stopTrillSpan\n\t}\n}"
 
   '''
   \new Voice {
           c'8 [ \startTrillSpan
           cs'8
           d'8
           r32
           ef'8
           e'8 ]
           f'8 [
           \times 2/3 {
                   fs'8
                   g'8
                   af'8
                   a'8
                   bf'8
                   b'8 ] \stopTrillSpan
           }
   }
'''

def test_embed_09( ):
   '''Embed complains on out of bounds indeces.'''
   t = Staff(Note(0, (1, 8)) * 8)
   Beam(t)
   assert raises(IndexError, 't.embed(8, Note(1, (1,4)))')
   assert raises(IndexError, 't.embed(-9, Note(1, (1,4)))')

def test_embed_10( ):
   '''Embed complains on empty Container.'''
   t = Staff([ ])
   Beam(t)
   assert raises(IndexError, 't.embed(0, Note(1, (1,4)))')
   assert raises(IndexError, 't.embed(-1, Note(1, (1,4)))')
