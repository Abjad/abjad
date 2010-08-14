class GrobNamespace(object):
   '''.. versionadded:: 1.1.2

   Grob namespace.
   '''
   
   def __init__(self, abjad_name):
      grob_name = self._abjad_name_to_lilypond_grob_name(abjad_name)
      self._grob_name = grob_name

   ## OVERLOADS ##

   def __repr__(self):
      return '<%s%s>' % (self.grob_name, self.__class__.__name__)

   ## PRIVATE ATTRIBUTES ##

   ## TODO: make work for containers ##
   @property
   def _overrides(self):
      from abjad.tools.lilyfiletools._grob_attribute_and_value_to_lilypond_override \
         import _grob_attribute_and_value_to_lilypond_override
      result = [ ]
      for name, value in vars(self).iteritems( ):
         if not name.startswith('_'):
            override = _grob_attribute_and_value_to_lilypond_override(self.grob_name, name, value)
            result.append(override)
      result.sort( )
      return result

   ## TODO: make work for containers ##
   @property
   def _reverts(self):
      result = [ ]
      result.sort( )
      return [ ]

   ## PRIVATE METHODS ##

   def _abjad_name_to_lilypond_grob_name(self, name):
      parts = name.split('_')
      parts = [part.title( ) for part in parts]
      grob_name = ''.join(parts)
      return grob_name

   ## PUBLIC ATTRIBUTES ##

   @property
   def grob_name(self):
      return self._grob_name
