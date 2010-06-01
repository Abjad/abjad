from abjad import *


def test_leaftools_change_written_duration_and_preserve_preprolated_duration_01( ):

   n = Note(0, (1, 4))
   leaftools.change_written_duration_and_preserve_preprolated_duration(
      n, Rational(3, 16))
   assert n.format == "c'8. * 4/3"


def test_leaftools_change_written_duration_and_preserve_preprolated_duration_02( ):

   n = Note(0, (1, 4))
   leaftools.change_written_duration_and_preserve_preprolated_duration(
      n, Rational(7, 8))
   assert n.format == "c'2.. * 2/7"


def test_leaftools_change_written_duration_and_preserve_preprolated_duration_03( ):

   n = Note(0, (1, 4))
   leaftools.change_written_duration_and_preserve_preprolated_duration(
      n, Rational(15, 16))
   assert n.format == "c'2... * 4/15"
