import copy
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Articulation(AbjadValueObject):
    r'''Articulation.

    ..  container:: example

        Initializes from name:

        >>> abjad.Articulation('staccato')
        Articulation('staccato')

    ..  container:: example

        Initializes from abbreviation:

        >>> abjad.Articulation('.')
        Articulation('.')

    ..  container:: example

        Initializes from other articulation:

        >>> articulation = abjad.Articulation('staccato')
        >>> abjad.Articulation(articulation)
        Articulation('staccato')

    ..  container:: example

        Initializes with direction:

        >>> abjad.Articulation('staccato', abjad.Up)
        Articulation('staccato', Up)

    .. container:: example

        Use `attach()` to attach articulations to notes, rests or chords:

        >>> note = abjad.Note("c'4")
        >>> articulation = abjad.Articulation('staccato')
        >>> abjad.attach(articulation, note)
        >>> abjad.show(note) # doctest: +SKIP

    ..  todo:: Simplify initializer. Allow only initialization from name.
        Implement new ``from_abbreviation()`` and ``from_articulation()``
        methods to replace existing initializer polymorphism.

    ..  container:: example

        Works with new:

        >>> abjad.new(abjad.Articulation('.'))
        Articulation('.')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
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
        import abjad
        if isinstance(name, type(self)):
            argument = name
            name = argument.name
            direction = direction or argument.direction
        name = str(name)
        if '\\' in name:
            direction, name = name.split('\\')
            direction = direction.strip()
            name = name.strip()
        direction = abjad.String.to_tridirectional_ordinal_constant(direction)
        directions = (abjad.Up, abjad.Down, abjad.Center, None)
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
        import abjad
        if format_specification in ('', 'storage'):
            return abjad.StorageFormatManager(self).get_storage_format()
        elif format_specification == 'lilypond':
            return self._get_lilypond_format()
        return str(self)

    def __illustrate__(self):
        r'''Illustrates articulation.

        Returns LilyPond file.
        '''
        import abjad
        note = abjad.Note("c'4")
        articulation = copy.copy(self)
        abjad.attach(articulation, note)
        lilypond_file = abjad.LilyPondFile.new(note)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    def __str__(self):
        r'''Gets string representation of articulation.

        Returns string.
        '''
        import abjad
        if self.name:
            string = self._shortcut_to_word.get(self.name)
            if not string:
                string = self.name
            if self.direction is None:
                direction = '-'
            else:
                direction = abjad.String.to_tridirectional_lilypond_symbol(
                    self.direction)
            return '{}\{}'.format(direction, string)
        else:
            return ''

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        if self.direction is not None:
            return '{!r}, {!r}'.format(self.name, self.direction)
        else:
            return repr(self.name)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        values = [self.name]
        if self.direction is not None:
            values.append(self.direction)
        return abjad.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_is_indented=False,
            )

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.right.articulations.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction of articulation.

        ..  container:: example

            Without direction:

            >>> articulation = abjad.Articulation('staccato')
            >>> articulation.direction is None
            True

        ..  container:: example

            With direction:

            >>> articulation = abjad.Articulation('staccato', direction=abjad.Up)
            >>> articulation.direction
            Up

        Returns ordinal constant or none.
        '''
        return self._direction

    @property
    def name(self):
        r'''Gets name of articulation.

        ..  container:: example

            Staccato:

            >>> articulation = abjad.Articulation('staccato')
            >>> articulation.name
            'staccato'

        ..  container:: example

            Tenuto:

            >>> articulation = abjad.Articulation('tenuto')
            >>> articulation.name
            'tenuto'

        Returns string.
        '''
        return self._name
