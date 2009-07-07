from abjad.hairpin.spanner import Hairpin


def Decrescendo(music, trim = False):
   '''Decrescendo spanner.'''

   return Hairpin(music, '>', trim)
