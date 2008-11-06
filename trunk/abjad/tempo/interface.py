from abjad.core.attributeformatter import _AttributeFormatter
from abjad.core.interface import _Interface
from abjad.core.spannerreceptor import _SpannerReceptor


class _TempoInterface(_Interface, _AttributeFormatter, _SpannerReceptor):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      _AttributeFormatter.__init__(self, 'MetronomeMark')
      _AttributeFormatter.__init__(self, ['Tempo'])
      self._metronome = None
 
   ### OVERLOADS ###

   def __eq__(self, arg):
      assert isinstance(arg, bool)
      return bool(self._metronome) == arg

   def __nonzero__(self):
      return bool(self._metronome)

   ### PRIVATE ATTRIBUTES ###
   
   @property
   def _before(self):
      result =  [ ] 
      if self._metronome:
         note = self._metronome[0].duration._dotted 
         tempo = self._metronome[1]
         result.append(r'\tempo %s=%s' % (note, tempo))
      return result

   ### PUBLIC METHODS ###

   def clear(self):
      self._metronome = None
      _AttributeFormatter.clear(self)

