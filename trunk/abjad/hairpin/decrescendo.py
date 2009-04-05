from abjad.hairpin.spanner import Hairpin


def Decrescendo(music, trim = False):
   return Hairpin(music, '>', trim)
