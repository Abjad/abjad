from abjad.spanners.Spanner.grobhandler import _GrobHandlerSpanner
from abjad.spanners.Trill.format import _TrillSpannerFormatInterface
import types


class Trill(_GrobHandlerSpanner):
   r'''Trill with continuation line.

   *  Interfaces to LilyPond ``startTrillSpan``, ``stopTrillSpan`` commands.
   *  Handles LilyPond TrillSpanner grob.

   ::

      abjad> t = Staff(macros.scale(4))
      abjad> Trill(t[:])
      Trill(c'8, d'8, e'8, f'8)
      abjad> print t.format
      \new Staff {
         c'8 \startTrillSpan
         d'8
         e'8
         f'8 \stopTrillSpan
      }
   '''

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
               :class:`Pitch <abjad.tools.pitchtools.NamedPitch.NamedPitch>`, ``None``.

            ::

               abjad> t = Staff(macros.scale(4))
               abjad> trill = Trill(t[:2])
               abjad> trill.pitch = pitchtools.NamedPitch('cs', 4)

               abjad> print t.format
               \new Staff {
                  \pitchedTrill c'8 \startTrillSpan cs'
                  d'8 \stopTrillSpan
                  e'8
                  f'8
               }
         '''

         return self._pitch
      def fset(self, expr):
         from abjad.tools import pitchtools
         if expr is None:
            self._pitch = expr
         else:
            pitch = pitchtools.NamedPitch(expr)
            self._pitch = pitch
      return property(**locals( ))
