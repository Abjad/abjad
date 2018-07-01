import copy
import typing
from abjad import enums
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.top.attach import attach
from abjad.utilities.String import String


class Articulation(AbjadValueObject):
    r"""
    Articulation.

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

        >>> abjad.Articulation('staccato', direction=abjad.Up)
        Articulation('staccato', Up)

    .. container:: example

        Use ``attach()`` to attach articulations to notes, rests or chords:

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

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_format_slot',
        '_name',
        '_tweaks',
        )

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

    def __init__(
        self,
        name: str = None,
        *,
        direction: typing.Union[str, enums.VerticalAlignment] = None,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        if isinstance(name, type(self)):
            argument = name
            name = argument.name
            direction = direction or argument.direction
        name = str(name)
        if '\\' in name:
            direction, name = name.split('\\')
            direction = direction.strip()
            name = name.strip()
        self._name = name
        direction_ = String.to_tridirectional_ordinal_constant(direction)
        if direction_ is not None:
            assert isinstance(direction_, enums.VerticalAlignment), repr(direction_)
            assert direction_ in (enums.Up, enums.Down, enums.Center), repr(direction_)
        self._direction = direction_
        self._format_slot = 'after'
        self._tweaks = None
        LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __format__(self, format_specification='') -> str:
        """
        Formats articulation.

        Set ``format_specification`` to `''`, `'lilypond`' or `'storage'`.
        Interprets `''` equal to `'storage'`.
        """
        if format_specification in ('', 'storage'):
            return StorageFormatManager(self).get_storage_format()
        else:
            assert format_specification == 'lilypond'
            return self._get_lilypond_format()

    def __illustrate__(self):
        """
        Illustrates articulation.

        Returns LilyPond file.
        """
        note = abjad.Note("c'4")
        articulation = copy.copy(self)
        attach(articulation, note)
        lilypond_file = abjad.LilyPondFile.new(note)
        return lilypond_file

    def __str__(self) -> str:
        """
        Gets string representation of articulation.
        """
        if self.name:
            string = self._shortcut_to_word.get(self.name)
            if not string:
                string = self.name
            if self.direction is None:
                direction = String('-')
            else:
                direction_ = String.to_tridirectional_lilypond_symbol(
                    self.direction)
                assert isinstance(direction_, String), repr(direction)
                direction = direction_
            return f'{direction}\{string}'
        else:
            return ''

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.name]
        if self.direction is not None:
            values.append(self.direction)
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_is_indented=False,
            )

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[enums.VerticalAlignment]:
        """
        Gets direction of articulation.

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

        """
        return self._direction

    @property
    def name(self) -> str:
        """
        Gets name of articulation.

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

        """
        return self._name

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation('marcato')
            >>> abjad.tweak(articulation).color = 'blue'
            >>> abjad.attach(articulation, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                - \tweak color #blue
                -\marcato

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation(
            ...     'marcato',
            ...     tweaks=[('color', 'blue')],
            ...     )
            >>> abjad.attach(articulation, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                - \tweak color #blue
                -\marcato

        """
        return self._tweaks
