class LilyPondContextProxy(object):
   '''.. versionadded:: 1.1.2

   LilyPond context proxy..
   '''

   def __init__(self):
      pass

   ## OVERLOADS ##

   def __repr__(self):
      body_string = ' '
      skeleton_strings = self._get_skeleton_strings( )
      if skeleton_strings:
         body_string = ', '.join(skeleton_strings)
      return '%s(%s)' % (self.__class__.__name__, body_string)

   ## PRIVATE METHODS ##

   def _get_attribute_pairs(self):
      return tuple(vars(self).iteritems( ))

   def _get_skeleton_strings(self):
      result = [ ]
      for attribute_name, attribute_value in self._get_attribute_pairs( ):
         result.append('%s = %s' % (attribute_name, repr(attribute_value)))
      return result
