from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class TupletNumberInterface(_Interface, _GrobHandler):
   r'''Handle LilyPond TupletNumber grob.

   ::

      abjad> t = Staff(construct.scale(4))
      abjad> t.tupletnumber.transparent = True
      abjad> print t.format
      \new Staff \with {
         \override TupletNumber #'transparent = ##t
      } {
         c'8
         d'8
         e'8
         f'8
      }
   '''

   def __init__(self, client):
      '''Bind to client and LilyPond TupletNumber grob.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TupletNumber')
