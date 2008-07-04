from abjad import *
from abjad.helpers.leaf_scale import leaf_scale_binary


def test_leaf_scale_binary_01( ):
   '''Identity.'''
   t = Note(0, (1, 4))
   leaf_scale_binary((1, 4), t)
   assert isinstance(t, Note)
   assert t.duration == Rational(1, 4)


def test_leaf_scale_binary_02( ):
   '''Binary augmentation.'''
   t = Note(0, (1, 8))
   leaf_scale_binary((1, 4), t)
   assert isinstance(t, Note)
   assert t.duration == Rational(1, 4)


def test_leaf_scale_binary_03( ):
   '''Binary diminution.'''
   t = Note(0, (1, 2))
   leaf_scale_binary((1, 4), t)
   assert isinstance(t, Note)
   assert t.duration == Rational(1, 4)


def test_leaf_scale_binary_04( ):
   '''Target features tied numerator. Leaf is split.'''
   t = Note(0, (1, 4))
   new = leaf_scale_binary((5, 16), t)
   assert isinstance(new, list)
   assert t.duration == Rational(4, 16)
   assert new[0].duration == Rational(4, 16)
   assert new[0].tie == True
   assert new[1].duration == Rational(1, 16)
   assert new[1].tie == False


def test_leaf_scale_binary_05( ):
   '''Target features D2 numerator. Leaf is split.'''
   t = Note(0, (1, 4))
   new = leaf_scale_binary((3, 16), t)
   assert isinstance(t, Note)
   assert t.duration == Rational(3, 16)
   assert t.tie == False
   assert isinstance(new, Note)
   assert new.duration == Rational(3, 16)
   assert new.tie == False


def test_leaf_scale_binary_10( ):
   '''Target is alone in Voice container.'''
   t = Voice([Note(0, (1, 4))])
   leaf_scale_binary((5,16), t[0])
   assert len(t) == 2
   assert t[0].duration == Rational(1, 4)
   assert t[1].duration == Rational(1, 16)


