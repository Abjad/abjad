from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _TupletBracketInterface(_Interface, _GrobHandler):
   r'''Handle LilyPond TupletBracket grob.

   ::

      abjad> t = Staff(construct.scale(4))
      abjad> t.tupletbracket.bracket_visibility = True
      abjad> print t.format
      \new Staff \with {
         \override TupletBracket #'bracket-visibility = ##t
      } {
         c'8
         d'8
         e'8
         f'8
      }
   '''

   def __init__(self, client):
      '''Bind to client and handle LilyPond TupletBracket grob.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TupletBracket')
