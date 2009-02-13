from abjad.helpers.agglomerate_durations_by_prolation import _agglomerate_durations_by_prolation
from py.test import raises

def test_agglomerate_durations_by_prolations_01( ):
   assert raises(AssertionError, '_agglomerate_durations_by_prolation([ ])')

def test_agglomerate_durations_by_prolations_02( ):
   t = _agglomerate_durations_by_prolation([(1, 4)])
   assert t == [[(1, 4)]]

def test_agglomerate_durations_by_prolations_03( ):
   t = _agglomerate_durations_by_prolation([(1, 4), (1, 4), (1, 8)])
   assert t == [[(1, 4), (1, 4), (1, 8)]]

def test_agglomerate_durations_by_prolations_04( ):
   t = _agglomerate_durations_by_prolation([(1, 4), (1, 3), (1, 8)])
   assert t == [[(1, 4)], [(1, 3)], [(1, 8)]]

def test_agglomerate_durations_by_prolations_05( ):
   t = _agglomerate_durations_by_prolation([(1, 4), (1, 2), (1, 3)])
   assert t == [[(1, 4), (1, 2)], [(1, 3)]]

def test_agglomerate_durations_by_prolations_06( ):
   t = _agglomerate_durations_by_prolation([(1, 4), (1, 2), (1, 3), (1, 6), 
      (1, 5)])
   assert t == [[(1, 4), (1, 2)], [(1, 3), (1, 6)], [(1, 5)]]

def test_agglomerate_durations_by_prolations_07( ):
   t = _agglomerate_durations_by_prolation([(1, 24), (2, 24), (3, 24), 
      (4, 24), (5, 24), (6, 24)])
   assert t == [[(1, 24), (2, 24), (3, 24), (4, 24), (5, 24), (6, 24)]]
