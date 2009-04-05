from abjad.core.interface import _Interface


class _FormatterSlotsInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      '''Format contributions immediately before open brackets.'''
      return ( )

   @property
   def slot_2(self):
      '''Open brackets, possibly including with-block.'''
      return ( )

   @property
   def slot_3(self):
      '''Format contributions immediately after open brackets.'''
      return ( )

   @property
   def slot_4(self):
      '''Formatted container contents or formatted leaf body.'''
      return ( )

   @property
   def slot_5(self):
      '''Format contributions immediately before close brackets.'''
      return ( )

   @property
   def slot_6(self):
      '''Close brackets.'''
      return ( )

   @property
   def slot_7(self):
      '''Format contributions immediately after close brackets.'''
      return ( )

   ## PUBLIC METHODS ##

   def report(self):
      print '%s: %s' % ('slot_1', self.slot_1)
      print '%s: %s' % ('slot_2', self.slot_2)
      print '%s: %s' % ('slot_3', self.slot_3)
      print '%s: %s' % ('slot_4', self.slot_4)
      print '%s: %s' % ('slot_5', self.slot_5)
      print '%s: %s' % ('slot_6', self.slot_6)
      print '%s: %s' % ('slot_7', self.slot_7)
