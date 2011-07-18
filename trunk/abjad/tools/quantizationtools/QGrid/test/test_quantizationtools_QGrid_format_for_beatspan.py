from abjad import Fraction
from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid_format_for_beatspan_01( ):

   assert QGrid([0], 0).format_for_beatspan(Fraction(1, 4)).format == \
      "{\n\tc'4\n}"
   assert QGrid([0, 0, 0], 0).format_for_beatspan(Fraction(1, 4)).format == \
      "\\times 2/3 {\n\tc'8\n\tc'8\n\tc'8\n}"
   assert QGrid([0, [0, [0, 0], 0], 0, 0, 0], 0).format_for_beatspan(Fraction(1, 4)).format == \
      "\\times 4/5 {\n\tc'16\n\t\\times 2/3 {\n\t\tc'32\n\t\t{\n\t\t\tc'64\n\t\t\tc'64\n\t\t}\n\t\tc'32\n\t}\n\tc'16\n\tc'16\n\tc'16\n}"
