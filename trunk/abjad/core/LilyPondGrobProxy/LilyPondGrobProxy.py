class LilyPondGrobProxy(object):
   '''.. versionadded:: 1.1.2

   LilyPond grob proxy.
   '''
   
   ## OVERLOADS ##

   def __repr__(self):
      body_string = ' '
      skeleton_strings = self._get_grob_override_skeleton_strings( )
      if skeleton_strings:
         body_string = ', '.join(skeleton_strings)
      return '%s(%s)' % (self.__class__.__name__, body_string)

   ## PRIVATE METHODS ##

   def _get_grob_override_skeleton_strings(self):
      result = [ ]
      for attribute_name, attribute_value in vars(self).iteritems( ):
         result.append('%s = %s' % (attribute_name, repr(attribute_value)))
      return result
