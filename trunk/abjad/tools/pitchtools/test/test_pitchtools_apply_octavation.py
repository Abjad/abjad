from abjad import *


def test_pitchtools_apply_octavation_01( ):

   t = Staff(leaftools.make_notes([24, 26, 27, 29], [(1, 8)]))
   pitchtools.apply_octavation(t, ottava_altitude = 14)

   r"""\new Staff {
      \ottava #1
      c'''8
      d'''8
      ef'''8
      f'''8
      \ottava #0
   }"""

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\ottava #1\n\tc'''8\n\td'''8\n\tef'''8\n\tf'''8\n\t\\ottava #0\n}"


def test_pitchtools_apply_octavation_02( ):

   t = Voice([Note(31, (1, 4))])
   assert t[0].pitch.altitude == 18
   pitchtools.apply_octavation(t,
      ottava_altitude = 15, quindecisima_altitude = 19)

   r"""
   \new Voice {
      \ottava #1
      g'''4
      \ottava #0
   }
   """

   assert t.format == "\\new Voice {\n\t\\ottava #1\n\tg'''4\n\t\\ottava #0\n}"
