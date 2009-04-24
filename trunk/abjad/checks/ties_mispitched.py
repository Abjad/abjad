from abjad.checks.check import _Check
from abjad.tools import iterate


class TiesMispitched(_Check):

   def _run(self, expr):
      '''Check for mispitched notes.
         Do not check tied rests or skips.
         Implement chord-checking later.'''
      from abjad.note.note import Note
      violators = [ ]
      total = 0
      for leaf in iterate.naive(expr, Note):
         total += 1
         if leaf.tie.spanned and not leaf.tie.last and leaf.next:
            if leaf.pitch != leaf.next.pitch:
               violators.append(leaf)
      return violators, total
