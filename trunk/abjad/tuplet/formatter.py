from .. containers.formatter import _ContainerFormatter

class _TupletFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
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
      if not self._client.duration._binary:
         return r'\fraction '
      else:
         return ''

   @property
   def _opening(self):
      '''Allow for no-multiplier and 1-multiplier tuplets.'''
      result = [ ]
      if self._client.duration.multiplier:
         if self._client.duration.multiplier != 1:
            result.append(r'%s\times %s %s' % (self._fraction, 
               self._client.duration.multiplier, self._client.brackets.open))
      inheritence = _ContainerFormatter._opening
      result.extend(inheritence.fget(self))
      return result

   @property
   def _closing(self):
      result = [ ]
      result.extend(_ContainerFormatter._closing.fget(self))
      if self._client.duration.multiplier:
         if self._client.duration.multiplier != 1:
            result.append(self._client.brackets.close)
      return result

   @property
   def lily(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self._label)
      result.extend(self.opening)
      result.extend(self._opening)
      result.extend(self._contents)
      result.extend(self._closing)
      result.extend(self.closing)
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)
