from abjad import *


def test_seqtools_repeat_sequence_to_weight_01( ):
   '''Repeat l until mathtools.weight(l) equals weight.'''

   l = [5, 5, 5]
   t = seqtools.repeat_sequence_to_weight(l, 23)

   assert t == [5, 5, 5, 5, 3]


def test_seqtools_repeat_sequence_to_weight_02( ):
   '''When remainder = less allow mathtools.weight(result)
      to be less than or equal to weight.'''

   l = [5, 5, 5]
   t = seqtools.repeat_sequence_to_weight(l, 23, remainder = 'less')

   assert t == [5, 5, 5, 5]


def test_seqtools_repeat_sequence_to_weight_03( ):
   '''When remainder = more allow mathtools.weight(result)
      to be greater than or equal to weight.'''

   l = [5, 5, 5]
   t = seqtools.repeat_sequence_to_weight(l, 23, remainder = 'more')

   assert t == [5, 5, 5, 5, 5]


def test_seqtools_repeat_sequence_to_weight_04( ):
   '''Weight is the sum of the absolute value of elements in list.'''

   l = [-5, -5, 5]
   t = seqtools.repeat_sequence_to_weight(l, 23)

   assert t == [-5, -5, 5, -5, -3]
