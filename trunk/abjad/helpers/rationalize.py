from abjad.duration.rational import Rational


### Don't need to use decorators to allow X.duration == (n, m), 
### but could be useful elsewhere?

def _rationalize(meth):
   '''Convert method argument from list or tuple to Rational.
      meth((m, n)) --> meth(Rational(m, n))
   '''
   def new(self, arg):
      if isinstance(arg, (list, tuple)):
         assert len(arg) < 3
         arg = Rational(*arg)
      return meth(self, arg)
   return new
