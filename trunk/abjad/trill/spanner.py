from abjad.pitch import Pitch
from abjad.spanner.grobhandler import _GrobHandlerSpanner
from abjad.trill.format import _TrillSpannerFormatInterface
import types


class Trill(_GrobHandlerSpanner):
   r'''Trill with continuation line.

      *  Inherits from *Abjad* spanner.
      *  Interfaces to *LilyPond* ``startTrillSpan``, \
         ``stopTrillSpan`` commands.
      *  Handles *LilyPond* ``TrillSpanner`` grob.

      ::

         abjad> t = Staff(construct.scale(4))
         abjad> Trill(t[:])
         Trill(c'8, d'8, e'8, f'8)

         abjad> print t.format
         \new Staff {
            c'8 \startTrillSpan
            d'8
            e'8
            f'8 \stopTrillSpan
         }'''

   def __init__(self, music = None):
      '''Initialize as type of grob-handling spanner.
         Set ``pitch`` to ``None``.'''

      _GrobHandlerSpanner.__init__(self, 'TrillSpanner', music)
      self._format = _TrillSpannerFormatInterface(self)
      self._pitch = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def pitch( ):
      def fget(self):
         r'''Optional read / write pitch for pitched trills.
   
            *  Default value: ``None``.
            *  Acceptable values: \
               :class:`Pitch <abjad.pitch.pitch.Pitch>`, ``None``.

            ::

               abjad> t = Staff(construct.scale(4))
               abjad> trill = Trill(t[:2])
               abjad> trill.pitch = Pitch('cs', 4)

               abjad> print t.format
               \new Staff {
                  \pitchedTrill c'8 \startTrillSpan cs'
                  d'8 \stopTrillSpan
                  e'8
                  f'8
               }'''

         return self._pitch
      def fset(self, expr):
         assert isinstance(expr, (Pitch, types.NoneType))
         self._pitch = expr
      return property(**locals( ))
