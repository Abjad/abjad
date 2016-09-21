# -*- coding: utf-8 -*-
import collections
import copy
import itertools
import types
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import systemtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import select


class Selection(object):
    r'''A selection of components.

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> selection = selectiontools.Selection(staff[:])
        >>> selection
        Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_music',
        )

    ### INITIALIZER ###

    def __init__(self, music=None):
        music = self._coerce_music(music)
        self._music = tuple(music)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Cocatenates `expr` to selection.

        Returns new selection.
        '''
        assert isinstance(expr, (type(self), list, tuple))
        if isinstance(expr, type(self)):
            music = self._music + expr._music
            return type(self)(music)
        elif isinstance(expr, (tuple, list)):
            music = self._music + tuple(expr)
        return type(self)(music)

    def __contains__(self, expr):
        r'''Is true when `expr` is in selection. Otherwise false.

        Returns true or false.
        '''
        return expr in self._music

    def __eq__(self, expr):
        r'''Is true when selection and `expr` are of the same type
        and when music of selection equals music of `expr`.
        Otherwise false.

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            return self._music == expr._music
        elif isinstance(expr, collections.Sequence):
            return self._music == tuple(expr)
        return False

    def __format__(self, format_specification=''):
        r'''Formats duration.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __getitem__(self, expr):
        r'''Gets item `expr` from selection.

        Returns component from selection.
        '''
        result = self._music.__getitem__(expr)
        if isinstance(result, tuple):
            selection = type(self)()
            selection._music = result[:]
            result = selection
        return result

    def __getstate__(self):
        r'''Gets state of selection.

        Returns dictionary.
        '''
        if hasattr(self, '__dict__'):
            return vars(self)
        state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                state[slot] = getattr(self, slot, None)
        return state

    def __hash__(self):
        r'''Hashes selection.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        hash_values = (type(self), self._music)
        return hash(hash_values)

    def __illustrate__(self):
        r'''Attempts to illustrate selection.

        Evaluates the storage format of the selection (to sever any references
        to the source score from which the selection was taken). Then tries to
        wrap the result in a staff; in the case that notes of only C4 are found
        then sets the staff context name to ``'RhythmicStaff'``. If this works
        then the staff is wrapped in a LilyPond file and the file is returned.
        If this doesn't work then the method raises an exception.

        The idea is that the illustration should work for simple selections of
        that represent an essentially contiguous snippet of a single voice of
        music.

        Returns LilyPond file.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import mutate
        music = mutate(self).copy()
        staff = scoretools.Staff(music)
        found_different_pitch = False
        for pitch in pitchtools.list_named_pitches_in_expr(staff):
            if pitch != pitchtools.NamedPitch("c'"):
                found_different_pitch = True
                break
        if not found_different_pitch:
            staff.context_name = 'RhythmicStaff'
        score = scoretools.Score([staff])
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    def __len__(self):
        r'''Number of components in selection.

        Returns nonnegative integer.
        '''
        return len(self._music)

    def __ne__(self, expr):
        r'''Is true when selection does not equal `expr`. Otherwise false.

        Returns true or false.
        '''
        return not self == expr

    def __radd__(self, expr):
        r'''Concatenates selection to `expr`.

        Returns newly created selection.
        '''
        assert isinstance(expr, (type(self), list, tuple))
        if isinstance(expr, type(self)):
            music = expr._music + self._music
            return type(self)(music)
        elif isinstance(expr, (tuple, list)):
            music = tuple(expr) + self._music
        return type(self)(music)

    def __repr__(self):
        r'''Gets interpreter representation of selection.

        Returns string.
        '''
        return systemtools.StorageFormatAgent(self).get_repr_format()

    def __setstate__(self, state):
        r'''Sets state of selection.

        Returns none.
        '''
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE METHODS ###

    @staticmethod
    def _all_are_components_in_same_logical_voice(
        expr, prototype=None, allow_orphans=True):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        allowable_types = (
            list,
            tuple,
            types.GeneratorType,
            selectiontools.Selection,
            )
        if not isinstance(expr, allowable_types):
            return False
        prototype = prototype or (scoretools.Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        if len(expr) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in expr:
                if not isinstance(component, prototype):
                    all_are_orphans_of_correct_type = False
                    break
                if not component._get_parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        first = expr[0]
        if not isinstance(first, prototype):
            return False
        orphan_components = True
        if not first._get_parentage().is_orphan:
            orphan_components = False
        same_logical_voice = True
        first_signature = first._get_parentage().logical_voice
        for component in expr[1:]:
            parentage = component._get_parentage()
            if not parentage.is_orphan:
                orphan_components = False
            if not allow_orphans and orphan_components:
                return False
            if parentage.logical_voice != first_signature:
                same_logical_voice = False
            if not allow_orphans and not same_logical_voice:
                return False
            if allow_orphans and not orphan_components and \
                not same_logical_voice:
                return False
        return True

    @staticmethod
    def _all_are_contiguous_components_in_same_logical_voice(
        expr, prototype=None, allow_orphans=True):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        allowable_types = (
            list,
            tuple,
            types.GeneratorType,
            selectiontools.Selection,
            )
        if not isinstance(expr, allowable_types):
            return False
        prototype = prototype or (scoretools.Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        if len(expr) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in expr:
                if not isinstance(component, prototype):
                    all_are_orphans_of_correct_type = False
                    break
                if not component._get_parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        if not allow_orphans:
            if any(x._get_parentage().is_orphan for x in expr):
                return False
        first = expr[0]
        if not isinstance(first, prototype):
            return False
        first_parentage = first._get_parentage()
        first_logical_voice = first_parentage.logical_voice
        first_root = first_parentage.root
        previous = first
        for current in expr[1:]:
            current_parentage = current._get_parentage()
            current_logical_voice = \
                current_parentage.logical_voice
            # false if wrong type of component found
            if not isinstance(current, prototype):
                return False
            # false if in different logical voices
            if current_logical_voice != first_logical_voice:
                return False
            # false if components are in same score and are discontiguous
            if current_parentage.root == first_root:
                if not previous._is_immediate_temporal_successor_of(current):
                    return False
            previous = current
        return True

    @staticmethod
    def _all_are_contiguous_components_in_same_parent(
        expr, prototype=None, allow_orphans=True):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        allowable_types = (
            list,
            tuple,
            types.GeneratorType,
            selectiontools.Selection,
            )
        if not isinstance(expr, allowable_types):
            return False
        prototype = prototype or (scoretools.Component, )
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        if len(expr) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in expr:
                if not isinstance(component, prototype):
                    all_are_orphans_of_correct_type = False
                    break
                if not component._get_parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        first = expr[0]
        if not isinstance(first, prototype):
            return False
        first_parent = first._parent
        if first_parent is None:
            if allow_orphans:
                orphan_components = True
            else:
                return False
        same_parent = True
        strictly_contiguous = True
        previous = first
        for current in expr[1:]:
            if not isinstance(current, prototype):
                return False
            if not current._get_parentage().is_orphan:
                orphan_components = False
            if current._parent is not first_parent:
                same_parent = False
            if not previous._is_immediate_temporal_successor_of(current):
                strictly_contiguous = False
            if (not allow_orphans or
                (allow_orphans and not orphan_components)) and \
                (not same_parent or not strictly_contiguous):
                return False
            previous = current
        return True

    def _attach_tie_spanner_to_leaf_pair(self, use_messiaen_style_ties=False):
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        assert len(self) == 2
        left_leaf, right_leaf = self
        assert isinstance(left_leaf, scoretools.Leaf), left_leaf
        assert isinstance(right_leaf, scoretools.Leaf), right_leaf
        left_logical_tie = left_leaf._get_logical_tie()
        right_logical_tie = right_leaf._get_logical_tie()
        prototype = (spannertools.Tie,)
        if left_logical_tie == right_logical_tie:
            return
        try:
            left_tie_spanner = left_leaf._get_spanner(prototype)
        except MissingSpannerError:
            left_tie_spanner = None
        try:
            right_tie_spanner = right_leaf._get_spanner(prototype)
        except MissingSpannerError:
            right_tie_spanner = None
        if left_tie_spanner is not None and right_tie_spanner is not None:
            left_tie_spanner._fuse_by_reference(right_tie_spanner)
        elif left_tie_spanner is not None and right_tie_spanner is None:
            left_tie_spanner._append(right_leaf)
        elif left_tie_spanner is None and right_tie_spanner is not None:
            right_tie_spanner._append_left(left_leaf)
        elif left_tie_spanner is None and right_tie_spanner is None:
            tie = spannertools.Tie(
                use_messiaen_style_ties=use_messiaen_style_ties,
                )
            attach(tie, [left_leaf, right_leaf])

    @staticmethod
    def _coerce_music(music):
        if music is None:
            music = ()
        elif isinstance(music, Selection):
            music = tuple(music)
        elif isinstance(music, collections.Sequence):
            music = tuple(music)
        elif isinstance(music, types.GeneratorType):
            music = tuple(music)
        else:
            music = (music,)
        return music

    def _copy(self, n=1, include_enclosing_containers=False):
        r'''Copies components in selection and fractures crossing spanners.

        Components in selection must be logical-voice-contiguous.

        The steps this function takes are as follows:

            * Deep copy `components`.

            * Deep copy spanners that attach to any component in `components`.

            * Fracture spanners that attach to components not in `components`.

            * Returns Python list of copied components.

        ..  container:: example

            **Example 1.** Copy components one time:

            ::

                >>> staff = Staff(r"c'8 ( d'8 e'8 f'8 )")
                >>> staff.append(r"g'8 a'8 b'8 c''8")
                >>> time_signature = TimeSignature((2, 4))
                >>> attach(time_signature, staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 2/4
                    c'8 (
                    d'8
                    e'8
                    f'8 )
                    g'8
                    a'8
                    b'8
                    c''8
                }

            ::

                >>> selection = staff[2:4]
                >>> result = selection._copy()
                >>> new_staff = Staff(result)
                >>> show(new_staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(new_staff))
                \new Staff {
                    e'8 (
                    f'8 )
                }

            ::

                >>> staff[2] is new_staff[0]
                False

        ..  container:: example

            **Example 2.** Copy components multiple times:

            Copy `components` a total of `n` times:

            ::

                >>> selection = staff[2:4]
                >>> result = selection._copy(n=4)
                >>> new_staff = Staff(result)
                >>> show(new_staff) # doctest: +SKIP

            ::

                >>> print(format(new_staff))
                \new Staff {
                    e'8 (
                    f'8 )
                    e'8 (
                    f'8 )
                    e'8 (
                    f'8 )
                    e'8 (
                    f'8 )
                }

        ..  container:: example

            **Example 3.** Copy leaves and include enclosing conatiners:

                >>> voice = Voice(r"\times 2/3 { c'4 d'4 e'4 }")
                >>> voice.append(r"\times 2/3 { f'4 e'4 d'4 }")
                >>> staff = Staff([voice])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \new Voice {
                        \times 2/3 {
                            c'4
                            d'4
                            e'4
                        }
                        \times 2/3 {
                            f'4
                            e'4
                            d'4
                        }
                    }
                }

            ::

                >>> selector = select().by_leaf(flatten=True)
                >>> leaves = selector(staff)
                >>> leaves = leaves[1:5]
                >>> new_staff = leaves._copy(include_enclosing_containers=True)
                >>> show(new_staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(new_staff))
                \new Staff {
                    \new Voice {
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            d'4
                            e'4
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            f'4
                            e'4
                        }
                    }
                }

        Returns contiguous selection.
        '''
        # check input
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        # return empty list when nothing to copy
        if n < 1:
            return []
        new_components = [
            component._copy_with_children_and_indicators_but_without_spanners()
            for component in self
            ]
        if include_enclosing_containers:
            return self._copy_and_include_enclosing_containers()
        new_components = type(self)(new_components)
        # make schema of spanners contained by components
        schema = self._make_spanner_schema()
        # copy spanners covered by components
        for covered_spanner, component_indices in list(schema.items()):
            new_covered_spanner = copy.copy(covered_spanner)
            del(schema[covered_spanner])
            schema[new_covered_spanner] = component_indices
        # reverse schema
        reversed_schema = {}
        for new_covered_spanner, component_indices in list(schema.items()):
            for component_index in component_indices:
                try:
                    reversed_schema[component_index].append(
                        new_covered_spanner)
                except KeyError:
                    reversed_schema[component_index] = [new_covered_spanner]
        # iterate components and add new components to new spanners
        for component_index, new_component in enumerate(
            iterate(new_components).by_class()):
            try:
                new_covered_spanners = reversed_schema[component_index]
                for new_covered_spanner in new_covered_spanners:
                    new_covered_spanner._append(new_component)
            except KeyError:
                pass
        # repeat as specified by input
        for i in range(n - 1):
            new_components += self._copy()
        # return new components
        return new_components

    def _copy_and_include_enclosing_containers(self):
        from abjad.tools import scoretools
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        # get governor
        parentage = self[0]._get_parentage(include_self=True)
        governor = parentage._get_governor()
        # find start and stop indices in governor
        governor_leaves = select(governor).by_leaf()
        for i, x in enumerate(governor_leaves):
            if x is self[0]:
                start_index_in_governor = i
        for i, x in enumerate(governor_leaves):
            if x is self[-1]:
                stop_index_in_governor = i
        # copy governor
        governor_copy = mutate(governor).copy()
        copied_leaves = select(governor_copy).by_leaf()
        # find start and stop leaves in copy of governor
        start_leaf = copied_leaves[start_index_in_governor]
        stop_leaf = copied_leaves[stop_index_in_governor]
        # trim governor copy forwards from first leaf
        found_start_leaf = False
        while not found_start_leaf:
            leaf = next(iterate(governor_copy).by_class(scoretools.Leaf))
            if leaf is start_leaf:
                found_start_leaf = True
            else:
                leaf._remove_and_shrink_durated_parent_containers()
        # trim governor copy backwards from last leaf
        found_stop_leaf = False
        while not found_stop_leaf:
            reverse_iterator = iterate(governor_copy).by_class(
                scoretools.Leaf, reverse=True)
            leaf = next(reverse_iterator)
            if leaf is stop_leaf:
                found_stop_leaf = True
            else:
                leaf._remove_and_shrink_durated_parent_containers()
        # return trimmed governor copy
        return governor_copy

    def _fuse(self):
        from abjad.tools import scoretools
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        if all(isinstance(x, scoretools.Leaf) for x in self):
            return self._fuse_leaves()
        elif all(isinstance(x, scoretools.Tuplet) for x in self):
            return self._fuse_tuplets()
        elif all(isinstance(x, scoretools.Measure) for x in self):
            return self._fuse_measures()
        else:
            message = 'can not fuse.'
            raise Exception(message)

    def _fuse_leaves(self):
        from abjad.tools import scoretools
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        assert all(isinstance(x, scoretools.Leaf) for x in self)
        leaves = self
        if len(leaves) <= 1:
            return leaves
        total_preprolated = leaves._preprolated_duration
        for leaf in leaves[1:]:
            parent = leaf._parent
            if parent:
                index = parent.index(leaf)
                del(parent[index])
        return leaves[0]._set_duration(total_preprolated)

    def _fuse_measures(self):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        # check input
        prototype = (scoretools.Measure,)
        assert self._all_are_contiguous_components_in_same_parent(
            self, prototype)
        # return none on empty measures
        if len(self) == 0:
            return None
        # TODO: instantiate a new measure
        #       instead of returning a reference to existing measure
        if len(self) == 1:
            return self[0]
        implicit_scaling = self[0].implicit_scaling
        assert all(
            x.implicit_scaling == implicit_scaling for x in self)
        selection = selectiontools.Selection(self)
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        old_denominators = []
        new_duration = durationtools.Duration(0)
        for measure in self:
            effective_time_signature = measure.time_signature
            old_denominators.append(effective_time_signature.denominator)
            new_duration += effective_time_signature.duration
        new_time_signature = \
            measure._duration_and_possible_denominators_to_time_signature(
                new_duration,
                old_denominators,
                )
        music = []
        for measure in self:
            # scale before reassignment to prevent logical tie scale drama
            signature = measure.time_signature
            prolation = signature.implied_prolation
            multiplier = prolation / new_time_signature.implied_prolation
            measure._scale_contents(multiplier)
            measure_music = measure[:]
            measure_music._set_parents(None)
            music += measure_music
        new_measure = scoretools.Measure(new_time_signature, music)
        new_measure.implicit_scaling = self[0].implicit_scaling
        if parent is not None:
            self._give_dominant_spanners([new_measure])
        self._set_parents(None)
        if parent is not None:
            parent.insert(start, new_measure)
        return new_measure

    def _fuse_tuplets(self):
        from abjad.tools import scoretools
        assert self._all_are_contiguous_components_in_same_parent(
            self, prototype=(scoretools.Tuplet,))
        if len(self) == 0:
            return None
        first = self[0]
        first_multiplier = first.multiplier
        first_type = type(first)
        for tuplet in self[1:]:
            if tuplet.multiplier != first_multiplier:
                message = 'tuplets must carry same multiplier.'
                raise ValueError(message)
            if type(tuplet) != first_type:
                message = 'tuplets must be same type.'
                raise TypeError(message)
        if isinstance(first, scoretools.FixedDurationTuplet):
            total_contents_duration = sum(
                [x._contents_duration for x in self])
            new_target_duration = first_multiplier * total_contents_duration
            new_tuplet = scoretools.FixedDurationTuplet(
                new_target_duration, [])
        elif isinstance(first, scoretools.Tuplet):
            new_tuplet = scoretools.Tuplet(first_multiplier, [])
        else:
            message = 'unknown tuplet type.'
            raise TypeError(message)
        wrapped = False
        if self[0]._get_parentage().root is not \
            self[-1]._get_parentage().root:
            dummy_container = scoretools.Container(self)
            wrapped = True
        mutate(self).swap(new_tuplet)
        if wrapped:
            del(dummy_container[:])
        return new_tuplet

    def _get_component(self, prototype=None, n=0, recurse=True):
        from abjad.tools import scoretools
        prototype = prototype or (scoretools.Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        if 0 <= n:
            if recurse:
                components = iterate(self).by_class(prototype)
            else:
                components = self._music
            for i, x in enumerate(components):
                if i == n:
                    return x
        else:
            if recurse:
                components = iterate(self).by_class(
                    prototype, reverse=True)
            else:
                components = reversed(self._music)
            for i, x in enumerate(components):
                if i == abs(n) - 1:
                    return x

    def _get_crossing_spanners(self):
        r'''Assert logical-voice-contiguous components.
        Collect spanners that attach to any component in selection.
        Returns unordered set of crossing spanners.
        A spanner P crosses a list of logical-voice-contiguous components C
        when P and C share at least one component and when it is the
        case that NOT ALL of the components in P are also in C.
        In other words, there is some intersection -- but not total
        intersection -- between the components of P and C.
        '''
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        all_components = set(iterate(self).by_class())
        contained_spanners = set()
        for component in iterate(self).by_class():
            contained_spanners.update(component._get_spanners())
        crossing_spanners = set([])
        for spanner in contained_spanners:
            spanner_components = set(spanner[:])
            if not spanner_components.issubset(all_components):
                crossing_spanners.add(spanner)
        return crossing_spanners

    def _get_dominant_spanners(self):
        r'''Returns spanners that dominate components in selection.
        Returns set of (spanner, index) pairs.
        Each (spanner, index) pair gives a spanner which dominates
        all components in selection together with the start index
        at which spanner first encounters selection.
        Use this helper to lift spanners temporarily from components
        in selection and perform some action to the underlying
        score tree before reattaching spanners.
        score components.
        '''
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        receipt = set([])
        if len(self) == 0:
            return receipt
        first, last = self[0], self[-1]
        start_components = first._get_descendants_starting_with()
        stop_components = last._get_descendants_stopping_with()
        stop_components = set(stop_components)
        for component in start_components:
            for spanner in component._get_spanners():
                if set(spanner[:]) & stop_components != set([]):
                    index = spanner._index(component)
                    receipt.add((spanner, index))
        return receipt

    def _get_format_specification(self):
        values = []
        if self._music:
            values = [list(self._music)]
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            )

    def _get_offset_lists(self):
        start_offsets, stop_offsets = [], []
        for component in self:
            start_offsets.append(component._get_timespan().start_offset)
            stop_offsets.append(component._get_timespan().stop_offset)
        return start_offsets, stop_offsets

    def _get_parent_and_start_stop_indices(self):
        assert self._all_are_contiguous_components_in_same_parent(self)
        if self:
            first, last = self[0], self[-1]
            parent = first._parent
            if parent is not None:
                first_index = parent.index(first)
                last_index = parent.index(last)
                return parent, first_index, last_index
        return None, None, None

    def _get_spanner(self, prototype=None):
        spanners = self._get_spanners(prototype=prototype)
        if not spanners:
            message = 'no spanners found.'
            raise MissingSpannerError(message)
        elif len(spanners) == 1:
            return spanners.pop()
        else:
            message = 'multiple spanners found.'
            raise ExtraSpannerError(message)

    def _get_spanners(self, prototype=None):
        from abjad.tools import spannertools
        prototype = prototype or (spannertools.Spanner,)
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        result = set()
        for component in self:
            spanners = component._get_spanners(prototype)
            result.update(spanners)
        return result

    def _give_dominant_spanners(self, recipients):
        r'''Find all spanners dominating music.
        Insert each component in recipients into each dominant spanner.
        Remove music from each dominating spanner.
        Returns none.
        Not composer-safe.
        '''
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        assert self._all_are_contiguous_components_in_same_logical_voice(
            recipients)
        receipt = self._get_dominant_spanners()
        for spanner, index in receipt:
            for recipient in reversed(recipients):
                spanner._insert(index, recipient)
            for component in self:
                spanner._remove(component)

    def _give_music_to_empty_container(self, container):
        r'''Not composer-safe.
        '''
        from abjad.tools import scoretools
        assert self._all_are_contiguous_components_in_same_parent(self)
        assert isinstance(container, scoretools.Container)
        assert not container
        music = []
        for component in self:
            music.extend(getattr(component, '_music', ()))
        container._music.extend(music)
        container[:]._set_parents(container)

    def _give_position_in_parent_to_container(self, container):
        r'''Not composer-safe.
        '''
        from abjad.tools import scoretools
        assert self._all_are_contiguous_components_in_same_parent(self)
        assert isinstance(container, scoretools.Container)
        parent, start, stop = self._get_parent_and_start_stop_indices()
        if parent is not None:
            parent._music.__setitem__(slice(start, start), [container])
            container._set_parent(parent)
            self._set_parents(None)

    def _iterate_components(self, recurse=True, reverse=False):
        if recurse:
            return iterate(self).by_class()
        else:
            return self._iterate_top_level_components(reverse=reverse)

    def _iterate_top_level_components(self, reverse=False):
        if reverse:
            for component in reversed(self):
                yield component
        else:
            for component in self:
                yield component

    def _make_spanner_schema(self):
        schema = {}
        spanners = set()
        for component in iterate(self).by_class():
            spanners.update(component._get_spanners())
        for spanner in spanners:
            schema[spanner] = []
        for i, component in \
            enumerate(iterate(self).by_class()):
            attached_spanners = component._get_spanners()
            for attached_spanner in attached_spanners:
                try:
                    schema[attached_spanner].append(i)
                except KeyError:
                    pass
        return schema

    def _set_parents(self, new_parent):
        r'''Not composer-safe.
        '''
        for component in self._music:
            component._set_parent(new_parent)

    def _withdraw_from_crossing_spanners(self):
        r'''Not composer-safe.
        '''
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        crossing_spanners = self._get_crossing_spanners()
        components_including_children = select(self).by_class()
        for crossing_spanner in list(crossing_spanners):
            spanner_components = crossing_spanner._components[:]
            for component in components_including_children:
                if component in spanner_components:
                    crossing_spanner._components.remove(component)
                    component._spanners.discard(crossing_spanner)

    ### PUBLIC METHODS ###

    def by_class(
        self,
        prototype=None,
        reverse=False,
        start=0,
        stop=None,
        with_grace_notes=False,
        ):
        r'''Select components by class.

        ..  container:: example

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "c'8 d'8"))
                >>> staff.append(Measure((2, 8), "e'8 f'8"))
                >>> staff.append(Measure((2, 8), "g'8 a'8"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                }

            ::

                >>> for note in select(staff).by_class(prototype=Note):
                ...     note
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Note("g'8")
                Note("a'8")

        Returns new selection.
        '''
        iterator = iterate(self).by_class(
            prototype=prototype,
            reverse=reverse,
            start=start,
            stop=stop,
            with_grace_notes=with_grace_notes,
            )
        return Selection(iterator)

    def by_leaf(
        self,
        prototype=None,
        reverse=False,
        start=0,
        stop=None,
        with_grace_notes=False,
        ):
        r'''Select components by leaf.

        ..  container:: example

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(Measure((2, 8), "af'8 r8"))
                >>> staff.append(Measure((2, 8), "r8 gf'8"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                    }
                    {
                        af'8
                        r8
                    }
                    {
                        r8
                        gf'8
                    }
                }

            ::

                >>> for leaf in select(staff).by_leaf():
                ...     leaf
                ...
                Chord("<c' bf'>8")
                Chord("<g' a'>8")
                Note("af'8")
                Rest('r8')
                Rest('r8')
                Note("gf'8")

        Returns new selection.
        '''
        iterator = iterate(self).by_leaf(
            prototype=prototype,
            reverse=reverse,
            start=start,
            stop=stop,
            with_grace_notes=with_grace_notes,
            )
        return Selection(iterator)

    def by_logical_tie(
        self,
        nontrivial=False,
        pitched=False,
        reverse=False,
        parentage_mask=None,
        with_grace_notes=False,
        ):
        r'''Select components by logical tie.

        ..  container:: example

            ::

                >>> staff = Staff(r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4 ~
                    \times 2/3 {
                        c'16
                        d'8
                    }
                    e'8
                    f'4 ~
                    f'16
                }

            ::

                >>> for logical_tie in select(staff).by_logical_tie():
                ...     logical_tie
                ...
                LogicalTie([Note("c'4"), Note("c'16")])
                LogicalTie([Note("d'8")])
                LogicalTie([Note("e'8")])
                LogicalTie([Note("f'4"), Note("f'16")])

        Returns new selection.
        '''
        iterator = iterate(self).by_logical_tie(
            nontrivial=nontrivial,
            pitched=pitched,
            reverse=reverse,
            parentage_mask=parentage_mask,
            with_grace_notes=with_grace_notes,
            )
        return Selection(iterator)

    def by_run(self, prototype=None):
        r'''Select components by run.

        ..  container:: example

            ::

                >>> staff = Staff(r"\times 2/3 { c'8 d'8 r8 }")
                >>> staff.append(r"\times 2/3 { r8 <e' g'>8 <f' a'>8 }")
                >>> staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8
                        d'8
                        r8
                    }
                    \times 2/3 {
                        r8
                        <e' g'>8
                        <f' a'>8
                    }
                    g'8
                    a'8
                    r8
                    r8
                    <b' d''>8
                    <c'' e''>8
                }

            ::

                >>> for group in select(staff[:]).by_run((Note, Chord)):
                ...     group
                ...
                Selection([Note("g'8"), Note("a'8")])
                Selection([Chord("<b' d''>8"), Chord("<c'' e''>8")])

        Returns new selection.
        '''
        iterator = iterate(self).by_run(prototype=prototype)
        return Selection(iterator)

    def by_timeline(self, prototype=None, reverse=False):
        r'''Select components by timeline.

        ..  container:: example

            ::

                >>> score = Score([])
                >>> score.append(Staff("c'4 d'4 e'4 f'4"))
                >>> score.append(Staff("g'8 a'8 b'8 c''8"))
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                    \new Staff {
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                >>

            ::

                >>> for leaf in select(score).by_timeline():
                ...     leaf
                ...
                Note("c'4")
                Note("g'8")
                Note("a'8")
                Note("d'4")
                Note("b'8")
                Note("c''8")
                Note("e'4")
                Note("f'4")


        Returns new selection.
        '''
        iterator = iterate(self).by_timeline(
            prototype=prototype,
            reverse=reverse,
            )
        return Selection(iterator)

    def by_timeline_and_logical_tie(
        self,
        nontrivial=False,
        pitched=False,
        reverse=False,
        ):
        r'''Select components by timeline and logical tie.

        ..  container:: example

            ::

                >>> score = Score([])
                >>> score.append(Staff("c''4 ~ c''8 d''8 r4 ef''4"))
                >>> score.append(Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c''4 ~
                        c''8
                        d''8
                        r4
                        ef''4
                    }
                    \new Staff {
                        r8
                        g'4. ~
                        g'8
                        r16
                        f'8. ~
                        f'8
                    }
                >>

            ::

                >>> for logical_tie in select(score).by_timeline_and_logical_tie():
                ...     logical_tie
                ...
                LogicalTie([Note("c''4"), Note("c''8")])
                LogicalTie([Rest('r8')])
                LogicalTie([Note("g'4."), Note("g'8")])
                LogicalTie([Note("d''8")])
                LogicalTie([Rest('r4')])
                LogicalTie([Rest('r16')])
                LogicalTie([Note("f'8."), Note("f'8")])
                LogicalTie([Note("ef''4")])

        Returns new selection.
        '''
        iterator = iterate(self).by_timeline_and_logical_tie(
            nontrivial=nontrivial,
            pitched=pitched,
            reverse=reverse,
            )
        return Selection(iterator)

    def get_duration(self, in_seconds=False):
        r'''Gets duration of contiguous selection.

        Returns duration.
        '''
        durations = []
        for element in self:
            if hasattr(element, '_get_duration'):
                duration = element._get_duration(in_seconds=in_seconds)
            else:
                duration = durationtools.Duration(element)
            durations.append(duration)
        return sum(durations)

    def get_spanners(self, prototype=None, in_parentage=False):
        r'''Gets spanners attached to any component in selection.

        Returns set.
        '''
        result = set()
        for component in self:
            spanners = component._get_spanners(
                prototype=prototype,
                in_parentage=in_parentage,
                )
            result.update(spanners)
        return result

    def get_timespan(self, in_seconds=False):
        r'''Gets timespan of contiguous selection.

        Returns timespan.
        '''
        from abjad.tools import timespantools
        if in_seconds:
            raise NotImplementedError
        timespan = self[0]._get_timespan()
        start_offset = timespan.start_offset
        stop_offset = timespan.stop_offset
        for x in self[1:]:
            timespan = x._get_timespan()
            if timespan.start_offset < start_offset:
                start_offset = timespan.start_offset
            if stop_offset < timespan.stop_offset:
                stop_offset = timespan.stop_offset
        return timespantools.Timespan(start_offset, stop_offset)

    def get_vertical_moment_at(self, offset):
        r'''Select vertical moment at `offset`.
        '''
        from abjad.tools import selectiontools
        return selectiontools.VerticalMoment(self, offset)

    def group_by(self, predicate):
        '''Groups components in contiguous selection by `predicate`.

        Returns list of tuples.
        '''
        result = []
        grouper = itertools.groupby(self, predicate)
        for label, generator in grouper:
            selection = tuple(generator)
            result.append(selection)
        return result

    def partition_by_durations(
        self,
        durations,
        cyclic=False,
        fill=Exact,
        in_seconds=False,
        overhang=False,
        ):
        r'''Partitions `components` according to `durations`.

        When `fill` is `Exact` then parts must equal `durations` exactly.

        When `fill` is `Less` then parts must be
        less than or equal to `durations`.

        When `fill` is `More` then parts must be
        greater or equal to `durations`.

        Reads `durations` cyclically when `cyclic` is true.

        Reads component durations in seconds when `in_seconds` is true.

        Returns remaining components at end in final part when `overhang`
        is true.
        '''
        durations = [durationtools.Duration(x) for x in durations]
        if cyclic:
            durations = datastructuretools.CyclicTuple(durations)
        result = []
        part = []
        current_duration_index = 0
        target_duration = durations[current_duration_index]
        cumulative_duration = durationtools.Duration(0)
        components_copy = list(self)
        while True:
            try:
                component = components_copy.pop(0)
            except IndexError:
                break
            component_duration = component._get_duration()
            if in_seconds:
                component_duration = component._get_duration(in_seconds=True)
            candidate_duration = cumulative_duration + component_duration
            if candidate_duration < target_duration:
                part.append(component)
                cumulative_duration = candidate_duration
            elif candidate_duration == target_duration:
                part.append(component)
                result.append(part)
                part = []
                cumulative_duration = durationtools.Duration(0)
                current_duration_index += 1
                try:
                    target_duration = durations[current_duration_index]
                except IndexError:
                    break
            elif target_duration < candidate_duration:
                if fill == Exact:
                    message = 'must partition exactly.'
                    raise Exception(message)
                elif fill == Less:
                    result.append(part)
                    part = [component]
                    if in_seconds:
                        cumulative_duration = \
                            sum([x._get_duration(in_seconds=True)
                            for x in part])
                    else:
                        cumulative_duration = \
                            sum([x._get_duration() for x in part])
                    current_duration_index += 1
                    try:
                        target_duration = durations[current_duration_index]
                    except IndexError:
                        break
                    if target_duration < cumulative_duration:
                        message = 'target duration {}'
                        message += ' is less than cumulative duration {}.'
                        message = message.format(
                            target_duration,
                            cumulative_duration,
                            )
                        raise Exception(message)
                elif fill == More:
                    part.append(component)
                    result.append(part)
                    part = []
                    cumulative_duration = durationtools.Duration(0)
                    current_duration_index += 1
                    try:
                        target_duration = durations[current_duration_index]
                    except IndexError:
                        break
        if len(part):
            if overhang:
                result.append(part)
        if len(components_copy):
            if overhang:
                result.append(components_copy)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _preprolated_duration(self):
        return sum(component._preprolated_duration for component in self)

collections.Sequence.register(Selection)
