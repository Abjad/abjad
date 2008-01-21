from .. containers.formatter import ContainerFormatter

class MeasureFormatter(ContainerFormatter):

   def __init__(self, client):
      ContainerFormatter.__init__(self, client)

   @property
   def _meter(self):
      result = [ ]
      if self._client.meter and not self._client.meter.hide:
         result.append('\t' + self._client.meter.lily)
      return result
   
   @property
   def lily(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self._meter)
      result.extend(self.opening)
      result.extend(self._opening)
      result.extend(self._contents)
      result.extend(self._client.barline._closing)
      result.extend(self._closing)
      result.extend(self.closing)
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)
