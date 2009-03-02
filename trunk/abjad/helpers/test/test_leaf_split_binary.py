from abjad import *


def test_leaf_split_binary_01( ):
   '''Split duration equals 0. Leaf is left unmodified.'''
   t = Note(0, (1, 4))
   new = leaf_split_binary(0, t)
   assert isinstance(new, list)
   assert len(new) == 1
   assert new[0] is t
   assert isinstance(new[0], Note)
   assert new[0].duration.written == Rational(1, 4)
   assert new[0] == t


def test_leaf_split_binary_02( ):
   '''Split duration >= Leaf duration. Leaf is left unmodified.'''
   t = Note(0, (1, 4))
   new = leaf_split_binary((3, 4), t)
   assert isinstance(new, list)
   assert len(new) == 1
   assert isinstance(new[0], Note)
   assert new[0].duration.written == Rational(1, 4)
   assert new[0] == t


def test_leaf_split_binary_03( ):
   '''Split returns two Leaves.'''
   t = Note(0, (1, 4))
   new = leaf_split_binary((1, 8), t)
   assert isinstance(new, list)
   assert len(new) == 2
   assert len(new[0]) == 1
   assert len(new[1]) == 1
   assert not new[0][0] is t
   assert new[1][0] is t  ### hmmm, is this what we want? does it matter?
   assert isinstance(new[0][0], Note)
   assert new[0][0].duration.written == Rational(1, 8)
   assert not new[0][0].tie.spanned
   assert isinstance(new[1][0], Note)
   assert new[1][0].duration.written == Rational(1, 8)
   assert not new[1][0].tie.spanned


def test_leaf_split_binary_04( ):
   '''Split returns two Leaves.'''
   t = Note(0, (1, 4))
   new = leaf_split_binary((1, 16), t)
   assert isinstance(new, list)
   assert len(new) == 2
   assert len(new[0]) == 1
   assert len(new[1]) == 1
   assert isinstance(new[0][0], Note)
   assert new[0][0].duration.written == Rational(1, 16)
   assert isinstance(new[1][0], Note)
   assert new[1][0].duration.written == Rational(3, 16)


def test_leaf_split_binary_05( ):
   '''Split returns three Leaves, two are tied.'''
   t = Note(0, (1, 4))
   new = leaf_split_binary((5, 32), t)
   assert isinstance(new, list)
   assert len(new) == 2
   assert len(new[0]) == 2
   assert len(new[1]) == 1
   assert isinstance(new[0], list)
   assert isinstance(new[0][0], Note)
   assert new[0][0].duration.written == Rational(4, 32)
   assert new[0][0].tie.spanned
   #assert not new[0][0].tie
   assert new[0][1].duration.written == Rational(1, 32)
   assert new[0][1].tie.spanned
   #assert not new[0][1].tie
   assert isinstance(new[1], list)
   assert isinstance(new[1][0], Note)
   assert new[1][0].duration.written == Rational(3, 32)
   assert not new[1][0].tie.spanned

### IN CONTEXT ###

def test_leaf_split_binary_06( ):
   '''Pre-tied leaves are kept tied after splitting and are not doubly tied.'''
   t = Staff([Note(0, (1, 4))])
   #Tie(t)
   Tie(t.leaves)
   new = leaf_split_binary((5, 32), t[0])
   assert isinstance(new, list)
   assert len(new) == 2
   assert len(new[0]) == 2
   assert len(new[1]) == 1
   assert isinstance(new[0], list)
   assert isinstance(new[0][0], Note)
   assert new[0][0].duration.written == Rational(4, 32)
   assert new[0][0].tie.spanned
   assert len(new[0][0].tie.spanners) == 1
   #assert not new[0][0].tie
   assert new[0][1].duration.written == Rational(1, 32)
   assert new[0][1].tie.spanned
   assert len(new[0][1].tie.spanners) == 1
   #assert not new[0][1].tie
   assert isinstance(new[1], list)
   assert isinstance(new[1][0], Note)
   assert new[1][0].duration.written == Rational(3, 32)
   assert len(new[1][0].tie.spanners) == 1
   #assert not new[1][0].tie

### LEAF SPANNED ###

def test_leaf_split_binary_10( ):
   '''Lone spanned Leaf results in two spanned leaves.'''
   t = Staff([Note(0, (1, 4))])
   s = Tie(t.leaves)
   new = leaf_split_binary((1, 8), t[0])
   assert len(t) == 2
   for leaf in t.leaves:
      assert leaf.spanners.attached == set([s])
      assert leaf.tie.spanner is s
      assert leaf._parent is t
   assert check(t)


def test_leaf_split_binary_11( ):
   '''Spanners are unaffected by leaf split.'''
   t = Staff(run(4))
   b = Beam(t.leaves)
   new = leaf_split_binary((5, 32), t[0])
   for l in t.leaves:
      assert l.spanners.attached == set([b])
      assert l.beam.spanner is b
      assert l._parent is t
   assert check(t)


def test_leaf_split_binary_12( ):
   '''
   Split returns three Leaves, two are tied.
   Spanner is shared by all 3 leaves.
   '''
   t = Staff([Note(0, (1, 4))])
   s = Tie(t.leaves)
   new = leaf_split_binary((5, 32), t[0])
   assert len(new) == 2
   assert len(new[0]) == 2
   assert len(new[1]) == 1
   for l in t.leaves:
      assert l.spanners.attached == set([s])
      assert l.tie.spanner is s
      assert l._parent is t
   assert check(t)
   
### CONTAINER SPANNED ###

def test_leaf_split_binary_20( ):
   '''
   Split leaf is not tied again when a Container containing it is 
   already Tie-spanned.
   '''
   t = Staff(run(4))
   b = Beam(t)
   new = leaf_split_binary((5, 32), t[0])
   assert t.beam.spanner is b
   assert b.components == [t]
   for l in t.leaves:
      assert not l.spanners.attached 
      assert l._parent is t
   assert check(t)


def test_leaf_split_binary_21( ):
   '''
   Split leaf is not tied again when a Container containing it is 
   already Tie-spanned.
   '''
   t = Staff(Voice(run(4)) * 2)
   b = Beam(t[:])
   new = leaf_split_binary((5, 32), t[0][0])
   assert b.components == t[:]
   for v in t:
      assert v.spanners.attached == set([b])
      for l in v.leaves:
         assert not l.spanners.attached 
         assert l._parent is v
   assert check(t)

### GRACE NOTES ###

def test_leaf_split_binary_30( ):
   '''After grace notes are removed from first leaf in bipartition.'''
   t = Note(0, (1, 4))
   t.grace.after = Note(0, (1, 32))
   new = leaf_split_binary((1, 8), t)
   assert len(new[0][0].grace.after) == 0
   assert len(new[1][0].grace.after) == 1


def test_leaf_split_binary_31( ):
   '''After grace notes are removed from first tied leaves in bipartition.'''
   t = Note(0, (1, 4))
   t.grace.after = Note(0, (1, 32))
   new = leaf_split_binary((5, 32), t)
   assert len(new[0]) == 2
   assert len(new[0][0].grace.after) == 0
   assert len(new[0][1].grace.after) == 0
   assert len(new[1]) == 1
   assert len(new[1][0].grace.after) == 1


def test_leaf_split_binary_32( ):
   '''Grace notes are removed from second leaf in bipartition.'''
   t = Note(0, (1, 4))
   t.grace.before = Note(0, (1, 32))
   new = leaf_split_binary((1, 8), t)
   assert len(new[0]) == 1
   assert len(new[1]) == 1
   assert len(new[0][0].grace.before) == 1
   assert len(new[1][0].grace.before) == 0
