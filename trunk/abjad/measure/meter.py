from .. duration.rational import Rational

class Meter(object):

   def __init__(self, n, d):
      self.pair = (n, d)
      self.hide = False

   ### REPR ###

   def __repr__(self):
      return 'Meter(%s, %s)' % (self.numerator, self.denominator)

   def __str__(self):
      return '%s/%s' % (self.numerator, self.denominator)
   
   ### MANAGED ATTRIBUTES ###

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

   @property
   def numerator(self):
      if self.pair:
         return self.pair[0]
      else:
         return None

   @property
   def denominator(self):
      if self.pair:
         return self.pair[-1]
      else:
         return None

   @property
   def duration(self):
      return Rational(self.numerator, self.denominator)

   ### COMPARISON TESTING ###

   def __eq__(self, arg):
      if isinstance(arg, Meter):
         return self.pair == arg.pair
      elif isinstance(arg, tuple):
         return self.pair == arg
      else:
         return False
   
   def __ne__(self, arg):
      return not self == arg

   ### FORMATTING ###

   @property
   def lily(self):
      return r'\time %s/%s' % (self.numerator, self.denominator)
