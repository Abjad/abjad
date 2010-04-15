class ExtentIndicator(object):
   '''.. versionadded:: 1.1.2

   Indicator of chord extent, such as triad, seventh chord, ninth chord,
   etc.

   Value object that can not be changed after instantiation.
   '''

   def __init__(self, number):
      if number not in self._acceptable_number:
         raise ValueError('can not initialize extent indicator: %s' % number)
      self._number = number

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.number == arg.number:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (type(self).__name__, self.number)

   ## PRIVATE ATTRIBUTES ##

   _acceptable_number = (5, 7, 9)

   _extent_number_to_extent_name = {
      5: 'triad', 7: 'seventh', 9: 'ninth',
   }

   ## PUBLIC ATTRIBUTES ##

   @property
   def name(self):
      return self._extent_number_to_extent_name[self.number]

   @property
   def number(self):
      return self._number
