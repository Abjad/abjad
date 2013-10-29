# -*- encoding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools.scoretools.Component import Component


class Container(Component):
    r'''An iterable container of music.

    **Example**:

    ..  container:: example

        ::

            >>> container = Container("c'4 e'4 d'4 e'8 f'8")
            >>> show(container) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
                c'4
                e'4
                d'4
                e'8
                f'8
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_formatter', 
        '_music', 
        '_named_children', 
        '_simultaneous',
        )

    _default_positional_input_arguments = (
        [],
        )

    _storage_format_attribute_mapping = {
        'music': '_music',
        }

    ### INITIALIZER ###

    def __init__(self, music=None, **kwargs):
        Component.__init__(self)
        self._named_children = {}
        self._simultaneous = False
        self._initialize_music(music)
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        r'''True when `expr` appears in container.
        Otherwise false.

        Returns boolean.
        '''
        for x in self._music:
            if x is expr:
                return True
        else:
            return False

    def __delitem__(self, i):
        r'''Delete container `i`.
        Detach component(s) from parentage.
        Withdraw component(s) from crossing spanners.
        Preserve spanners that component(s) cover(s).

        Returns none.
        '''
        components = self[i]
        #if not isinstance(components, selectiontools.SliceSelection):
        if not isinstance(components, selectiontools.Selection):
            components = selectiontools.SliceSelection([components])
        if not self.is_simultaneous:
            components._withdraw_from_crossing_spanners()
        components._set_parents(None)

    def __getitem__(self, i):
        r'''Get container `i`.
        Shallow traversal of container for numeric indices only.

        Returns component.
        '''
        if isinstance(i, int):
            return self._music[i]
        elif isinstance(i, slice) and not self.is_simultaneous:
            return selectiontools.SliceSelection(self._music[i])
        elif isinstance(i, slice) and self.is_simultaneous:
            return selectiontools.SimultaneousSelection(self._music[i])
        elif isinstance(i, str):
            if i not in self._named_children:
                raise MissingNamedComponentError(repr(i))
            elif 1 < len(self._named_children[i]):
                raise ExtraNamedComponentError(repr(i))
            return self._named_children[i][0]
        raise ValueError(repr(i))

    def __len__(self):
        r'''Number of items in container.

        Returns nonnegative integer.
        '''
        return len(self._music)

    def __repr__(self):
        r'''Representation of container in Python interpreter.

        Returns string.
        '''
        return self._compact_representation

    def __setitem__(self, i, expr):
        r'''Set container `i` equal to `expr`.
        Find spanners that dominate self[i] and children of self[i].
        Replace contents at self[i] with 'expr'.
        Reattach spanners to new contents.
        This operation always leaves score tree in tact.

        Returns none.
        '''
        return self._set_item(i, expr)

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        if not self.is_simultaneous:
            return '{%s}' % self._summary
        else:
            return '<<%s>>' % self._summary

    @property
    def _contents_duration(self):
        if self.is_simultaneous:
            return max([durationtools.Duration(0)] + 
                [x._preprolated_duration for x in self])
        else:
            duration = durationtools.Duration(0)
            for x in self:
                duration += x._preprolated_duration
            return duration

    @property
    def _duration_in_seconds(self):
        from abjad.tools import iterationtools
        if self.is_simultaneous:
            return max([durationtools.Duration(0)] + 
                [x._get_duration(in_seconds=True) for x in self])
        else:
            duration = durationtools.Duration(0)
            for leaf in iterationtools.iterate_leaves_in_expr(self):
                duration += leaf._get_duration(in_seconds=True)
            return duration

    @property
    def _preprolated_duration(self):
        return self._contents_duration

    @property
    def _space_delimited_summary(self):
        if 0 < len(self):
            result = []
            for x in self._music:
                if hasattr(x, '_compact_representation_with_tie'):
                    result.append(x._compact_representation_with_tie)
                else:
                    result.append(str(x))
            return ' '.join(result)
        else:
            return ''

    @property
    def _summary(self):
        if 0 < len(self):
            return ', '.join([str(x) for x in self._music])
        else:
            return ''

    ### PRIVATE METHODS ###

    def _append_without_withdrawing_from_crossing_spanners(self, component):
        '''Not composer-safe.
        '''
        self._set_item(slice(len(self), len(self)), [component],
            withdraw_components_in_expr_from_crossing_spanners=False)

    def _copy_with_children_and_marks_but_without_spanners(self):
        new = self._copy_with_marks_but_without_children_or_spanners()
        for component in self:
            new_component = \
                component._copy_with_children_and_marks_but_without_spanners()
            new.append(new_component)
        return new

    def _copy_with_marks_but_without_children_or_spanners(self):
        new = Component._copy_with_marks_but_without_children_or_spanners(self)
        new.is_simultaneous = self.is_simultaneous
        return new

    def _format_after_slot(self, format_contributions):
        result = []
        result.append((
            'lilypond command marks',
            format_contributions.get(
                'after', {}).get('lilypond command marks', [])))
        result.append((
            'comments', 
            format_contributions.get('after', {}).get('comments', [])))
        return tuple(result)

    def _format_before_slot(self, format_contributions):
        result = []
        result.append(('comments', 
            format_contributions.get('before', {}).get('comments', [])))
        result.append(('lilypond command marks',
            format_contributions.get('before', {}).get(
                'lilypond command marks', [])))
        return tuple(result)

    def _format_close_brackets_slot(self, format_contributions):
        result = []
        if self.is_simultaneous:
            brackets_close = ['>>']
        else:
            brackets_close = ['}']
        result.append([('close brackets', ''), brackets_close])
        return tuple(result)

    def _format_closing_slot(self, format_contributions):
        result = []
        result.append((
            'grob reverts', format_contributions.get('grob reverts', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'closing', {}).get('lilypond command marks', [])))
        result.append(('comments', 
            format_contributions.get('closing', {}).get('comments', [])))
        return self._format_slot_contributions_with_indent(result)

    def _format_content_pieces(self):
        result = []
        for m in self._music:
            result.extend(m.lilypond_format.split('\n'))
        result = ['\t' + x for x in result]
        return result

    def _format_contents_slot(self, format_contributions):
        result = []
        result.append(
            [('contents', '_contents'), self._format_content_pieces()])
        return tuple(result)

    def _format_open_brackets_slot(self, format_contributions):
        result = []
        if self.is_simultaneous:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        result.append([('open brackets', ''), brackets_open])
        return tuple(result)

    def _format_opening_slot(self, format_contributions):
        result = []
        result.append(('comments', 
            format_contributions.get('opening', {}).get('comments', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'opening', {}).get('lilypond command marks', [])))
        result.append(('grob overrides', 
            format_contributions.get('grob overrides', [])))
        result.append(('context settings', 
            format_contributions.get('context settings', [])))
        return self._format_slot_contributions_with_indent(result)

    def _format_slot_contributions_with_indent(self, slot):
        result = []
        for contributor, contributions in slot:
            result.append(
                (contributor, tuple(['\t' + x for x in contributions])))
        return tuple(result)

    def _get_spanners_that_dominate_component_pair(self, left, right):
        r'''Returns spanners that dominant component pair.
        Returns set (spanner, index) pairs.
        `left` must be an Abjad component or None.
        `right` must be an Abjad component or None.

        If both `left` and `right` are components,
        then `left` and `right` must be logical-voice-contiguous.

        This is a version of ContiguousSelection._get_dominant_spanners().
        This version is useful for finding spanners that dominant
        a zero-length slice between components, as in staff[2:2].
        '''
        from abjad.tools import spannertools
        Selection = selectiontools.Selection
        if left is None or right is None:
            return set([])
        assert Selection._all_are_contiguous_components_in_same_logical_voice(
            [left, right])
        left_contained = left._get_descendants()._get_spanners()
        right_contained = right._get_descendants()._get_spanners()
        dominant_spanners = left_contained & right_contained
        right_start_offset = right._get_timespan().start_offset
        components_after_gap = []
        for component in right._get_lineage():
            if component._get_timespan().start_offset == right_start_offset:
                components_after_gap.append(component)
        receipt = set([])
        for spanner in dominant_spanners:
            for component in components_after_gap:
                if component in spanner:
                    index = spanner.index(component)
                    receipt.add((spanner, index))
                    continue
        return receipt

    def _get_spanners_that_dominate_slice(self, start, stop):
        from abjad.tools import spannertools
        if start == stop:
            if start == 0:
                left = None
            else:
                left = self[start - 1]
            if len(self) <= stop:
                right = None
            else:
                right = self[stop]
            spanners_receipt = \
                self._get_spanners_that_dominate_component_pair(left, right)
        else:
            selection = self[start:stop]
            spanners_receipt = selection._get_dominant_spanners()
        return spanners_receipt

    def _scale_contents(self, multiplier):
        from abjad.tools import iterationtools
        for expr in \
            iterationtools.iterate_topmost_tie_chains_and_components_in_expr(
            self[:]):
            expr._scale(multiplier)

    def _set_item(
        self, 
        i, 
        expr, 
        withdraw_components_in_expr_from_crossing_spanners=True,
        ):
        r'''This method exists beacuse __setitem__ can not accept keywords.
        Note that setting 
        withdraw_components_in_expr_from_crossing_spanners=False
        constitutes a composer-unsafe use of this method.
        Only private methods should set this keyword.
        '''
        from abjad.tools import scoretools
        from abjad.tools import containertools
        from abjad.tools import contexttools
        from abjad.tools import iterationtools
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        # cache context marks attached to expr
        expr_context_marks = []
        for component in iterationtools.iterate_components_in_expr(expr):
            context_marks = component._get_marks(contexttools.ContextMark)
            expr_context_marks.extend(context_marks)
        # item assignment
        if isinstance(i, int):
            if isinstance(expr, str):
                expr = self._parse_string(expr)[:]
                assert len(expr) == 1, repr(expr)
                expr = expr[0]
            assert all(isinstance(x, scoretools.Component) for x in [expr])
            if any(isinstance(x, containertools.GraceContainer) for x in [expr]):
                message = 'must attach grace container to note or chord.'
                raise Exception(message)
            old = self[i]
            selection = selectiontools.ContiguousSelection(old)
            spanners_receipt = selection._get_dominant_spanners()
            for child in iterationtools.iterate_components_in_expr([old]):
                for spanner in child._get_spanners():
                    spanner._remove(child)
            if i < 0:
                i = len(self) + i
            del(self[i])
            # must withdraw from spanners before withdrawing from parentage!
            # otherwise begin / end assessments don't work!
            if withdraw_components_in_expr_from_crossing_spanners:
                selection = selectiontools.SliceSelection([expr])
                selection._withdraw_from_crossing_spanners()
            expr._set_parent(self)
            self._music.insert(i, expr)
            for spanner, index in spanners_receipt:
                spanner._insert(index, expr)
                expr._spanners.add(spanner)
        # slice assignment
        else:
            if isinstance(expr, str):
                expr = self._parse_string(expr)[:]
            elif isinstance(expr, list) and \
                len(expr) == 1 and \
                isinstance(expr[0], str):
                expr = self._parse_string(expr[0])[:]
            assert all(isinstance(x, scoretools.Component) for x in expr)
            if any(isinstance(x, containertools.GraceContainer) for x in expr):
                message = 'must attach grace container to note or chord.'
                raise Exception(message)
            if i.start == i.stop and i.start is not None \
                and i.stop is not None and i.start <= -len(self):
                start, stop = 0, 0
            else:
                start, stop, stride = i.indices(len(self))
            old = self[start:stop]
            spanners_receipt = self._get_spanners_that_dominate_slice(
                start, stop)
            for component in old:
                for child in iterationtools.iterate_components_in_expr(
                    [component]):
                    for spanner in child._get_spanners():
                        spanner._remove(child)
            del(self[start:stop])
            # must withdraw before setting in self!
            # otherwise circular withdraw ensues!
            if withdraw_components_in_expr_from_crossing_spanners:
                selection = selectiontools.SliceSelection(expr)
                if selection._all_are_contiguous_components_in_same_logical_voice(
                    selection):
                    selection._withdraw_from_crossing_spanners()
            self._music.__setitem__(slice(start, start), expr)
            for component in expr:
                component._set_parent(self)
            for spanner, index in spanners_receipt:
                for component in reversed(expr):
                    spanner._insert(index, component)
                    component._spanners.add(spanner)
        for expr_context_mark in expr_context_marks:
            expr_context_mark._update_effective_context()

    ### PUBLIC PROPERTIES ###

    @apply
    def is_simultaneous():
        def fget(self):
            r'''Simultaneity status of container.

            ..  container:: example

                **Example 1.** Get simultaneity status of container:

                ::

                    >>> container = Container()
                    >>> container.append(Voice("c'8 d'8 e'8"))
                    >>> container.append(Voice('g4.'))
                    >>> show(container) # doctest: +SKIP

                ..  doctest::

                    >>> f(container)
                    {
                        \new Voice {
                            c'8
                            d'8
                            e'8
                        }
                        \new Voice {
                            g4.
                        }
                    }

                ::

                    >>> container.is_simultaneous
                    False

            ..  container:: example

                **Example 2.** Set simultaneity status of container:

                ::

                    >>> container = Container()
                    >>> container.append(Voice("c'8 d'8 e'8"))
                    >>> container.append(Voice('g4.'))
                    >>> show(container) # doctest: +SKIP

                ..  doctest::

                    >>> f(container)
                    {
                        \new Voice {
                            c'8
                            d'8
                            e'8
                        }
                        \new Voice {
                            g4.
                        }
                    }

                ::

                    >>> container.is_simultaneous = True
                    >>> show(container) # doctest: +SKIP

                ..  doctest::

                    >>> f(container)
                    <<
                        \new Voice {
                            c'8
                            d'8
                            e'8
                        }
                        \new Voice {
                            g4.
                        }
                    >>

            Returns boolean.
            '''
            return self._simultaneous
        def fset(self, expr):
            from abjad.tools.contexttools.Context import Context
            from abjad.tools import scoretools
            assert isinstance(expr, bool), repr(expr)
            if expr == True:
                assert all(isinstance(x, Context) for x in self._music)
            self._simultaneous = expr
            self._update_later(offsets=True)
        return property(**locals())

    ### PRIVATE METHODS ###

    @staticmethod
    def _all_are_orphan_components(expr):
        from abjad.tools import scoretools
        for component in expr:
            if not isinstance(component, scoretools.Component):
                return False
            if not component._get_parentage().is_orphan:
                return False
        return True

    def _initialize_music(self, music):
        from abjad.tools import scoretools
        Selection = selectiontools.Selection
        if music is None:
            music = []
        if self._all_are_orphan_components(music):
            self._music = list(music)
            self[:]._set_parents(self)
        elif Selection._all_are_contiguous_components_in_same_logical_voice(
            music):
            music = selectiontools.SliceSelection(music)
            parent, start, stop = music._get_parent_and_start_stop_indices()
            self._music = list(music)
            self[:]._set_parents(self)
            assert parent is not None
            parent._music.insert(start, self)
            self._set_parent(parent)
        elif isinstance(music, str):
            parsed = self._parse_string(music)
            self._music = []
            self.is_simultaneous = parsed.is_simultaneous
            if parsed.is_simultaneous or \
                not Selection._all_are_contiguous_components_in_same_logical_voice(
                parsed[:]):
                while len(parsed):
                    self.append(parsed.pop(0))
            else:
                self[:] = parsed[:]
        else:
            message = 'can not initialize container from {!r}.'
            message = message.format((music))
            raise TypeError(message)

    def _is_one_of_my_first_leaves(self, leaf):
        return leaf in self._get_descendants_starting_with()

    def _is_one_of_my_last_leaves(self, leaf):
        return leaf in self._get_descendants_stopping_with()

    def _move_spanners_to_children(self):
        for spanner in self._get_spanners():
            i = spanner.index(self)
            spanner._components.__setitem__(slice(i, i + 1), self[:])
            for component in self:
                component._spanners.add(spanner)
            self._spanners.discard(spanner)
        return self

    def _parse_string(self, string):
        from abjad.tools import lilypondfiletools
        from abjad.tools import lilypondparsertools
        from abjad.tools import rhythmtreetools
        user_input = string.strip()
        if user_input.startswith('abj:'):
            parser = lilypondparsertools.ReducedLyParser()
            parsed = parser(user_input[4:])
            if parser._toplevel_component_count == 1:
                parsed = Container([parsed])
        elif user_input.startswith('rtm:'):
            parsed = rhythmtreetools.parse_rtm_syntax(user_input[4:])
        else:
            if not user_input.startswith('<<') or \
                not user_input.endswith('>>'):
                user_input = '{{ {} }}'.format(user_input)
            parsed = lilypondparsertools.LilyPondParser()(user_input)
            if isinstance(parsed, lilypondfiletools.LilyPondFile):
                parsed = Container(parsed[:])
            assert isinstance(parsed, Container)
        return parsed

    def _scale(self, multiplier):
        self._scale_contents(multiplier)

    def _split_at_index(self, i, fracture_spanners=False):
        r'''Splits container to the left of index `i`.

        Preserves tuplet multiplier when container is a tuplet.

        Preserves time signature denominator when container is a measure.

        Resizes resizable containers.

        Returns split parts.
        '''
        from abjad.tools import spannertools
        from abjad.tools import containertools
        from abjad.tools import contexttools
        from abjad.tools import measuretools
        from abjad.tools import tuplettools
        # partition my music
        left_music = self[:i]
        right_music = self[i:]
        # instantiate new left and right containers
        if isinstance(self, measuretools.Measure):
            time_signature = self._get_effective_context_mark(
                contexttools.TimeSignatureMark)
            denominator = time_signature.denominator
            left_duration = sum([x._get_duration() for x in left_music])
            left_pair = mathtools.NonreducedFraction(left_duration)
            left_pair = left_pair.with_multiple_of_denominator(denominator)
            left_time_signature = contexttools.TimeSignatureMark(left_pair)
            left = self.__class__(left_time_signature, left_music)
            right_duration = sum([x._get_duration() for x in right_music])
            right_pair = mathtools.NonreducedFraction(right_duration)
            right_pair = right_pair.with_multiple_of_denominator(denominator)
            right_time_signature = contexttools.TimeSignatureMark(right_pair)
            right = self.__class__(right_time_signature, right_music)
        elif isinstance(self, tuplettools.FixedDurationTuplet):
            multiplier = self.multiplier
            left = self.__class__(1, left_music)
            right = self.__class__(1, right_music)
            target_duration = multiplier * left._contents_duration
            left.target_duration = target_duration
            target_duration = multiplier * right._contents_duration
            right.target_duration = target_duration
        elif isinstance(self, tuplettools.Tuplet):
            multiplier = self.multiplier
            left = self.__class__(multiplier, left_music)
            right = self.__class__(multiplier, right_music)
        else:
            left = self.__class__(left_music)
            right = self.__class__(right_music)
        # save left and right containers together for iteration
        halves = (left, right)
        nonempty_halves = [half for half in halves if len(half)]
        # give my attached spanners to my children
        self._move_spanners_to_children()
        # incorporate left and right parents in score if possible
        selection = self.select(sequential=True)
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        if parent is not None:
            parent._music.__setitem__(slice(start, stop + 1), nonempty_halves)
            for part in nonempty_halves:
                part._set_parent(parent)
        else:
            left._set_parent(None)
            right._set_parent(None)
        # fracture spanners if requested
        if fracture_spanners:
            for spanner in left._get_spanners():
                index = spanner.index(left)
                spanner.fracture(index, direction=Right)
        # return new left and right containers
        return halves

    def _split_by_duration(
        self,
        duration,
        fracture_spanners=False,
        tie_split_notes=True,
        ):
        from abjad.tools import scoretools
        from abjad.tools import containertools
        from abjad.tools import iterationtools
        from abjad.tools import leaftools
        from abjad.tools import measuretools
        from abjad.tools import notetools
        from abjad.tools import resttools
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        # check input
        duration = durationtools.Duration(duration)
        assert 0 <= duration, repr(duration)
        # if zero duration then return empty list and self
        if duration == 0:
            return [], self
        # get split point score offset
        global_split_point = self._get_timespan().start_offset + duration
        # get any duration-crossing descendents
        cross_offset = self._get_timespan().start_offset + duration
        duration_crossing_descendants = []
        for descendant in self._get_descendants():
            start_offset = descendant._get_timespan().start_offset
            stop_offset = descendant._get_timespan().stop_offset
            if start_offset < cross_offset < stop_offset:
                duration_crossing_descendants.append(descendant)
        # get any duration-crossing measure descendents
        measures = [
            x for x in duration_crossing_descendants 
            if isinstance(x, measuretools.Measure)
            ]
        # if we must split a power-of-two measure at non-power-of-two 
        # split point then go ahead and transform the power-of-two measure 
        # to non-power-of-two equivalent now; 
        # code that crawls and splits later on will be happier
        if len(measures) == 1:
            measure = measures[0]
            split_point_in_measure = \
                global_split_point - measure._get_timespan().start_offset
            if measure.has_non_power_of_two_denominator:
                if not measure.implied_prolation ==\
                    split_point_in_measure.implied_prolation:
                    raise NotImplementedError
            elif not mathtools.is_nonnegative_integer_power_of_two(
                split_point_in_measure.denominator):
                non_power_of_two_factors = mathtools.remove_powers_of_two(
                    split_point_in_measure.denominator)
                non_power_of_two_factors = mathtools.factors(
                    non_power_of_two_factors)
                non_power_of_two_product = 1
                for non_power_of_two_factor in non_power_of_two_factors:
                    non_power_of_two_product *= non_power_of_two_factor
                measuretools.scale_measure_denominator_and_adjust_measure_contents(
                    measure, non_power_of_two_product)
                # rederive duration crosses with possibly new measure contents
                cross_offset = self._get_timespan().start_offset + duration
                duration_crossing_descendants = []
                for descendant in self._get_descendants():
                    start_offset = descendant._get_timespan().start_offset
                    stop_offset = descendant._get_timespan().stop_offset
                    if start_offset < cross_offset < stop_offset:
                        duration_crossing_descendants.append(descendant)
        elif 1 < len(measures):
            raise Exception('measures can not nest.')
        # any duration-crossing leaf will be at end of list
        bottom = duration_crossing_descendants[-1]
        did_split_leaf = False
        # if split point necessitates leaf split
        if isinstance(bottom, leaftools.Leaf):
            assert isinstance(bottom, leaftools.Leaf)
            did_split_leaf = True
            split_point_in_bottom = \
                global_split_point - bottom._get_timespan().start_offset
            left_list, right_list = bottom._split_by_duration(
                split_point_in_bottom,
                fracture_spanners=fracture_spanners,
                tie_split_notes=tie_split_notes,
                )
            right = right_list[0]
            leaf_right_of_split = right
            leaf_left_of_split = left_list[-1]
            duration_crossing_containers = duration_crossing_descendants[:-1]
            if not len(duration_crossing_containers):
                return left_list, right_list
        # if split point falls between leaves
        # then find leaf to immediate right of split point
        # in order to start upward crawl through duration-crossing containers
        else:
            duration_crossing_containers = duration_crossing_descendants[:]
            for leaf in iterationtools.iterate_leaves_in_expr(bottom):
                if leaf._get_timespan().start_offset == global_split_point:
                    leaf_right_of_split = leaf
                    leaf_left_of_split = leaf_right_of_split._get_leaf(-1)
                    break
            else:
                message = 'can not split empty container {!r}.'
                message = message.format(bottom)
                raise Exception(message)
        # find component to right of split that is also immediate child of 
        # last duration-crossing container
        for component in \
            leaf_right_of_split._get_parentage(include_self=True):
            if component._parent is duration_crossing_containers[-1]:
                highest_level_component_right_of_split = component
                break
        else:
            message = 'should we be able to get here?'
            raise ValueError(message)
        # crawl back up through duration-crossing containers and 
        # fracture spanners if requested
        if fracture_spanners:
            start_offset = leaf_right_of_split._get_timespan().start_offset
            for parent in leaf_right_of_split._get_parentage():
                if parent._get_timespan().start_offset == start_offset:
                    for spanner in parent._get_spanners():
                        index = spanner.index(parent)
                        spanner.fracture(index, direction=Left)
                if parent is component:
                    break
        # crawl back up through duration-crossing containers and split each
        previous = highest_level_component_right_of_split
        for duration_crossing_container in \
            reversed(duration_crossing_containers):
            assert isinstance(
                duration_crossing_container, containertools.Container)
            i = duration_crossing_container.index(previous)
            left, right = duration_crossing_container._split_at_index(
                i,
                fracture_spanners=fracture_spanners,
                )
            previous = right
        # NOTE: If tie chain here is convenience, then fusing is good.
        #       If tie chain here is user-given, then fusing is less good.
        #       Maybe later model difference between user tie chains and not.
        left_tie_chain = leaf_left_of_split._get_tie_chain()
        right_tie_chain = leaf_right_of_split._get_tie_chain()
        left_tie_chain._fuse_leaves_by_immediate_parent()
        right_tie_chain._fuse_leaves_by_immediate_parent()
        # reapply tie here if crawl above killed tie applied to leaves
        if did_split_leaf:
            if tie_split_notes and \
                isinstance(leaf_left_of_split, notetools.Note):
                if leaf_left_of_split._get_parentage().root is \
                    leaf_right_of_split._get_parentage().root:
                    leaves_around_split = \
                        (leaf_left_of_split, leaf_right_of_split)
                    selection = selectiontools.ContiguousSelection(
                        leaves_around_split)
                    selection._attach_tie_spanner_to_leaf_pair()
        # return pair of left and right list-wrapped halves of container
        return ([left], [right])

    ### PUBLIC METHODS ###

    def append(self, component):
        r'''Appends `component` to container.

        ..  container:: example

            ::

                >>> container = Container("c'4 ( d'4 f'4 )")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    c'4 (
                    d'4
                    f'4 )
                }

            ::

                >>> container.append(Note("e'4"))
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    c'4 (
                    d'4
                    f'4 )
                    e'4
                }

        Returns none.
        '''
        self.__setitem__(slice(len(self), len(self)), [component])

    def extend(self, expr):
        r'''Extends container with `expr`.

        ..  container:: example

            ::

                >>> container = Container("c'4 ( d'4 f'4 )")
                >>> show(container) # doctest: +SKIP

            ..  doctest:: 

                >>> f(container)
                {
                    c'4 (
                    d'4
                    f'4 )
                }

            ::

                >>> notes = [Note("e'32"), Note("d'32"), Note("e'16")]
                >>> container.extend(notes)
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    c'4 (
                    d'4
                    f'4 )
                    e'32
                    d'32
                    e'16
                }

        Returns none.
        '''
        self.__setitem__(
            slice(len(self), len(self)), 
            expr.__getitem__(slice(0, len(expr)))
            )

    def index(self, component):
        r'''Returns index of `component` in container.

        ..  container:: example

            ::

                >>> container = Container("c'4 d'4 f'4 e'4")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    c'4
                    d'4
                    f'4
                    e'4
                }

            ::

                >>> note = container[-1]
                >>> note
                Note("e'4")

            ::

                >>> container.index(note)
                3

        Returns nonnegative integer.
        '''
        for i, element in enumerate(self._music):
            if element is component:
                return i
        else:
            message = 'component {!r} not in Abjad container {!r}.'
            message = message.format(component, self)
            raise ValueError(message)

    def insert(self, i, component, fracture_spanners=False):
        r'''Inserts `component` at index `i` in container.

        ..  container:: example

            **Example 1.** Insert note. Do not fracture spanners:

            ::

                >>> container = Container([])
                >>> container.extend("fs16 cs' e' a'")
                >>> container.extend("cs''16 e'' cs'' a'")
                >>> container.extend("fs'16 e' cs' fs")
                >>> slur = spannertools.SlurSpanner()
                >>> attach(slur, container[:])
                >>> slur.direction = Down
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    fs16 _ (
                    cs'16
                    e'16
                    a'16
                    cs''16
                    e''16
                    cs''16
                    a'16
                    fs'16
                    e'16
                    cs'16
                    fs16 )
                }

            ::

                >>> container.insert(-4, Note("e'4"), fracture_spanners=False)
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    fs16 _ (
                    cs'16
                    e'16
                    a'16
                    cs''16
                    e''16
                    cs''16
                    a'16
                    e'4
                    fs'16
                    e'16
                    cs'16
                    fs16 )
                }

        ..  container:: example

            **Example 2.** Insert note. Fracture spanners:

            ::

                >>> container = Container([])
                >>> container.extend("fs16 cs' e' a'")
                >>> container.extend("cs''16 e'' cs'' a'")
                >>> container.extend("fs'16 e' cs' fs")
                >>> slur = spannertools.SlurSpanner()
                >>> attach(slur, container[:])
                >>> slur.direction = Down
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    fs16 _ (
                    cs'16
                    e'16
                    a'16
                    cs''16
                    e''16
                    cs''16
                    a'16
                    fs'16
                    e'16
                    cs'16
                    fs16 )
                }

            ::

                >>> container.insert(-4, Note("e'4"), fracture_spanners=True)
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    fs16 _ (
                    cs'16
                    e'16
                    a'16
                    cs''16
                    e''16
                    cs''16
                    a'16 )
                    e'4
                    fs'16 _ (
                    e'16
                    cs'16
                    fs16 )
                }

        Returns none.
        '''
        from abjad.tools import scoretools
        from abjad.tools import containertools
        from abjad.tools import leaftools
        from abjad.tools import spannertools
        assert isinstance(component, scoretools.Component)
        assert isinstance(i, int)
        if not fracture_spanners:
            self.__setitem__(slice(i, i), [component])
            return
        component._set_parent(self)
        self._music.insert(i, component)
        previous_leaf = component._get_leaf(-1)
        if previous_leaf:
            for spanner in previous_leaf._get_spanners():
                index = spanner.index(previous_leaf)
                spanner.fracture(index, direction=Right)
        next_leaf = component._get_leaf(1)
        if next_leaf:
            for spanner in next_leaf._get_spanners():
                index = spanner.index(next_leaf)
                spanner.fracture(index, direction=Left)

    def pop(self, i=-1):
        r'''Pops component from container at index `i`.

        ..  container:: example

            ::

                >>> container = Container("c'4 ( d'4 f'4 ) e'4")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    c'4 (
                    d'4
                    f'4 )
                    e'4
                }

            ::

                >>> container.pop()
                Note("e'4")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    c'4 (
                    d'4
                    f'4 )
                }

        Returns component.
        '''
        component = self[i]
        del(self[i])
        return component

    def remove(self, component):
        r'''Removes `component` from container.

        ..  container:: example

            ::

                >>> container = Container("c'4 ( d'4 f'4 ) e'4")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    c'4 (
                    d'4
                    f'4 )
                    e'4
                }

            ::

                >>> note = container[2]
                >>> note
                Note("f'4")

            ::

                >>> container.remove(note)
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    c'4 (
                    d'4 )
                    e'4
                }

        Returns none.
        '''
        i = self.index(component)
        del(self[i])

    def reverse(self):
        r'''Reverses contents of container.

        ..  container:: example
        
            ::

                >>> staff = Staff("c'8 [ d'8 ] e'8 ( f'8 )")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 [
                    d'8 ]
                    e'8 (
                    f'8 )
                }

            ::

                >>> staff.reverse()
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff) # doctest: +SKIP
                \new Staff {
                    f'8 (
                    e'8 )
                    d'8 [
                    c'8 ]
                }

        Returns none.
        '''
        from abjad.tools import containertools
        from abjad.tools import spannertools
        def _offset(x, y):
            if x._get_timespan().start_offset < y._get_timespan().start_offset:
                return -1
            elif y._get_timespan().start_offset < x._get_timespan().start_offset:
                return 1
            else:
                return 0
        self._music.reverse()
        self._update_later(offsets=True)
        spanners = self._get_descendants()._get_spanners()
        for s in spanners:
            s._components.sort(_offset)

    def select_leaves(
        self,
        start=0,
        stop=None,
        leaf_classes=None,
        recurse=True,
        allow_discontiguous_leaves=False,
        ):
        r'''Selects leaves in container.

        ..  container:: example

            ::

                >>> container = Container("c'8 d'8 r8 e'8")

            ::

                >>> container.select_leaves()
                ContiguousSelection(Note("c'8"), Note("d'8"), Rest('r8'), Note("e'8"))

        Returns contiguous leaf selection or free leaf selection.
        '''
        from abjad.tools import scoretools
        from abjad.tools import iterationtools
        from abjad.tools import leaftools
        from abjad.tools import selectiontools
        Selection = selectiontools.Selection
        leaf_classes = leaf_classes or (leaftools.Leaf,)
        expr = self
        if recurse:
            expr = iterationtools.iterate_leaves_in_expr(expr)
        music = [
                component for component in expr
                if isinstance(component, leaf_classes)
                ]
        music = music[start:stop]
        if allow_discontiguous_leaves:
            selection = selectiontools.Selection(music=music)
        else:
            assert Selection._all_are_contiguous_components_in_same_logical_voice(
                music)
            selection = selectiontools.ContiguousSelection(music=music)
        return selection

    def select_notes_and_chords(self):
        r'''Selects notes and chords in container.

        ..  container:: example

            ::

                >>> container.select_notes_and_chords()
                Selection(Note("c'8"), Note("d'8"), Note("e'8"))

        Returns leaf selection.
        '''
        from abjad.tools import iterationtools
        from abjad.tools import selectiontools
        generator = iterationtools.iterate_notes_and_chords_in_expr(self)
        return selectiontools.Selection(generator)
