import typing
from abjad import enums
from abjad import typings
from abjad.core.Chord import Chord
from abjad.core.Component import Component
from abjad.core.Leaf import Leaf
from abjad.core.Note import Note
from abjad.core.Selection import Selection
from abjad.indicators.Dynamic import Dynamic
from abjad.indicators.DynamicTrend import DynamicTrend
from abjad.lilypondnames.LilyPondGrobOverride import LilyPondGrobOverride
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.Tag import Tag
from abjad.system.Wrapper import Wrapper
from abjad.top.attach import attach
from abjad.top.inspect import inspect
from abjad.top.select import select
from abjad.top.tweak import tweak
from abjad.utilities.Expression import Expression
from abjad.utilities.String import String
from .Spanner import Spanner


class Hairpin(Spanner):
    r"""
    Hairpin.

    ..  note:: ``abjad.Hairpin`` is deprecated. Use the ``abjad.hairpin()``
        factory function instead.

    ..  container:: example

        Crescendo:

        >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
        >>> hairpin = abjad.Hairpin('p < f')
        >>> abjad.attach(hairpin, voice[1:-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                r8
                d'8
                \<
                \p
                e'8
                f'8
                g'8
                a'8
                b'8
                \f
                r8
            }

        >>> for leaf in abjad.select(voice).leaves():
        ...     leaf, abjad.inspect(leaf).effective(abjad.Dynamic)
        ...
        (Rest('r8'), None)
        (Note("d'8"), None)
        (Note("e'8"), None)
        (Note("f'8"), None)
        (Note("g'8"), None)
        (Note("a'8"), None)
        (Note("b'8"), None)
        (Rest('r8'), None)

    ..  container:: example

        Decrescendo:

        >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
        >>> hairpin = abjad.Hairpin('f > p')
        >>> abjad.attach(hairpin, voice[1:-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                r8
                d'8
                \>
                \f
                e'8
                f'8
                g'8
                a'8
                b'8
                \p
                r8
            }

        >>> for leaf in abjad.select(voice).leaves():
        ...     leaf, abjad.inspect(leaf).effective(abjad.Dynamic)
        ...
        (Rest('r8'), None)
        (Note("d'8"), None)
        (Note("e'8"), None)
        (Note("f'8"), None)
        (Note("g'8"), None)
        (Note("a'8"), None)
        (Note("b'8"), None)
        (Rest('r8'), None)

    ..  container:: example

        Decrescendo al niente:

        >>> voice = abjad.Voice("c'2. r4")
        >>> hairpin = abjad.Hairpin('f > niente')
        >>> abjad.attach(hairpin, voice[:])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'2.
                - \tweak circled-tip ##t
                \>
                \f
                r4
                \!
            }

        >>> for leaf in abjad.select(voice).leaves():
        ...     leaf, abjad.inspect(leaf).effective(abjad.Dynamic)
        ...
        (Note("c'2."), None)
        (Rest('r4'), None)

    ..  container:: example

        Multiple hairpins enchained with dynamics:

        >>> voice = abjad.Voice("c'8 d' e' f' c' d' e' f' c'")
        >>> abjad.attach(abjad.Dynamic('p'), voice[0])
        >>> abjad.attach(abjad.Hairpin('<'), voice[:3])
        >>> abjad.attach(abjad.Dynamic('f'), voice[2])
        >>> abjad.attach(abjad.Hairpin('>'), voice[2:5])
        >>> abjad.attach(abjad.Dynamic('p'), voice[4])
        >>> abjad.attach(abjad.Hairpin('<'), voice[4:7])
        >>> abjad.attach(abjad.Dynamic('f'), voice[6])
        >>> abjad.attach(abjad.Hairpin('>'), voice[6:])
        >>> abjad.attach(abjad.Dynamic('p'), voice[8])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'8
                \p
                \<
                d'8
                e'8
                \f
                \>
                f'8
                c'8
                \p
                \<
                d'8
                e'8
                \f
                \>
                f'8
                c'8
                \p
            }

        >>> for leaf in abjad.select(voice).leaves():
        ...     leaf, abjad.inspect(leaf).effective(abjad.Dynamic)
        ...
        (Note("c'8"), Dynamic('p'))
        (Note("d'8"), Dynamic('p'))
        (Note("e'8"), Dynamic('f'))
        (Note("f'8"), Dynamic('f'))
        (Note("c'8"), Dynamic('p'))
        (Note("d'8"), Dynamic('p'))
        (Note("e'8"), Dynamic('f'))
        (Note("f'8"), Dynamic('f'))
        (Note("c'8"), Dynamic('p'))

    """

    ### CLASS VARIABLES ###

    _hairpin_shape_strings = (
        '<',
        '>',
        )

    __slots__ = (
        '_descriptor',
        '_direction',
        '_shape_string',
        '_start_dynamic',
        '_stop_dynamic',
        )

    _stop_command = r'\!'

    ### INITIALIZER ###

    def __init__(
        self,
        descriptor: str = None,
        *,
        direction: enums.VerticalAlignment = None,
        ) -> None:
        Spanner.__init__(self)
        direction_ = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction_
        self._descriptor: typing.Optional[str] = None
        if descriptor is not None:
            assert self._is_valid_descriptor(descriptor), repr(descriptor)
            result = self._parse_descriptor(descriptor)
            start_dynamic, shape_string, stop_dynamic = result
            self._descriptor = descriptor
            assert shape_string in ('<', '>')
            self._shape_string = shape_string
            if start_dynamic is not None:
                start_dynamic = Dynamic(start_dynamic)
            self._start_dynamic = start_dynamic
            if stop_dynamic is not None:
                stop_dynamic = Dynamic(stop_dynamic)
            self._stop_dynamic = stop_dynamic
        else:
            self._descriptor = None
            self._shape_string = None
            self._start_dynamic = None
            self._stop_dynamic = None

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        r"""
        Is true when hairpin equals ``argument``.

        ..  container:: example

            >>> hairpin_1 = abjad.Hairpin('p < f')
            >>> hairpin_2 = abjad.Hairpin('p < f')
            >>> hairpin_3 = abjad.Hairpin('f > p')

            >>> hairpin_1 == hairpin_1
            True

            >>> hairpin_1 == hairpin_2
            True

            >>> hairpin_1 == hairpin_3
            False

            >>> hairpin_2 == hairpin_1
            True

            >>> hairpin_2 == hairpin_2
            True

            >>> hairpin_2 == hairpin_3
            False

            >>> hairpin_3 == hairpin_1
            False

            >>> hairpin_3 == hairpin_2
            False

            >>> hairpin_3 == hairpin_3
            True

        """
        if not isinstance(argument, type(self)):
            return False
        if (self.start_dynamic == argument.start_dynamic and
            self.stop_dynamic == argument.stop_dynamic):
            return True
        return False

    def __hash__(self) -> int:
        """
        Hashes hairpin.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, argument):
        if isinstance(argument, (Chord, Note)):
            return True
        assert all(isinstance(_, Leaf) for _ in argument)
        leaves = select(argument).leaves()
        return 1 <= len(leaves)

    @staticmethod
    def _circled_tip():
        return LilyPondGrobOverride(
            grob_name='Hairpin',
            once=True,
            property_path='circled-tip',
            value=True,
            )

    def _copy_keywords(self, new):
        Spanner._copy_keywords(self, new)
        new._descriptor = self.descriptor
        new._direction = self.direction
        new._shape_string = self.shape_string
        new._start_dynamic = self.start_dynamic
        new._stop_dynamic = self.stop_dynamic

    def _get_directed_start_dynamic(self):
        string = rf'\{self.start_dynamic.name}'
        string = self._add_direction(string)
        return string

    def _get_directed_stop_dynamic(self):
        string = rf'\{self.stop_dynamic.name}'
        string = self._add_direction(string)
        return string

    def _get_lilypond_format_bundle(self, leaf):
        assert self.descriptor is not None
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_lone_pleaf():
            string = self._get_directed_start_dynamic()
            bundle.after.spanner_starts.append(string)
            return bundle
        if leaf is self[0] and self._has_niente():
            override = self._circled_tip()
            string = override.tweak_string()
            bundle.after.spanner_starts.append(string)
        if leaf is self[0]:
            strings = self._tweaked_start_command_strings()
            bundle.after.spanner_starts.extend(strings)
            if self._has_sounding_start_dynamic():
                string = self._get_directed_start_dynamic()
                bundle.after.spanner_starts.append(string)
        if leaf is self[-1]:
            string = self._stop_command_string()
            if string is not None:
                bundle.after.spanner_stops.append(string)
        return bundle

    def _has_niente(self):
        if self.start_dynamic and self.start_dynamic.name == 'niente':
            return True
        if self.stop_dynamic and self.stop_dynamic.name == 'niente':
            return True
        return False

    def _has_sounding_start_dynamic(self):
        if self.start_dynamic and self.start_dynamic.name != 'niente':
            return True
        return False

    def _has_sounding_stop_dynamic(self):
        if self.stop_dynamic and self.stop_dynamic.name != 'niente':
            return True
        return False

    def _is_lone_pleaf(self):
        if len(self) == 1 and isinstance(self[0], (Chord, Note)):
            return True
        return False

    def _is_valid_descriptor(self, descriptor):
        start, shape, stop = self._parse_descriptor(descriptor)
        if shape not in self._hairpin_shape_strings:
            return False
        if start is not None:
            try:
                start = Dynamic(start)
            except AssertionError:
                return False
        if stop is not None:
            try:
                stop = Dynamic(stop)
            except AssertionError:
                return False
        if start is not None and stop is not None:
            start_ordinal = start.ordinal
            stop_ordinal = stop.ordinal
            if shape == '<' and not start_ordinal < stop_ordinal:
                return False
            if shape == '>' and not start_ordinal > stop_ordinal:
                return False
        return True

    @staticmethod
    def _parse_descriptor(descriptor):
        assert isinstance(descriptor, str)
        parts = descriptor.split()
        num_parts = len(parts)
        start, shape, stop = None, None, None
        if parts[0] in ('<', '>'):
            assert 1 <= num_parts <= 2
            if num_parts == 1:
                shape = parts[0]
            else:
                shape = parts[0]
                stop = parts[1]
        else:
            assert 2 <= num_parts <= 3
            if num_parts == 2:
                start = parts[0]
                shape = parts[1]
            else:
                start = parts[0]
                shape = parts[1]
                stop = parts[2]
        assert shape in ('<', '>')
        return start, shape, stop

    def _stop_command_string(self):
        leaf = self[-1]
        if self._has_sounding_stop_dynamic():
            string = self._get_directed_stop_dynamic()
            return string
        effective_dynamic = inspect(leaf).effective(Dynamic)
        if effective_dynamic is None or effective_dynamic.name == 'niente':
            string = self._stop_command
            return string
        if effective_dynamic not in inspect(leaf).wrappers():
            found_match = False
            for indicator in inspect(leaf).indicators(Dynamic):
                if indicator == effective_dynamic:
                    found_match = True
            if not found_match:
                string = self._stop_command
                return string
        return None

    def _tweaked_start_command_strings(self):
        strings = []
        contributions = tweak(self)._list_format_contributions()
        strings.extend(contributions)
        string = rf'\{self.shape_string}'
        string = self._add_direction(string)
        strings.append(string)
        return strings

    ### PUBLIC PROPERTIES ###

    @property
    def descriptor(self) -> typing.Optional[str]:
        r"""
        Gets descriptor.

        ..  container:: example

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin('p < f')
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    r8
                    d'8
                    \<
                    \p
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8
                    \f
                    r8
                }

            >>> hairpin.descriptor
            'p < f'

        """
        return self._descriptor

    @property
    def direction(self) -> typing.Optional[String]:
        r"""
        Gets direction.

        ..  container:: example

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin('p < f', direction=abjad.Up)
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    r8
                    d'8
                    ^ \<
                    ^ \p
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8
                    ^ \f
                    r8
                }

            >>> hairpin.direction
            '^'

        """
        return self._direction

    @property
    def shape_string(self) -> str:
        r"""
        Gets shape string.

        ..  container:: example

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin('p < f')
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    r8
                    d'8
                    \<
                    \p
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8
                    \f
                    r8
                }

            >>> hairpin.shape_string
            '<'

        """
        return self._shape_string

    @property
    def start_dynamic(self) -> typing.Optional[Dynamic]:
        r"""
        Gets start dynamic.

        ..  container:: example

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin('p < f')
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    r8
                    d'8
                    \<
                    \p
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8
                    \f
                    r8
                }

            >>> hairpin.start_dynamic
            Dynamic('p')

        """
        return self._start_dynamic

    @property
    def stop_dynamic(self) -> typing.Optional[Dynamic]:
        r"""
        Gets stop dynamic.

        ..  container:: example

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin('p < f')
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    r8
                    d'8
                    \<
                    \p
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8
                    \f
                    r8
                }

            >>> hairpin.stop_dynamic
            Dynamic('f')

        """
        return self._stop_dynamic

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> hairpin = abjad.Hairpin('p < f')
            >>> abjad.tweak(hairpin).color = 'blue'
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(hairpin, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \<
                    \p
                    d'4
                    e'4
                    f'4
                    \f
                }

        """
        return super().tweaks

    ### PUBLIC METHODS ###

def hairpin(
    descriptor: str,
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.Selector = 'abjad.select().leaves()',
    ) -> None:
    r"""
    Attaches hairpin indicators.

    ..  container:: example

        With three-part string descriptor:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.hairpin('p < f', staff[:])
        >>> abjad.override(staff[0]).dynamic_line_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override DynamicLineSpanner.staff-padding = #4
                c'4
                \p
                \<
                d'4
                e'4
                f'4
                \f
            }

    ..  container:: example

        With dynamic objects:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start = abjad.Dynamic('niente', command=r'\!')
        >>> trend = abjad.DynamicTrend('o<|')
        >>> abjad.tweak(trend).color = 'blue'
        >>> stop = abjad.Dynamic('"f"')
        >>> abjad.hairpin([start, trend, stop], staff[:])
        >>> abjad.override(staff[0]).dynamic_line_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override DynamicLineSpanner.staff-padding = #4
                c'4
                \!
                - \tweak color #blue
                - \tweak circled-tip ##t
                - \tweak stencil #abjad-flared-hairpin
                \<
                d'4
                e'4
                f'4
                _ #(make-dynamic-script
                    (markup
                        #:whiteout
                        #:line (
                            #:general-align Y -2 #:normal-text #:larger "“"
                            #:hspace -0.4
                            #:dynamic "f"
                            #:hspace -0.2
                            #:general-align Y -2 #:normal-text #:larger "”"
                            )
                        )
                    )
            }

    """
    import abjad

    indicators: typing.List = []
    start_dynamic: typing.Optional[Dynamic]
    dynamic_trend: typing.Optional[DynamicTrend]
    stop_dynamic: typing.Optional[Dynamic]
    known_shapes = DynamicTrend('<').known_shapes
    if isinstance(descriptor, str):
        for string in descriptor.split():
            if string in known_shapes:
                dynamic_trend = DynamicTrend(string)
                indicators.append(dynamic_trend)
            else:
                dynamic = Dynamic(string)
                indicators.append(dynamic)
    else:
        assert isinstance(descriptor, list), repr(descriptor)
        indicators = descriptor

    start_dynamic, dynamic_trend, stop_dynamic = None, None, None
    if len(indicators) == 1:
        if isinstance(indicators[0], Dynamic):
            start_dynamic = indicators[0]
        else:
            dynamic_trend = indicators[0]
    elif len(indicators) == 2:
        if isinstance(indicators[0], Dynamic):
            start_dynamic = indicators[0]
            dynamic_trend = indicators[1]
        else:
            dynamic_trend = indicators[0]
            stop_dynamic = indicators[1]
    elif len(indicators) == 3:
        start_dynamic, dynamic_trend, stop_dynamic = indicators
    else:
        raise Exception(indicators)

    assert isinstance(start_dynamic, Dynamic), repr(start_dynamic)

    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]

    if start_dynamic is not None:
        attach(start_dynamic, start_leaf)
    if dynamic_trend is not None:
        attach(dynamic_trend, start_leaf)
    if stop_dynamic is not None:
        attach(stop_dynamic, stop_leaf)
