from abjad.tuplet.tuplet import _Tuplet


def subsume(tuplet):
   '''Make tuplet go away, leaving scaled tuplet contents.
      Return empty tuplet outside of score.'''

   assert isinstance(tuplet, _Tuplet)
   from abjad.tools import containertools
   from abjad.tools import scoretools
   
   containertools.contents_scale(tuplet, tuplet.duration.multiplier)
   scoretools.bequeath([tuplet], tuplet[:])

   return tuplet
