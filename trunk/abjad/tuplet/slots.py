from abjad.container.slots import _ContainerFormatterSlotsInterface
from abjad.helpers.rational_as_fraction import _rational_as_fraction


class _TupletFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      result = [ ]
      tuplet = self.formatter.tuplet
      result.extend(['% ' + x for x in tuplet.comments.before])
      result.extend(tuplet.directives.before)
      result.extend(tuplet.interfaces.overrides)
      if tuplet.duration.multiplier == 1 and \
         hasattr(tuplet.__class__, 'color'):
         result.append(r"\tweak #'color #blue")
      return tuple(result)

   @property
   def slot_2(self):
      result = [ ]
      formatter = self.formatter
      tuplet = formatter.tuplet
      if tuplet.duration.multiplier:
         if tuplet.duration.multiplier != 1 or \
            hasattr(tuplet.__class__, 'color'):
            if tuplet.invisible:
               multiplier = tuplet.duration.multiplier
               n, d = multiplier._n, multiplier._d
               result.append(r"\scaleDurations #'(%s . %s) {" % (n, d))
            else:
               result.append(r'%s\times %s %s' % (
                  formatter._fraction, 
                  _rational_as_fraction(tuplet.duration.multiplier), 
                  tuplet.brackets.open))
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      tuplet = self.formatter.tuplet
      result.extend(['\t% ' + x for x in tuplet.comments.opening])
      result.extend(['\t' + x for x in tuplet.directives.opening])
      result.extend(['\t' + x for x in tuplet.interfaces.opening])
      return tuple(result)

   @property
   def slot_5(self):
      result = [ ]
      tuplet = self.formatter.tuplet
      result.extend(['\t' + x for x in tuplet.interfaces.closing])
      result.extend(['\t' + x for x in tuplet.directives.closing])
      result.extend(['\t% ' + x for x in tuplet.comments.closing])
      return tuple(result)

   @property
   def slot_6(self):
      result = [ ]
      tuplet = self.formatter.tuplet
      if tuplet.duration.multiplier:
         if tuplet.duration.multiplier != 1 or \
            hasattr(tuplet.__class__, 'color'):
            result.append(tuplet.brackets.close)
      return tuple(result)

   @property
   def slot_7(self):
      result = [ ]
      tuplet = self.formatter.tuplet
      result.extend(tuplet.directives.after)
      result.extend(tuplet.interfaces.reverts)
      result.extend(['% ' + x for x in tuplet.comments.after])
      return tuple(result)
