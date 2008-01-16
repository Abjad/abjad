from .. containers.formatter import ContainerFormatter

class TupletFormatter(ContainerFormatter):

   def __init__(self, client):
      ContainerFormatter.__init__(self, client)
      self.label = None

   @property
   def _label(self):
      result = [ ]
      if self.label:
         if len(self.label) == 1:
            label = str(self.label[0])
         else:
            label = '%s:%s' % self.label
         directive = """\once \override TupletNumber #'text = """
         directive += """\markup { "%s" }""" % label
         result.append(directive)
      return result

   @property
   def _fraction(self):
      if not self._client.duration.isBinary( ):
         return r'\fraction '
      else:
         return ''

   @property
   def _opening(self):
      '''Allow for no-multiplier and 1-multiplier tuplets.'''
      result = [ ]
      if self._client.multiplier:
         if self._client.multiplier != 1:
            result.append(r'%s\times %s %s' % (self._fraction, 
               self._client.multiplier, self._client.brackets.open))
      return result

   @property
   def _closing(self):
      result = [ ]
      if self._client.multiplier:
         if self._client.multiplier != 1:
            result.append(self._client.brackets.close)
      return result

   @property
   def lily(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self._label)
      result.extend(self._opening)
      result.extend(self._contents)
      result.extend(self._client.barline._closing)
      result.extend(self._closing)
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)
