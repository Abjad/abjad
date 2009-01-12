from abjad.core.formatcarrier import _FormatCarrier
from abjad.core.parser import _Parser


class _GrobHandler(_FormatCarrier):

   def __init__(self, grob):
      _FormatCarrier.__init__(self)
      self._grob = grob
      self._parser = _Parser( )
      self._promotions = { }

   ### OVERLOADS ###

   def __len__(self):
      return len([kvp for kvp in self.__dict__.items( ) 
         if not kvp[0].startswith('_')])

   def __setattr__(self, attr, value):
      if not attr.startswith('_') and value is None and attr in self.__dict__:
         delattr(self, attr) 
      else:
         object.__setattr__(self, attr, value)

   ### PRIVATE METHODS ###

   def _promotedGrob(self, attribute):
      context = self._promotions.get(attribute, None)
      if context:
         return '%s.%s' % (str(context), self._grob)
      else:
         return '%s' % self._grob

   ### PRIVATE ATTRIBUTES ###

   @property
   def _before(self):
      result = [ ]
      return result

   @property
   def _frequencyIndicator(self):
      if hasattr(self, '_client') and self._client.kind('_Leaf'):
         return r'\once '
      else:
         return ''

   @property
   #def _before(self):
   def _grobOverrides(self):
      result = [ ]
      for key, value in self.__dict__.items( ):
         if not key.startswith('_'):
            result.append(r'%s\override %s %s = %s' % (
               self._frequencyIndicator,
               self._promotedGrob(key),
               self._parser.formatAttribute(key),
               self._parser.formatValue(value)))
      return result

   @property
   def _grobReverts(self):
      result = [ ]
      for key, value in self.__dict__.items( ):
         if not key.startswith('_'):
            result.append(r'%s\revert %s %s' % (
               self._frequencyIndicator,
               self._promotedGrob(key),
               self._parser.formatAttribute(key)))
      return result

   ### PUBLIC METHODS ###

   def clear(self):
      for key, value in self.__dict__.items( ):
         if not key.startswith('_'):
            delattr(self, key)

   def promote(self, attribute, context):
      assert isinstance(context, str)
      if hasattr(self, attribute):
         self._promotions[attribute] = str(context)
      else:
         raise AttributeError('%s has no %s attribute.' %
            (self.__class__.__name__, attribute))
