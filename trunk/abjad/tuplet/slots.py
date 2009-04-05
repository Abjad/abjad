from abjad.container.slots import _ContainerFormatterSlotsInterface
from abjad.helpers.rational_as_fraction import _rational_as_fraction


class _TupletFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      result = [ ]
      #client = self._client
      tuplet = self._client._client
      result.extend(tuplet.interfaces.overrides)
      if tuplet.duration.multiplier == 1 and \
         hasattr(tuplet.__class__, 'color'):
         result.append(r"\tweak #'color #blue")
      return result

   @property
   def slot_2(self):
      result = [ ]
      #client = self._client
      formatter = self._client
      tuplet = formatter._client
      if tuplet.duration.multiplier:
         if tuplet.duration.multiplier != 1 or \
            hasattr(tuplet.__class__, 'color'):
            if tuplet.invisible:
               multiplier = tuplet.duration.multiplier
               n, d = multiplier._n, multiplier._d
               result.append(r"\scaleDurations #'(%s . %s) {" % (n, d))
            else:
               if tuplet.parallel:
                  brackets_open = '<<'
               else:
                  brackets_open = '{'
               result.append(r'%s\times %s %s' % (formatter.fraction, 
                  _rational_as_fraction(tuplet.duration.multiplier), 
                  brackets_open))
      return result

   @property
   def slot_3(self):
      result = [ ]
      result.extend([
         '\t' + x for x in self._client._client.interfaces.opening])
      return result

   @property
   def slot_5(self):
      result = [ ]
      result.extend([
         '\t' + x for x in self._client._client.interfaces.closing])
      return result

   @property
   def slot_6(self):
      result = [ ]
      #client = self._client
      tuplet = self._client._client
      if tuplet.duration.multiplier:
         if tuplet.duration.multiplier != 1 or \
            hasattr(tuplet.__class__, 'color'):
            if tuplet.parallel:
               result.append('>>')
            else:
               result.append('}')
      return result

   @property
   def slot_7(self):
      result = [ ]
      result.extend(self._client._client.interfaces.reverts)
      return result
