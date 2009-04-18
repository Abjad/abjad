from abjad.core.abjadcore import _Abjad


class FixedSystemIndicator(_Abjad):
   '''Fixed system indication for regular system layout.'''

   def __init__(self, yOffsetTuple, startingSystem = 0):
      '''Set y offset values and starting system number.'''
      self.yOffsetTuple = yOffsetTuple
      self.startingSystem = startingSystem

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, FixedSystemIndicator):
         if self.yOffsetTuple == expr.yOffsetTuple:
            if self.startingSystem == expr.startingSystem:
               return True
      return False

   def __ne__(self, expr):
      return not self == expr

   ## PUBLIC ATTRIBUTES ##

   @apply
   def startingSystem( ):
      def fget(self):
         return self._startingSystem
      def fset(self, arg):
         if not isinstance(arg, int):
            raise TypeError
         self._startingSystem = arg
      return property(**locals( ))

   @apply
   def yOffsetTuple( ):
      def fget(self):
         return self._yOffsetTuplet
      def fset(self, arg):
         if not isinstance(arg, tuple):
            raise TypeError
         self._yOffsetTuplet = arg
      return property(**locals( ))
