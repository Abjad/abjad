from abjad.debug.debug import debug, DEBUG
import py.test


def test_debug_01( ):
   '''
   @debug( ) decorator correctly returns the return value/object of the
   function or method it decorates.
   '''
   def mycheck(expr):
      return True

   @debug(mycheck)
   def dummy(expr):
      return expr

   assert dummy('hello') == 'hello'


## DEBUG ON DEPENDENT TESTS ##

if DEBUG:

   def test_debug_02( ):
      '''debug throws a Warning exception if the check function returns False.'''
      def mycheck(expr):
         return isinstance(expr, str)

      @debug(mycheck)
      def dummy(expr):
         return expr

      assert dummy('hello')
      assert py.test.raises(Warning, 'dummy(1)')


   def test_debug_03( ):
      '''the checking function passed to the debugger must take one argument.'''
      def mycheck( ):
         pass

      @debug(mycheck)
      def dummy(expr):
         return expr

      assert py.test.raises(TypeError, "dummy('hello')")

