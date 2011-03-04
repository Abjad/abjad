from abjad.core import _Immutable
#from abjad.core import _StrictComparator


#class MarkupCommand(_StrictComparator, _Immutable):
class MarkupCommand(_Immutable):
   r'''Abjad model of a LilyPond markup command::

      abjad> circle = markuptools.MarkupCommand('draw-circle', ['#2.5', '#0.1', '##f'], None)
      abjad> square = markuptools.MarkupCommand('rounded-box', None, ['hello?'])
      abjad> line = markuptools.MarkupCommand('line', None, [square, 'wow!'])
      abjad> rotate = markuptools.MarkupCommand('rotate', ['#60'], [line])
      abjad> combine = markuptools.MarkupCommand('combine', None, [rotate, circle], is_braced = False)

   ::

      abjad> print combine
      \combine \rotate #60 \line { \rounded-box hello? wow! } \draw-circle #2.5 #0.1 ##f

   Insert markup command in markup to attach to score components::

      abjad> note = Note("c'4")

   ::

      abjad> markup = markuptools.Markup(combine)

   ::

      abjad> markup(note)

   ::

      abjad> f(note) 
      c'4 \markup { \combine \rotate #60 \line { \rounded-box hello? wow! } \draw-circle #2.5 #0.1 ##f }

   Return markup command.
   '''

   ## TODO: Implement a multi-line, indented version for human readability. ##

   __slots__ = ('args', 'is_braced', 'command', 'markup')

   def __init__(self, command, args, markup, is_braced = True):
      assert isinstance(command, str) \
         and len(command) and command.find(' ') == -1
      assert isinstance(args, type(None)) or \
         (isinstance(args, (list, tuple)) and len(args))
      assert isinstance(markup, type(None)) or \
         (isinstance(markup, (list, tuple)) and len(markup))
      if markup:
         assert all([isinstance(x, (MarkupCommand, str)) for x in markup])
      
      object.__setattr__(self, 'is_braced', bool(is_braced))
      object.__setattr__(self, 'command', command)

      if args:
         object.__setattr__(self, 'args', tuple(args))
      else:
         object.__setattr__(self, 'args', args)

      if markup:
         object.__setattr__(self, 'markup', tuple(markup))
      else:
         object.__setattr__(self, 'markup', markup)

   ### OVERRIDES ###

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
          if self.args == arg.args and \
             self.is_braced == arg.is_braced and \
             self.command == arg.command and \
             self.markup == arg.markup:
             return True  
      return False

   def __repr__(self):
      return '%s(%s, %s, %s)' % (self.__class__.__name__, self.command, self.args, self.markup)

   def __str__(self):
#     markup_delimiter = '\n'
      markup_delimiter = ' '
      return markup_delimiter.join(self.format)

   ### PUBLIC ATTRIBUTES ###

   @property
   def format(self):
      r'''Read-only format of markup command::

         abjad> markup_command = markuptools.MarkupCommand('draw-circle', ['#2.5', '#0.1', '##f'], None)
         abjad> markup_command.format
         ['\\draw-circle #2.5 #0.1 ##f']

      Return list of strings.
      '''
#     indent_delimiter = '\t'
      indent_delimiter = ''

      parts = [r'\%s' % self.command]

      if self.args is not None:
         for arg in self.args:
            if 'format' in dir(arg) and not isinstance(arg, str):
               parts[0] += ' %s' % arg.format
            else:
               parts[0] += ' %s' % arg

      if self.markup is not None:
         for markup in self.markup:
            if 'format' in dir(markup) and not isinstance(markup, str):
               parts.extend([indent_delimiter + x for x in markup.format])
            else:
               parts.append(indent_delimiter + markup)

      if self.is_braced and self.markup and 1 < len(self.markup):
         parts[0] += ' {'
         parts.append('}')

      return parts
