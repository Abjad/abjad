from abjad.core.parser import _Parser


class _BlockAttributed(object):
   '''Model of attribute block in LilyPond input file.'''

   def __init__(self):
      self._parser = _Parser( )

   ## OVERLOADS ##

   def __repr__(self):
      if not len(self._user_attributes):
         return '%s( )' % self.__class__.__name__
      else:
         return '%s(%s)' % (
            self.__class__.__name__, len(self._user_attributes))

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_pieces(self):
      result = [ ]
      #if not self._user_attributes:
      if not self._formatted_user_attributes and \
         not getattr(self, 'contexts', None):
         result.append('%s { }' % self._escaped_name)
      else:
         result = ['%s {' % self._escaped_name]
         if getattr(self, 'contexts', None):
            specs = self._formatted_context_specifications
            result.extend(['\t' + x for x in specs])
         formatted_attributes = self._formatted_user_attributes
         formatted_attributes = ['\t' + x for x in formatted_attributes]
         result.extend(formatted_attributes)
         result.append('}')
      return result

   @property
   def _formatted_user_attributes(self):
      result = [ ]
      for key, value in sorted(vars(self).items( )):
         if not key.startswith('_'):
            formatted_key = key.replace('_', '-')
            formatted_value = self._parser.formatValue(value)
            setting = '%s = %s' % (formatted_key, formatted_value)
            result.append(setting)
      return result

   @property
   def _user_attributes(self):
      all_attributes = vars(self).keys( )
      user_attributes = [x for x in all_attributes if not x.startswith('_')]
      user_attributes.sort( )
      return user_attributes

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return '\n'.join(self._format_pieces)
