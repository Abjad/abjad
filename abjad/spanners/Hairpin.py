import typing
from abjad import typings
from .Spanner import Spanner
from abjad import enumerations
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


class Hairpin(Spanner):
    r"""
    Hairpin.

    ..  note:: Conventional (nonpiecewise) hairpins are deprecated.
        Use piecewise hairpins instead.

    ..  container:: example

        Conventional (nonpiecewise) crescendo:

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
        ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
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

        Conventional (nonpiecewise) diminuendo:

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
        ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
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

        Diminuendi al niente.

        Piecewise:

        >>> voice = abjad.Voice("c'2. r4")
        >>> hairpin = abjad.Hairpin()
        >>> abjad.attach(hairpin, voice[:])
        >>> hairpin.attach(abjad.Dynamic('f'), hairpin[0])
        >>> hairpin.attach(abjad.Dynamic('niente'), hairpin[-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'2.
                \f
                - \tweak circled-tip ##t
                \>
                r4
                \!
            }

        >>> for leaf in abjad.select(voice).leaves():
        ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
        ...
        (Note("c'2."), Dynamic('f'))
        (Rest('r4'), Dynamic('niente', direction=Down, name_is_textual=True))

        Conventional (nonpiecewise):

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
        ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
        ...
        (Note("c'2."), None)
        (Rest('r4'), None)

    ..  container:: example

        Multiple conventional (nonpiecewise) hairpins enchained with dynamics:

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
        ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
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


    ..  container:: example

        Piecewise hairpins work with effort dynamics:

        >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
        >>> hairpin = abjad.Hairpin()
        >>> abjad.attach(hairpin, voice[1:-1])
        >>> hairpin.attach(abjad.Dynamic('"p"'), hairpin[0])
        >>> hairpin.attach(abjad.Dynamic('"f"'), hairpin[-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                r8
                d'8
                _ #(make-dynamic-script
                    (markup
                        #:whiteout
                        #:line (
                            #:general-align Y -2 #:normal-text #:larger "“"
                            #:hspace -0.1
                            #:dynamic "p"
                            #:hspace -0.25
                            #:general-align Y -2 #:normal-text #:larger "”"
                            )
                        )
                    )
                \<
                e'8
                f'8
                g'8
                a'8
                b'8
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
                r8
            }

        >>> for leaf in abjad.select(voice).leaves():
        ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
        ...
        (Rest('r8'), None)
        (Note("d'8"), Dynamic('"p"', direction=Down))
        (Note("e'8"), Dynamic('"p"', direction=Down))
        (Note("f'8"), Dynamic('"p"', direction=Down))
        (Note("g'8"), Dynamic('"p"', direction=Down))
        (Note("a'8"), Dynamic('"p"', direction=Down))
        (Note("b'8"), Dynamic('"f"', direction=Down))
        (Rest('r8'), Dynamic('"f"', direction=Down))

    """

    ### CLASS VARIABLES ###

    _hairpin_shape_strings = (
        '<',
        '>',
        )

    __slots__ = (
        '_context',
        '_descriptor',
        '_direction',
        '_shape_string',
        '_start_dynamic',
        '_start_dynamic_is_textual',
        '_stop_dynamic',
        '_stop_dynamic_is_textual',
        )

    _stop_command = r'\!'

    ### INITIALIZER ###

    def __init__(
        self,
        descriptor: str = None,
        *,
        context: str = None,
        direction: enumerations.VerticalAlignment = None,
        start_dynamic_is_textual: bool = None,
        stop_dynamic_is_textual: bool = None,
        ) -> None:
        Spanner.__init__(self)
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        direction_ = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction_
        if start_dynamic_is_textual is not None:
            start_dynamic_is_textual = bool(start_dynamic_is_textual)
        self._start_dynamic_is_textual = start_dynamic_is_textual
        if stop_dynamic_is_textual is not None:
            stop_dynamic_is_textual = bool(stop_dynamic_is_textual)
        self._stop_dynamic_is_textual = stop_dynamic_is_textual
        self._descriptor: typing.Optional[str] = None
        if descriptor is not None:
            assert self._is_valid_descriptor(descriptor), repr(descriptor)
            result = self._parse_descriptor(descriptor)
            start_dynamic, shape_string, stop_dynamic = result
            self._descriptor = descriptor
            assert shape_string in ('<', '>')
            self._shape_string = shape_string
            if start_dynamic is not None:
                start_dynamic = Dynamic(
                    start_dynamic,
                    name_is_textual=self.start_dynamic_is_textual,
                    )
            self._start_dynamic = start_dynamic
            if stop_dynamic is not None:
                stop_dynamic = Dynamic(
                    stop_dynamic,
                    name_is_textual=self.stop_dynamic_is_textual,
                    )
            self._stop_dynamic = stop_dynamic
        else:
            self._descriptor = None
            self._shape_string = None
            self._start_dynamic = None
            self._stop_dynamic = None

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

    def _make_circled_tip_tweaks(self, leaf):
        override = self._circled_tip()
        string = override.tweak_string()
        if self._left_broken == 'niente' or self._right_broken == 'niente':
            return [string]
        dynamic = self._get_piecewise_dynamic(leaf)
        if not dynamic:
            return []
        if self._right_broken and dynamic.name == 'niente':
            return [string]
        next_dynamic = self._get_next_piecewise_dynamic_from(leaf)
        if not next_dynamic:
            return []
        if dynamic.name == 'niente' or next_dynamic.name == 'niente':
            return [string]
        return []

    def _add_piecewise_dynamic(self, leaf, bundle):
        dynamic = self._get_piecewise_dynamic(leaf)
        if dynamic is None:
            return
        if dynamic.name == 'niente' and leaf is self[0] and self._left_broken:
            string = self._stop_command
        elif dynamic.name == 'niente' and leaf is self[0]:
            return
        elif dynamic.name == 'niente' and leaf is not self[0]:
            string = self._stop_command
        else:
            string = dynamic._get_lilypond_format()
        string = self._add_direction(string)
        previous_dynamic = self._get_previous_piecewise_dynamic_from(leaf)
        if previous_dynamic is None:
            bundle.after.spanner_starts.append(string)
        else:
            bundle.after.spanner_stops.append(string)

    def _add_piecewise_hairpin_start(self, leaf, bundle, tweaks):
        if (leaf is self[0] and
            self._left_broken is not None and
            self._is_long_enough()):
            string = '\\' + self._left_broken
            string = self._add_direction(string)
            strings = tweaks + [string]
            strings = self._tag_hide(strings)
        else:
            dynamic = self._get_piecewise_dynamic(leaf)
            if dynamic is None:
                return
            next_dynamic = self._get_next_piecewise_dynamic_from(leaf)
            if next_dynamic is None:
                if self._right_broken is not None:
                    right_broken = self._right_broken
                    if right_broken == 'niente':
                        right_broken = '>'
                    assert right_broken in ('<', '>')
                    string = '\\' + right_broken
                    string = self._add_direction(string)
                    strings = tweaks + [string]
                    if leaf is self[-1]:
                        strings = self._tag_show(strings)
                else:
                    return
            elif dynamic.ordinal == next_dynamic.ordinal:
                return
            elif dynamic.ordinal < next_dynamic.ordinal:
                string = r'\<'
                string = self._add_direction(string)
                strings = tweaks + [string]
            elif next_dynamic.ordinal < dynamic.ordinal:
                string = r'\>'
                string = self._add_direction(string)
                strings = tweaks + [string]
        bundle.after.spanner_starts.extend(strings)

    def _add_piecewise_right_broken_hairpin_stop(self, leaf, bundle):
        if self._right_broken is None:
            return
        if leaf is not self[-1]:
            return
        if leaf is self[0]:
            return
        strings = [self._stop_command]
        strings = self._tag_hide(strings)
        bundle.after.spanner_stops.extend(strings)

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
        if self.descriptor is None:
            return self._get_piecewise_lilypond_format_bundle(leaf)
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
            strings = self.start_command()
            bundle.after.spanner_starts.extend(strings)
            if self._has_sounding_start_dynamic():
                string = self._get_directed_start_dynamic()
                bundle.after.spanner_starts.append(string)
        if leaf is self[-1]:
            string = self.stop_command()
            if string is not None:
                bundle.after.spanner_stops.append(string)
        return bundle

    def _get_next_piecewise_dynamic_from(self, leaf):
        index = self._index(leaf)
        number = index + 1
        for leaf in self[number:]:
            if self._has_piecewise_indicator(leaf, Dynamic):
                return self._get_piecewise_indicator(leaf, Dynamic)

    def _get_piecewise_dynamic(self, leaf):
        if self._has_piecewise_indicator(leaf, Dynamic):
            return self._get_piecewise_indicator(leaf, Dynamic)

    def _get_piecewise_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        tweaks = self._make_circled_tip_tweaks(leaf)
        tweaks_ = tweak(self)._list_format_contributions()
        tweaks.extend(tweaks_)
        self._add_piecewise_dynamic(leaf, bundle)
        self._add_piecewise_hairpin_start(leaf, bundle, tweaks)
        self._add_piecewise_right_broken_hairpin_stop(leaf, bundle)
        if self._is_my_only(leaf):
            bundle.after.spanner_starts.extend(bundle.after.spanner_stops)
            bundle.after.spanner_stops[:] = []
        return bundle

    def _get_previous_piecewise_dynamic_from(self, leaf):
        index = self._index(leaf)
        for leaf in reversed(self[:index]):
            if self._has_piecewise_indicator(leaf, Dynamic):
                return self._get_piecewise_indicator(leaf, Dynamic)

    def _has_niente(self):
        if self.start_dynamic and self.start_dynamic.name == 'niente':
            return True
        if self.stop_dynamic and self.stop_dynamic.name == 'niente':
            return True
        if self._right_broken == 'niente':
            return True
        if self._left_broken == 'niente':
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

    @staticmethod
    def _is_hairpin_shape_string(argument):
        return argument in Hairpin._hairpin_shape_strings

    @staticmethod
    def _is_hairpin_token(argument):
        """
        Is true when ``argument`` is hairpin token.

        >>> abjad.Hairpin._is_hairpin_token(('', '<', ''))
        True

        >>> abjad.Hairpin._is_hairpin_token(('p', '<', 'f'))
        True

        >>> abjad.Hairpin._is_hairpin_token(('p', '@', 'f'))
        False

        >>> abjad.Hairpin._is_hairpin_token(('p', '>', 'f'))
        False

        """
        if (isinstance(argument, tuple) and
            len(argument) == 3 and
            (not argument[0] or Dynamic.is_dynamic_name(argument[0]))
            and Hairpin._is_hairpin_shape_string(argument[1]) and
            (not argument[2] or Dynamic.is_dynamic_name(argument[2]))):
            if argument[0] and argument[2]:
                start_ordinal = Dynamic.dynamic_name_to_dynamic_ordinal(
                    argument[0])
                stop_ordinal = Dynamic.dynamic_name_to_dynamic_ordinal(
                    argument[2])
                if argument[1] == '<':
                    return start_ordinal < stop_ordinal
                else:
                    return stop_ordinal < start_ordinal
            else:
                return True
        else:
            return False
                
    def _is_lone_pleaf(self):
        if len(self) == 1 and isinstance(self[0], (Chord, Note)):
            return True
        return False

    def _is_long_enough(self):
        if 1 < len(self):
            return True
        return False

    def _is_trending(self, leaf):
        if leaf not in self:
            return False
        return True

    def _is_valid_descriptor(self, descriptor):
        start, shape, stop = self._parse_descriptor(descriptor)
        if shape not in self._hairpin_shape_strings:
            return False
        if start is not None:
            try:
                start = Dynamic(
                    start,
                    name_is_textual=self.start_dynamic_is_textual,
                    )
            except AssertionError:
                return False
        if stop is not None:
            try:
                stop = Dynamic(
                    stop,
                    name_is_textual=self.stop_dynamic_is_textual,
                    )
            except AssertionError:
                return False
        if (getattr(start, 'name_is_textual', None) or
            getattr(stop, 'name_is_textual', None)):
            return True
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

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> typing.Optional[str]:
        r"""
        Gets context name (for piecewise attach).

        ..  container:: example

            Simultaneous hairpins on a single staff:

            >>> voice_1 = abjad.Voice("e'8 f' g' a' f' g' a' b' g'")
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
            >>> grob_proxy = abjad.override(voice_1).dynamic_line_spanner
            >>> grob_proxy.direction = abjad.Up
            >>> grob_proxy.staff_padding = 4
            >>> hairpin_1 = abjad.Hairpin(context='Voice')
            >>> abjad.attach(hairpin_1, voice_1[:])
            >>> hairpin_1.attach(abjad.Dynamic('mf'), hairpin_1[0])
            >>> hairpin_1.attach(abjad.Dynamic('f'), hairpin_1[2])
            >>> hairpin_1.attach(abjad.Dynamic('mf'), hairpin_1[4])
            >>> hairpin_1.attach(abjad.Dynamic('f'), hairpin_1[6])
            >>> hairpin_1.attach(abjad.Dynamic('mf'), hairpin_1[8])
            >>> voice_2 = abjad.Voice("c'2 b2 ~ b8")
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
            >>> grob_proxy = abjad.override(voice_2).dynamic_line_spanner
            >>> grob_proxy.staff_padding = 6
            >>> hairpin_2 = abjad.Hairpin(context='Voice')
            >>> abjad.attach(hairpin_2, voice_2[:])
            >>> hairpin_2.attach(abjad.Dynamic('pp'), hairpin_2[0])
            >>> hairpin_2.attach(abjad.Dynamic('p'), hairpin_2[-1])
            >>> staff = abjad.Staff([voice_1, voice_2], is_simultaneous=True)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                <<
                    \new Voice
                    \with
                    {
                        \override DynamicLineSpanner.direction = #up
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        \voiceOne
                        e'8
                        \mf
                        \<
                        f'8
                        g'8
                        \f
                        \>
                        a'8
                        f'8
                        \mf
                        \<
                        g'8
                        a'8
                        \f
                        \>
                        b'8
                        g'8
                        \mf
                    }
                    \new Voice
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #6
                    }
                    {
                        \voiceTwo
                        c'2
                        \pp
                        \<
                        b2
                        ~
                        b8
                        \p
                    }
                >>

            >>> for leaf in abjad.select(voice_1).leaves():
            ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
            ...
            (Note("e'8"), Dynamic('mf'))
            (Note("f'8"), Dynamic('mf'))
            (Note("g'8"), Dynamic('f'))
            (Note("a'8"), Dynamic('f'))
            (Note("f'8"), Dynamic('mf'))
            (Note("g'8"), Dynamic('mf'))
            (Note("a'8"), Dynamic('f'))
            (Note("b'8"), Dynamic('f'))
            (Note("g'8"), Dynamic('mf'))

            >>> for leaf in abjad.select(voice_2).leaves():
            ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
            ...
            (Note("c'2"), Dynamic('pp'))
            (Note('b2'), Dynamic('pp'))
            (Note('b8'), Dynamic('p'))

        """
        return self._context

    def cross_segment_examples(self):
        r"""
        Cross-segment examples.

        ..  container:: example

            Cross-segment example #1 (one-to-one):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[-1:], right_broken='<')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[-1])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    d'4
                    e'4
                    f'4
                    \p
                %@% \<                                            %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:1], left_broken='<')
            >>> hairpin.attach(abjad.Dynamic('f'), hairpin[0])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \f
                    d'4
                    e'4
                    f'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        \p
                        \<                                        %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                        \f
                        d'4
                        e'4
                        f'4
                    }
                }

        ..  container:: example

            Cross-segment example #2 (one-to-many):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[-1:], right_broken='<')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[-1])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    d'4
                    e'4
                    f'4
                    \p
                %@% \<                                            %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:], left_broken='<')
            >>> hairpin.attach(abjad.Dynamic('f'), hairpin[-1])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \<                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    d'4
                    e'4
                    f'4
                    \f
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        \p
                        \<                                        %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                    %%% \<                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                        d'4
                        e'4
                        f'4
                        \f
                    }
                }

        ..  container:: example

            Cross-segment example #3 (many-to-one):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[:], right_broken='<')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[0])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    \p
                    \<
                    d'4
                    e'4
                    f'4
                    \!                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:1], left_broken='<')
            >>> hairpin.attach(abjad.Dynamic('f'), hairpin[0])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \f
                    d'4
                    e'4
                    f'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        \p
                        \<
                        d'4
                        e'4
                        f'4
                    %%% \!                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                        \f
                        d'4
                        e'4
                        f'4
                    }
                }

        ..  container:: example

            Cross-segment example #4 (many-to-many):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[:], right_broken='<')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[0])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    \p
                    \<
                    d'4
                    e'4
                    f'4
                    \!                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:], left_broken='<')
            >>> hairpin.attach(abjad.Dynamic('f'), hairpin[-1])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \<                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    d'4
                    e'4
                    f'4
                    \f
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        \p
                        \<
                        d'4
                        e'4
                        f'4
                    %%% \!                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                    %%% \<                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                        d'4
                        e'4
                        f'4
                        \f
                    }
                }

        ..  container:: example

            Cross-segment example #5 (one-to-one dal niente)

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[-1:], right_broken='<')
            >>> hairpin.attach(abjad.Dynamic('niente'), hairpin[-1])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    d'4
                    e'4
                    f'4
                %@% - \tweak circled-tip ##t                      %! SHOW_TO_JOIN_BROKEN_SPANNERS
                %@% \<                                            %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:1], left_broken='<')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[0])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \p
                    d'4
                    e'4
                    f'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        - \tweak circled-tip ##t                  %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                        \<                                        %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                        \p
                        d'4
                        e'4
                        f'4
                    }
                }

        ..  container:: example

            Cross-segment example #6 (one-to-many dal niente)

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[-1:], right_broken='<')
            >>> hairpin.attach(abjad.Dynamic('niente'), hairpin[-1])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    d'4
                    e'4
                    f'4
                %@% - \tweak circled-tip ##t                      %! SHOW_TO_JOIN_BROKEN_SPANNERS
                %@% \<                                            %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:], left_broken='<')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[-1])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \<                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    d'4
                    e'4
                    f'4
                    \p
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        - \tweak circled-tip ##t                  %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                        \<                                        %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                    %%% \<                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                        d'4
                        e'4
                        f'4
                        \p
                    }
                }

        ..  container:: example

            Cross-segment example #7 (many-to-one dal niente)

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[:], right_broken='<')
            >>> hairpin.attach(abjad.Dynamic('niente'), hairpin[0])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    - \tweak circled-tip ##t
                    \<
                    d'4
                    e'4
                    f'4
                    \!                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:1], left_broken='<')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[0])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \p
                    d'4
                    e'4
                    f'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        - \tweak circled-tip ##t
                        \<
                        d'4
                        e'4
                        f'4
                    %%% \!                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                        \p
                        d'4
                        e'4
                        f'4
                    }
                }

        ..  container:: example

            Cross-segment example #8 (many-to-many dal niente)

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[:], right_broken='<')
            >>> hairpin.attach(abjad.Dynamic('niente'), hairpin[0])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    - \tweak circled-tip ##t
                    \<
                    d'4
                    e'4
                    f'4
                    \!                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:], left_broken='<')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[-1])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \<                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    d'4
                    e'4
                    f'4
                    \p
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        - \tweak circled-tip ##t
                        \<
                        d'4
                        e'4
                        f'4
                    %%% \!                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                    %%% \<                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                        d'4
                        e'4
                        f'4
                        \p
                    }
                }

        ..  container:: example

            Cross-segment example #9 (one-to-one al niente)

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[-1:], right_broken='niente')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[-1])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    d'4
                    e'4
                    f'4
                    \p
                %@% - \tweak circled-tip ##t                      %! SHOW_TO_JOIN_BROKEN_SPANNERS
                %@% \>                                            %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:1], left_broken='>')
            >>> hairpin.attach(abjad.Dynamic('niente'), hairpin[0])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \!
                    d'4
                    e'4
                    f'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        \p
                        - \tweak circled-tip ##t                  %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                        \>                                        %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                        \!
                        d'4
                        e'4
                        f'4
                    }
                }

        ..  container:: example

            Cross-segment example #10 (one-to-many al niente)

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[-1:], right_broken='niente')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[-1])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    d'4
                    e'4
                    f'4
                    \p
                %@% - \tweak circled-tip ##t                      %! SHOW_TO_JOIN_BROKEN_SPANNERS
                %@% \>                                            %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:], left_broken='>')
            >>> hairpin.attach(abjad.Dynamic('niente'), hairpin[-1])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \>                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    d'4
                    e'4
                    f'4
                    \!
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        \p
                        - \tweak circled-tip ##t                  %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                        \>                                        %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                    %%% \>                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                        d'4
                        e'4
                        f'4
                        \!
                    }
                }

        ..  container:: example

            Cross-segment example #11 (many-to-one al niente)

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[:], right_broken='niente')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[0])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    \p
                    - \tweak circled-tip ##t
                    \>
                    d'4
                    e'4
                    f'4
                    \!                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:1], left_broken='>')
            >>> hairpin.attach(abjad.Dynamic('niente'), hairpin[-1])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \!
                    d'4
                    e'4
                    f'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        \p
                        - \tweak circled-tip ##t
                        \>
                        d'4
                        e'4
                        f'4
                    %%% \!                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                        \!
                        d'4
                        e'4
                        f'4
                    }
                }

        ..  container:: example

            Cross-segment example #12 (many-to-many al niente)

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_1[:], right_broken='niente')
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[0])
            >>> abjad.override(segment_1).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'4
                    \p
                    - \tweak circled-tip ##t
                    \>
                    d'4
                    e'4
                    f'4
                    \!                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, segment_2[:], left_broken='>')
            >>> hairpin.attach(abjad.Dynamic('niente'), hairpin[-1])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \>                                            %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    d'4
                    e'4
                    f'4
                    \!
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    \with
                    {
                        \override DynamicLineSpanner.staff-padding = #4
                    }
                    {
                        c'4
                        \p
                        - \tweak circled-tip ##t
                        \>
                        d'4
                        e'4
                        f'4
                    %%% \!                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                    }
                    \context Voice = "MainVoice"
                    {
                        c'4
                    %%% \>                                        %! HIDE_TO_JOIN_BROKEN_SPANNERS
                        d'4
                        e'4
                        f'4
                        \!
                    }
                }

        """
        pass

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
    def start_dynamic_is_textual(self) -> typing.Optional[bool]:
        r"""
        Is true when start dynamic is textual.

        ..  container:: example

            Conventional:

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin(
            ...     'appena_udibile < f',
            ...     start_dynamic_is_textual=True,
            ...     )
            >>> abjad.attach(hairpin, voice[1:-1])

            Only LilyPond output appears below because the example command
            is meant to be user-defined:

            >>> abjad.f(voice)
            \new Voice
            {
                r8
                d'8
                \<
                \appena_udibile
                e'8
                f'8
                g'8
                a'8
                b'8
                \f
                r8
            }

            >>> hairpin.start_dynamic_is_textual
            True

        ..  container:: example

            Piecewise with noncommand start dynamic:

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> barely_audible = abjad.Dynamic(
            ...     'barely audible',
            ...     name_is_textual=True,
            ...     ordinal=-99,
            ...     )
            >>> hairpin.attach(barely_audible, voice[1])
            >>> hairpin.attach(abjad.Dynamic('f'), voice[-2])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    r8
                    d'8
                    _ #(make-dynamic-script (markup #:whiteout #:normal-text #:italic "barely audible"))
                    \<
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8
                    \f
                    r8
                }

        ..  container:: example

            Piecewise with command (user-defined) start dynamic:

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> barely_audible = abjad.Dynamic(
            ...     'barely audible',
            ...     command=r'\barely_audible',
            ...     name_is_textual=True,
            ...     ordinal=-99,
            ...     )
            >>> hairpin.attach(barely_audible, voice[1])
            >>> hairpin.attach(abjad.Dynamic('f'), voice[-2])

            Only LilyPond output appears below because the example command
            is meant to be user-defined:

            >>> abjad.f(voice)
            \new Voice
            {
                r8
                d'8
                \barely_audible
                \<
                e'8
                f'8
                g'8
                a'8
                b'8
                \f
                r8
            }

        """
        return self._start_dynamic_is_textual

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
    def stop_dynamic_is_textual(self) -> typing.Optional[bool]:
        r"""
        Is true when stop dynamic is textual.

        ..  container:: example

            Piecewise with noncommand stop dynamic:

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> extremely_loud = abjad.Dynamic(
            ...     'extremely loud',
            ...     name_is_textual=True,
            ...     ordinal=99,
            ...     )
            >>> hairpin.attach(abjad.Dynamic('p'), voice[1])
            >>> hairpin.attach(extremely_loud, voice[-2])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    r8
                    d'8
                    \p
                    \<
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8
                    _ #(make-dynamic-script (markup #:whiteout #:normal-text #:italic "extremely loud"))
                    r8
                }

        ..  container:: example

            Piecewise with command (user-defined) stop dynamic:

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> extremely_loud = abjad.Dynamic(
            ...     'extremely loud',
            ...     command=r'\extremely_loud',
            ...     name_is_textual=True,
            ...     ordinal=99,
            ...     )
            >>> hairpin.attach(abjad.Dynamic('p'), voice[1])
            >>> hairpin.attach(extremely_loud, voice[-2])

            Only LilyPond output appears below because the example command
            is meant to be user-defined:

            >>> abjad.f(voice)
            \new Voice
            {
                r8
                d'8
                \p
                \<
                e'8
                f'8
                g'8
                a'8
                b'8
                \extremely_loud
                r8
            }

        """
        return self._stop_dynamic_is_textual

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks.

        ..  container:: example

            Tweaks work with piecewise hairpins:

            >>> hairpin = abjad.Hairpin()
            >>> abjad.tweak(hairpin).color = 'blue'
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(hairpin, staff[:])
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[0])
            >>> hairpin.attach(abjad.Dynamic('f'), hairpin[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \p
                    - \tweak color #blue
                    \<
                    d'4
                    e'4
                    f'4
                    \f
                }

        """
        return super().tweaks

    ### PUBLIC METHODS ###

    def attach(
        self,
        indicator,
        leaf: Leaf,
        deactivate: bool = None,
        tag: typing.Union[str, Tag] = None,
        wrapper: bool = None,
        ) -> typing.Optional[Wrapper]:
        r"""
        Attaches ``indicator`` to ``leaf`` in spanner.

        ..  container:: example

            >>> voice = abjad.Voice("c'8 d' e' f' c' d' e' f' c'")
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, voice[:])
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[0])
            >>> hairpin.attach(abjad.Dynamic('f'), hairpin[2])
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[4])
            >>> hairpin.attach(abjad.Dynamic('f'), hairpin[6])
            >>> hairpin.attach(abjad.Dynamic('p'), hairpin[8])
            >>> abjad.override(voice).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
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
            ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
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

        ..  container:: example

            >>> voice = abjad.Voice("c'8 d' e' f' c' d' e' f' c'")
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, voice[:])
            >>> hairpin.attach(abjad.Dynamic('"p"'), hairpin[0])
            >>> hairpin.attach(abjad.Dynamic('"f"'), hairpin[2])
            >>> hairpin.attach(abjad.Dynamic('"p"'), hairpin[4])
            >>> hairpin.attach(abjad.Dynamic('"f"'), hairpin[6])
            >>> hairpin.attach(abjad.Dynamic('"p"'), hairpin[8])
            >>> abjad.override(voice).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'8
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.1
                                #:dynamic "p"
                                #:hspace -0.25
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    \<
                    d'8
                    e'8
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
                    \>
                    f'8
                    c'8
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.1
                                #:dynamic "p"
                                #:hspace -0.25
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                    \<
                    d'8
                    e'8
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
                    \>
                    f'8
                    c'8
                    _ #(make-dynamic-script
                        (markup
                            #:whiteout
                            #:line (
                                #:general-align Y -2 #:normal-text #:larger "“"
                                #:hspace -0.1
                                #:dynamic "p"
                                #:hspace -0.25
                                #:general-align Y -2 #:normal-text #:larger "”"
                                )
                            )
                        )
                }

            >>> for leaf in abjad.select(voice).leaves():
            ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
            ...
            (Note("c'8"), Dynamic('"p"', direction=Down))
            (Note("d'8"), Dynamic('"p"', direction=Down))
            (Note("e'8"), Dynamic('"f"', direction=Down))
            (Note("f'8"), Dynamic('"f"', direction=Down))
            (Note("c'8"), Dynamic('"p"', direction=Down))
            (Note("d'8"), Dynamic('"p"', direction=Down))
            (Note("e'8"), Dynamic('"f"', direction=Down))
            (Note("f'8"), Dynamic('"f"', direction=Down))
            (Note("c'8"), Dynamic('"p"', direction=Down))

        ..  container:: example

            >>> voice = abjad.Voice("c'8 d' e' r r f' e' d' c'")
            >>> hairpin = abjad.Hairpin()
            >>> abjad.attach(hairpin, voice[:])
            >>> hairpin.attach(abjad.Dynamic('f'), hairpin[0])
            >>> hairpin.attach(abjad.Dynamic('niente'), hairpin[3])
            >>> hairpin.attach(abjad.Dynamic('niente'), hairpin[-4])
            >>> hairpin.attach(abjad.Dynamic('f'), hairpin[-1])
            >>> abjad.override(voice).dynamic_line_spanner.staff_padding = 4
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4
                }
                {
                    c'8
                    \f
                    - \tweak circled-tip ##t
                    \>
                    d'8
                    e'8
                    r8
                    \!
                    r8
                    f'8
                    \!
                    - \tweak circled-tip ##t
                    \<
                    e'8
                    d'8
                    c'8
                    \f
                }

            >>> for leaf in abjad.select(voice).leaves():
            ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
            ...
            (Note("c'8"), Dynamic('f'))
            (Note("d'8"), Dynamic('f'))
            (Note("e'8"), Dynamic('f'))
            (Rest('r8'), Dynamic('niente', direction=Down, name_is_textual=True))
            (Rest('r8'), Dynamic('niente', direction=Down, name_is_textual=True))
            (Note("f'8"), Dynamic('niente', direction=Down, name_is_textual=True))
            (Note("e'8"), Dynamic('niente', direction=Down, name_is_textual=True))
            (Note("d'8"), Dynamic('niente', direction=Down, name_is_textual=True))
            (Note("c'8"), Dynamic('f'))

        """
        return super()._attach_piecewise(
            indicator,
            leaf,
            deactivate=deactivate,
            tag=tag,
            wrapper=wrapper,
            )

    def start_command(self) -> typing.List[str]:
        r"""
        Gets start command.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> hairpin = abjad.Hairpin('<')
            >>> abjad.attach(hairpin, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \<
                    d'4
                    e'4
                    f'4
                    \!
                }

            >>> hairpin.start_command()
            ['\\<']

        ..  container:: example

            With direction:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> hairpin = abjad.Hairpin('<', direction=abjad.Up)
            >>> abjad.attach(hairpin, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    ^ \<
                    d'4
                    e'4
                    f'4
                    \!
                }

            >>> hairpin.start_command()
            ['^ \\<']

        """
        strings: typing.List[str] = []
        contributions = tweak(self)._list_format_contributions()
        strings.extend(contributions)
        string = rf'\{self.shape_string}'
        string = self._add_direction(string)
        strings.append(string)
        return strings

    def stop_command(self) -> typing.Optional[str]:
        r"""
        Gets stop command.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> hairpin = abjad.Hairpin('<')
            >>> abjad.attach(hairpin, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \<
                    d'4
                    e'4
                    f'4
                    \!
                }

            >>> hairpin.stop_command()
            '\\!'

        ..  container:: example

            With stop dynamic:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> hairpin = abjad.Hairpin('p < f')
            >>> abjad.attach(hairpin, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \<
                    \p
                    d'4
                    e'4
                    f'4
                    \f
                    \f
                }

            >>> hairpin.stop_command()
            '\\f'

        ..  container:: example

            With dynamic on stop leaf:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> hairpin = abjad.Hairpin('<')
            >>> abjad.attach(hairpin, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \<
                    d'4
                    e'4
                    f'4
                    \f
                }

            >>> hairpin.stop_command() is None
            True

        """
        leaf = self[-1]
        if self._has_sounding_stop_dynamic():
            string = self._get_directed_stop_dynamic()
            return string
        effective_dynamic = inspect(leaf).get_effective(Dynamic)
        if effective_dynamic is None or effective_dynamic.name == 'niente':
            string = self._stop_command
            return string
        if effective_dynamic not in inspect(leaf).wrappers():
            found_match = False
            for indicator in inspect(leaf).get_indicators(Dynamic):
                if indicator == effective_dynamic:
                    found_match = True
            if not found_match:
                string = self._stop_command
                return string
        return None

def hairpin(
    descriptor: str,
    argument: typing.Union[Component, Selection],
    start_selector: typings.Selector = 'abjad.select().leaf(0)',
    stop_selector: typings.Selector = 'abjad.select().leaf(-1)',
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

    if isinstance(descriptor, str):
        start, shape, stop = descriptor.split()
        start_dynamic = Dynamic(start)
        dynamic_trend = DynamicTrend(shape)
        stop_dynamic = Dynamic(stop)
    else:
        assert isinstance(descriptor, list), repr(descriptor)
        assert len(descriptor) == 3, repr(descriptor)
        start_dynamic, dynamic_trend, stop_dynamic = descriptor

    assert isinstance(start_dynamic, Dynamic), repr(start_dynamic)
    if isinstance(start_selector, str):
        start_selector = eval(start_selector)
    assert isinstance(start_selector, Expression)
    start_leaf = start_selector(argument)
    attach(start_dynamic, start_leaf)

    assert isinstance(dynamic_trend, DynamicTrend), repr(dynamic_trend)
    attach(dynamic_trend, start_leaf)
    
    assert isinstance(stop_dynamic, Dynamic), repr(stop_dynamic)
    if isinstance(stop_selector, str):
        stop_selector = eval(stop_selector)
    assert isinstance(stop_selector, Expression)
    stop_leaf = stop_selector(argument)
    attach(stop_dynamic, stop_leaf)
