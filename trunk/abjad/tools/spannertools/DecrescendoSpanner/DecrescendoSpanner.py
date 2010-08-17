from abjad.tools.spannertools.HairpinSpanner import HairpinSpanner


class DecrescendoSpanner(HairpinSpanner):
   '''Decrescendo spanner.'''

   def __init__(self, music, trim = False):
      HairpinSpanner.__init__(self, music, '>', trim)
