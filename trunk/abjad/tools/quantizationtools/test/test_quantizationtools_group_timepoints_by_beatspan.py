from random import shuffle
from abjad import Fraction
from abjad.tools.quantizationtools import group_timepoints_by_beatspan


def test_quantizationtools_quantizationtools_group_timepoints_by_beatspan_01( ):
   '''Groups ints.'''
   values = [0, 500, 1000, 1333, 1666, 2000]
   beatspan = 1000
   groups = group_timepoints_by_beatspan(values, beatspan)
   assert groups == {
      0: [0, 500], 
      1: [1000, 1333, 1666], 
      2: [2000]
   }


def test_quantizationtools_quantizationtools_group_timepoints_by_beatspan_02( ):
   '''Input is sorted, then grouped.'''
   values = [0, 500, 1000, 1333, 1666, 2000]
   beatspan = 1000
   for i in range(10):
      shuffle(values)
      groups = group_timepoints_by_beatspan(values, beatspan)   
      assert groups == {
         0: [0, 500],
         1: [1000, 1333, 1666],
         2: [2000]
      }


def test_quantizationtools_quantizationtools_group_timepoints_by_beatspan_03( ):
   '''Handles Fractions.'''
   values = [Fraction(1, 7), Fraction(1, 3), Fraction(8, 11), Fraction(25, 13), Fraction(17, 8)]
   beatspan = Fraction(1, 2)
   groups = group_timepoints_by_beatspan(values, beatspan)
   assert groups == {
      0: [Fraction(1, 7), Fraction(1, 3)],
      1: [Fraction(8, 11)], 
      3: [Fraction(25, 13)],
      4: [Fraction(17, 8)]
   }


def test_quantizationtools_quantizationtools_group_timepoints_by_beatspan_04( ):
   '''Handles grouping iterables with a subscript keyword.'''
   values = [5, 495, 505, 995, 1005, 1333, 1334, 1666, 1667, 1999, 2000, 2251, 2668, 2887]
   values = [(x, 'dummy') for x in values]
   beatspan = 1000
   groups = group_timepoints_by_beatspan(values, beatspan, subscript = 0)
   assert groups == {
      0: [(5, 'dummy'), (495, 'dummy'), (505, 'dummy'), (995, 'dummy')],
      1: [(1005, 'dummy'), (1333, 'dummy'), (1334, 'dummy'), (1666, 'dummy'), (1667, 'dummy'), (1999, 'dummy')],
      2: [(2000, 'dummy'), (2251, 'dummy'), (2668, 'dummy'), (2887, 'dummy')]
   }


def test_quantizationtools_quantizationtools_group_timepoints_by_beatspan_05( ):
   '''Subscripted input is sorted.'''
   values = [0, 500, 1000, 1333, 1666, 2000]
   beatspan = 1000
   for i in range(10):   
      shuffle(values)
      groups = group_timepoints_by_beatspan(values, beatspan)
      assert groups == {
         0: [0, 500],
         1: [1000, 1333, 1666],
         2: [2000]
      }
