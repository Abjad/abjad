class ChromaticInterval(object):

   def __init__(self, number):
      if isinstance(number, (int, float, long)):
         self._number = number
      else:
         raise TypeError

   ## OVERLOADS ##

   def __abs__(self):
      return ChromaticInterval(abs(self._number))

   def __add__(self, arg):
      if isinstance(arg, ChromaticInterval):
         return ChromaticInterval(self._number + arg._number)
      else:
         raise TypeError

   def __eq__(self, arg):
      if isinstance(arg, ChromaticInterval):
         return self._number == arg._number
      else:
         raise TypeError

   def __float__(self):
      return float(self._number)

   def __int__(self):
      return int(self._number)

   def __ne__(self, arg):
      return not self == arg

   def __neg__(self):
      return ChromaticInterval(-self._number)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._number)

   def __sub__(self, arg):
      if isinstance(arg, ChromaticInterval):
         return ChromaticInterval(self._number - arg._number)
      else:
         raise TypeError
