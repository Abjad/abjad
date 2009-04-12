from abjad.core.abjadcore import _Abjad
from abjad.cfg.read_config_value import _read_config_value
from abjad.tools import check

if _read_config_value('DEBUG').lower( ) == 'false':
   DEBUG = False
else:
   DEBUG = True

class debug(_Abjad):
   '''
   Debug decorator class. 
   The purpose of this decorator is to run "live bug tracking" when "DEBUG" 
   is set to True. 
   Apply the decorator to any function that requires live debugging.
   Because this decorator is a class, you must instantiated by using 
   parenthesis.

   Example:
   You want the debugger to track function insert( ):

   def insert(self, expr): 
      ...

   To get the debugger called every time insert( ) is called put '@debug( )' 
   immediately above the function definition:

   @debug( )
   def insert(self, expr): 
      ...
   '''

   def __init__(self, check_function=check.wf, verbose=False):
      self.check_function = check_function
      self.verbose = verbose

   def __call__(self, f):
      def wrapper(*args, **kwargs):
         result = f(*args, **kwargs)
         if DEBUG:
            if self.verbose:
               print '---- Debugger verbose ----'
               print '"%s( )" executed.' % f.__name__
               print '--------------------------'
               
            component = args[0]
            if not self.check_function(component):
               raise Warning("check( ) not passed in %s" % f.__name__)
         return result

      return wrapper 
