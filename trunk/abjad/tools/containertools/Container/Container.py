# -*- encoding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import selectiontools
from abjad.tools.componenttools.Component import Component


class Container(Component):
    r'''Abjad model of an iterable container of music.

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

        Return boolean.
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

        Return none.
        '''
        components = self[i]
        if not isinstance(components, selectiontools.SliceSelection):
            components = selectiontools.SliceSelection([components])
        components._withdraw_from_crossing_spanners()
        components._set_parents(None)

    def __getitem__(self, i):
        r'''Get container `i`.
        Shallow traversal of container for numeric indices only.

        Return component.
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

        Return nonnegative integer.
        '''
        return len(self._music)

    def __repr__(self):
        r'''Representation of container in Python interpreter.

        Return string.
        '''
        return self._compact_representation

    def __setitem__(self, i, expr):
        r'''Set container `i` equal to `expr`.
        Find spanners that dominate self[i] and children of self[i].
        Replace contents at self[i] with 'expr'.
        Reattach spanners to new contents.
        This operation always leaves score tree in tact.

        Return none.
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
        if self.is_simultaneous:
            return max([durationtools.Duration(0)] + 
                [x._get_duration(in_seconds=True) for x in self])
        else:
            duration = durationtools.Duration(0)
            for leaf in self.select_leaves(allow_discontiguous_leaves=True):
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
        from abjad.tools import componenttools
        from abjad.tools import contexttools
        from abjad.tools import leaftools
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
            assert all(isinstance(x, componenttools.Component) for x in [expr])
            if any(isinstance(x, leaftools.GraceContainer) for x in [expr]):
                message = 'must attach grace container to note or chord.'
                raise GraceContainerError(message)
            old = self[i]
            spanners_receipt = \
                spannertools.get_spanners_that_dominate_components([old])
            # must withdraw from spanners before parentage!
            # otherwise begin / end assessments don't work!
            if withdraw_components_in_expr_from_crossing_spanners:
                selection = selectiontools.SliceSelection([expr])
                selection._withdraw_from_crossing_spanners()
            expr._set_parent(self)
            self._music.insert(i, expr)
            componenttools.remove_component_subtree_from_score_and_spanners(
                [old])
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
            assert all(isinstance(x, componenttools.Component) for x in expr)
            if any(isinstance(x, leaftools.GraceContainer) for x in expr):
                message = 'must attach grace container to note or chord.'
                raise GraceContainerError(message)
            if i.start == i.stop and i.start is not None \
                and i.stop is not None and i.start <= -len(self):
                start, stop = 0, 0
            else:
                start, stop, stride = i.indices(len(self))
            old = self[start:stop]
            spanners_receipt = \
                spannertools.get_spanners_that_dominate_container_components_from_to(
                self, start, stop)
            componenttools.remove_component_subtree_from_score_and_spanners(
                old)
            # must withdraw before setting in self!
            # otherwise circular withdraw ensues!
            if withdraw_components_in_expr_from_crossing_spanners:
                selection = selectiontools.SliceSelection(expr)
                if selection._all_are_thread_contiguous_components():
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
            r'''Set to true to interpret container contents in simultaneous.
            Set to false to interpret container contents sequentially.

            **Example 1.** Sequential container:

            ..  container:: example

                ::

                    >>> container = Container([Voice("c'8 d'8 e'8"), Voice('g4.')])
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

            **Example 2.** simultaneous container:

            ..  container:: example

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

            Return boolean.
            '''
            return self._simultaneous
        def fset(self, expr):
            from abjad.tools.contexttools.Context import Context
            from abjad.tools import componenttools
            assert isinstance(expr, bool), repr(expr)
            if expr == True:
                assert all(isinstance(x, Context) for x in self._music)
            self._simultaneous = expr
            self._mark_entire_score_tree_for_later_update('prolated')
        return property(**locals())

    ### PRIVATE METHODS ###

    def _initialize_music(self, music):
        from abjad.tools import componenttools
        if music is None:
            music = []
        if componenttools.all_are_contiguous_components_in_same_thread(music):
            music = selectiontools.SliceSelection(music)
            parent, start, stop = music._get_parent_and_start_stop_indices()
            self._music = list(music)
            self[:]._set_parents(self)
            if parent is not None:
                parent._music.insert(start, self)
                self._set_parent(parent)
        elif isinstance(music, str):
            parsed = self._parse_string(music)
            self._music = []
            self.is_simultaneous = parsed.is_simultaneous
            if parsed.is_simultaneous or \
                not componenttools.all_are_thread_contiguous_components(
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
        return leaf in self._select_descendants_starting_with()

    def _is_one_of_my_last_leaves(self, leaf):
        return leaf in self._select_descendants_stopping_with()

    def _parse_string(self, string):
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
            if not user_input.startswith('<<') and \
                not user_input.endswith('>>'):
                user_input = '{ %s }' % user_input
            parsed = lilypondparsertools.LilyPondParser()(user_input)
            assert isinstance(parsed, Container)
        return parsed

    def _shorten(self, duration):
        accumulated_duration = durationtools.Duration(0)
        components = []
        for component in self:
            current_duration = component._get_duration()
            if accumulated_duration + current_duration <= duration:
                components.append(component)
                accumulated_duration += current_duration
            else:
                break
        del(self[:len(components)])
        remaining_subtrahend_duration = duration - accumulated_duration
        self[0]._shorten(remaining_subtrahend_duration)

    ### PUBLIC METHODS ###

    def append(self, component):
        r'''Append `component` to container.

        **Example**:

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

        Return none.
        '''
        self.__setitem__(slice(len(self), len(self)), [component])

    def extend(self, expr):
        r'''Extend container with `expr`.

        **Example**:

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

        Return none.
        '''
        self.__setitem__(
            slice(len(self), len(self)), 
            expr.__getitem__(slice(0, len(expr)))
            )

    def index(self, component):
        r'''Return index of `component` in container.

        **Example**:

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

        Return nonnegative integer.
        '''
        for i, element in enumerate(self._music):
            if element is component:
                return i
        else:
            message = 'component {!r} not in Abjad container {!r}.'
            message = message.format(component, self)
            raise ValueError(message)

    def insert(self, i, component, fracture_spanners=False):
        r'''Insert `component` at index `i` in container.

        **Example 1.** Insert note. Do not fracture spanners:

        ..  container:: example

            ::

                >>> container = Container([])
                >>> container.extend("fs16 cs' e' a'")
                >>> container.extend("cs''16 e'' cs'' a'")
                >>> container.extend("fs'16 e' cs' fs")
                >>> slur = spannertools.SlurSpanner(container[:])
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

        **Example 2.** Insert note. Fracture spanners:

        ..  container:: example

            ::

                >>> container = Container([])
                >>> container.extend("fs16 cs' e' a'")
                >>> container.extend("cs''16 e'' cs'' a'")
                >>> container.extend("fs'16 e' cs' fs")
                >>> slur = spannertools.SlurSpanner(container[:])
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

        Return none.
        '''
        from abjad.tools import componenttools
        from abjad.tools import containertools
        from abjad.tools import leaftools
        from abjad.tools import spannertools
        assert isinstance(component, componenttools.Component)
        assert isinstance(i, int)
        if not fracture_spanners:
            self.__setitem__(slice(i, i), [component])
            return
        result = []
        component._set_parent(self)
        self._music.insert(i, component)
        previous_leaf = leaftools.get_nth_leaf_in_thread_from_leaf(
            component, -1)
        if previous_leaf:
            result.extend(
                spannertools.fracture_spanners_attached_to_component(
                    previous_leaf, direction=Right))
        next_leaf = leaftools.get_nth_leaf_in_thread_from_leaf(component, 1)
        if next_leaf:
            result.extend(
                spannertools.fracture_spanners_attached_to_component(
                    next_leaf, direction=Left))

    def pop(self, i=-1):
        r'''Pop component from container at index `i`.

        **Example**:

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

        Return component.
        '''
        component = self[i]
        del(self[i])
        return component

    def remove(self, component):
        r'''Remove `component` from container.

        **Example**:

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

        Return none.
        '''
        i = self.index(component)
        del(self[i])

    def reverse(self):
        r'''Reverse contents of container.

        **Example**:

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

        Return none.
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
        self._mark_entire_score_tree_for_later_update('prolated')
        spanners = spannertools.get_spanners_attached_to_any_improper_child_of_component(
            self)
        for s in spanners:
            s._components.sort(_offset)

    def select_leaves(
        self,
        leaf_classes=None,
        recurse=True,
        allow_discontiguous_leaves=False,
        ):
        r'''Select leaves in container.

        ..  container:: example

            **Example**:

            ::

                >>> container = Container("c'8 d'8 r8 e'8")

            ::

                >>> container.select_leaves()
                ContiguousLeafSelection(Note("c'8"), Note("d'8"), Rest('r8'), Note("e'8"))

        Return contiguous leaf selection or free leaf selection.
        '''
        from abjad.tools import selectiontools
        return selectiontools.select_leaves(
            expr=self,
            leaf_classes=leaf_classes,
            recurse=recurse,
            allow_discontiguous_leaves=allow_discontiguous_leaves,
            )

    def select_notes_and_chords(self):
        r'''Select notes and chords in container.

        **Example**:

        ..  container:: example

            ::

                >>> container.select_notes_and_chords()
                ContiguousLeafSelection(Note("c'8"), Note("d'8"), Note("e'8"))

        Return leaf selection.
        '''
        from abjad.tools import iterationtools
        from abjad.tools import selectiontools
        generator = iterationtools.iterate_notes_and_chords_in_expr(self)
        return selectiontools.ContiguousLeafSelection(generator)
