from abjad.core import _StrictComparator


class CommentsInterface(_StrictComparator):
   
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
   
   @property
   def contributions(self):
      result = [ ]
      for location in self.locations:
         result.append((location, tuple(getattr(self, location))))
      return tuple(result)

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

   def report(self, verbose = False, output = 'screen'):
      '''Print comment fields and comment contributions to screen.
         Set verbose = True to include all comment fields.
         Set output = 'string' to return report as string.'''
      result = ''
      for location in self.locations:
         contributions = getattr(self, location)
         if contributions or verbose:
            result += '%s\n' % location
            for contribution in contributions:
               result += '\t%% %s\n' % contribution
      if output == 'screen':
         print result
      else:
         return result
