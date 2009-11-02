
class _BaseRC(object):
   '''Abstract base class for residue class RC and residue class
   expression RCexpression.'''

   def _operate(self, arg, op):
      from abjad.tools.sievetools.rcexpression import RCexpression
      from abjad.tools.sievetools.rc import RC
      if isinstance(self, RCexpression) and self.operator == op:
         argA = self.rcs
      else:
         argA = [self]

      if isinstance(arg, RCexpression) and arg.operator == op:
         argB = arg.rcs
      else:
         argB = [arg]

      return RCexpression(argA + argB, op)


   def __and__(self, arg):
      assert isinstance(arg, _BaseRC)
      return self._operate(arg, 'and')


   def __or__(self, arg):
      assert isinstance(arg, _BaseRC)
      return self._operate(arg, 'or')


   def __xor__(self, arg):
      assert isinstance(arg, _BaseRC)
      return self._operate(arg, 'xor')
