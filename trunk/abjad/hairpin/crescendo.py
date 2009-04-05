from abjad.hairpin.spanner import Hairpin


def Crescendo(music, trim = False):
   return Hairpin(music, '<', trim)
