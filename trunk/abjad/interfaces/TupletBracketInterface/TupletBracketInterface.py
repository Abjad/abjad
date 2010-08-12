from abjad.core import _GrobHandler
from abjad.core import _ContextSettingHandler
from abjad.interfaces._Interface import _Interface
import types


class TupletBracketInterface(_Interface, _GrobHandler, _ContextSettingHandler):
   r'''Handle LilyPond TupletBracket grob.

   Interface to LilyPond ``tupletFullLength`` setting.

   ::

      abjad> t = Staff(macros.scale(4))
      abjad> t.tuplet_bracket.bracket_visibility = True
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
      self._tuplet_full_length = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def tuplet_full_length( ):
      def fget(self):
         r'''Read / write LilyPond ``tupletFullLength`` context setting.

         ::

            abjad> staff = Staff(macros.scale(4))
            abjad> staff.tuplet_bracket.tuplet_full_length = True
            abjad> f(staff)
            \new Staff \with {
                    tupletFullLength = ##t
            } {
                    c'8
                    d'8
                    e'8
                    f'8
            }
         '''
         return self._tuplet_full_length
      def fset(self, expr):
         assert isinstance(expr, (bool, type(None)))
         self._tuplet_full_length = expr
      return property(**locals( ))
      
   @property
   def settings(self):
      r'''Read-only list of LilyPond context settings
      picked up at format-time.
      '''
      result = [ ]
      tuplet_full_length = self.tuplet_full_length
      if tuplet_full_length is not None:
         if tuplet_full_length:
            result.append('tupletFullLength = ##t')
         else:
            result.append('tupletFullLength = ##f')
      return result
