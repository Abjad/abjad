from fractions import Fraction


class Duration(Fraction):
   '''.. versionadded:: 1.1.2

   Abjad model of musical duration::

      abjad> Duration(15, 16)
      Duration(15, 16)

   Durations inherit from built-in ``Fraction``.
   '''

   def __new__(klass, *args):
      if isinstance(args[0], tuple):
         n, d = args[0]
         self = Fraction.__new__(klass, n, d)
      else:
         self = Fraction.__new__(klass, *args)
      return self

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s, %s)' % (self.__class__.__name__, self.numerator, self.denominator)
