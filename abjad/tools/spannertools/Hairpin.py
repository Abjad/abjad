# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import stringtools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import override


class Hairpin(Spanner):
    r'''Hairpin.

    ..  container:: example

        **Example 1.** Crescendo:

        ::

            >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
            >>> hairpin = spannertools.Hairpin(
            ...     descriptor='p < f',
            ...     include_rests=False,
            ...     )
            >>> attach(hairpin, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                r4
                c'8 \< \p
                d'8
                e'8
                f'8 \f
                r4
            }

        **Example 2.** Decrescendo:

        ::

            >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
            >>> hairpin = spannertools.Hairpin(
            ...     descriptor='f > p',
            ...     include_rests=False,
            ...     )
            >>> attach(hairpin, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                r4
                c'8 \> \f
                d'8
                e'8
                f'8 \p
                r4
            }

    ..  container:: example

        **Example 3.** Crescendo dal niente:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> hairpin = spannertools.Hairpin(
            ...     descriptor='niente < f',
            ...     include_rests=False,
            ...     )
            >>> attach(hairpin, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \once \override Hairpin.circled-tip = ##t
                c'4 \<
                d'4
                e'4
                f'4 \f
            }

        **Example 4.** Decrescendo al niente:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> hairpin = spannertools.Hairpin(
            ...     descriptor='f > niente',
            ...     include_rests=False,
            ...     )
            >>> attach(hairpin, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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
        descriptor='<',
        direction=None,
        include_rests=False,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        direction = stringtools.expr_to_tridirectional_lilypond_symbol(
            direction)
        self._direction = direction
        self._include_rests = include_rests
        assert self._is_valid_descriptor(descriptor), repr(descriptor)
        start_dynamic, shape_string, stop_dynamic = \
            self._parse_descriptor(descriptor)
        self._descriptor = descriptor
        assert shape_string in ('<', '>')
        self._shape_string = shape_string
        if start_dynamic is not None:
            start_dynamic = indicatortools.Dynamic(start_dynamic)
        self._start_dynamic = start_dynamic
        if stop_dynamic is not None:
            stop_dynamic = indicatortools.Dynamic(stop_dynamic)
        self._stop_dynamic = stop_dynamic

    ### PRIVATE METHODS ###

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
        from abjad.tools import systemtools
        self._format_time_test(leaf)
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        if self._is_my_first_leaf(leaf):
            contributions = override(self)._list_format_contributions(
                'override',
                is_once=False,
                )
            lilypond_format_bundle.grob_overrides.extend(contributions)
        if self._is_my_last_leaf(leaf):
            contributions = override(self)._list_format_contributions(
                'revert',
                )
            lilypond_format_bundle.grob_reverts.extend(contributions)
        direction_string = ''
        if self.direction is not None:
            direction_string = \
                stringtools.expr_to_tridirectional_lilypond_symbol(
                    self.direction)
            direction_string = '{} '.format(direction_string)
        if (self._is_my_first_leaf(leaf) and
            (self.start_dynamic and self.start_dynamic.name == 'niente' or
            self.stop_dynamic and self.stop_dynamic.name == 'niente')):
            override(leaf).hairpin.circled_tip = True
        if self.include_rests:
            if self._is_my_first_leaf(leaf):
                string = r'{}\{}'.format(direction_string, self.shape_string)
                lilypond_format_bundle.right.spanner_starts.append(string)
                if (self.start_dynamic and
                    not self.start_dynamic.name == 'niente'):
                        string = r'{}\{}'.format(
                            direction_string,
                            self.start_dynamic.name,
                            )
                        lilypond_format_bundle.right.spanner_starts.append(
                            string)
            if self._is_my_last_leaf(leaf):
                if (self.stop_dynamic and
                    not self.stop_dynamic.name == 'niente'):
                        string = r'{}\{}'.format(
                            direction_string,
                            self.stop_dynamic.name,
                            )
                        lilypond_format_bundle.right.spanner_stops.append(
                            string)
                else:
                    effective_dynamic = leaf._get_effective(
                        indicatortools.Dynamic)
                    if effective_dynamic is None or \
                        effective_dynamic.name == 'niente':
                        string = r'\!'
                        lilypond_format_bundle.right.spanner_stops.append(
                            string)
                    elif effective_dynamic not in leaf._indicator_expressions:
                        found_match = False
                        for indicator in \
                            leaf._get_indicators(indicatortools.Dynamic):
                            if indicator == effective_dynamic:
                                found_match = True
                        if not found_match:
                            string = r'\!'
                            lilypond_format_bundle.right.spanner_stops.append(
                                string)
        else:
            if self._is_my_first(leaf, (scoretools.Chord, scoretools.Note)):
                string = r'{}\{}'.format(
                    direction_string,
                    self.shape_string,
                    )
                lilypond_format_bundle.right.spanner_starts.append(string)
                if (self.start_dynamic and
                    not self.start_dynamic.name == 'niente'):
                        string = r'{}\{}'.format(
                            direction_string,
                            self.start_dynamic.name,
                            )
                        lilypond_format_bundle.right.spanner_starts.append(
                            string)
            if self._is_my_last(leaf, (scoretools.Chord, scoretools.Note)):
                if (self.stop_dynamic and
                    not self.stop_dynamic.name == 'niente'):
                        string = r'{}\{}'.format(
                            direction_string,
                            self.stop_dynamic.name,
                            )
                        lilypond_format_bundle.right.spanner_stops.append(
                            string)
                else:
                    effective_dynamic = leaf._get_effective(
                        indicatortools.Dynamic)
                    if effective_dynamic is None or \
                        effective_dynamic.name == 'niente':
                        string = r'\!'
                        lilypond_format_bundle.right.spanner_stops.append(
                            string)
                    elif effective_dynamic not in leaf._indicator_expressions:
                        found_match = False
                        for indicator in \
                            leaf._get_indicators(indicatortools.Dynamic):
                            if indicator == effective_dynamic:
                                found_match = True
                        if not found_match:
                            string = r'\!'
                            lilypond_format_bundle.right.spanner_stops.append(
                                string)
        if self._is_my_only_leaf(leaf):
            lilypond_format_bundle.right.spanner_starts.extend(
                lilypond_format_bundle.right.spanner_stops)
            lilypond_format_bundle.right.spanner_stops[:] = []
        return lilypond_format_bundle

    @staticmethod
    def _is_hairpin_shape_string(arg):
        return arg in Hairpin._hairpin_shape_strings

    @staticmethod
    def _is_hairpin_token(arg):
        r'''Is true when `arg` is a hairpin token. Otherwise false:

        ::

            >>> spannertools.Hairpin._is_hairpin_token(('p', '<', 'f'))
            True

        ::

            >>> spannertools.Hairpin._is_hairpin_token(('f', '<', 'p'))
            False

        Returns true or false.
        '''
        Dynamic = indicatortools.Dynamic
        if (isinstance(arg, tuple) and
            len(arg) == 3 and
            (not arg[0] or indicatortools.Dynamic.is_dynamic_name(arg[0]))
            and Hairpin._is_hairpin_shape_string(arg[1]) and
            (not arg[2] or indicatortools.Dynamic.is_dynamic_name(arg[2]))):
            if arg[0] and arg[2]:
                start_ordinal = \
                    Dynamic.dynamic_name_to_dynamic_ordinal(arg[0])
                stop_ordinal = \
                    Dynamic.dynamic_name_to_dynamic_ordinal(arg[2])
                if arg[1] == '<':
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

            **Example 1.** Gets descriptor of crescendo:

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = spannertools.Hairpin(descriptor='p < f')
                >>> attach(hairpin, staff[:])
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

            **Example 1.** Positions hairpin above staff:

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = spannertools.Hairpin(
                ...     descriptor='p < f',
                ...     direction=Up,
                ...     )
                >>> attach(hairpin, staff[:])
                >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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

            **Example 1.** Crescendo includes rests:

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = spannertools.Hairpin(
                ...     descriptor='p < f',
                ...     include_rests=True,
                ...     )
                >>> attach(hairpin, staff[:])
                >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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

        Returns true or false.
        '''
        return self._include_rests

    @property
    def shape_string(self):
        r'''Gets shape string of hairpin.

        ..  container:: example

            **Example 1.** Gets shape string of crescendo:

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = spannertools.Hairpin(descriptor='p < f')
                >>> attach(hairpin, staff[:])
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

            **Example 1.** Gets start dynamic of crescendo:

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = spannertools.Hairpin(descriptor='p < f')
                >>> attach(hairpin, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> hairpin.start_dynamic
                Dynamic(name='p')

        Returns dynamic or none.
        '''
        return self._start_dynamic

    @property
    def stop_dynamic(self):
        r'''Gets stop dynamic string of hairpin.

        ..  container:: example

            **Example 1.** Gets stop dynamic of crescendo:

            ::

                >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
                >>> hairpin = spannertools.Hairpin(descriptor='p < f')
                >>> attach(hairpin, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> hairpin.stop_dynamic
                Dynamic(name='f')

        Returns dynamic or none.
        '''
        return self._stop_dynamic
