class _LilyPondComponentPlugIn(object):
   '''.. versionadded:: 1.1.2

   Shared LilyPond grob proxy and LilyPond context proxy functionality.
   '''
   
   ## OVERLOADS ##
   
   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self._get_attribute_tuples( ) == arg._get_attribute_tuples( )
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      body_string = ' '
      skeleton_strings = self._get_skeleton_strings( )
      if skeleton_strings:
         body_string = ', '.join(skeleton_strings)
      return '%s(%s)' % (self.__class__.__name__, body_string)
