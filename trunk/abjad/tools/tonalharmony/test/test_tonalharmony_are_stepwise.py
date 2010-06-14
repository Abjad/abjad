from abjad import *


def test_tonalharmony_are_stepwise_01( ):
   '''Notes with the same pitch name are stepwise so long
   as pitch numbers differ.'''

   assert tonalharmony.are_stepwise(Note('c', (1, 4)), Note('cs', (1, 4)))


def test_tonalharmony_are_stepwise_02( ):
   '''Notes with the different pitch name are stepwise so long
   as they differ by exactly one staff space.'''

   assert tonalharmony.are_stepwise(Note('c', (1, 4)), Note('d', (1, 4)))
   assert tonalharmony.are_stepwise(Note('c', (1, 4)), Note('ds', (1, 4)))

   assert tonalharmony.are_stepwise(Note('c', (1, 4)), Note('b,', (1, 4)))
   assert tonalharmony.are_stepwise(Note('c', (1, 4)), Note('bf,', (1, 4)))


def test_tonalharmony_are_stepwise_03( ):
   '''Notes with the same pitch are not stepwise.'''

   assert not tonalharmony.are_stepwise(Note('c', (1, 4)), Note('c', (1, 4)))


def test_tonalharmony_are_stepwise_04( ):
   '''Notes separated by more than 1 staff space are not stepwise.'''

   assert not tonalharmony.are_stepwise(Note('c', (1, 4)), Note('e', (1, 4)))


def test_tonalharmony_are_stepwise_05( ):
   '''Contour changes in note sequence qualifies as tepwise.'''

   notes = leaftools.make_notes([0, 2, 4, 5, 4, 2, 0], [(1, 4)])
   t = Staff(notes)

   assert tonalharmony.are_stepwise(t)
