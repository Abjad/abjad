from abjad import *


def test_HistoryInterface_01( ):

   t = Note(0, (1, 4))
   t.history.foo = 'bar'

   assert t.history.foo == 'bar'


def test_HistoryInterface_02( ):

   t = Note(0, (1, 4))
   t.history.foo = 'bar'
   delattr(t.history, 'foo')

   assert not hasattr(t.history, 'foo')

   foo = getattr(t.history, 'foo', 'bar')

   assert foo == 'bar'
