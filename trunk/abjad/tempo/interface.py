from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.rational.rational import Rational
from abjad.spanner.receptor import _SpannerReceptor


class _TempoInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond MetronomeMark grob and Abjad Tempo spanner.'''
   
   def __init__(self, client):
      '''Bind to client and LilyPond MetronomMark grob.
         Receive Abjad Tempo spanner.'''
      from abjad.tempo.spanner import Tempo
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'MetronomeMark')
      _GrobHandler.__init__(self, (Tempo, ))
      self._indication = None
 
   ## PUBLIC ATTRIBUTES ##

   @apply
   def indication( ):
      '''Read / write tempo indication.'''
      def fget(self):
         return self._indication
      def fset(self, arg):
         if arg is None:
            self._indication = arg
         elif isinstance(arg, (tuple)):
            assert isinstance(arg, tuple)
            assert isinstance(arg[0], (tuple, Rational))
            assert isinstance(arg[1], (int, float, long))
            from abjad.note.note import Note
            if isinstance(arg[0], tuple):
               self._indication = (Note(0, arg[0]), arg[1])
            elif isinstance(arg[0], Rational):
               self._indication = (Note(0, arg[0]), arg[1])
      return property(**locals( ))

   ## PUBLIC METHODS ##

   ## TODO: Replace interface clear( ) method with override interface ##

   def clear(self):
      self.indication = None
      _GrobHandler.clear(self)

   @property
   def opening(self):
      '''Format contribution at container opening or before leaf.'''
      result =  [ ] 
      if self.indication:
         note = self.indication[0].duration._dotted 
         tempo = self.indication[1]
         result.append(r'\tempo %s=%s' % (note, tempo))
      return result
