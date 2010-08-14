from abjad.core._FormatContributor import _FormatContributor
#from abjad.core._Parser import _Parser


class _GrobHandler(_FormatContributor):
   '''Abstract class from which all concrete Abjad grob handlers inherit.

   Concrete Abjad grob handlers include the accidentals interface, dots
   interface, text interface and tuplet bracket interface.

   See :term:`grob` for information on the core LilyPond concept.'''

   def __init__(self, grob):
      _FormatContributor.__init__(self)
      self._grob = grob
      #self._parser = _Parser( )
      self._promotions = { }

   ## OVERLOADS ##

   ## TODO: Deprecate _GrobHandler.__len__ because not semantic. ##

   def __len__(self):
      return len([kvp for kvp in vars(self).items( ) 
         if not kvp[0].startswith('_')])

   def __setattr__(self, attr, value):
      if not attr.startswith('_') and value is None and attr in vars(self):
         delattr(self, attr) 
      else:
         object.__setattr__(self, attr, value)

   ## PRIVATE METHODS ##

   def _promoted_grob(self, attribute):
      context = self._promotions.get(attribute, None)
      if context:
         return '%s.%s' % (str(context), self._grob)
      else:
         return '%s' % self._grob

   ## PRIVATE ATTRIBUTES ##

   @property
   def _before(self):
      '''Read-only list of strings to contribute at format time.'''

      result = [ ]
      return result

   @property
   def _dynamic_key_value_pairs(self):
      '''To be overriden in concrete classes inheriting from this class.'''
      result = [ ]
      return result

   @property
   def _frequency_indicator(self):
      from abjad.components._Leaf import _Leaf
      if hasattr(self, '_client') and isinstance(self._client, _Leaf):
         return r'\once '
      else:
         return ''

   @property
   def _key_value_pairs(self):
      result = [ ]
      result.extend(vars(self).items( ))
      result.extend(self._dynamic_key_value_pairs)
      result.sort( )
      return result

   @property
   def _overrides(self):
      r'''Read-only, alphabetized list of LilyPond \override strings 
      to contribute at format time.'''
      from abjad.tools.lilyfiletools._format_lilypond_attribute import _format_lilypond_attribute
      from abjad.tools.lilyfiletools._format_lilypond_value import _format_lilypond_value

      result = [ ]
         
      for key, value in self._key_value_pairs:
         if not key.startswith('_'):
            #result.append(r'%s\override %s %s = %s' % (
            #   self._frequency_indicator,
            #   self._promoted_grob(key),
            #   self._parser.format_attribute(key),
            #   self._parser.format_value(value)))
            result.append(r'%s\override %s %s = %s' % (
               self._frequency_indicator,
               self._promoted_grob(key),
               _format_lilypond_attribute(key),
               _format_lilypond_value(value)))
      ## to ensure predictable (alphabetic) output of output
      result.sort( )
      return result

   @property
   def _reverts(self):
      r'''Read-only list of LilyPond revert strings to contribute
      at format time.
      '''
      from abjad.tools.lilyfiletools._format_lilypond_attribute import _format_lilypond_attribute

      result = [ ]
      for key, value in vars(self).items( ):
         if not key.startswith('_'):
            #result.append(r'%s\revert %s %s' % (
            #   self._frequency_indicator,
            #   self._promoted_grob(key),
            #   self._parser.format_attribute(key)))
            result.append(r'%s\revert %s %s' % (
               self._frequency_indicator,
               self._promoted_grob(key),
               _format_lilypond_attribute(key)))
      ## to ensure predictable (alphabetic) output of output
      result.sort( )
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def grob(self):
      '''Read-only string name of LilyPond grob handled by this class.
      '''
      return self._grob
