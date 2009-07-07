from abjad.hairpin.spanner import Hairpin


def Crescendo(music, trim = False):
   '''Crescendo spanner.'''

   return Hairpin(music, '<', trim)
