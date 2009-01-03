from abjad.core.grobhandler import _GrobHandler
from abjad.rational.rational import Rational


#class _Meter(_GrobHandler):
class Meter(_GrobHandler):

   #def __init__(self, n, d):
   def __init__(self, *args):
      _GrobHandler.__init__(self, 'TimeSignature')
      #self.pair = (n, d)
      self.hide = False
      if len(args) == 1 and isinstance(args[0], Meter):
         meter = args[0]
         self.numerator = meter.numerator
         self.denominator = meter.denominator
      elif len(args) == 1 and isinstance(args[0], Rational):
         self.numerator = args[0]._n
         self.denominator = args[0]._d
      elif len(args) == 1 and isinstance(args[0], tuple):
         numerator, denominator = args[0][0], args[0][1]
         self.numerator = numerator
         self.denominator = denominator
      elif len(args) == 2 and all([isinstance(x, int) for x in args]):
         self.numerator = args[0]
         self.denominator = args[1]
      else:
         raise ValueError('invalid %s meter initialization.' % str(args))

   ### OVERLOADS ###

   def __eq__(self, arg):
      #if isinstance(arg, _Meter):
      if isinstance(arg, Meter):
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
      #return '_Meter(%s, %s)' % (self.numerator, self.denominator)
      return 'Meter(%s, %s)' % (self.numerator, self.denominator)

   def __str__(self):
      return '%s/%s' % (self.numerator, self.denominator)

   ### PUBLIC ATTRIBUTES ###

#   @property
#   def denominator(self):
#      if self.pair:
#         return self.pair[-1]
#      else:
#         return None

   @apply
   def denominator( ):
      def fget(self):
         return self._denominator
      def fset(self, arg):
         assert isinstance(arg, int)
         self._denominator = arg
      return property(**locals( ))

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

#   @property
#   def numerator(self):
#      if self.pair:
#         return self.pair[0]
#      else:
#         return None

   @apply
   def numerator( ):
      def fget(self):
         return self._numerator
      def fset(self, arg):
         assert isinstance(arg, int)
         self._numerator = arg
      return property(**locals( ))

   @apply
   def pair( ):
      def fget(self):
         #return self._pair
         return self.numerator, self.denominator
      def fset(self, arg):
         if isinstance(arg, tuple) and len(arg) == 2 and \
            isinstance(arg[0], (int, float, long)) and \
            isinstance(arg[1], (int, float, long)):
            #self._pair = arg
            self.numerator = arg[0]
            self.denominator = arg[1]
         else:
            raise ValueError('meter %s must be (m . n) pair.' % str(arg))
      return property(**locals( ))
