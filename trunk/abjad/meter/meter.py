from abjad.core.grobhandler import _GrobHandler
from abjad.rational.rational import Rational


### TODO: Make Meter public.
###       There's no reason to have private _Meter, yes?

class _Meter(_GrobHandler):

   def __init__(self, n, d):
      #_GrobHandler.__init__(self, 'Staff.TimeSignature')
      _GrobHandler.__init__(self, 'TimeSignature')
      self.pair = (n, d)
      self.hide = False

   ### OVERLOADS ###

   def __eq__(self, arg):
      if isinstance(arg, _Meter):
         return self.pair == arg.pair
      elif isinstance(arg, tuple):
         return self.pair == arg
      else:
         return False
   
   def __ne__(self, arg):
      return not self == arg

   def __nonzero__(self):
      return True
   
   def __repr__(self):
      return '_Meter(%s, %s)' % (self.numerator, self.denominator)

   def __str__(self):
      return '%s/%s' % (self.numerator, self.denominator)

   ### PUBLIC ATTRIBUTES ###

   @property
   def denominator(self):
      if self.pair:
         return self.pair[-1]
      else:
         return None

   @property
   def duration(self):
      return Rational(self.numerator, self.denominator)

   @apply
   def hide( ):
      def fget(self):
         return self._hide
      def fset(self, arg):
         if isinstance(arg, bool):
            self._hide = arg
         else:
            raise ValueError('meter hide must be boolean.')
      return property(**locals( ))

   @property
   def lily(self):
      return r'\time %s/%s' % (self.numerator, self.denominator)

   @property
   def numerator(self):
      if self.pair:
         return self.pair[0]
      else:
         return None

   @apply
   def pair( ):
      def fget(self):
         return self._pair
      def fset(self, arg):
         if isinstance(arg, tuple) and len(arg) == 2 and \
            isinstance(arg[0], (int, float, long)) and \
            isinstance(arg[1], (int, float, long)):
            self._pair = arg
         else:
            raise ValueError('meter %s must be (m . n) pair.' % str(arg))
      return property(**locals( ))
