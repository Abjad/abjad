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

        abjad> markup = markuptools.Markup("(markup #:draw-line '(0 . -1))", style_string='scheme')

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

    Set `style_string` to ``'backslash'``, ``'scheme'`` or none. Default to ``'backslash'``.

    Markup objects are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_contents_string', '_direction', '_format_slot', '_markup_name', '_style_string')
    _style_strings = ('backslash', 'scheme')

    ### INITIALIZER ###

    def __init__(self, arg, direction=None, markup_name=None, style_string=None):
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
        self._markup_name = markup_name

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return [r'\markup { %s }' % self.contents_string]

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(
            self._contents_string,
            direction=self._direction, 
            markup_name=self._markup_name,
            style_string=self._style_string
            )

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

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return (
            'direction',
            'markup_name',
            'style_string',
            )

    @property
    def _mandatory_argument_values(self):
        return (
            self.contents_string,
            )

    ### PUBLIC READ-ONLY PROPERTIES ###

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
        if self.style_string in (None, 'backslash'):
            result = r'\markup { %s }' % self.contents_string
            if self.direction is not None:
                result = '%s %s' % (self.direction, result)
        elif self.style_string == 'scheme':
            result = '#%s' % self.contents_string
        else:
            raise ValueError('unknown markup style string: "%s".' % self.style_string)
        return result

    @property
    def markup_name(self):
        r'''Read-only name of markup::

            abjad> markup = markuptools.Markup(r'\bold { allegro ma non troppo }', markup_name='non troppo')

        ::

            abjad> markup.markup_name
            'non troppo'

        Return string or none.
        '''
        return self._markup_name

    @property
    def style_string(self):
        '''Read-only style string of markup.
        '''
        return self._style_string
