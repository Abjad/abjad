# -*- encoding: utf-8 -*-
import copy
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Articulation(AbjadObject):
    r'''An articulation.

    ..  container:: example

        Initializes from name:

        ::

            >>> Articulation('staccato')
            Articulation('staccato')

    ..  container:: example

        Initializes from abbreviation:

        ::

            >>> Articulation('.')
            Articulation('.')

    ..  container:: example

        Initializes from other articulation:

        ::

            >>> articulation = Articulation('staccato')
            >>> Articulation(articulation)
            Articulation('staccato')

    ..  container:: example

        Initializes with direction:

        ::

            >>> Articulation('staccato', Up)
            Articulation('staccato', Up)

    .. container:: example

        Use `attach()` to attach articulations to notes, rests or chords:

        ::

            >>> note = Note("c'4")
            >>> articulation = Articulation('staccato')
            >>> attach(articulation, note)
            >>> show(note) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        '_direction',
        '_format_slot',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import datastructuretools
        assert len(args) in range(3), repr(args)
        if 2 <= len(args):
            assert isinstance(args[0], (str, type(None))), repr(args[0])
            assert isinstance(args[1],
                (str, type(None), datastructuretools.OrdinalConstant)), \
                repr(args[1])
            name, direction = args
        elif len(args) == 1 and isinstance(args[0], type(self)):
            name = args[0].name
            direction = args[0].direction
        elif len(args) == 1:
            assert isinstance(args[0],
                (str, type(None), datastructuretools.OrdinalConstant)), \
                repr(args[0])
            if args[0]:
                splits = args[0].split('\\')
                assert len(splits) in (1, 2), repr(splits)
                if len(splits) == 1:
                    name, direction = args[0], None
                elif len(splits) == 2:
                    name = splits[1]
                    if splits[0]:
                        direction = splits[0]
                    else:
                        direction = None
            else:
                name, direction = None, None
        else:
            name, direction = None, None
        self._name = name
        direction = \
            stringtools.arg_to_tridirectional_ordinal_constant(direction)
        self._direction = direction
        self._format_slot = 'right'

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies articulation.

        Returns new articulation.
        '''
        return type(self)(self.name, self.direction)

    def __eq__(self, expr):
        r'''True when `expr` is an articulation with name and direction 
        equal to that of this articulation. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if expr.name == self.name:
                if self.direction == expr.direction:
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats articulation.

        Set `format_specification` to `''`, `'lilypond`' or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        elif format_specification == 'lilypond':
            return self._lilypond_format
        return str(self)

    def __illustrate__(self):
        r'''Illustrates articulation.

        Returns LilyPond file.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        from abjad.tools import topleveltools
        note = scoretools.Note("c'4")
        articulation = copy.copy(self)
        topleveltools.attach(articulation, note)
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(note)
        lilypond_file.header_block.tagline = markuptools.Markup('""')
        return lilypond_file

    def __str__(self):
        r'''String representation of articulation.

        Returns string.
        '''
        if self.name:
            string = self._shortcut_to_word.get(self.name)
            if not string:
                string = self.name
            if self.direction is None:
                direction = '-'
            else:
                direction = \
                    stringtools.arg_to_tridirectional_lilypond_symbol(
                    self.direction)
            return '%s\%s' % (direction, string)
        else:
            return ''

    ### PRIVATE PROPERTIES ###

    # this causes unnecessary coupling to changeable lilypond codebase
    # and is discouraged
    _articulations_supported = (
        'accent',
        'marcato',
        'staccatissimo',
        'espressivo'
        'staccato',
        'tenuto'
        'portato'
        'upbow',
        'downbow'
        'flageolet'
        'thumb',
        'lheel'
        'rheel'
        'ltoe',
        'rtoe'
        'open'
        'stopped',
        'turn'
        'reverseturn'
        'trill',
        'prall'
        'mordent'
        'prallprall'
        'prallmordent',
        'upprall',
        'downprall',
        'upmordent',
        'downmordent',
        'pralldown',
        'prallup',
        'lineprall',
        'signumcongruentiae',
        'shortfermata',
        'fermata',
        'longfermata',
        'verylongfermata',
        'segno',
        'coda',
        'varcoda',
        '^',
        '+',
        '-',
        '|',
        '>',
        '.',
        '_',
        )

    # this causes unnecessary coupling to changeable lilypond codebase
    # and is discouraged
    _shortcut_to_word = {
        '^': 'marcato',
        '+': 'stopped',
        '-': 'tenuto',
        '|': 'staccatissimo',
        '>': 'accent',
        '.': 'staccato',
        '_': 'portato',
        }

    @property
    def _contents_repr_string(self):
        if self.direction is not None:
            return '{!r}, {!r}'.format(self.name, self.direction)
        else:
            return repr(self.name)

    @property
    def _lilypond_format(self):
        return str(self)

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = [self.name]
        if self.direction is not None:
            positional_argument_values.append(self.direction)
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Direction of articulation.

        Returns ordinal constant or none.
        '''
        assert self._direction in (Up, Down, Center, None), \
            repr(self._direction)
        return self._direction


    @property
    def name(self):
        r'''Name of articulation.

        ::

            >>> articulation.name
            'staccato'

        Returns string.
        '''
        return self._name
