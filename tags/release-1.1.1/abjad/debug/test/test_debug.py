from abjad.debug.debug import _debug
from abjad.debug.debug import DEBUG
import py.test


def test__debug_01( ):
   '''@_debug( ) decorator correctly returns the return value/object 
   of the function or method it decorates.
   '''

   def mycheck(expr):
      return True

   @_debug(mycheck)
   def dummy(expr):
      return expr

   assert dummy('hello') == 'hello'


## DEBUG ON DEPENDENT TESTS ##

if DEBUG:

   def test__debug_02( ):
      '''debug throws a Warning exception if the check function 
      returns False.
      '''

      def mycheck(expr):
         return isinstance(expr, str)

      @_debug(mycheck)
      def dummy(expr):
         return expr

      assert dummy('hello')
      assert py.test.raises(Warning, 'dummy(1)')


   def test__debug_03( ):
      '''The checking function passed to the debugger 
      must take one argument.
      '''

      def mycheck( ):
         pass

      @_debug(mycheck)
      def dummy(expr):
         return expr

      assert py.test.raises(TypeError, "dummy('hello')")
