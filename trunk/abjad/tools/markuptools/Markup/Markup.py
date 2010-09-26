from abjad.core import _StrictComparator


class Markup(_StrictComparator):
   r'''Abjad model of LilyPond markup:

   ::

      abjad> markuptools.Markup(r'\bold { "This is markup text." }')
      Markup(\bold { "This is markup text." })
   '''

   __slots__ = ('_contents_string', '_style_string')

   def __init__(self, arg, style_string = 'backslash'):
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
      self._style_string = style_string
      
   ## PRIVATE ATTRIBUTES ##

   _style_strings = ('backslash', 'scheme')

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, Markup):
         if self.format == arg.format:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.contents_string)

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
   def format(self):
      r'''Read-only LilyPond input format of markup:

      ::

         abjad> markup = markuptools.Markup(r'\bold { "This is markup text." }')
         abjad> markup.format
         '\\markup { \\bold { "This is markup text." } }'
      '''
      if self.style_string == 'backslash':
         return r'\markup { %s }' % self.contents_string
      elif self.style_string == 'scheme':
         return '#%s' % self.contents_string
      else:
         raise ValueError('unknown markup style string: "%s".' % self.style_string)

   @property
   def style_string(self):
      r'''Read-only style string of markup:

      ::

         abjad> markup = markuptools.Markup(r'\bold { "This is markup text." }')
         abjad> markup.style_string
         'backslash'
      '''
      return self._style_string
