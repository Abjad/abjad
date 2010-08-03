from abjad.spanners.Hairpin import Hairpin


class Crescendo(Hairpin):
   '''Abjad model of crescendo hairpin.'''

   def __init__(self, music, trim = False):
      Hairpin.__init__(self, music, '<', trim)
