from abjad.tools.spannertools.HairpinSpanner import HairpinSpanner


class CrescendoSpanner(HairpinSpanner):
   '''Abjad model of crescendo hairpin.'''

   def __init__(self, music, trim = False):
      HairpinSpanner.__init__(self, music, '<', trim)
