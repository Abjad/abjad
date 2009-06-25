from abjad import *


def test_pitchtools_apply_octavation_01( ):

   t = Staff(construct.notes([24, 26, 27, 29], [(1, 8)]))
   pitchtools.apply_octavation(t, ottava_altitude = 14)

   r"""\new Staff {
      \ottava #1
      c'''8
      d'''8
      ef'''8
      f'''8
      \ottava #0
   }"""

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\ottava #1\n\tc'''8\n\td'''8\n\tef'''8\n\tf'''8\n\t\\ottava #0\n}"
