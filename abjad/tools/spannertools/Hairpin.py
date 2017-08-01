# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import datastructuretools
from abjad.tools.spannertools.Spanner import Spanner


class Hairpin(Spanner):
    r'''Hairpin.

    ::

        >>> import abjad

    ..  container:: example

        Crescendo:

        ::

            >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
            >>> hairpin = abjad.Hairpin(
            ...     descriptor='p < f',
            ...     include_rests=False,
            ...     )
            >>> abjad.attach(hairpin, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                r4
                c'8 \< \p
                d'8
                e'8
                f'8 \f
                r4
            }

        Decrescendo:

        ::

            >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
            >>> hairpin = abjad.Hairpin(
            ...     descriptor='f > p',
            ...     include_rests=False,
            ...     )
            >>> abjad.attach(hairpin, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                r4
                c'8 \> \f
                d'8
                e'8
                f'8 \p
                r4
            }

    ..  container:: example

        Crescendo dal niente:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> hairpin = abjad.Hairpin(
            ...     descriptor='niente < f',
            ...     include_rests=False,
            ...     )
            >>> abjad.attach(hairpin, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \once \override Hairpin.circled-tip = ##t
                c'4 \<
                d'4
                e'4
                f'4 \f
            }

        Decrescendo al niente:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> hairpin = abjad.Hairpin(
            ...     descriptor='f > niente',
            ...     include_rests=False,
            ...     )
            >>> abjad.attach(hairpin, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \once \override Hairpin.circled-tip = ##t
                c'4 \> \f
                d'4
                e'4
                f'4 \!
            }

    .. todo:: Make niente hairpins work with ``include_rests=True``.
    '''

    ### CLASS VARIABLES ###

    _hairpin_shape_strings = (
        '<',
        '>',
        )

    __slots__ = (
        '_descriptor',
        '_direction',
        '_include_rests',
        '_shape_string',
        '_start_dynamic',
        '_stop_dynamic',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        descriptor=None,
        direction=None,
        include_rests=None,
        overrides=None,
        ):
        import abjad
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        direction = abjad.String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction
        self._include_rests = include_rests
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
        dynamic = self._get_piecewise_dynamic(leaf)
        if dynamic is None:
            return
        string = '\\' + dynamic.name
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

    def _attachment_test_all(self, component_expression):
        if isinstance(component_expression, scoretools.Leaf):
            return False
        if not self._at_least_two_leaves(component_expression):
            return False
        formattable_components = []
        for component in component_expression:
            if (self.include_rests or
                isinstance(component, (scoretools.Note, scoretools.Chord))):
                formattable_components.append(component)
        return 1 < len(formattable_components)

    def _copy_keyword_args(self, new):
        Spanner._copy_keyword_args(self, new)
        new._descriptor = self.descriptor
        new._direction = self.direction
        new._include_rests = self.include_rests
        new._shape_string = self.shape_string
        new._start_dynamic = self.start_dynamic
        new._stop_dynamic = self.stop_dynamic

    def _format_time_test(self, leaf):
        if not 1 < len(self._get_leaves()):
            message = '{} fails format-time test.'
            message = message.format(self)
            raise Exception(message)

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        if self.descriptor is None:
            return self._get_piecewise_lilypond_format_bundle(leaf)
        self._format_time_test(leaf)
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        direction_string = ''
        if self.direction is not None:
            direction_string = abjad.String.to_tridirectional_lilypond_symbol(
                self.direction)
            direction_string = '{} '.format(direction_string)
        if (self._is_my_first_leaf(leaf) and
            (self.start_dynamic and self.start_dynamic.name == 'niente' or
            self.stop_dynamic and self.stop_dynamic.name == 'niente')):
            string = r'\once \override Hairpin.circled-tip = ##t'
            bundle.before.commands.append(string)
        if self.include_rests:
            if self._is_my_first_leaf(leaf):
                string = r'{}\{}'.format(direction_string, self.shape_string)
                bundle.right.spanner_starts.append(string)
                if (self.start_dynamic and
                    not self.start_dynamic.name == 'niente'):
                        string = r'{}\{}'.format(
                            direction_string,
                            self.start_dynamic.name,
                            )
                        bundle.right.spanner_starts.append(string)
            if self._is_my_last_leaf(leaf):
                if (self.stop_dynamic and
                    not self.stop_dynamic.name == 'niente'):
                        string = r'{}\{}'.format(
                            direction_string,
                            self.stop_dynamic.name,
                            )
                        bundle.right.spanner_stops.append(string)
                else:
                    effective_dynamic = leaf._get_effective(abjad.Dynamic)
                    if (effective_dynamic is None or
                        effective_dynamic.name == 'niente'):
                        string = r'\!'
                        bundle.right.spanner_stops.append(string)
                    elif effective_dynamic not in leaf._indicator_wrappers:
                        found_match = False
                        for indicator in leaf._get_indicators(abjad.Dynamic):
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
                if (self.start_dynamic and
                    not self.start_dynamic.name == 'niente'):
                        string = r'{}\{}'.format(
                            direction_string,
                            self.start_dynamic.name,
                            )
                        bundle.right.spanner_starts.append(string)
            if self._is_my_last(leaf, (abjad.Chord, abjad.Note)):
                if (self.stop_dynamic and
                    not self.stop_dynamic.name == 'niente'):
                        string = r'{}\{}'.format(
                            direction_string,
                            self.stop_dynamic.name,
                            )
                        bundle.right.spanner_stops.append(string)
                else:
                    effective_dynamic = leaf._get_effective(abjad.Dynamic)
                    if (effective_dynamic is None or
                        effective_dynamic.name == 'niente'):
                        string = r'\!'
                        bundle.right.spanner_stops.append(string)
                    elif effective_dynamic not in leaf._indicator_wrappers:
                        found_match = False
                        for indicator in leaf._get_indicators(abjad.Dynamic):
                            if indicator == effective_dynamic:
                                found_match = True
                        if not found_match:
                            string = r'\!'
                            bundle.right.spanner_stops.append(string)
        if self._is_my_only_leaf(leaf):
            bundle.right.spanner_starts.extend(bundle.right.spanner_stops)
            bundle.right.spanner_stops[:] = []
        return bundle

    def _get_next_piecewise_dynamic_from(self, leaf):
        import abjad
        index = self._index(leaf)
        for leaf in self[index+1:]:
            if self._has_piecewise_indicator(leaf, abjad.Dynamic):
                return self._get_piecewise_indicator(leaf, abjad.Dynamic)

    def _get_piecewise_dynamic(self, leaf):
        import abjad
        if self._has_piecewise_indicator(leaf, abjad.Dynamic):
            return self._get_piecewise_indicator(leaf, abjad.Dynamic)

    def _get_piecewise_lilypond_format_bundle(self, leaf):
        import abjad
        self._format_time_test(leaf)
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
        start, shape, stop = self._parse_descriptor(descriptor)
        if shape not in self._hairpin_shape_strings:
            return False
        if (start is not None and
            start not in indicatortools.Dynamic._dynamic_names):
            return False
        if (stop is not None and
            stop not in indicatortools.Dynamic._dynamic_names):
            return False
        if start is not None and stop is not None:
            start_ordinal = \
                indicatortools.Dynamic.dynamic_name_to_dynamic_ordinal(start)
            stop_ordinal = \
                indicatortools.Dynamic.dynamic_name_to_dynamic_ordinal(stop)
            if shape == '<' and not start_ordinal < stop_ordinal:
                return False
            if shape == '>' and not start_ordinal > stop_ordinal:
                return False
        return True

    def _parse_descriptor(self, descriptor):
        r'''Example descriptors:

        ::

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
    def descriptor(self):
        r'''Gets descriptor of hairpin.

        ..  container:: example

            Gets descriptor of crescendo:

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = abjad.Hairpin(descriptor='p < f')
                >>> abjad.attach(hairpin, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> hairpin.descriptor
                'p < f'

        Returns string.
        '''
        return self._descriptor

    @property
    def direction(self):
        r'''Gets direction.

        ..  container:: example

            Positions hairpin above staff:

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = abjad.Hairpin(
                ...     descriptor='p < f',
                ...     direction=Up,
                ...     )
                >>> abjad.attach(hairpin, staff[:])
                >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                r4
                c'8 ^ \< ^ \p
                d'8
                e'8
                f'8 ^ \f
                r4
            }

            ::

                >>> hairpin.direction
                '^'

        Defaults to none.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._direction

    @property
    def include_rests(self):
        r'''Gets include-rests flag of hairpin.

        ..  container:: example

            Crescendo includes rests:

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = abjad.Hairpin(
                ...     descriptor='p < f',
                ...     include_rests=True,
                ...     )
                >>> abjad.attach(hairpin, staff[:])
                >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                r4 \< \p
                c'8
                d'8
                e'8
                f'8
                r4 \f
            }

            ::

                >>> hairpin.include_rests
                True

        ..  container:: example

            ::

                >>> staff = abjad.Staff(abjad.Rest((1, 8)) * 4 + [abjad.Note(n, (1, 8)) for n in range(4, 8)])
                >>> crescendo = abjad.Hairpin('<', include_rests=False)
                >>> abjad.attach(crescendo, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    r8
                    r8
                    r8
                    r8
                    e'8 \<
                    f'8
                    fs'8
                    g'8 \!
                }

        ..  container:: example

            ::

                >>> staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)] + abjad.Rest((1, 8)) * 4)
                >>> crescendo = abjad.Hairpin('<', include_rests=False)
                >>> abjad.attach(crescendo, staff[:])

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8 \<
                    cs'8
                    d'8
                    ef'8 \!
                    r8
                    r8
                    r8
                    r8
                }

        Returns true or false.
        '''
        return self._include_rests

    @property
    def shape_string(self):
        r'''Gets shape string of hairpin.

        ..  container:: example

            Gets shape string of crescendo:

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = abjad.Hairpin(descriptor='p < f')
                >>> abjad.attach(hairpin, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> hairpin.shape_string
                '<'

        Returns string.
        '''
        return self._shape_string

    @property
    def start_dynamic(self):
        r'''Gets start dynamic string of hairpin.

        ..  container:: example

            Gets start dynamic of crescendo:

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = abjad.Hairpin(descriptor='p < f')
                >>> abjad.attach(hairpin, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> hairpin.start_dynamic
                Dynamic('p')

        Returns dynamic or none.
        '''
        return self._start_dynamic

    @property
    def stop_dynamic(self):
        r'''Gets stop dynamic string of hairpin.

        ..  container:: example

            Gets stop dynamic of crescendo:

            ::

                >>> staff = abjad.Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = abjad.Hairpin(descriptor='p < f')
                >>> abjad.attach(hairpin, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> hairpin.stop_dynamic
                Dynamic('f')

        Returns dynamic or none.
        '''
        return self._stop_dynamic

    ### PUBLIC METHODS ###

    def attach(self, indicator, leaf):
        r'''Attaches `indicator` to `leaf` in spanner.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'8 d' e' f' c' d' e' f' c'")
                >>> hairpin = abjad.Hairpin()
                >>> abjad.attach(hairpin, staff[:])
                >>> hairpin.attach(abjad.Dynamic('p'), hairpin[0])
                >>> hairpin.attach(abjad.Dynamic('f'), hairpin[2])
                >>> hairpin.attach(abjad.Dynamic('p'), hairpin[4])
                >>> hairpin.attach(abjad.Dynamic('f'), hairpin[6])
                >>> hairpin.attach(abjad.Dynamic('p'), hairpin[8])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
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

        Returns none.
        '''
        super(Hairpin, self)._attach_piecewise(indicator, leaf)
