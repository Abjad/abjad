from abjad.components._Component import _Component
#from abjad.core import _StrictComparator
from abjad.tools.contexttools.ContextMark import ContextMark


#class Markup(_StrictComparator):
class Markup(Mark):
   r'''Abjad model of LilyPond markup:

   ::

      abjad> markuptools.Markup(r'\bold { "This is markup text." }')
      Markup(\bold { "This is markup text." })
   '''

   __slots__ = ('_contents_string', '_direction_string', '_format_slot', '_style_string')

   #def __init__(self, arg, style_string = 'backslash'):
   def __init__(self, arg, direction_string = None, style_string = 'backslash'):
      Mark.__init__(self, target_context = _Component)
      if isinstance(arg, str):
         contents_string = arg
         style_string = style_string
      elif isinstance(arg, Markup):
         contents_string = arg.contents_string
         style_string = arg.style_string
      else:
         #raise TypeError('must be string or other markup instance.')
         contents_string = str(arg)
      #object.__setattr__(self, 'contents_string', contents)
      #object.__setattr__(self, 'style_string', style_string)
      self._contents_string = contents_string
      self._direction_string = direction_string
      self._style_string = style_string
      self._format_slot = 'right'
      
   ## PRIVATE ATTRIBUTES ##

   _direction_string_to_direction_symbol = {'up': '^', 'down': '_', 'neutral': '-'}

   _style_strings = ('backslash', 'scheme')

   ## OVERLOADS ##

   def __copy__(self, *args):
      return type(self)(self._contents_string, 
         direction_string = self.direction_string, style_string = self.style_string)

   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, Markup):
         if self.format == arg.format:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      if self.direction_string is not None:
         return '%s(%s, %s)' % (
            self.__class__.__name__, repr(self.contents_string), repr(self.direction_string))
      else:
         return '%s(%s)' % (self.__class__.__name__, repr(self.contents_string))

   def __str__(self):
      return self.format

   ## PUBLIC ATTRIBUTES ##

   @property
   def contents_string(self):
      r'''Read-only contents string of markup:

      ::

         abjad> markup = markuptools.Markup(r'\bold { "This is markup text." }')
         abjad> markup.contents_string
         '\\bold { "This is markup text." }'
      '''
      return self._contents_string

   @property
   def direction_string(self):
      return self._direction_string
   
   @property
   def format(self):
      r'''Read-only LilyPond input format of markup:

      ::

         abjad> markup = markuptools.Markup(r'\bold { "This is markup text." }')
         abjad> markup.format
         '\\markup { \\bold { "This is markup text." } }'
      '''
      result = ''
      if self.style_string == 'backslash':
         result = r'\markup { %s }' % self.contents_string
      elif self.style_string == 'scheme':
         result = '#%s' % self.contents_string
      else:
         raise ValueError('unknown markup style string: "%s".' % self.style_string)
      direction_string = self.direction_string
      if direction_string is not None:
         direction_symbol = self._direction_string_to_direction_symbol[direction_string]
         result = '%s %s' % (direction_symbol, result)
      return result

   @property
   def style_string(self):
      r'''Read-only style string of markup:

      ::

         abjad> markup = markuptools.Markup(r'\bold { "This is markup text." }')
         abjad> markup.style_string
         'backslash'
      '''
      return self._style_string
