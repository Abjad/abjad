from abjad.core import _Abjad
from abjad.cfg._read_config_file import _read_config_file
from abjad.tools import componenttools

if _read_config_file( )['DEBUG'] == False:
   DEBUG = False
else:
   DEBUG = True


class _debug(_Abjad):
   '''Debug decorator class.  

   The purpose of this decorator is to run "live bug tracking" 
   when ``DEBUG`` is set to `True`. 

   Apply the decorator to any function that requires live debugging.
   Instantiate with parentheses.

   Example:

   You want the debugger to track function ``insert( )``::

      def insert(self, expr): 
         ...

   To get the debugger called every time ``insert( )`` is called,
   put ``@_debug( )`` immediately above the function definition::

      @_debug( )
      def insert(self, expr): 
         ...
   '''

   def __init__(self, check_function=componenttools.is_well_formed_component, verbose=False):
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
               raise Warning("check not passed in %s" % f.__name__)
         return result

      return wrapper 
