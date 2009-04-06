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
      result.append(self.wrap(tuplet.comments, 'before'))
      result.append(self.wrap(tuplet.directives, 'before'))
      result.append(self.wrap(tuplet.interfaces, 'overrides'))
      if tuplet.duration.multiplier == 1 and \
         hasattr(tuplet.__class__, 'color'):
         contributor = (tuplet.__class__, 'color')
         contributions = [r"\tweak #'color #blue"]
         result.append([contributor, contributions])
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
               contributor = (tuplet, 'invisible')
               contributions = [r"\scaleDurations #'(%s . %s) {" % (n, d)]
               result.append([contributor, contributions])
            else:
               contributor = (tuplet.brackets, 'open')
               contributions = [r'%s\times %s %s' % (
                  formatter._fraction, 
                  _rational_as_fraction(tuplet.duration.multiplier), 
                  tuplet.brackets.open[0])]
               result.append([contributor, contributions])
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      tuplet = self.formatter.tuplet
      result.append(self.wrap(tuplet.comments, 'opening'))
      result.append(self.wrap(tuplet.directives, 'opening'))
      result.append(self.wrap(tuplet.interfaces, 'opening'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_5(self):
      result = [ ]
      tuplet = self.formatter.tuplet
      result.append(self.wrap(tuplet.interfaces, 'closing'))
      result.append(self.wrap(tuplet.directives, 'closing'))
      result.append(self.wrap(tuplet.comments, 'closing'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_6(self):
      result = [ ]
      tuplet = self.formatter.tuplet
      if tuplet.duration.multiplier:
         if tuplet.duration.multiplier != 1 or \
            hasattr(tuplet.__class__, 'color'):
            result.append(self.wrap(tuplet.brackets, 'close'))
      return tuple(result)

   @property
   def slot_7(self):
      result = [ ]
      tuplet = self.formatter.tuplet
      result.append(self.wrap(tuplet.directives, 'after'))
      result.append(self.wrap(tuplet.interfaces, 'reverts'))
      result.append(self.wrap(tuplet.comments, 'after'))
      return tuple(result)
