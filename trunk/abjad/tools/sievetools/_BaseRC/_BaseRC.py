class _BaseRC(object):
   '''Abstract base class for residue class RC and residue class
   expression RCExpression.
   '''

   ## OVERLOADS ##

   ## TODO: implement __neg__( ) ##

   def __and__(self, arg):
      assert isinstance(arg, _BaseRC)
      return self._operate(arg, 'and')

   def __or__(self, arg):
      assert isinstance(arg, _BaseRC)
      return self._operate(arg, 'or')

   def __xor__(self, arg):
      assert isinstance(arg, _BaseRC)
      return self._operate(arg, 'xor')

   ## PRIVATE METHODS ##

   def _operate(self, arg, op):
      from abjad.tools.sievetools.RCExpression import RCExpression
      from abjad.tools.sievetools.RC import RC
      if isinstance(self, RCExpression) and self.operator == op:
         argA = self.rcs
      else:
         argA = [self]
      if isinstance(arg, RCExpression) and arg.operator == op:
         argB = arg.rcs
      else:
         argB = [arg]
      return RCExpression(argA + argB, op)
