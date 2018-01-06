from .Spanner import Spanner


class Hairpin(Spanner):
    r'''Hairpin.

    ..  container:: example

        >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
        >>> hairpin = abjad.Hairpin('p < f')
        >>> abjad.attach(hairpin, voice[1:-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice {
                r8
                d'8 \< \p
                e'8
                f'8
                g'8
                a'8
                b'8 \f
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

        >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
        >>> hairpin = abjad.Hairpin('f > p')
        >>> abjad.attach(hairpin, voice[1:-1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice {
                r8
                d'8 \> \f
                e'8
                f'8
                g'8
                a'8
                b'8 \p
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

        >>> voice = abjad.Voice("c'2. r4")
        >>> hairpin = abjad.Hairpin('f > niente')
        >>> abjad.attach(hairpin, voice[:])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice {
                \once \override Hairpin.circled-tip = ##t
                c'2. \> \f
                r4 \!
            }

        >>> for leaf in abjad.select(voice).leaves():
        ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
        ...
        (Note("c'2."), None)
        (Rest('r4'), None)

    ..  container:: example

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
            \new Voice {
                c'8 \p \<
                d'8
                e'8 \f \>
                f'8
                c'8 \p \<
                d'8
                e'8 \f \>
                f'8
                c'8 \p
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


    '''

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
        '_stop_dynamic',
        '_trim',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        descriptor=None,
        context=None,
        direction=None,
        overrides=None,
        trim=None,
        ):
        import abjad
        Spanner.__init__(self, overrides=overrides)
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        direction = abjad.String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction
        self._trim = trim
        if descriptor is not None:
            assert self._is_valid_descriptor(descriptor), repr(descriptor)
            result = self._parse_descriptor(descriptor)
            start_dynamic, shape_string, stop_dynamic = result
            self._descriptor = descriptor
            assert shape_string in ('<', '>')
            self._shape_string = shape_string
            if start_dynamic is not None:
                start_dynamic = abjad.Dynamic(start_dynamic)
            self._start_dynamic = start_dynamic
            if stop_dynamic is not None:
                stop_dynamic = abjad.Dynamic(stop_dynamic)
            self._stop_dynamic = stop_dynamic
        else:
            self._descriptor = None
            self._shape_string = None
            self._start_dynamic = None
            self._stop_dynamic = None

    def __eq__(self, argument):
        r'''Is true when hairpin equals `argument`.

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

        Returns true or false.
        '''
        if not isinstance(argument, type(self)):
            return False
        if (self.start_dynamic == argument.start_dynamic and
            self.stop_dynamic == argument.stop_dynamic and
            self.trim == argument.trim):
            return True
        return False

    def __hash__(self):
        r'''Hashes hairpin.

        Returns integer.
        '''
        return super(Hairpin, self).__hash__()

    ### PRIVATE METHODS ###

    def _add_circled_tip_override(self, leaf, bundle):
        dynamic = self._get_piecewise_dynamic(leaf)
        if not dynamic:
            return
        next_dynamic = self._get_next_piecewise_dynamic_from(leaf)
        if not next_dynamic:
            return
        if dynamic.name == 'niente' or next_dynamic.name == 'niente':
            string = r'\once \override Hairpin.circled-tip = ##t'
            bundle.before.commands.append(string)

    def _add_dynamic(self, leaf, bundle):
        import abjad
        dynamic = self._get_piecewise_dynamic(leaf)
        if dynamic is None:
            return
        if dynamic.name == 'niente':
            string = r'\!'
        else:
            string = dynamic._get_lilypond_format()
        if self.direction is not None:
            direction = abjad.String.to_tridirectional_lilypond_symbol(
                self.direction
                )
            string = '{} {}'.format(direction, string)
        previous_dynamic = self._get_previous_piecewise_dynamic_from(leaf)
        if previous_dynamic is None:
            bundle.right.spanner_starts.append(string)
        else:
            bundle.right.spanner_stops.append(string)

    def _add_hairpin_start(self, leaf, bundle):
        import abjad
        dynamic = self._get_piecewise_dynamic(leaf)
        if dynamic is None:
            return
        next_dynamic = self._get_next_piecewise_dynamic_from(leaf)
        if next_dynamic is None:
            return
        if dynamic.ordinal == next_dynamic.ordinal:
            return
        if dynamic.ordinal < next_dynamic.ordinal:
            string = r'\<'
        if next_dynamic.ordinal < dynamic.ordinal:
            string = r'\>'
        if self.direction is not None:
            direction = abjad.String.to_tridirectional_lilypond_symbol(
                self.direction
                )
            string = '{} {}'.format(direction, string)
        bundle.right.spanner_starts.append(string)

    def _attachment_test_all(self, argument):
        import abjad
        if isinstance(argument, (abjad.Chord, abjad.Note)):
            return True
        assert all(isinstance(_, abjad.Leaf) for _ in argument)
        if self.trim:
            leaves = abjad.select(argument).leaves(trim=True)
        else:
            leaves = abjad.select(argument).leaves()
        return 1 <= len(leaves)

    def _copy_keyword_args(self, new):
        Spanner._copy_keyword_args(self, new)
        new._descriptor = self.descriptor
        new._direction = self.direction
        new._shape_string = self.shape_string
        new._start_dynamic = self.start_dynamic
        new._stop_dynamic = self.stop_dynamic
        new._trim = self.trim

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        if self.descriptor is None:
            return self._get_piecewise_lilypond_format_bundle(leaf)
        direction_string = ''
        if self.direction is not None:
            direction_string = abjad.String.to_tridirectional_lilypond_symbol(
                self.direction)
            direction_string = '{} '.format(direction_string)
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if len(self) == 1 and isinstance(self[0], (abjad.Chord, abjad.Note)):
            string = r'{}\{}'.format(direction_string, self.start_dynamic.name)
            bundle.right.spanner_starts.append(string)
            return bundle
        if (leaf is self[0] and
            (self.start_dynamic and self.start_dynamic.name == 'niente' or
            self.stop_dynamic and self.stop_dynamic.name == 'niente')):
            string = r'\once \override Hairpin.circled-tip = ##t'
            bundle.before.commands.append(string)
        if not self.trim:
            if leaf is self[0]:
                string = r'{}\{}'.format(direction_string, self.shape_string)
                bundle.right.spanner_starts.append(string)
                if (self.start_dynamic and self.start_dynamic.name != 'niente'):
                    string = r'{}\{}'.format(
                        direction_string,
                        self.start_dynamic.name,
                        )
                    bundle.right.spanner_starts.append(string)
            if leaf is self[-1]:
                if (self.stop_dynamic and self.stop_dynamic.name != 'niente'):
                    string = r'{}\{}'.format(
                        direction_string,
                        self.stop_dynamic.name,
                        )
                    bundle.right.spanner_stops.append(string)
                else:
                    effective_dynamic = abjad.inspect(leaf).get_effective(
                        abjad.Dynamic)
                    if (effective_dynamic is None or
                        effective_dynamic.name == 'niente'):
                        string = r'\!'
                        bundle.right.spanner_stops.append(string)
                    elif (effective_dynamic not in
                        abjad.inspect(leaf).wrappers()):
                        found_match = False
                        for indicator in abjad.inspect(leaf).get_indicators(
                            abjad.Dynamic):
                            if indicator == effective_dynamic:
                                found_match = True
                        if not found_match:
                            string = r'\!'
                            bundle.right.spanner_stops.append(string)
        else:
            if self._is_my_first(leaf, (abjad.Chord, abjad.Note)):
                string = r'{}\{}'.format(
                    direction_string,
                    self.shape_string,
                    )
                bundle.right.spanner_starts.append(string)
                if (self.start_dynamic and self.start_dynamic.name != 'niente'):
                    string = r'{}\{}'.format(
                        direction_string,
                        self.start_dynamic.name,
                        )
                    bundle.right.spanner_starts.append(string)
            if self._is_my_last(leaf, (abjad.Chord, abjad.Note)):
                if (self.stop_dynamic and self.stop_dynamic.name != 'niente'):
                    string = r'{}\{}'.format(
                        direction_string,
                        self.stop_dynamic.name,
                        )
                    bundle.right.spanner_stops.append(string)
                else:
                    effective_dynamic = abjad.inspect(leaf).get_effective(
                        abjad.Dynamic)
                    if (effective_dynamic is None or
                        effective_dynamic.name == 'niente'):
                        string = r'\!'
                        bundle.right.spanner_stops.append(string)
                    elif effective_dynamic not in leaf._wrappers:
                        found_match = False
                        for indicator in abjad.inspect(leaf).get_indicators(
                            abjad.Dynamic):
                            if indicator == effective_dynamic:
                                found_match = True
                        if not found_match:
                            string = r'\!'
                            bundle.right.spanner_stops.append(string)
        if leaf is self[0] and len(self) == 1:
            bundle.right.spanner_starts.extend(bundle.right.spanner_stops)
            bundle.right.spanner_stops[:] = []
        return bundle

    def _get_next_piecewise_dynamic_from(self, leaf):
        import abjad
        index = self._index(leaf)
        number = index + 1
        for leaf in self[number:]:
            if self._has_piecewise_indicator(leaf, abjad.Dynamic):
                return self._get_piecewise_indicator(leaf, abjad.Dynamic)

    def _get_piecewise_dynamic(self, leaf):
        import abjad
        if self._has_piecewise_indicator(leaf, abjad.Dynamic):
            return self._get_piecewise_indicator(leaf, abjad.Dynamic)

    def _get_piecewise_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        self._add_circled_tip_override(leaf, bundle)
        self._add_hairpin_start(leaf, bundle)
        self._add_dynamic(leaf, bundle)
        if self._is_my_only_leaf(leaf):
            bundle.right.spanner_starts.extend(bundle.right.spanner_stops)
            bundle.right.spanner_stops[:] = []
        return bundle

    def _get_previous_piecewise_dynamic_from(self, leaf):
        import abjad
        index = self._index(leaf)
        for leaf in reversed(self[:index]):
            if self._has_piecewise_indicator(leaf, abjad.Dynamic):
                return self._get_piecewise_indicator(leaf, abjad.Dynamic)

    @staticmethod
    def _is_hairpin_shape_string(argument):
        return argument in Hairpin._hairpin_shape_strings

    @staticmethod
    def _is_hairpin_token(argument):
        r'''Is true when `argument` is hairpin token.

        >>> abjad.Hairpin._is_hairpin_token(('', '<', ''))
        True

        >>> abjad.Hairpin._is_hairpin_token(('p', '<', 'f'))
        True

        >>> abjad.Hairpin._is_hairpin_token(('p', '@', 'f'))
        False

        >>> abjad.Hairpin._is_hairpin_token(('p', '>', 'f'))
        False

        '''
        import abjad
        if (isinstance(argument, tuple) and
            len(argument) == 3 and
            (not argument[0] or abjad.Dynamic.is_dynamic_name(argument[0]))
            and Hairpin._is_hairpin_shape_string(argument[1]) and
            (not argument[2] or abjad.Dynamic.is_dynamic_name(argument[2]))):
            if argument[0] and argument[2]:
                start_ordinal = abjad.Dynamic.dynamic_name_to_dynamic_ordinal(
                    argument[0])
                stop_ordinal = abjad.Dynamic.dynamic_name_to_dynamic_ordinal(
                    argument[2])
                if argument[1] == '<':
                    return start_ordinal < stop_ordinal
                else:
                    return stop_ordinal < start_ordinal
            else:
                return True
        else:
            return False

    def _is_valid_descriptor(self, descriptor):
        import abjad
        start, shape, stop = self._parse_descriptor(descriptor)
        if shape not in self._hairpin_shape_strings:
            return False
        if (start is not None and
            start not in abjad.Dynamic._dynamic_names):
            return False
        if (stop is not None and
            stop not in abjad.Dynamic._dynamic_names):
            return False
        if start is not None and stop is not None:
            start_ordinal = \
                abjad.Dynamic.dynamic_name_to_dynamic_ordinal(start)
            stop_ordinal = \
                abjad.Dynamic.dynamic_name_to_dynamic_ordinal(stop)
            if shape == '<' and not start_ordinal < stop_ordinal:
                return False
            if shape == '>' and not start_ordinal > stop_ordinal:
                return False
        return True

    def _parse_descriptor(self, descriptor):
        r'''Example descriptors:

        '<'
        'p <'
        'p < f'

        '''
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
    def context(self):
        r'''Gets context name (for piecewise attach).

        ..  container:: example

            Simultaneous hairpins on a single staff:

            >>> voice_1 = abjad.Voice("e'8 f' g' a' f' g' a' b' g'")
            >>> abjad.attach(abjad.LilyPondCommand('voiceOne'), voice_1)
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
            >>> abjad.attach(abjad.LilyPondCommand('voiceTwo'), voice_2)
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
                \new Staff <<
                    \new Voice \with {
                        \override DynamicLineSpanner.direction = #up
                        \override DynamicLineSpanner.staff-padding = #4
                    } {
                        \voiceOne
                        e'8 \< \mf
                        f'8
                        g'8 \f \>
                        a'8
                        f'8 \mf \<
                        g'8
                        a'8 \f \>
                        b'8
                        g'8 \mf
                    }
                    \new Voice \with {
                        \override DynamicLineSpanner.staff-padding = #6
                    } {
                        \voiceTwo
                        c'2 \< \pp
                        b2 ~
                        b8 \p
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

        Returns string or none.
        '''
        return self._context

    @property
    def descriptor(self):
        r'''Gets descriptor.

        ..  container:: example

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin('p < f')
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice {
                    r8
                    d'8 \< \p
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8 \f
                    r8
                }

            >>> hairpin.descriptor
            'p < f'

        Returns string.
        '''
        return self._descriptor

    @property
    def direction(self):
        r'''Gets direction.

        ..  container:: example

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin('p < f', direction=abjad.Up)
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice {
                    r8
                    d'8 ^ \< ^ \p
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8 ^ \f
                    r8
                }

            >>> hairpin.direction
            '^'

        Defaults to none.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._direction

    @property
    def trim(self):
        r'''Is true when hairpin trims edge-rests.

        ..  container:: example

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin('p < f', trim=True)
            >>> abjad.attach(hairpin, voice[:])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice {
                    r8
                    d'8 \< \p
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8 \f
                    r8
                }

        Returns true or false.
        '''
        return self._trim

    @property
    def shape_string(self):
        r'''Gets shape string.

        ..  container:: example

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin('p < f')
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice {
                    r8
                    d'8 \< \p
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8 \f
                    r8
                }

            >>> hairpin.shape_string
            '<'

        Returns string.
        '''
        return self._shape_string

    @property
    def start_dynamic(self):
        r'''Gets start dynamic.

        ..  container:: example

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin('p < f')
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice {
                    r8
                    d'8 \< \p
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8 \f
                    r8
                }

            >>> hairpin.start_dynamic
            Dynamic('p')

        Returns dynamic or none.
        '''
        return self._start_dynamic

    @property
    def stop_dynamic(self):
        r'''Gets stop dynamic.

        ..  container:: example

            >>> voice = abjad.Voice("r8 d' e' f' g' a' b' r")
            >>> hairpin = abjad.Hairpin('p < f')
            >>> abjad.attach(hairpin, voice[1:-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice {
                    r8
                    d'8 \< \p
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8 \f
                    r8
                }

            >>> hairpin.stop_dynamic
            Dynamic('f')

        Returns dynamic or none.
        '''
        return self._stop_dynamic

    ### PUBLIC METHODS ###

    def attach(self, indicator, leaf, deactivate=None, site=None, tag=None):
        r'''Attaches `indicator` to `leaf` in spanner.

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
                \new Voice \with {
                    \override DynamicLineSpanner.staff-padding = #4
                } {
                    c'8 \< \p
                    d'8
                    e'8 \f \>
                    f'8
                    c'8 \p \<
                    d'8
                    e'8 \f \>
                    f'8
                    c'8 \p
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
                \new Voice \with {
                    \override DynamicLineSpanner.staff-padding = #4
                } {
                    c'8 \< _ #(make-dynamic-script
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
                    d'8
                    e'8 _ #(make-dynamic-script
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
                        ) \>
                    f'8
                    c'8 _ #(make-dynamic-script
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
                        ) \<
                    d'8
                    e'8 _ #(make-dynamic-script
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
                        ) \>
                    f'8
                    c'8 _ #(make-dynamic-script
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
                \new Voice \with {
                    \override DynamicLineSpanner.staff-padding = #4
                } {
                    \once \override Hairpin.circled-tip = ##t
                    c'8 \> \f
                    d'8
                    e'8
                    \once \override Hairpin.circled-tip = ##t
                    r8 \!
                    r8
                    \once \override Hairpin.circled-tip = ##t
                    f'8 \! \<
                    e'8
                    d'8
                    c'8 \f
                }

            >>> for leaf in abjad.select(voice).leaves():
            ...     leaf, abjad.inspect(leaf).get_effective(abjad.Dynamic)
            ...
            (Note("c'8"), Dynamic('f'))
            (Note("d'8"), Dynamic('f'))
            (Note("e'8"), Dynamic('f'))
            (Rest('r8'), Dynamic('niente', direction=Down))
            (Rest('r8'), Dynamic('niente', direction=Down))
            (Note("f'8"), Dynamic('niente', direction=Down))
            (Note("e'8"), Dynamic('niente', direction=Down))
            (Note("d'8"), Dynamic('niente', direction=Down))
            (Note("c'8"), Dynamic('f'))

        Returns none.
        '''
        superclass = super(Hairpin, self)
        superclass._attach_piecewise(
            indicator,
            leaf,
            deactivate=deactivate,
            site=site,
            tag=tag,
            )
