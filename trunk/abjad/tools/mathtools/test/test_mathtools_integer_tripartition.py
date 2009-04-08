from abjad import *


def test_mathtools_integer_tripartition_01( ):
   '''Test.'''

   assert mathtools.integer_tripartition(0) == (0, 0, 0)
   assert mathtools.integer_tripartition(1) == (0, 1, 0)
   assert mathtools.integer_tripartition(2) == (1, 0, 1)
   assert mathtools.integer_tripartition(3) == (1, 1, 1)
   assert mathtools.integer_tripartition(4) == (1, 2, 1)
   assert mathtools.integer_tripartition(5) == (2, 1, 2)
   assert mathtools.integer_tripartition(6) == (2, 2, 2)
   assert mathtools.integer_tripartition(7) == (2, 3, 2)
   assert mathtools.integer_tripartition(8) == (3, 2, 3)
   assert mathtools.integer_tripartition(9) == (3, 3, 3)


def test_mathtools_integer_tripartition_02( ):
   '''Smallest part on left.'''

   assert mathtools.integer_tripartition(0, smallest ='left') == (0, 0, 0)
   assert mathtools.integer_tripartition(1, smallest ='left') == (0, 1, 0)
   assert mathtools.integer_tripartition(2, smallest ='left') == (0, 1, 1)
   assert mathtools.integer_tripartition(3, smallest ='left') == (1, 1, 1)
   assert mathtools.integer_tripartition(4, smallest = 'left') == (1, 2, 1)
   assert mathtools.integer_tripartition(5, smallest = 'left') == (1, 2, 2)
   assert mathtools.integer_tripartition(6, smallest = 'left') == (2, 2, 2)
   assert mathtools.integer_tripartition(7, smallest = 'left') == (2, 3, 2)
   assert mathtools.integer_tripartition(8, smallest = 'left') == (2, 3, 3)
   assert mathtools.integer_tripartition(9, smallest = 'left') == (3, 3, 3)


def test_mathtools_integer_tripartition_03( ):
   '''Smallest part on right.'''

   assert mathtools.integer_tripartition(0, smallest = 'right') == (0, 0, 0)
   assert mathtools.integer_tripartition(1, smallest = 'right') == (0, 1, 0)
   assert mathtools.integer_tripartition(2, smallest = 'right') == (1, 1, 0)
   assert mathtools.integer_tripartition(3, smallest = 'right') == (1, 1, 1)
   assert mathtools.integer_tripartition(4, smallest = 'right') == (1, 2, 1)
   assert mathtools.integer_tripartition(5, smallest = 'right') == (2, 2, 1)
   assert mathtools.integer_tripartition(6, smallest = 'right') == (2, 2, 2)
   assert mathtools.integer_tripartition(7, smallest = 'right') == (2, 3, 2)
   assert mathtools.integer_tripartition(8, smallest = 'right') == (3, 3, 2)
   assert mathtools.integer_tripartition(9, smallest = 'right') == (3, 3, 3)


def test_mathtools_integer_tripartition_04( ):
   '''Biggest part on left.'''

   assert mathtools.integer_tripartition(0, biggest = 'left') == (0, 0, 0)
   assert mathtools.integer_tripartition(1, biggest = 'left') == (1, 0, 0)
   assert mathtools.integer_tripartition(2, biggest = 'left') == (1, 0, 1)
   assert mathtools.integer_tripartition(3, biggest = 'left') == (1, 1, 1)
   assert mathtools.integer_tripartition(4, biggest = 'left') == (2, 1, 1)
   assert mathtools.integer_tripartition(5, biggest = 'left') == (2, 1, 2)
   assert mathtools.integer_tripartition(6, biggest = 'left') == (2, 2, 2)
   assert mathtools.integer_tripartition(7, biggest = 'left') == (3, 2, 2)
   assert mathtools.integer_tripartition(8, biggest = 'left') == (3, 2, 3)
   assert mathtools.integer_tripartition(9, biggest = 'left') == (3, 3, 3)


def test_mathtools_integer_tripartition_05( ):
   '''Biggest part on right.'''

   assert mathtools.integer_tripartition(0, biggest = 'right') == (0, 0, 0)
   assert mathtools.integer_tripartition(1, biggest = 'right') == (0, 0, 1)
   assert mathtools.integer_tripartition(2, biggest = 'right') == (1, 0, 1)
   assert mathtools.integer_tripartition(3, biggest = 'right') == (1, 1, 1)
   assert mathtools.integer_tripartition(4, biggest = 'right') == (1, 1, 2)
   assert mathtools.integer_tripartition(5, biggest = 'right') == (2, 1, 2)
   assert mathtools.integer_tripartition(6, biggest = 'right') == (2, 2, 2)
   assert mathtools.integer_tripartition(7, biggest = 'right') == (2, 2, 3)
   assert mathtools.integer_tripartition(8, biggest = 'right') == (3, 2, 3)
   assert mathtools.integer_tripartition(9, biggest = 'right') == (3, 3, 3)
