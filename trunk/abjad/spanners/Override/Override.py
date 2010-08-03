from abjad.core.parser import _Parser
from abjad.spanners.Override.format import _OverrideSpannerFormatInterface
from abjad.spanners.Spanner.grobhandler import _GrobHandlerSpanner


class Override(_GrobHandlerSpanner):
   r'''Arbitrary LilyPond override spanner.

   Five-argument form of initializer uses context specification. ::

      abjad> staff = Staff(macros.scale(8))
      abjad> Override(staff[:4], 'Staff', 'Beam', 'positions', (8, 8))
      abjad> print staff.format
      \new Staff {
              \override Staff.Beam #'positions = #'(8 . 8)
              c'8
              d'8
              e'8
              f'8
              \revert Staff.Beam #'positions
              g'8
              a'8
              b'8
              c''8
      }

   Four-argument form of initializer does not use context specification. ::

      abjad> staff = Staff(macros.scale(8))
      abjad> Override(staff[:4], 'Beam', 'positions', (8, 8))
      abjad> print staff.format
      \new Staff {
              \override Beam #'positions = #'(8 . 8)
              c'8
              d'8
              e'8
              f'8
              \revert Beam #'positions
              g'8
              a'8
              b'8
              c''8
      }
   '''

   def __init__(self, music, *args):
      _GrobHandlerSpanner.__init__(self, 'TemporaryGrob', music)
      if len(args) == 3:
         self._context = None
         self._grob, self._attribute, self._value  = args
      elif len(args) == 4:
         self._context, self._grob, self._attribute, self._value  = args
      else:
         raise ValueError('need 3 or 4 args, not %s.' % len(args))
      self._format = _OverrideSpannerFormatInterface(self)
      self._parser = _Parser( )

   ## OVERLOADS ##

   def __repr__(self):
      if self._context:
         return 'Override([%s], %s, %s, %s, %s)' % (self._compact_summary, 
            self._context, self._grob, self._attribute, self._value)
      else:
         return 'Override([%s], %s, %s, %s)' % (self._compact_summary, 
            self._grob, self._attribute, self._value)

   ## PRIVATE METHODS ##

   def _prepend_context(self, expr):
      if self._context:
         return '%s.%s' % (self._context, expr)
      else:
         return expr

   def _prepend_counter(self, expr):
      if len(self.leaves) == 1:
         return r'\once ' + expr
      else:
         return expr
