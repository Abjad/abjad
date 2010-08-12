from abjad.core import _GrobHandler
from abjad.core import _ContextSettingHandler
from abjad.interfaces._Interface import _Interface
from abjad.interfaces._SpannerReceptor import _SpannerReceptor
from abjad.spanners import BeamSpanner
import types


class BeamInterface(_Interface, _GrobHandler, _ContextSettingHandler, _SpannerReceptor):
   '''Handle LilyPond Beam grob.

   Interface to LilyPond \setStemLeftBeamCount, \setStemRightBeamCount.

   Receive Abjad Beam spanner.
   '''

   def __init__(self, client):
      '''Bind to client, LilyPond Beam grob and Abjad Beam spanner.
      Set 'counts' to (None, None).'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Beam')
      _SpannerReceptor.__init__(self, (BeamSpanner, ))
      self.auto_beaming = None
      #self._counts = (None, None)
      self._counts = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _before(self):
      '''Format contribution before leaf.'''
      result = [ ]
      result.extend(_GrobHandler._before.fget(self))
      if self.counts is not None:
         if self.counts[0] is not None:
            result.append(r'\set stemLeftBeamCount = #%s' % self.counts[0])
         if self.counts[1] is not None:
            result.append(r'\set stemRightBeamCount = #%s' % self.counts[1])
      return result

   ## PUBLIC ATTRIBUTES ##

   @apply
   def auto_beaming( ):
      def fget(self):
         r'''Interface to LilyPond automatic beaming command.
      
         ::

            abjad> staff = Staff(macros.scale(4))
            abjad> staff.beam.auto_beaming = False
            abjad> f(staff)
            \new Staff \with {
                    autoBeaming = ##f
            } {
                    c'8
                    d'8
                    e'8
                    f'8
            }
         '''
         return self._auto_beaming
      def fset(self, expr):
         assert isinstance(expr, (bool, type(None)))
         self._auto_beaming = expr
      return property(**locals( ))

   @property
   def beamable(self):
      '''True when client is beamable, otherwise False.'''
      from abjad.components.Chord import Chord
      from abjad.components.Container import Container
      from abjad.components.Note import Note
      from abjad.tools import durtools
      client = self._client
      if isinstance(client, Container):
         return False
      #flags = client.duration._flags
      flag_count = durtools.rational_to_flag_count(client.duration.written)
      #return isinstance(client, (Note, Chord)) and 0 < flags
      return isinstance(client, (Note, Chord)) and 0 < flag_count

   @apply
   def counts( ):
      def fget(self):
         '''Interface to LilyPond \setStemLeftBeamCount, 
         \setStemRightBeamCount.  Set to nonzero integer, pair or None.'''
         return self._counts
      def fset(self, expr):
         if expr is None:
            #self._counts = (None, None)
            self._counts = None
         elif isinstance(expr, int):
            self._counts = (expr, expr)
         elif isinstance(expr, (tuple, list)):
            self._counts = (expr[0], expr[1])
         else:
            raise ValueError('must be nonzero integer, pair or None.')
      return property(**locals( ))

   @property
   def settings(self):
      r'''Read-only list of LilyPond context settings
      picked up at format-time.'''
      result = [ ]
      auto_beaming = self.auto_beaming
      if auto_beaming is not None:
         if auto_beaming:
            result.append('autoBeaming = ##t')
         else:
            result.append('autoBeaming = ##f')
      return result
