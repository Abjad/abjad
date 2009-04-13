from abjad import *
import py.test


def test_leaftools_scale_binary_01( ):
   '''Identity.'''

   t = Note(0, (1, 4))
   new = leaftools.scale_binary(t, Rational(1, 4))

   assert isinstance(new, list)
   assert isinstance(new[0], Note)
   assert new[0] is t
   assert new[0].duration.written == Rational(1, 4)
   assert not new[0].tie.spanned


def test_leaftools_scale_binary_02( ):
   '''Binary augmentation.'''

   t = Note(0, (1, 8))
   new = leaftools.scale_binary(t, Rational(1, 4))

   assert isinstance(new, list)
   assert isinstance(new[0], Note)
   assert new[0] is t
   assert new[0].duration.written == Rational(1, 4)
   assert not new[0].tie.spanned


def test_leaftools_scale_binary_03( ):
   '''Binary diminution.'''

   t = Note(0, (1, 2))
   new = leaftools.scale_binary(t, Rational(1, 4))

   assert isinstance(new, list)
   assert isinstance(new[0], Note)
   assert new[0] is t
   assert new[0].duration.written == Rational(1, 4)
   assert not new[0].tie.spanned


def test_leaftools_scale_binary_04( ):
   '''Target features tied numerator. Leaf is split.'''

   t = Note(0, (1, 4))
   new = leaftools.scale_binary(t, Rational(5, 16))

   assert isinstance(new, list)
   assert len(new) == 2
   assert isinstance(new[0], Note)
   assert isinstance(new[1], Note)
   assert not new[0] is t
   assert not new[1] is t
   assert new[0].duration.written == Rational(4, 16)
   assert new[0].tie.spanned
   assert new[1].duration.written == Rational(1, 16)
   assert new[1].tie.spanned


def test_leaftools_scale_binary_05( ):
   '''Target features dotted numerator. Leaf is not split.'''

   t = Note(0, (1, 4))
   new = leaftools.scale_binary(t, Rational(3, 16))

   assert isinstance(new, list)
   assert len(new) == 1
   assert isinstance(new[0], Note)
   assert new[0].duration.written == Rational(3, 16)
   assert not new[0].tie.spanned


def test_leaftools_scale_binary_06( ):
   '''Target is alone in Voice container.'''

   t = Voice([Note(0, (1, 4))])
   new = leaftools.scale_binary(t[0], Rational(5, 16))
   assert len(t) == 2
   assert len(new) == 2
   assert new[0] is t[0]
   assert new[1] is t[1]
   assert t[0].duration.written == Rational(1, 4)
   assert t[1].duration.written == Rational(1, 16)
   assert t[0].tie.spanned
   assert t[1].tie.spanned


## IN CONTEXT ##

def test_leaftools_scale_binary_11( ):
   '''Tied leaf is not tied again in splitting.'''

   t = Voice([Note(0, (1, 4))])
   Tie(t.leaves)
   assert t[0].tie.spanned

   new = leaftools.scale_binary(t[0], Rational(5, 16))
   assert len(t) == 2
   assert len(new) == 2
   assert new[0] is t[0]
   assert new[1] is t[1]
   assert t[0].duration.written == Rational(1, 4)
   assert t[1].duration.written == Rational(1, 16)
   assert t[0].tie.spanned
   assert len(t[0].tie.spanners) == 1
   assert t[1].tie.spanned
   assert len(t[1].tie.spanners) == 1


def test_leaftools_scale_binary_12( ):
   '''spanner-Tied leaf is not tied again in splitting.'''

   t = Voice([Note(0, (1, 4))])
   Tie(t.leaves)
   assert t[0].tie.spanned

   new = leaftools.scale_binary(t[0], Rational(5, 16))
   assert len(t) == 2
   assert len(new) == 2
   assert new[0] is t[0]
   assert new[1] is t[1]
   assert t[0].duration.written == Rational(1, 4)
   assert t[1].duration.written == Rational(1, 16)
   assert t[0].tie.spanned
   assert len(t[0].tie.spanners) == 1
   assert t[1].tie.spanned
   assert len(t[1].tie.spanners) == 1


def test_leaftools_scale_binary_13( ):
   '''leaf-Tied leaf is not tied again in splitting.'''

   t = Voice([Note(0, (1, 4))])
   new = leaftools.scale_binary(t[0], Rational(5, 16))

   assert len(t) == 2
   assert len(new) == 2
   assert new[0] is t[0]
   assert new[1] is t[1]
   assert t[0].duration.written == Rational(1, 4)
   assert t[1].duration.written == Rational(1, 16)
   assert t[0].tie.spanned
   assert len(t[0].tie.spanners) == 1
   assert t[1].tie.spanned
   assert len(t[1].tie.spanners) == 1


## GRACE NOTES ##

def test_leaftools_scale_binary_20( ):
   '''Grace notes are removed from all but the first leaf.'''

   t = Note(0, (1, 4))
   t.grace.before = Note(1, (1, 64))
   new = leaftools.scale_binary(t, Rational(5, 16))

   assert len(new) == 2
   assert len(new[0].grace.before) == 1
   assert len(new[1].grace.before) == 0


def test_leaftools_scale_binary_21( ):
   '''AfterGrace notes are removed from all but the last leaf.'''

   t = Note(0, (1, 4))
   t.grace.after = Note(1, (1, 64))
   new = leaftools.scale_binary(t, Rational(5, 16))

   assert len(new) == 2
   assert len(new[0].grace.after) == 0
   assert len(new[1].grace.after) == 1


## SPANNED (LEAF ATTACHMENT) ##

def test_leaftools_scale_binary_30( ):

   t = Staff([Note(0, (1, 4))])
   s = Tie(t.leaves)
   new = leaftools.scale_binary(t[0], Rational(1, 16))

   assert len(t) == 1
   assert t[0].spanners.attached == set([s])
   assert s.components == [t[0]]


def test_leaftools_scale_binary_31( ):

   t = Staff(run(4))
   s = Tie(t.leaves)
   new = leaftools.scale_binary(t[0], Rational(1, 16))

   assert len(t) == 4
   assert s.components == t.leaves
   for leaf in t.leaves:
      assert leaf.spanners.attached == set([s])


def test_leaftools_scale_binary_32( ):

   t = Staff([Note(0, (1, 4))])
   s = Tie(t.leaves)
   new = leaftools.scale_binary(t[0], Rational(5, 16))

   assert len(t) == 2
   assert s.components == t.leaves
   for leaf in t.leaves:
      assert leaf.spanners.attached == set([s])


def test_leaftools_scale_binary_33( ):

   t = Staff(run(4))
   s = Tie(t.leaves)
   new = leaftools.scale_binary(t[0], Rational(5, 32))

   assert len(t) == 5
   assert s.components == t.leaves
   for leaf in t.leaves:
      assert leaf.spanners.attached == set([s])


## SPANNED (CONTAINER ATTACHMENT) ##

def test_leaftools_scale_binary_40( ):

   t = Staff(Voice(run(2)) * 2)
   s = py.test.raises(ContiguityError, 'Tie(t[:])')
   t = Staff(Container(run(2)) * 2)
   s = Tie(t[:])
   new = leaftools.scale_binary(t[0][0], Rational(5, 32))

   assert len(t) == 2
   assert s.components == t[:]
   for leaf in t.leaves:
      assert not leaf.spanners.attached
