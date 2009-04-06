from abjad.component.slots import _ComponentFormatterSlotsInterface


class _ContainerFormatterSlotsInterface(_ComponentFormatterSlotsInterface):

   def __init__(self, client):
      _ComponentFormatterSlotsInterface.__init__(self, client)

   ## PRIVATE METHODS ##

   def _indent_slot_contributions(self, slot):
      for contributor, contributions in slot:
         if contributions:
            for i, contribution in enumerate(contributions):
               contributions[i] = '\t' + contribution
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      result = [ ]
      container = self.formatter.container
      result.append(self.wrap(container.comments, 'before'))
      result.append(self.wrap(container.directives, 'before'))
      return tuple(result)

   @property
   def slot_2(self):
      result = [ ]
      result.append(self.wrap(self.formatter.container.brackets, 'open'))
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      container = self.formatter.container
      result.append(self.wrap(container.comments, 'opening'))
      result.append(self.wrap(container.directives, 'opening'))
      result.append(self.wrap(container.interfaces, 'overrides'))
      result.append(self.wrap(container.interfaces, 'opening'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_4(self):
      result = [ ]
      result.append(self.wrap(self.formatter, '_contents'))
      return tuple(result)

   @property
   def slot_5(self):
      result = [ ]
      container = self.formatter.container
      result.append(self.wrap(container.interfaces, 'closing'))
      result.append(self.wrap(container.interfaces, 'reverts'))
      result.append(self.wrap(container.directives, 'closing'))
      result.append(self.wrap(container.comments, 'closing'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_6(self):
      result = [ ]
      result.append(self.wrap(self.formatter.container.brackets, 'close'))
      return tuple(result)

   @property
   def slot_7(self):
      result = [ ]
      container = self.formatter.container
      result.append(self.wrap(container.directives, 'after'))
      result.append(self.wrap(container.comments, 'after'))
      return tuple(result)

   ## PUBLIC METHODS ##

   def contributions(self, attr):
      result = [ ]
      for contributor, contributions in getattr(self, attr):
         result.extend(contributions)
      return result
