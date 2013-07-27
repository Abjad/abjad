import copy
import itertools
import types
from abjad.tools.abctools.AbjadObject import AbjadObject


class Selection(AbjadObject):
    '''Selection of components taken from a single score:

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> selection = staff[:2]
        >>> selection
        Selection(Note("c'4"), Note("d'4"))

    Selection objects will eventually pervade the system and 
    model all user selections.

    This means that selection objects will eventually serve as input
    to most functions in the API. Selection objects will also
    eventually be returned as output from most functions in the API.

    Selections are immutable and never change after instantiation.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_music',
        )

    _default_positional_input_arguments = (
        [],
        )

    ### INITIALIZER ###

    def __init__(self, music=None):
        if music is None:
            music = ()
        elif isinstance(music, (tuple, list)):
            music = tuple(music)
        elif isinstance(music, Selection):
            music = tuple(music)
        elif isinstance(music, types.GeneratorType):
            music = tuple(music)
        else:
            music = (music, )
        self._music = tuple(music)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        assert isinstance(expr, (type(self), list, tuple))
        if isinstance(expr, type(self)):
            music = self.music + expr.music
            return type(self)(music)
        # eventually remove this permissive branch 
        # and force the use of selections only
        elif isinstance(expr, (tuple, list)):
            music = self.music + tuple(expr)
        return type(self)(music)

    def __contains__(self, expr):
        return expr in self.music

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            return self.music == expr.music
        # eventually remove this permissive branch
        # and force the use of selections only
        elif isinstance(expr, (list, tuple)):
            return self.music == tuple(expr)

    def __getitem__(self, expr):
        result = self.music.__getitem__(expr)
        if isinstance(result, tuple):
            selection = type(self)()
            selection._music = result[:]
            result = selection
        return result

    def __len__(self):
        return len(self.music)

    def __ne__(self, expr):
        return not self == expr

    def __radd__(self, expr):
        assert isinstance(expr, (type(self), list, tuple))
        if isinstance(expr, type(self)):
            music = expr.music + self.music
            return Selection(music)
        # eventually remove this permissive branch 
        # and force the use of selections only
        elif isinstance(expr, (tuple, list)):
            music = tuple(expr) + self.music
        return Selection(music)

    def __repr__(self):
        return '{}{!r}'.format(self._class_name, self.music)

    ### PRIVATE METHODS ###

    def _attach_tie_spanner_to_leaf_pair(self):
        from abjad.tools import leaftools
        from abjad.tools import spannertools
        assert len(self) == 2
        left_leaf, right_leaf = self
        assert isinstance(left_leaf, leaftools.Leaf)
        assert isinstance(right_leaf, leaftools.Leaf)
        left_tie_chain = left_leaf.select_tie_chain()
        right_tie_chain = right_leaf.select_tie_chain()
        spanner_classes = (spannertools.TieSpanner,)
        if left_tie_chain == right_tie_chain:
            return
        try:
            left_tie_spanner = left_leaf._get_spanner(spanner_classes)
        except MissingSpannerError:
            left_tie_spanner = None
        try:
            right_tie_spanner = right_leaf._get_spanner(spanner_classes)
        except MissingSpannerError:
            right_tie_spanner = None
        if left_tie_spanner is not None and right_tie_spanner is not None:
            left_tie_spanner.fuse(right_tie_spanner)
        elif left_tie_spanner is not None and right_tie_spanner is None:
            left_tie_spanner.append(right_leaf)
        elif left_tie_spanner is None and right_tie_spanner is not None:
            right_tie_spanner.append_left(left_leaf)
        elif left_tie_spanner is None and right_tie_spanner is None:
            spannertools.TieSpanner([left_leaf, right_leaf])

    # TODO: eventually migrate method to SliceSelection;
    #       then remove explicit contiguity check.
    def _give_dominant_spanners_to_components(self, recipients):
        '''Find all spanners dominating music.
        Insert each component in recipients into each dominant spanner.
        Remove music from each dominating spanner.
        Return none.
        Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import spannertools
        assert componenttools.all_are_thread_contiguous_components(self)
        assert componenttools.all_are_thread_contiguous_components(recipients)
        receipt = spannertools.get_spanners_that_dominate_components(self)
        for spanner, index in receipt:
            for recipient in reversed(recipients):
                spanner._insert(index, recipient)
            for component in self:
                spanner._remove(component)

    # TODO: eventually migrate method to SliceSelection;
    #       then remove explicit contiguity check.
    def _give_music_to_empty_container(self, container):
        '''Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import containertools
        assert componenttools.all_are_contiguous_components_in_same_parent(
            self)
        assert isinstance(container, containertools.Container)
        assert not container
        music = []
        for component in self:
            music.extend(getattr(component, 'music', ()))
        container._music.extend(music)
        container[:]._set_parents(container)

    # TODO: eventually migrate method to SliceSelection;
    #       then remove explicit contiguity check.
    def _give_position_in_parent_to_container(self, container):
        '''Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import containertools
        assert componenttools.all_are_contiguous_components_in_same_parent(
            self)
        assert isinstance(container, containertools.Container)
        parent, start, stop = self.get_parent_and_start_stop_indices()
        if parent is not None:
            parent._music.__setitem__(slice(start, start), [container])
            container._set_parent(parent)
            self._set_parents(None)

    def _iterate_components(self, recurse=True, reverse=False):
        from abjad.tools import iterationtools
        if recurse:
            return iterationtools.iterate_components_in_expr(self)
        else:
            return self._iterate_top_level_components(reverse=reverse)

    def _iterate_top_level_components(self, reverse=False):
        if reverse:
            for component in reversed(self):
                yield component
        else:
            for component in self:
                yield component

    def _set_parents(self, new_parent):
        '''Not composer-safe.
        '''
        for component in self.music:
            component._set_parent(new_parent)

    # TODO: eventually migrate method to SliceSelection;
    #       then remove explicit contiguity check.
    def _withdraw_from_crossing_spanners(self):
        '''Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        from abjad.tools import spannertools
        assert componenttools.all_are_thread_contiguous_components(self)
        crossing_spanners = \
            spannertools.get_spanners_that_cross_components(self)
        components_including_children = \
            list(iterationtools.iterate_components_in_expr(self))
        for crossing_spanner in list(crossing_spanners):
            spanner_components = crossing_spanner._components[:]
            for component in components_including_children:
                if component in spanner_components:
                    crossing_spanner._components.remove(component)
                    component._spanners.discard(crossing_spanner)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        '''Duration of components in selection.

        Return duration.
        '''
        return sum(component.duration for component in self)

    @property
    def duration_in_seconds(self):
        '''Duration in seconds of components in selection.

        Return duration.
        '''
        return sum(component.duration_in_seconds for component in self)

    @property
    def music(self):
        '''Tuple of components in selection.
        '''
        return self._music

    @property
    def preprolated_duration(self):
        '''Preprolated duration of components in selection.

        Return duration.
        '''
        return sum(component.preprolated_duration for component in self)

    @property
    def timespan(self):
        '''Timespan of selection.
        '''
        from abjad.tools import timespantools
        start_offset = min(x.timespan.start_offset for x in self)
        stop_offset = max(x.timespan.stop_offset for x in self)
        return timespantools.Timespan(start_offset, stop_offset)

    ### PUBLIC METHODS ###

    def attach_marks(self, marks, recurse=False):
        '''Attach copy of each mark in `marks` 
        to each component in selection.

        Return tuple of marks created.
        '''
        from abjad.tools import marktools
        if not isinstance(marks, (list, tuple)):
            marks = (marks,)
        instantiated_marks = []
        for mark in marks:
            if not isinstance(mark, marktools.Mark):
                if issubclass(mark, marktools.Mark):
                    mark = mark()
            assert isinstance(mark, marktools.Mark)
            instantiated_marks.append(mark)
        marks = instantiated_marks
        result = []
        for component in self._iterate_components(recurse=recurse):
            for mark in marks:
                copied_mark = copy.copy(mark)
                copied_mark.attach(component)
                result.append(copied_mark)
        return tuple(result)

    def attach_spanners(self, spanner, recurse=False):
        '''Attach shallow copy of `spanner` 
        to each component in selection.

        Return list of spanners created.
        '''
        from abjad.tools import spannertools
        if issubclass(spanner, spannertools.Spanner):
            spanner = spanner()
        assert isinstance(spanner, spannertools.Spanner)
        spanners = []
        for component in self._iterate_components(recurse=recurse):
            copied_spanner = copy.copy(spanner)
            copied_spanner.attach([component])
            spanners.append(copied_spanner)
        return tuple(spanners)

    def detach_marks(self, mark_classes=None, recurse=True):
        marks = []
        for component in self._iterate_components(recurse=recurse):
            marks.extend(component._detach_marks(mark_classes=mark_classes))
        return tuple(marks)

    def detach_spanners(self, spanner_classes=None, recurse=True):
        r'''Detach `spanner_classes` from components in selection.

        Example 1. Detach tie spanners from components in selection:

        ::

            >>> staff = Staff("e'4 ( ~ e'16 fs'8 ~ fs'16 )")
            >>> time_signature = contexttools.TimeSignatureMark((2, 4))
            >>> time_signature.attach(staff)
            TimeSignatureMark((2, 4))(Staff{4})

        ::

            >>> f(staff)
            \new Staff {
                \time 2/4
                e'4 ( ~
                e'16
                fs'8 ~
                fs'16 )
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> selection = staff[:]
            >>> selection.detach_spanners(
            ...     spanner_classes=(spannertools.TieSpanner,))
            (TieSpanner(), TieSpanner())

        ::

            >>> f(staff)
            \new Staff {
                \time 2/4
                e'4 (
                e'16
                fs'8
                fs'16 )
            }

        ::

            >>> show(staff) # doctest: +SKIP

        Detach spanners from components at all levels
        of selection when `recurse` is true.

        Detach spanners at only top level of selection
        when `recurse` is false.

        Detach all spanners when `spanner_classes` is none.

        Detach spanners of only `spanner_classes` when
        `spanners_classes` is not none.

        Return none.
        '''
        spanners = []
        for component in self._iterate_components(recurse=recurse):
            spanners.extend(
                component._detach_spanners(spanner_classes=spanner_classes))
        return tuple(spanners)

    def get(self, component_classes=None, n=0, recurse=True):
        '''Get instance `n` of `component_classes` in selection.
        '''
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        component_classes = component_classes or (componenttools.Component,)
        if not isinstance(component_classes, tuple):
            component_classes = (component_classes,)
        if 0 <= n:
            if recurse:
                components = iterationtools.iterate_components_in_expr(
                    self, component_classes)
            else:
                components = self.music
            for i, x in enumerate(components):
                if i == n:
                    return x
        else:
            if recurse:
                components = iterationtools.iterate_components_in_expr(
                    self, component_classes, reverse=True)
            else:
                components = reversed(self.music)
            for i, x in enumerate(components):
                if i == abs(n) - 1:
                    return x

    def get_badly_formed_components(self):
        r'''Get badly formed components in selection:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> staff[1].written_duration = Duration(1, 4)
            >>> spannertools.BeamSpanner(staff[:])
            BeamSpanner(c'8, d'4, e'8, f'8)

        ::

            >>> f(staff)
            \new Staff {
                c'8 [
                d'4
                e'8
                f'8 ]
            }

        ::
            >>> staff[:].get_badly_formed_components()
            [Note("d'4")]

        (Beamed quarter notes are not well formed.)

        Return list.
        '''
        from abjad.tools import wellformednesstools
        badly_formed_components = []
        for checker in wellformednesstools.Check.list_checks():
            badly_formed_components.extend(checker.violators(self))
        return badly_formed_components

    def get_offset_lists(self):
        '''Get offset lists of components in selection:

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> selection = staff[:2]
            >>> selection
            Selection(Note("c'4"), Note("d'4"))

        ::

            >>> start_offsets, stop_offsets = selection.get_offset_lists()
            >>> start_offsets
            [Offset(0, 1), Offset(1, 4)]

        ::

            >>> stop_offsets
            [Offset(1, 4), Offset(1, 2)]

        Return list of start offsets together with list of stop offsets.
        '''
        start_offsets, stop_offsets = [], []
        for component in self:
            start_offsets.append(component.timespan.start_offset)
            stop_offsets.append(component.timespan.stop_offset)
        return start_offsets, stop_offsets

    def get_marks(self, mark_classes=None, recurse=True):
        '''Get `mark_classes` attached to components in selection.

        Return tuple.
        '''
        result = []
        for component in self._iterate_components(recurse=recurse):
            marks = component.get_marks(mark_classes=mark_classes)
            result.extend(marks)
        return tuple(result)

    def get_parent_and_start_stop_indices(self):
        if self:
            first, last = self[0], self[-1]
            parent = first.parent
            if parent is not None:
                first_index = parent.index(first)
                last_index = parent.index(last)
                return parent, first_index, last_index
        return None, None, None

    def group_by(self, predicate):
        result = []
        grouper = itertools.groupby(self, predicate)
        for label, generator in grouper:
            #selection = type(self)(generator)
            selection = tuple(generator)
            result.append(selection)
        return result

    def is_well_formed(self, allow_empty_containers=True):
        from abjad.tools import wellformednesstools
        results = []
        for component in self:
            for checker in wellformednesstools.Check.list_checks():
                if allow_empty_containers:
                    if getattr(checker, 'runtime', False) == 'composition':
                        continue
                results.append(checker.check(component))
        return all(results)

    def select_vertical_moment_at(self, offset):
        '''Select vertical moment at `offset`.
        '''
        from abjad.tools import componenttools
        return componenttools.VerticalMoment(self, offset)

    def tabulate_well_formedness_violations(self):
        r'''Tabulate well-formedness violations in selection:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> staff[1].written_duration = Duration(1, 4)
            >>> spannertools.BeamSpanner(staff[:])
            BeamSpanner(c'8, d'4, e'8, f'8)

        ::

            >>> f(staff)
            \new Staff {
                c'8 [
                d'4
                e'8
                f'8 ]
            }

        ::

            >>> result =  select(staff).tabulate_well_formedness_violations()

        ::

            >>> print result
            1 /    4 beamed quarter note
            0 /    1 discontiguous spanner
            0 /    5 duplicate id
            0 /    1 empty container
            0 /    0 intermarked hairpin
            0 /    0 misdurated measure
            0 /    0 misfilled measure
            0 /    4 mispitched tie
            0 /    4 misrepresented flag
            0 /    5 missing parent
            0 /    0 nested measure
            0 /    1 overlapping beam
            0 /    0 overlapping glissando
            0 /    0 overlapping octavation
            0 /    0 short hairpin

        Beamed quarter notes are not well formed.
        '''
        from abjad.tools import wellformednesstools
        lines = []
        for checker in wellformednesstools.Check.list_checks():
            lines.append(checker.report(self))
        result = '\n'.join(lines)
        return result
