from abjad.core.GrobNamespace import GrobNamespace


class OverrideNamespace(object):
   '''.. versionadded:: 1.1.2

   Override namespace.
   '''

   def __init__(self):
      pass

   ## OVERLOADS ##

   def __getattr__(self, attribute_name):
      if attribute_name.startswith('_'):
         return getattr(self.__class__, attribute_name).fget(self)
      else:
         return vars(self).setdefault(attribute_name, GrobNamespace(attribute_name))

   def __repr__(self):
      return '<%s>' % self.__class__.__name__

   ## PRIVATE ATTRIBUTES ##

   @property
   def _overrides(self):
      result = [ ]
      for grob_name, grob_namespace in vars(self).iteritems( ):
         result.extend(grob_namespace._overrides)
      result.sort( )
      return result   

#   @property
#   def _reverts(self):
#      result = [ ]
#      result.sort( )
#      return result   
