from abjad import *
from abjad.helpers.leaf_scale import leaf_scale_binary


def test_leaf_scale_binary_01( ):
   '''Identity.'''
   t = Note(0, (1, 4))
   new = leaf_scale_binary((1, 4), t)
   assert isinstance(new, list)
   assert isinstance(new[0], Note)
   assert new[0] is t
   assert new[0].duration == Rational(1, 4)
   assert not new[0].tie.isTied( )


def test_leaf_scale_binary_02( ):
   '''Binary augmentation.'''
   t = Note(0, (1, 8))
   new = leaf_scale_binary((1, 4), t)
   assert isinstance(new, list)
   assert isinstance(new[0], Note)
   assert new[0] is t
   assert new[0].duration == Rational(1, 4)
   assert not new[0].tie.isTied( )


def test_leaf_scale_binary_03( ):
   '''Binary diminution.'''
   t = Note(0, (1, 2))
   new = leaf_scale_binary((1, 4), t)
   assert isinstance(new, list)
   assert isinstance(new[0], Note)
   assert new[0] is t
   assert new[0].duration == Rational(1, 4)
   assert not new[0].tie.isTied( )


def test_leaf_scale_binary_04( ):
   '''Target features tied numerator. Leaf is split.'''
   t = Note(0, (1, 4))
   new = leaf_scale_binary((5, 16), t)
   assert isinstance(new, list)
   assert len(new) == 2
   assert isinstance(new[0], Note)
   assert isinstance(new[1], Note)
   assert not new[0] is t
   assert not new[1] is t
   assert new[0].duration == Rational(4, 16)
   assert new[0].tie.isTied( )
   assert not new[0].tie
   assert new[0].tie.spanner
   assert new[1].duration == Rational(1, 16)
   assert new[1].tie.isTied( )
   assert not new[1].tie
   assert new[1].tie.spanner


def test_leaf_scale_binary_05( ):
   '''Target features dotted numerator. Leaf is split.'''
   t = Note(0, (1, 4))
   new = leaf_scale_binary((3, 16), t)
   assert isinstance(new, list)
   assert len(new) == 1
   assert isinstance(new[0], Note)
   assert new[0].duration == Rational(3, 16)
   assert not new[0].tie.isTied( )


def test_leaf_scale_binary_10( ):
   '''Target is alone in Voice container.'''
   t = Voice([Note(0, (1, 4))])
   new = leaf_scale_binary((5,16), t[0])
   assert len(t) == 2
   assert len(new) == 2
   assert new[0] is t[0]
   assert new[1] is t[1]
   assert t[0].duration == Rational(1, 4)
   assert t[1].duration == Rational(1, 16)
   assert t[0].tie.isTied( )
   assert not t[0].tie
   assert t[0].tie.spanner
   assert t[1].tie.isTied( )
   assert not t[1].tie
   assert t[1].tie.spanner


### IN CONTEXT ###

def test_leaf_scale_binary_11( ):
   '''Tied leaf is not tied again in splitting.'''
   t = Voice([Note(0, (1, 4))])
   Tie(t)
   assert t[0].tie.isTied( )
   new = leaf_scale_binary((5,16), t[0])
   assert len(t) == 2
   assert len(new) == 2
   assert new[0] is t[0]
   assert new[1] is t[1]
   assert t[0].duration == Rational(1, 4)
   assert t[1].duration == Rational(1, 16)
   assert t[0].tie.isTied( )
   assert not t[0].tie
   assert len(t[0].tie.spanners) == 1
   assert t[1].tie.isTied( )
   assert not t[1].tie
   assert len(t[1].tie.spanners) == 1


def test_leaf_scale_binary_12( ):
   '''spanner-Tied leaf is not tied again in splitting.'''
   t = Voice([Note(0, (1, 4))])
   Tie(t)
   assert t[0].tie.isTied( )
   new = leaf_scale_binary((5,16), t[0])
   assert len(t) == 2
   assert len(new) == 2
   assert new[0] is t[0]
   assert new[1] is t[1]
   assert t[0].duration == Rational(1, 4)
   assert t[1].duration == Rational(1, 16)
   assert t[0].tie.isTied( )
   assert not t[0].tie
   assert len(t[0].tie.spanners) == 1
   assert t[1].tie.isTied( )
   assert not t[1].tie
   assert len(t[1].tie.spanners) == 1


def test_leaf_scale_binary_13( ):
   '''leaf-Tied leaf is not tied again in splitting.'''
   t = Voice([Note(0, (1, 4))])
   t[0].tie = True
   assert t[0].tie.isTied( )
   new = leaf_scale_binary((5,16), t[0])
   assert len(t) == 2
   assert len(new) == 2
   assert new[0] is t[0]
   assert new[1] is t[1]
   assert t[0].duration == Rational(1, 4)
   assert t[1].duration == Rational(1, 16)
   assert t[0].tie.isTied( )
   assert not t[0].tie
   assert len(t[0].tie.spanners) == 1
   assert t[1].tie.isTied( )
   assert not t[1].tie
   assert len(t[1].tie.spanners) == 1


