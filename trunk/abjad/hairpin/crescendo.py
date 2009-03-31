from abjad.hairpin.hairpin import Hairpin


def Crescendo(music, trim = False):
   return Hairpin(music, '<', trim)
