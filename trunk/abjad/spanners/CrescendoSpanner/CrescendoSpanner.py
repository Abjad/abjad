from abjad.spanners.HairpinSpanner import HairpinSpanner


class CrescendoSpanner(Hairpin):
   '''Abjad model of crescendo hairpin.'''

   def __init__(self, music, trim = False):
      HairpinSpanner.__init__(self, music, '<', trim)
