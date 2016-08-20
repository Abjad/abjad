# -*- coding: utf-8 -*-
import copy
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Articulation(AbjadValueObject):
    r'''An articulation.

    ..  container:: example

        **Example 1.** Initializes from name:

        ::

            >>> Articulation('staccato')
            Articulation('staccato')

    ..  container:: example

        **Example 2.** Initializes from abbreviation:

        ::

            >>> Articulation('.')
            Articulation('.')

    ..  container:: example

        **Example 3.** Initializes from other articulation:

        ::

            >>> articulation = Articulation('staccato')
            >>> Articulation(articulation)
            Articulation('staccato')

    ..  container:: example

        **Example 4.** Initializes with direction:

        ::

            >>> Articulation('staccato', Up)
            Articulation('staccato', Up)

    .. container:: example

        **Example 5.** Use `attach()` to attach articulations to notes, rests
        or chords:

        ::

            >>> note = Note("c'4")
            >>> articulation = Articulation('staccato')
            >>> attach(articulation, note)
            >>> show(note) # doctest: +SKIP

    ..  todo:: Simplify initializer. Allow only initialization from name.
        Implement new ``from_abbreviation()`` and ``from_articulation()``
        methods to replace existing initializer polymorphism.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_direction',
        '_format_slot',
        '_name',
        )

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

    ### INITIALIZER ###

    def __init__(self, name=None, direction=None):
        self._default_scope = None
        if isinstance(name, type(self)):
            expr = name
            name = expr.name
            direction = direction or expr.direction
        name = str(name)
        if '\\' in name:
            direction, name = name.split('\\')
            direction = direction.strip()
            name = name.strip()
        direction = \
            stringtools.expr_to_tridirectional_ordinal_constant(direction)
        directions = (Up, Down, Center, None)
        assert direction in directions, repr(direction)
        self._name = name
        self._direction = direction
        self._format_slot = 'right'

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats articulation.

        Set `format_specification` to `''`, `'lilypond`' or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        elif format_specification == 'lilypond':
            return self._lilypond_format
        return str(self)

    def __illustrate__(self):
        r'''Illustrates articulation.

        Returns LilyPond file.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import scoretools
        from abjad.tools import topleveltools
        note = scoretools.Note("c'4")
        articulation = copy.copy(self)
        topleveltools.attach(articulation, note)
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(note)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    def __str__(self):
        r'''Gets string representation of articulation.

        Returns string.
        '''
        if self.name:
            string = self._shortcut_to_word.get(self.name)
            if not string:
                string = self.name
            if self.direction is None:
                direction = '-'
            else:
                direction = stringtools.expr_to_tridirectional_lilypond_symbol(
                    self.direction)
            return '{}\{}'.format(direction, string)
        else:
            return ''

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.name]
        if self.direction is not None:
            values.append(self.direction)
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_is_indented=False,
            )

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.articulations.append(str(self))
        return lilypond_format_bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        if self.direction is not None:
            return '{!r}, {!r}'.format(self.name, self.direction)
        else:
            return repr(self.name)

    @property
    def _lilypond_format(self):
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of articulation.

        ..  container:: example

            >>> articulation = Articulation('staccato')
            >>> articulation.default_scope is None
            True

        Returns none.
        '''
        return self._default_scope

    @property
    def direction(self):
        r'''Gets direction of articulation.

        ..  container:: example

            **Example 1.** Without direction:

            >>> articulation = Articulation('staccato')
            >>> articulation.direction is None
            True

        ..  container:: example

            **Example 2.** With direction:

            >>> articulation = Articulation('staccato', direction=Up)
            >>> articulation.direction
            Up

        Returns ordinal constant or none.
        '''
        return self._direction

    @property
    def name(self):
        r'''Gets name of articulation.

        ..  container:: example

            **Example 1.** Staccato:

            ::

                >>> articulation = Articulation('staccato')
                >>> articulation.name
                'staccato'

        ..  container:: example

            **Example 2.** Tenuto:

            ::

                >>> articulation = Articulation('tenuto')
                >>> articulation.name
                'tenuto'

        Returns string.
        '''
        return self._name
