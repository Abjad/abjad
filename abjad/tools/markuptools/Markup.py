# -*- encoding: utf-8 -*-
from abjad.tools import schemetools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Markup(AbjadObject):
    r'''A LilyPond markup.

    ..  container:: example

        Initializes from string:

        ::

            >>> string = r'\bold { "This is markup text." }'
            >>> markup = Markup(string)
            >>> show(markup) # doctest: +SKIP

        ..  doctest::

            >>> print format(markup)
            \markup { \bold { "This is markup text." } }

    ..  container:: example

        Initializes from other markup:

        ::

            >>> markup_1 = Markup('foo', direction=Up)
            >>> markup_2 = Markup(markup_1, direction=Down)
            >>> show(markup_2) # doctest: +SKIP

        ..  doctest::

            >>> print format(markup_1)
            ^ \markup { foo }

        ..  doctest::

            >>> print format(markup_2)
            _ \markup { foo }

    ..  container:: example

        Attaches markup to score components:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> string = r'\italic { "This is also markup text." }'
            >>> markup = Markup(string, direction=Up)
            >>> attach(markup, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new Staff {
                c'8
                    ^ \markup {
                        \italic
                            {
                                "This is also markup text."
                            }
                        }
                d'8
                e'8
                f'8
            }

    Set `direction` to ``Up``, ``Down``, ``'neutral'``,
    ``'^'``, ``'_'``, ``'-'`` or None.

    Markup objects are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contents',
        '_direction',
        '_format_slot',
        '_markup_name',
        )

    ### INITIALIZER ###

    def __init__(self, argument, direction=None, markup_name=None):
        from abjad.tools import lilypondparsertools
        from abjad.tools import markuptools
        if not argument:
            #contents = None
            contents = 'This is markup text.'
        # WARNING: running the LilyPondParser here on a regular basis
        #          by setting (for example) argument='' in the intializer
        #          slows performance of the entire system by up to 25%!
        elif isinstance(argument, str):
            to_parse = r'\markup {{ {} }}'.format(argument)
            parsed = lilypondparsertools.LilyPondParser()(to_parse)
            if all(isinstance(x, str) for x in parsed.contents):
                contents = (' '.join(parsed.contents),)
            else:
                contents = tuple(parsed.contents)
        elif isinstance(argument, markuptools.MarkupCommand):
            contents = (argument,)
        elif isinstance(argument, type(self)):
            contents = tuple(argument._contents)
            direction = direction or argument._direction
            markup_name = markup_name or argument._markup_name
        elif isinstance(argument, (list, tuple)) and 0 < len(argument):
            contents = []
            for arg in argument:
                if isinstance(arg, (str, markuptools.MarkupCommand)):
                    contents.append(arg)
                else:
                    contents.append(str(arg))
            contents = tuple(contents)
        else:
            contents = (str(argument),)
        self._contents = contents
        self._format_slot = 'right'
        self._markup_name = markup_name
        direction = \
            stringtools.arg_to_tridirectional_ordinal_constant(direction)
        self._direction = direction

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies markup.

        ..  container:: example

            ::

                >>> import copy
                >>> string = r'\bold { allegro ma non troppo }'
                >>> markup = Markup(string)
                >>> new_markup = copy.copy(markup)
                >>> show(new_markup) # doctest: +SKIP

        Returns new markup.
        '''
        return type(self)(
            self._contents,
            direction=self._direction,
            markup_name=self._markup_name,
            )

    def __eq__(self, expr):
        r'''Is true when `expr` is a markup with format equal to that
        of this markup. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if format(self) == format(expr):
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats markup.

        ..  container:: example

            ::

                >>> string = r'\bold { allegro ma non troppo }'
                >>> markup = Markup(string)
                >>> print format(markup)
                \markup {
                    \bold
                        {
                            allegro
                            ma
                            non
                            troppo
                        }
                    }

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'lilypond'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __hash__(self):
        r'''Hashes markup.

        Returns integer.
        '''
        return hash((type(self).__name__, self.contents))

    def __illustrate__(self):
        r'''Illustrates markup.

        ..  container:: example

            ::

                >>> string = r'\bold { allegro ma non troppo }'
                >>> markup = Markup(string)
                >>> show(markup) # doctest: +SKIP

        Returns LilyPond file.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        lilypond_file = lilypondfiletools.make_basic_lilypond_file()
        lilypond_file.header_block.tagline = markuptools.Markup('""')
        lilypond_file.items.append(self)
        return lilypond_file

    def __str__(self):
        r'''Gets string representation of markup.

        ..  container:: example

            ::

                >>> string = r'\bold { allegro ma non troppo }'
                >>> markup = Markup(string)
                >>> print str(markup)
                \markup {
                    \bold
                        {
                            allegro
                            ma
                            non
                            troppo
                        }
                    }

        Returns string.
        '''
        return self._lilypond_format

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return self._get_format_pieces()

    @property
    def _lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=(
                self.contents,
                ),
            )

    ### PRIVATE METHODS ###

    def _get_format_pieces(self):
        indent = '\t'
        direction = ''
        if self.direction is not None:
            direction = stringtools.arg_to_tridirectional_lilypond_symbol(
                self.direction)
        # None
        if self.contents is None:
            return [r'\markup { }']
        # a single string
        if len(self.contents) == 1 and isinstance(self.contents[0], str):
            content = self.contents[0]
            if '"' in content:
                content = schemetools.Scheme.format_scheme_value(content)
            if direction:
                return [r'{} \markup {{ {} }}'.format(direction, content)]
            return [r'\markup {{ {} }}'.format(content)]
        # multiple strings or markup commands
        if direction:
            pieces = [r'{} \markup {{'.format(direction)]
        else:
            pieces = [r'\markup {']
        for content in self.contents:
            if isinstance(content, str):
                content = schemetools.Scheme.format_scheme_value(content)
                pieces.append('{}{}'.format(indent, content))
            else:
                pieces.extend(['{}{}'.format(indent, x) for x in
                    content._get_format_pieces()])
        pieces.append('{}}}'.format(indent))
        return pieces

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        r'''Gets contents of markup.

        ..  container:: example

            ::

                >>> string = r'\bold { "This is markup text." }'
                >>> markup = Markup(string)
                >>> show(markup) # doctest: +SKIP

            ::

                >>> markup.contents
                (MarkupCommand('bold', ['This is markup text.']),)

        Returns tuple.
        '''
        return self._contents

    @property
    def direction(self):
        r'''Gets direction of markup.

        ..  container:: example

            ::

                >>> string = r'\bold { "This is markup text." }'
                >>> markup = Markup(string, direction=Up)
                >>> show(markup) # doctest: +SKIP

            ::

                >>> markup.direction
                Up

        Returns up, down, center or none.
        '''
        return self._direction

    @property
    def markup_name(self):
        r'''Gets markup name of markup.

        ..  container:: example

            ::

                >>> string = r'\bold { allegro ma non troppo }'
                >>> markup = Markup(string, markup_name='non troppo')
                >>> show(markup) # doctest: +SKIP

            ::

                >>> markup.markup_name
                'non troppo'

        Returns string or none.
        '''
        return self._markup_name
