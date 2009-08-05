from abjad import *
import py.test


def test_durtools_agglomerate_by_prolations_01( ):
   assert py.test.raises(
      AssertionError, 'durtools.agglomerate_by_prolation([ ])')


def test_durtools_agglomerate_by_prolations_02( ):
   t = durtools.agglomerate_by_prolation([(1, 4)])
   assert t == [[(1, 4)]]


def test_durtools_agglomerate_by_prolations_03( ):
   t = durtools.agglomerate_by_prolation([(1, 4), (1, 4), (1, 8)])
   assert t == [[(1, 4), (1, 4), (1, 8)]]


def test_durtools_agglomerate_by_prolations_04( ):
   t = durtools.agglomerate_by_prolation([(1, 4), (1, 3), (1, 8)])
   assert t == [[(1, 4)], [(1, 3)], [(1, 8)]]


def test_durtools_agglomerate_by_prolations_05( ):
   t = durtools.agglomerate_by_prolation([(1, 4), (1, 2), (1, 3)])
   assert t == [[(1, 4), (1, 2)], [(1, 3)]]


def test_durtools_agglomerate_by_prolations_06( ):
   t = durtools.agglomerate_by_prolation([(1, 4), (1, 2), (1, 3), (1, 6), 
      (1, 5)])
   assert t == [[(1, 4), (1, 2)], [(1, 3), (1, 6)], [(1, 5)]]


def test_durtools_agglomerate_by_prolations_07( ):
   t = durtools.agglomerate_by_prolation([(1, 24), (2, 24), (3, 24), 
      (4, 24), (5, 24), (6, 24)])
   assert t == [[(1, 24), (2, 24), (3, 24), (4, 24), (5, 24), (6, 24)]]
