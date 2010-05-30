from abjad import *
import py.test


def test_containertools_get_index_starting_at_prolated_offset_01( ):

   voice = Voice(construct.scale(8))
   t = containertools.get_index_starting_at_prolated_offset(
      voice, Rational(6, 8))

   assert t == 6


def test_containertools_get_index_starting_at_prolated_offset_02( ):

   voice = Voice(construct.scale(8))

   assert py.test.raises(IndexError, 'containertools.get_index_starting_at_prolated_offset(voice, Rational(15, 8))')
