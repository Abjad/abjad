from abjad.container.formatter import _ContainerFormatter
from abjad.helpers.rational_as_fraction import _rational_as_fraction


class _TupletFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self.label = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def fraction(self):
      if not self._client.duration._binary:
         if not self._client.invisible:
            return r'\fraction '
      else:
         return ''

   @property
   #def flamingo_before(self):
   def slot_1(self):
      result = [ ]
      client = self._client
      result.extend(client.interfaces.overrides)
      if client.duration.multiplier == 1 and \
         hasattr(client.__class__, 'color'):
         result.append(r"\tweak #'color #blue")
      return result

   @property
   #def invocation_opening(self):
   def slot_2(self):
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
               result.append(r'%s\times %s %s' % (self.fraction, 
                  _rational_as_fraction(client.duration.multiplier), 
                  brackets_open))
      return result

   @property
   #def flamingo_opening(self):
   def slot_3(self):
      result = [ ]
      client = self._client
      result.extend(['\t' + x for x in client.interfaces.opening])
      return result

   @property
   #def flamingo_closing(self):
   def slot_5(self):
      result = [ ]
      client = self._client
      result.extend(['\t' + x for x in client.interfaces.closing])
      return result

   @property
   #def invocation_closing(self):
   def slot_6(self):
      client = self._client
      result = [ ]
      if client.duration.multiplier:
         if client.duration.multiplier != 1 or \
            hasattr(client.__class__, 'color'):
            if client.parallel:
               result.append('>>')
            else:
               result.append('}')
      return result

   @property
   #def flamingo_after(self):
   def slot_7(self):
      result = [ ]
      result.extend(self._client.interfaces.reverts)
      return result
