from abjad import *


def test_kind_01( ):
   '''Returns True on exact classnames and all baseclass classnames.'''
   t = Note(0, (1, 4))
   assert not t.kind('Rest')
   assert not t.kind('Chord')
   assert t.kind('Note')
   assert t.kind('Leaf')


def test_kind_02( ):
   '''Accepts tuple to mirror isinstance interface.'''
   t = Note(0, (1, 4))
   assert not t.kind('Rest')
   assert t.kind(('Rest', 'Note'))
