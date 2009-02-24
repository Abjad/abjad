from abjad.helpers.contiguity import _are_successive_components
from abjad import *


def test_are_successive_components_01( ):
   '''True for list of orphan Abjad components.'''

   t = scale(4)
   assert _are_successive_components(t)


def test_are_successive_components_02( ):
   '''True for list of containerized Abjad components.'''

   t = Staff(scale(4))
   assert _are_successive_components(t[:])


def test_are_successive_components_03( ):
   '''False for scrambled list of containerized Abjad components.'''

   t = Staff(scale(4))
   assert not _are_successive_components(t[2:] + t[:2])


def test_are_successive_components_04( ):
   '''True for empty list.'''

   assert _are_successive_components([ ])


def test_are_successive_components_05( ):
   '''False for lone Abjad component.'''

   assert not _are_successive_components(Note(0, (1, 4)))
   ## TODO: decide whether this should return True or False
   ## assert not _are_successive_components(Staff(scale(4)))


def test_are_successive_components_06( ):
   '''False when any list element is not Abjad component.'''

   t = scale(4)
   t.append('foo')
   assert not _are_successive_components(t)
