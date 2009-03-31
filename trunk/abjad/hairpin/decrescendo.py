from abjad.hairpin.hairpin import Hairpin


def Decrescendo(music, trim = False):
   return Hairpin(music, '>', trim)
