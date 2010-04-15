class DoublingIndicator(object):
   '''.. versionadded:: 1.1.2

   Indicator of chord doubling.

   Value object that can not be changed after instantiation.
   '''

   def __init__(self, doublings):
      self._doublings = doublings

   ## PUBLIC ATTRIBUTES ##

   @property
   def doublings(self):
      return self._doublings
