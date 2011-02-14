from abjad.tools.pitchtools._IntervalClass import _IntervalClass


## TODO: implement _CounterpointObject
class _CounterpointIntervalClass(_IntervalClass):
   '''.. versionadded:: 1.1.2

   Abstract counterpoint interval class class from which concrete
   counterpoint interval classes can inherit.
   '''

   ## OVERLOADS ##

   def __abs__(self):
      return type(self)(abs(self._number))

   def __float__(self):
      return float(self._number)

   def __int__(self):
      return self._number
