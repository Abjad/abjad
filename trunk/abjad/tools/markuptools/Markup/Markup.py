#from abjad.tools.componenttools._Component import _Component
#from abjad.tools.contexttools.ContextMark import ContextMark
from abjad.tools.marktools._DirectedMark._DirectedMark import _DirectedMark


class Markup(_DirectedMark):
    r'''Abjad model of backslash-style LilyPond markup or Scheme-style LilyPond markup.

    Initialize backslash-style markup from string::

        abjad> markup = markuptools.Markup(r'\bold { "This is markup text." }')

    ::

        abjad> markup
        Markup('\\bold { "This is markup text." }')

    ::

        abjad> f(markup)
        \markup { \bold { "This is markup text." } }

    Initialize Scheme-style markup from string::

        abjad> markup = markuptools.Markup("(markup #:draw-line '(0 . -1))", style_string = 'scheme')

    ::

        abjad> markup
        Markup("(markup #:draw-line '(0 . -1))")

    ::

        abjad> f(markup)
        #(markup #:draw-line '(0 . -1))

    Initialize any markup from existing markup::

        abjad> markup_1 = markuptools.Markup('foo', direction = 'up')
        abjad> markup_2 = markuptools.Markup(markup_1, direction = 'down')

    ::

        abjad> f(markup_1)
        ^ \markup { foo }

    ::

        abjad> f(markup_2)
        _ \markup { foo }

    Attach markup to score components like this::

        abjad> note = Note("c'4")

    ::

        abjad> markup = markuptools.Markup(r'\bold { "This is markup text." }')

    ::

        abjad> markup(note)
        Markup('\\bold { "This is markup text." }')

    ::

        abjad> f(note)
        c'4 - \markup { \bold { "This is markup text." } }

    Set `direction` to ``'up'``, ``'down'``, ``'neutral'``, ``'^'``, ``'_'``, ``'-'`` or None.

    Set `style_string` to ``'backslash'`` or ``'scheme'``.

    Markup objects are immutable.
    '''

    __slots__ = ('_contents_string', '_direction', '_format_slot', '_style_string')

    def __init__(self, arg, direction = None, style_string = 'backslash'):
        #ContextMark.__init__(self, target_context = _Component)
        if isinstance(arg, str):
            contents_string = arg
        elif isinstance(arg, Markup):
            contents_string = arg._contents_string
            style_string = arg._style_string
        else:
            contents_string = str(arg)

        _DirectedMark.__init__(self, direction=direction)
        self._contents_string = contents_string
        self._style_string = style_string
        self._format_slot = 'right'

    ### PRIVATE ATTRIBUTES ###

    _style_strings = ('backslash', 'scheme')

    @property
    def _format_pieces(self):
        return [r'\markup { %s }' % self.contents_string]

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self._contents_string,
            direction = self._direction, style_string = self._style_string)

    __deepcopy__ = __copy__

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.format == arg.format:
                return True
        return False

    def __hash__(self):
        return hash((type(self).__name__, self.format))

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        if self._direction is not None:
            return '%s(%r, %r)' % (type(self).__name__, 
                self._contents_string, self._direction)
        else:
            return '%s(%r)' % (type(self).__name__, self._contents_string)

    def __str__(self):
        return self.format

    ### PUBLIC ATTRIBUTES ###

    @property
    def contents_string(self):
        r'''Read-only contents string of markup:

        ::

            abjad> markup = markuptools.Markup(r'\bold { "This is markup text." }')
            abjad> markup.contents_string
            '\\bold { "This is markup text." }'

        Return string
        '''
        return self._contents_string

    @property
    def format(self):
        r'''Read-only LilyPond format of markup::

            abjad> markup = markuptools.Markup(r'\bold { "This is markup text." }')
            abjad> markup.format
            '\\markup { \\bold { "This is markup text." } }'

        Return string.
        '''
        result = ''
        if self._style_string == 'backslash':
            result = r'\markup { %s }' % self._contents_string
            if self._direction is not None:
                result = '%s %s' % (self._direction, result)
        elif self._style_string == 'scheme':
            result = '#%s' % self._contents_string
        else:
            raise ValueError('unknown markup style string: "%s".' % self._style_string)
        return result

#   @property
#   def style_string(self):
#      r'''Read-only style string of markup:
#
#      ::
#
#         abjad> markup = markuptools.Markup(r'\bold { "This is markup text." }')
#         abjad> markup.style_string
#         'backslash'
#      '''
#      return self._style_string
