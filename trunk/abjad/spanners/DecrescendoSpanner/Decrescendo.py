from abjad.spanners.Hairpin import Hairpin


class Decrescendo(Hairpin):
   '''Decrescendo spanner.'''

   def __init__(self, music, trim = False):
      Hairpin.__init__(self, music, '>', trim)
