from abjad.core.abjadcore import _Abjad
import pprint


class _UserComments(_Abjad):
   
   def __init__(self):
      self._after = [ ]
      self._before = [ ]
      self._closing = [ ]
      self._opening = [ ]
      self._right = [ ]

   ## PUBLIC ATTRIBUTES ##

   @apply
   def after( ):
      def fget(self):
         return self._after
      def fset(self, arg):
         assert arg is None
         self._after = [ ]
      return property(**locals( ))

   @apply
   def before( ):
      def fget(self):
         return self._before
      def fset(self, arg):
         assert arg is None
         self._before = [ ]
      return property(**locals( ))

   @apply
   def closing( ):
      def fget(self):
         return self._closing
      def fset(self, arg):
         assert arg is None
         self._closing = [ ]
      return property(**locals( ))
   
   ## TODO: Clean up _UserComments.contributions ##

   @property
   def contributions(self):
      result = [ ]
      result.append(('before', tuple(self.before)))
      result.append(('opening', tuple(self.opening)))
      result.append(('right', tuple(self.right)))
      result.append(('closing', tuple(self.closing)))
      result.append(('after', tuple(self.after)))
      return tuple(result)
      #result = [ ]
      #for location in self.locations:
      #   result.append((location, tuple(getattr(self, location))))

   @property
   def locations(self):
      return ('before', 'opening', 'right', 'closing', 'after')

   @apply
   def opening( ):
      def fget(self):
         return self._opening
      def fset(self, arg):
         assert arg is None
         self._opening = [ ]
      return property(**locals( ))

   @apply
   def right( ):
      def fget(self):
         return self._right
      def fset(self, arg):
         assert arg is None
         self._right = [ ]
      return property(**locals( ))

   ## PUBLIC METHODS ##

   def clear(self):
      '''Remove all comments.'''
      for location in self.locations:
         setattr(self, location, None)

   ## TODO: Add _UserComments.report( ) 'output' keyword. ##
   ## TODO: Add _UserComments.report( ) tests. ##

   def report(self):
      '''Report all comments.'''
      for location in self.locations:
         print '%s: %s' % (location, getattr(self, location))
