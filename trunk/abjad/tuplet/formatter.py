from abjad.container.formatter import _ContainerFormatter
from abjad.helpers.rational_as_fraction import _rational_as_fraction


class _TupletFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self.label = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _before(self):
      result = [ ]
      if self._client.duration.multiplier == 1 and \
         hasattr(self._client.__class__, 'color'):
         result.append(r"\tweak #'color #blue")
      return result

   @property
   def _closing(self):
      result = [ ]
      result.extend(['\t' + x for x in self._grobReverts])
      result.extend(_ContainerFormatter._collectLocation(self, '_closing'))
      if self._client.duration.multiplier:
         if self._client.duration.multiplier != 1 or \
            hasattr(self._client.__class__, 'color'):
            if self._client.parallel:
               result.append('>>')
            else:
               result.append('}')
      return result

   @property
   def _fraction(self):
      if not self._client.duration._binary:
         if not self._client.invisible:
            return r'\fraction '
      else:
         return ''

   @property
   def _opening(self):
      '''Allow for no-multiplier and 1-multiplier tuplets.'''
      result = [ ]
      client = self._client
      if client.duration.multiplier:
         if client.duration.multiplier != 1 or \
            hasattr(client.__class__, 'color'):
            if client.invisible:
               multiplier = client.duration.multiplier
               n, d = multiplier._n, multiplier._d
               result.append(r"\scaleDurations #'(%s . %s) {" % (n, d))
            else:
               if client.parallel:
                  brackets_open = '<<'
               else:
                  brackets_open = '{'
               result.append(r'%s\times %s %s' % (self._fraction, 
                  _rational_as_fraction(client.duration.multiplier), 
                  brackets_open))
      inheritence = _ContainerFormatter._opening
      result.extend(inheritence.fget(self))
      return result

   @property
   def _pieces(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self._before)
      result.extend(self.opening)
      result.extend(self._opening)
      result.extend(self._contents)
      result.extend(self._closing)
      result.extend(self.closing)
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return '\n'.join(self._pieces)
