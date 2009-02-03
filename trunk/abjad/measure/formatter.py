from abjad.container.formatter import _ContainerFormatter
from abjad.exceptions.underfullmeasure import UnderfullMeasureException
from abjad.rational.rational import Rational
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet


class _MeasureFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

   ### PRIVATE ATTRIBUTES ###

   @property
   def _compressedContents(self):
      result = [ ]
      compression = self._client.duration.compression
      if len(self._client):
         ### TODO - may be dangerous; run tests; write tests
         measure_music = self._client[ : ]
         for x in measure_music:
            x._parent = None
         tuplet = FixedMultiplierTuplet(
            compression, measure_music)
         tuplet.invisible = True
         result.extend(['\t' + x for x in tuplet.formatter._pieces])
         for x in measure_music:
            x._parent = self._client
      return result

   @property
   def _processedContents(self):
      result = [ ]
      client = self._client
      if client.duration.compression != Rational(1, 1):
         if client.__class__.__name__ == 'RigidMeasure':
            ### TODO: rename to WronglyFullMeasureException ###
            msg = 'Meter %s does not equal %s contents duration.'
            msg %= (client.meter.effective, client.duration.contents)
            raise UnderfullMeasureException(msg)
         elif client.__class__.__name__ in ('Measure', 'ProlatingMeasure'):
            result.extend(self._compressedContents)
      else:
         result.extend(self._contents)
      return result
   
   ### PUBLIC ATTRIBUTES ###

   @property
   def format(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self.opening)
      result.extend(self._opening)
      result.extend(self._processedContents)
      result.extend(self._closing)
      result.extend(self.closing)
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)
