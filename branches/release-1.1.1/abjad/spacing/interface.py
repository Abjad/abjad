from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class SpacingInterface(_Interface, _GrobHandler, _SpannerReceptor):
   r'''Handle *LilyPond* ``SpacingSpanner`` grob.
      Receive *Abjad* ``SpacingSpanner`` spanner.

      Example::

         abjad> t = Score([ ])

         abjad> t.spacing.strict_grace_spacing = True
         abjad> t.spacing.strict_note_spacing = True
         abjad> t.spacing.uniform_stretching = True
         abjad> print t.format

         \new Score \with {
                 \override SpacingSpanner #'strict-note-spacing = ##t
                 \override SpacingSpanner #'uniform-stretching = ##t
                 \override SpacingSpanner #'strict-grace-spacing = ##t
         } <<
         >>
   
   *LilyPond* ``SpacingSpanner`` lives in score context by default.'''

   def __init__(self, _client):
      '''Bind to client. Handle *LilyPond* ``SpacingSpanner`` grob.
         Receive *Abjad* ``SpacingSpanner`` spanner.'''
      from abjad.spacing.spanner import SpacingSpanner
      _Interface.__init__(self, _client)
      _GrobHandler.__init__(self, 'SpacingSpanner')
      _SpannerReceptor.__init__(self, (SpacingSpanner, ))
