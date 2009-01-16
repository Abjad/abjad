from abjad import *
from py.test import raises


### SPANNERS ATTACH TO LEAVES ### 

def test_embed_01( ):
   '''
   Containers can embed a Leaf to index position 0. 
   Components embeded at index 0 are not attached to spanners.
   '''
   t = Staff(run(4))
   b = Beam(t.leaves)
   t.embed(0, Note(1, (1, 8)))
   assert len(t) == 5
   assert not t[0] in b.components 
   for child in t:
      assert child._parent is t

   
def test_embed_02( ):
   '''
   Containers can embed with negative indeces.
   '''
   t = Staff(run(4))
   b = Beam(t.leaves)
   t.embed(-1, Note(1, (1, 8)))
   assert len(t) == 5
   for child in t:
      assert child._parent is t
      assert child.beam.spanner is b


def test_embed_03( ):
   '''
   Containers can embed another Container.
   '''
   t = Staff(run(4))
   b = Beam(t.leaves)
   v = Voice(run(2))
   t.embed(2, v)
   assert len(t) == 5
   for child in t:
      assert child._parent is t
      assert child.beam.spanner is b


def test_embed_04( ):
   '''
   Containers can embed a list of Components.
   '''
   t = Staff(run(4))
   b = Beam(t.leaves)
   v = Voice(run(2))
   n = Note(1, (1, 8))
   t.embed(2, [v, n])
   assert len(t) == 6
   for child in t:
      assert child._parent is t
      assert child.beam.spanner is b
   for leaf in v:
      assert not leaf.spanners.attached


def test_embed_05( ):
   '''
   Spanners not spanning embedding index are unaffected.
   '''
   t = Staff(run(4))
   b1 = Beam(t.leaves[0:2])
   b2 = Beam(t.leaves[2:])
   v = Voice(run(2))
   t.embed(2, v)
   assert len(t) == 5
   assert not v.spanners.attached
   for leaf in v:
      assert not leaf.spanners.attached
   assert b1.components == t[0:2]
   assert b2.components == t[3:]


def test_embed_06( ):
   '''
   Spanners not spanning embedding index are unaffected.
   Spanners spanning embedding index are affected.
   '''
   t = Staff(run(4))
   b1 = Beam(t.leaves[0:2])
   b2 = Beam(t.leaves[2:])
   tr = Trill(t.leaves)
   v = Voice(run(2))
   t.embed(2, v)
   assert len(t) == 5
   assert v.spanners.attached == set([tr])
   for child in t:
      assert child in tr.components
   for leaf in v:
      assert not leaf.spanners.attached
   assert b1.components == t[0:2]
   assert b2.components == t[3:]


def test_embed_07( ):
   '''Containers with two parallel spanners can embed a Container.'''
   t = Staff(run(4))
   b = Beam(t.leaves)
   tr= Trill(t.leaves)
   t.embed(2, Voice(run(2)))
   assert len(t) == 5
   for child in t:
      assert child._parent is t
      assert child.spanners.attached == set([b, tr])
   assert isinstance(t[2], Voice)
   for leaf in t[2]:
      assert not leaf.spanners.attached


### SPANNERS ATTACH TO CONTAINERS ### 

def test_embed_10( ):
   '''
   Containers can embed a Leaf.
   '''
   t = Staff(run(4))
   b = Beam(t)
   n = Note(1, (1, 8))
   t.embed(2, n)
   assert len(t) == 5
   assert b.components == [t]
   for child in t:
      assert child._parent is t
      assert not child.spanners.attached 


def test_embed_11( ):
   '''
   Containers can embed a Container.
   '''
   t = Staff(run(4))
   b = Beam(t)
   v = Voice(run(2))
   t.embed(2, v)
   assert len(t) == 5
   assert b.components == [t]
   for child in t:
      assert child._parent is t
      assert not child.spanners.attached 
   for leaf in v:
      assert not leaf.spanners.attached


def test_embed_12( ):
   '''
   Containers can embed a list of Components.
   '''
   t = Staff(run(4))
   b = Beam(t)
   v = Voice(run(2))
   n = Note(1, (1, 8))
   t.embed(2, [v, n])
   assert len(t) == 6
   for child in t:
      assert child._parent is t
      assert not child.spanners.attached
   for leaf in v:
      assert not leaf.spanners.attached


def test_embed_13( ):
   '''
   Spanners not spanning embedding index are unaffected.
   '''
   t = Staff(Voice(run(2)) * 2)
   b1 = Beam(t[0])
   b2 = Beam(t[1])
   t.embed(1, Rest((1, 16)))
   assert len(t) == 3
   for child in t:
      assert child._parent is t
   assert isinstance(t[1], Rest)
   assert not t[1].spanners.attached 
   assert b1.components == [t[0]]
   assert b2.components == [t[2]]


### SPANNERS ATTACH TO LEAVES AND CONTAINERS ###

def test_embed_20( ):
   '''Embedding works on spanners spanning leaves and containers.'''
   t = Staff(run(4))
   b = Beam(t.leaves)
   tr = Trill(t)
   t.embed(2, Rest((1,8)))
   assert len(t) == 5
   for child in t:
      assert child._parent is t
   for leaf in t:
      assert leaf.spanners.attached == set([b])
   assert tr.components == [t]
   


### EXCEPTIONS ###

def test_embed_30( ):
   '''Embed complains on out of bounds indeces.'''
   t = Staff(Note(0, (1, 8)) * 8)
   #Beam(t)
   Beam(t[ : ])
   assert raises(IndexError, 't.embed(8, Note(1, (1,4)))')
   assert raises(IndexError, 't.embed(-9, Note(1, (1,4)))')
