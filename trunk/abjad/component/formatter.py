from abjad.core.interface import _Interface
from abjad.component.slots import _ComponentFormatterSlotsInterface


class _ComponentFormatter(_Interface):

   ## The 'number' attribute causes only leaf numbering but attaches
   ## to _ComponentFormatter so that containers can number leaves.
   def __init__(self, client):
      _Interface.__init__(self, client)
      self._slots = _ComponentFormatterSlotsInterface(self)
      #self.number = False

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      result = [ ]
      result.extend(self.slots.contributions('slot_1'))
      result.extend(self.slots.contributions('slot_2'))
      result.extend(self.slots.contributions('slot_3'))
      result.extend(self.slots.contributions('slot_4'))
      result.extend(self.slots.contributions('slot_5'))
      result.extend(self.slots.contributions('slot_6'))
      result.extend(self.slots.contributions('slot_7'))
      result = '\n'.join(result)
      return result

   @property
   def slots(self):
      return self._slots

   ## PUBLIC METHODS ##

   def report(self, verbose = False, output = 'screen'):
      '''Report format contributions.'''
      result = ''
      slots = self.slots
      for i in range(1, 7 + 1):
         label = 'slot_%s' % i
         attr = label
         result += slots._format_slot(
            label, getattr(slots, attr), verbose, output = 'string')
      if output == 'screen':
         print result
      else:
         return result
