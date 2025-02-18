import collections
import copy as python_copy
import itertools

from . import _iterlib
from . import bind as _bind
from . import duration as _duration
from . import enums as _enums
from . import exceptions as _exceptions
from . import get as _get
from . import indicators as _indicators
from . import iterate as _iterate
from . import makers as _makers
from . import parentage as _parentage
from . import pitch as _pitch
from . import score as _score
from . import select as _select
from . import sequence as _sequence
from . import spanners as _spanners
from . import tag as _tag


def _are_contiguous_logical_voice(
    selection, prototype=None, *, ignore_before_after_grace=None
) -> bool:
    r"""
    Is true when items in selection are contiguous components in the same logical voice.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> abjad.mutate._are_contiguous_logical_voice(staff[:])
        True

        >>> staves = [staff[0], staff[-1]]
        >>> abjad.mutate._are_contiguous_logical_voice(staves)
        False

    ..  container:: example

        REGRESSION. Before-grace music may be ignored:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \grace {
                    cs'16
                }
                d'4
                e'4
                f'4
            }

        >>> voice[:]
        [Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")]

        >>> abjad.mutate._are_contiguous_logical_voice(voice[:])
        False

        >>> abjad.mutate._are_contiguous_logical_voice(
        ...     voice[:],
        ...     ignore_before_after_grace=True
        ... )
        True

        After-grace music may be ignored, too:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> container = abjad.AfterGraceContainer("cs'16")
        >>> abjad.attach(container, voice[0])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \afterGrace
                c'4
                {
                    cs'16
                }
                d'4
                e'4
                f'4
            }

        >>> voice[:]
        [Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")]

        >>> abjad.mutate._are_contiguous_logical_voice(voice[:])
        False

        >>> abjad.mutate._are_contiguous_logical_voice(
        ...     voice[:],
        ...     ignore_before_after_grace=True
        ... )
        True

    """
    if not isinstance(selection, collections.abc.Sequence):
        return False
    prototype = prototype or (_score.Component,)
    if not isinstance(prototype, tuple):
        prototype = (prototype,)
    assert isinstance(prototype, tuple)
    if len(selection) == 0:
        return True
    if all(isinstance(_, prototype) and _._parent is None for _ in selection):
        return True
    first = selection[0]
    if not isinstance(first, prototype):
        return False
    first_parentage = _parentage.Parentage(first)
    first_logical_voice = first_parentage.logical_voice()
    first_root = first_parentage.root
    previous = first
    for current in selection[1:]:
        current_parentage = _parentage.Parentage(current)
        current_logical_voice = current_parentage.logical_voice()
        # false if wrong type of component found
        if not isinstance(current, prototype):
            return False
        # false if in different logical voices
        if current_logical_voice != first_logical_voice:
            return False
        # false if components are in same score and are discontiguous
        if current_parentage.root == first_root:
            if not _immediately_precedes(
                previous,
                current,
                ignore_before_after_grace=ignore_before_after_grace,
            ):
                return False
        previous = current
    return True


def _are_contiguous_same_parent(
    self, prototype=None, *, ignore_before_after_grace=None
) -> bool:
    r"""
    Is true when items in selection are all contiguous components in the same parent.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> abjad.mutate._are_contiguous_same_parent(staff[:])
        True

        >>> staves = [staff[0], staff[-1]]
        >>> abjad.mutate._are_contiguous_same_parent(staves)
        False

    ..  container:: example

        REGRESSION. Before-grace music music may be ignored:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> container = abjad.BeforeGraceContainer("cs'16")
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \grace {
                    cs'16
                }
                d'4
                e'4
                f'4
            }

        >>> voice[:]
        [Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")]

        >>> abjad.mutate._are_contiguous_same_parent(voice[:])
        False

        >>> abjad.mutate._are_contiguous_same_parent(
        ...     voice[:],
        ...     ignore_before_after_grace=True
        ... )
        True

        After-grace music may be ignored, too:

        >>> voice = abjad.Voice("c'4 d' e' f'")
        >>> container = abjad.AfterGraceContainer("cs'16")
        >>> abjad.attach(container, voice[0])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \afterGrace
                c'4
                {
                    cs'16
                }
                d'4
                e'4
                f'4
            }

        >>> voice[:]
        [Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")]

        >>> abjad.mutate._are_contiguous_same_parent(voice[:])
        False

        >>> abjad.mutate._are_contiguous_same_parent(
        ...     voice[:],
        ...     ignore_before_after_grace=True
        ... )
        True

    """
    prototype = prototype or (_score.Component,)
    if not isinstance(prototype, tuple):
        prototype = (prototype,)
    assert isinstance(prototype, tuple)
    if len(self) == 0:
        return True
    if all(isinstance(_, prototype) and _._parent is None for _ in self):
        return True
    first = self[0]
    if not isinstance(first, prototype):
        return False
    first_parent = first._parent
    same_parent = True
    strictly_contiguous = True
    previous = first
    for current in self[1:]:
        if not isinstance(current, prototype):
            return False
        if current._parent is not first_parent:
            same_parent = False
        if not _immediately_precedes(
            previous,
            current,
            ignore_before_after_grace=ignore_before_after_grace,
        ):
            strictly_contiguous = False
        if current._parent is not None and (not same_parent or not strictly_contiguous):
            return False
        previous = current
    return True


def _attach_tie_to_leaves(selection):
    for leaf in selection[:-1]:
        _bind.detach(_indicators.Tie, leaf)
        _bind.attach(_indicators.Tie(), leaf)


def _copy_selection(selection):
    assert _are_contiguous_logical_voice(selection)
    new_components = []
    for component in selection:
        if isinstance(component, _score.Container):
            new_component = component._copy_with_children()
        else:
            new_component = component.__copy__()
        new_components.append(new_component)
    new_components = type(selection)(new_components)
    return new_components


def _extract(component):
    selection = [component]
    parent, start, stop = _get_parent_and_start_stop_indices(selection)
    if parent is not None:
        components = list(getattr(component, "components", ()))
        parent.__setitem__(slice(start, stop + 1), components)
    return component


def _fuse(components, *, tag=None):
    assert _are_contiguous_logical_voice(components)
    if all(isinstance(_, _score.Leaf) for _ in components):
        return _fuse_leaves(components, tag=tag)
    elif all(isinstance(_, _score.Tuplet) for _ in components):
        return _fuse_tuplets(components, tag=tag)
    else:
        raise Exception(f"can only fuse leaves and tuplets (not {components}).")


def _fuse_leaves(leaves, *, tag=None):
    assert all(isinstance(_, _score.Leaf) for _ in leaves)
    assert _are_contiguous_logical_voice(leaves)
    if len(leaves) <= 1:
        return leaves
    originally_tied = leaves[-1]._has_indicator(_indicators.Tie)
    total_preprolated = sum(_._get_preprolated_duration() for _ in leaves)
    for leaf in leaves[1:]:
        parent = leaf._parent
        if parent:
            index = parent.index(leaf)
            del parent[index]
    result = _set_leaf_duration(leaves[0], total_preprolated, tag=tag)
    if not originally_tied:
        last_leaf = _select.leaf(result, -1)
        _bind.detach(_indicators.Tie, last_leaf)
    return result


# TODO: remove because unused?
def _fuse_leaves_by_immediate_parent(leaves, *, tag=None):
    result = []
    parts = _get_leaves_grouped_by_immediate_parents(leaves)
    for part in parts:
        fused = _fuse(part, tag=tag)
        result.append(fused)
    return result


def _fuse_tuplets(tuplets, *, tag=None):
    assert _are_contiguous_same_parent(tuplets, prototype=_score.Tuplet)
    if len(tuplets) == 0:
        return None
    first = tuplets[0]
    first_multiplier = first.multiplier
    for tuplet in tuplets[1:]:
        if tuplet.multiplier != first_multiplier:
            raise ValueError("tuplets must carry same multiplier.")
    assert isinstance(first, _score.Tuplet)
    new_tuplet = _score.Tuplet(first_multiplier, [], tag=tag)
    wrapped = False
    if _get.parentage(tuplets[0]).root is not _get.parentage(tuplets[-1]).root:
        dummy_container = _score.Container(tuplets)
        wrapped = True
    swap(tuplets, new_tuplet)
    if wrapped:
        del dummy_container[:]
    return new_tuplet


def _get_leaves_grouped_by_immediate_parents(leaves):
    result = []
    pairs_generator = itertools.groupby(leaves, lambda _: id(_._parent))
    for key, values_generator in pairs_generator:
        group = list(values_generator)
        result.append(group)
    return result


def _give_components_to_empty_container(selection, container):
    assert _are_contiguous_same_parent(selection)
    assert isinstance(container, _score.Container)
    assert not container
    components = []
    for component in selection:
        components.extend(getattr(component, "components", ()))
    container._components.extend(components)
    _set_parents(container)


def _get_parent_and_start_stop_indices(selection, ignore_before_after_grace=None):
    assert _are_contiguous_same_parent(
        selection, ignore_before_after_grace=ignore_before_after_grace
    )
    if selection:
        first, last = selection[0], selection[-1]
        parent = first._parent
        if parent is not None:
            first_index = parent.index(first)
            last_index = parent.index(last)
            return parent, first_index, last_index
    return None, None, None


def _give_position_in_parent_to_container(selection, container):
    assert _are_contiguous_same_parent(selection)
    assert isinstance(container, _score.Container)
    parent, start, stop = _get_parent_and_start_stop_indices(selection)
    if parent is not None:
        parent._components.__setitem__(slice(start, start), [container])
        container._set_parent(parent)
        for component in selection:
            component._set_parent(None)


def _immediately_precedes(component_1, component_2, ignore_before_after_grace=None):
    successors = []
    current = component_1
    # do not include OnBeatGraceContainer here because
    # OnBeatGraceContainer is a proper container
    grace_prototype = (_score.AfterGraceContainer, _score.BeforeGraceContainer)
    while current is not None:
        sibling = _iterlib._get_sibling_with_graces(current, 1)
        while (
            ignore_before_after_grace
            and sibling is not None
            and isinstance(sibling._parent, grace_prototype)
        ):
            sibling = _iterlib._get_sibling_with_graces(sibling, 1)
        if sibling is None:
            current = current._parent
        else:
            descendants = sibling._get_descendants_starting_with()
            successors = descendants
            break
    return component_2 in successors


def _set_leaf_duration(leaf, new_duration, *, tag=None):
    new_duration = _duration.Duration(new_duration)
    if leaf.multiplier is not None:
        multiplier = new_duration.__div__(leaf.written_duration)
        leaf.multiplier = _duration.pair(multiplier)
        return [leaf]
    try:
        leaf.written_duration = new_duration
        return [leaf]
    except _exceptions.AssignabilityError:
        pass
    components = _makers.make_notes(0, new_duration, tag=tag)
    new_leaves = _select.leaves(components)
    following_leaf_count = len(new_leaves) - 1
    following_leaves = []
    for i in range(following_leaf_count):
        following_leaf = copy(leaf)
        for indicator in _get.indicators(following_leaf):
            if i != following_leaf_count - 1:
                if getattr(indicator, "time_orientation", _enums.LEFT) != _enums.MIDDLE:
                    _bind.detach(indicator, following_leaf)
            elif (
                getattr(indicator, "time_orientation", _enums.LEFT) != _enums.RIGHT
                and getattr(indicator, "time_orientation", _enums.LEFT) != _enums.MIDDLE
            ):
                _bind.detach(indicator, following_leaf)
        _bind.detach(_score.BeforeGraceContainer, following_leaf)
        following_leaves.append(following_leaf)
    if following_leaf_count > 0:
        for indicator in _get.indicators(leaf):
            if getattr(indicator, "time_orientation", _enums.LEFT) == _enums.RIGHT:
                _bind.detach(indicator, leaf)
    all_leaves = [leaf] + following_leaves
    assert len(all_leaves) == len(new_leaves)
    for all_leaf, new_leaf in zip(all_leaves, new_leaves):
        all_leaf.written_duration = new_leaf.written_duration
    logical_tie = _get.logical_tie(leaf)
    logical_tie_leaves = list(logical_tie)
    for leaf_ in logical_tie:
        _bind.detach(_indicators.Tie, leaf_)
        _bind.detach(_indicators.RepeatTie, leaf_)
    if leaf._parent is not None:
        index = leaf._parent.index(leaf)
        next_ = index + 1
        leaf._parent[next_:next_] = following_leaves
    index = logical_tie_leaves.index(leaf)
    next_ = index + 1
    logical_tie_leaves[next_:next_] = following_leaves
    if 1 < len(logical_tie_leaves) and isinstance(leaf, _score.Note | _score.Chord):
        _spanners.tie(logical_tie_leaves)
    if isinstance(components[0], _score.Leaf):
        assert isinstance(all_leaves, list)
        return all_leaves
    else:
        assert isinstance(components[0], _score.Tuplet)
        assert len(components) == 1
        tuplet = components[0]
        multiplier = tuplet.multiplier
        tuplet = _score.Tuplet(multiplier, [])
        assert isinstance(all_leaves, list)
        wrap(all_leaves, tuplet)
        return [tuplet]


def _set_parents(container):
    for component in container:
        component._set_parent(container)


def _split_container_at_index(CONTAINER, i):
    """
    Splits container to the left of index ``i``.

    Preserves tuplet multiplier when container is a tuplet.

    Preserves time signature denominator when container is a measure.

    Resizes resizable containers.


    Returns split parts.
    """
    # partition my components
    left_components = CONTAINER[:i]
    right_components = CONTAINER[i:]
    # instantiate new left and right containers
    if isinstance(CONTAINER, _score.Tuplet):
        multiplier = CONTAINER.multiplier
        left = type(CONTAINER)(multiplier, [])
        wrap(left_components, left)
        right = type(CONTAINER)(multiplier, [])
        wrap(right_components, right)
    else:
        left = CONTAINER.__copy__()
        wrap(left_components, left)
        right = CONTAINER.__copy__()
        wrap(right_components, right)
    # save left and right containers together for iteration
    halves = (left, right)
    nonempty_halves = [half for half in halves if len(half)]
    # incorporate left and right parents in score if possible
    selection = [CONTAINER]
    parent, start, stop = _get_parent_and_start_stop_indices(selection)
    if parent is not None:
        parent._components.__setitem__(slice(start, stop + 1), nonempty_halves)
        for part in nonempty_halves:
            part._set_parent(parent)
    else:
        left._set_parent(None)
        right._set_parent(None)
    # return new left and right containers
    return halves


def _split_container_by_duration(CONTAINER, duration, *, tag=None):
    if CONTAINER.simultaneous:
        return _split_simultaneous_by_duration(CONTAINER, duration=duration, tag=tag)
    duration = _duration.Duration(duration)
    assert 0 <= duration, repr(duration)
    if duration == 0:
        # TODO: disallow and raise Exception
        return [], CONTAINER
    # get split point score offset
    timespan = _get.timespan(CONTAINER)
    global_split_point = timespan.start_offset + duration
    # get any duration-crossing descendents
    cross_offset = timespan.start_offset + duration
    duration_crossing_descendants = []
    for descendant in _get.descendants(CONTAINER):
        timespan = _get.timespan(descendant)
        start_offset = timespan.start_offset
        stop_offset = timespan.stop_offset
        if start_offset < cross_offset < stop_offset:
            duration_crossing_descendants.append(descendant)
    # any duration-crossing leaf will be at end of list
    bottom = duration_crossing_descendants[-1]
    did_split_leaf = False
    # if split point necessitates leaf split
    if isinstance(bottom, _score.Leaf):
        assert isinstance(bottom, _score.Leaf)
        original_bottom_parent = bottom._parent
        did_split_leaf = True
        timespan = _get.timespan(bottom)
        split_point_in_bottom = global_split_point - timespan.start_offset
        new_leaves = _split_leaf_by_durations(
            bottom,
            [split_point_in_bottom],
            tag=tag,
        )
        if new_leaves[0]._parent is not original_bottom_parent:
            new_leaves_tuplet_wrapper = new_leaves[0]._parent
            assert isinstance(new_leaves_tuplet_wrapper, _score.Tuplet)
            assert new_leaves_tuplet_wrapper._parent is original_bottom_parent
            _split_container_by_duration(
                new_leaves_tuplet_wrapper,
                split_point_in_bottom,
                tag=tag,
            )
        for leaf in new_leaves:
            timespan = _get.timespan(leaf)
            if timespan.stop_offset == global_split_point:
                leaf_left_of_split = leaf
            if timespan.start_offset == global_split_point:
                leaf_right_of_split = leaf
        duration_crossing_containers = duration_crossing_descendants[:-1]
        assert len(duration_crossing_containers)
    # if split point falls between leaves
    # then find leaf to immediate right of split point
    # in order to start upward crawl through duration-crossing containers
    else:
        duration_crossing_containers = duration_crossing_descendants[:]
        for leaf in _iterate.leaves(bottom):
            timespan = _get.timespan(leaf)
            if timespan.start_offset == global_split_point:
                leaf_right_of_split = leaf
                leaf_left_of_split = _get.leaf(leaf, -1)
                break
        else:
            raise Exception("can not split empty container {bottom!r}.")
    assert leaf_left_of_split is not None
    assert leaf_right_of_split is not None
    # find component to right of split
    # that is also immediate child of last duration-crossing container
    for component in leaf_right_of_split._get_parentage():
        if component._parent is duration_crossing_containers[-1]:
            highest_level_component_right_of_split = component
            break
    else:
        raise ValueError("should not be able to get here.")
    # crawl back up through duration-crossing containers and split each
    previous = highest_level_component_right_of_split
    for container in reversed(duration_crossing_containers):
        assert isinstance(container, _score.Container)
        index = container.index(previous)
        left, right = _split_container_at_index(container, index)
        previous = right
    # reapply tie here if crawl above killed tie applied to leaves
    if did_split_leaf:
        if isinstance(leaf_left_of_split, _score.Note):
            if (
                _get.parentage(leaf_left_of_split).root
                is _get.parentage(leaf_right_of_split).root
            ):
                leaves_around_split = (
                    leaf_left_of_split,
                    leaf_right_of_split,
                )
                _attach_tie_to_leaves(leaves_around_split)
    # return list-wrapped halves of container
    return [left], [right]


def _split_simultaneous_by_duration(CONTAINER, duration, *, tag=None):
    assert CONTAINER.simultaneous
    left_components, right_components = [], []
    for component in CONTAINER[:]:
        halves = _split_container_by_duration(component, duration=duration, tag=tag)
        left_components_, right_components_ = halves
        left_components.extend(left_components_)
        right_components.extend(right_components_)
    left_container = CONTAINER.__copy__()
    right_container = CONTAINER.__copy__()
    left_container.extend(left_components)
    right_container.extend(right_components)
    if _get.parentage(CONTAINER).parent is not None:
        containers = [left_container, right_container]
        replace(CONTAINER, containers)
    # return list-wrapped halves of container
    return [left_container], [right_container]


def _split_leaf_by_durations(leaf, durations, *, cyclic=False, tag=None):
    durations = [_duration.Duration(_) for _ in durations]
    leaf_duration = _get.duration(leaf)
    if cyclic:
        durations = _sequence.repeat_to_weight(durations, leaf_duration)
    if sum(durations) < leaf_duration:
        last_duration = leaf_duration - sum(durations)
        durations = list(durations)
        durations.append(last_duration)
    durations = _sequence.truncate(durations, weight=leaf_duration)
    originally_tied = leaf._has_indicator(_indicators.Tie)
    originally_repeat_tied = leaf._has_indicator(_indicators.RepeatTie)
    result_selections = []
    # detach grace containers
    before_grace_container = leaf._before_grace_container
    if before_grace_container is not None:
        _bind.detach(before_grace_container, leaf)
    after_grace_container = leaf._after_grace_container
    if after_grace_container is not None:
        _bind.detach(after_grace_container, leaf)
    # do other things
    leaf_prolation = _get.parentage(leaf).prolation
    for duration in durations:
        new_leaf = python_copy.copy(leaf)
        preprolated_duration = duration / leaf_prolation
        selection = _set_leaf_duration(new_leaf, preprolated_duration, tag=tag)
        result_selections.append(selection)
    result_components = _sequence.flatten(result_selections, depth=-1)
    result_leaves = _select.leaves(result_components, grace=False)
    assert all(isinstance(_, _score.Component) for _ in result_components)
    assert all(isinstance(_, _score.Leaf) for _ in result_leaves)
    # strip result leaves of all indicators
    for leaf_ in result_leaves:
        _bind.detach(object, leaf_)
    # replace leaf with flattened result
    if _get.parentage(leaf).parent is not None:
        replace(leaf, result_components)
    # move indicators
    first_result_leaf = result_leaves[0]
    last_result_leaf = result_leaves[-1]
    for indicator in _get.indicators(leaf):
        _bind.detach(indicator, leaf)
        direction = getattr(indicator, "time_orientation", _enums.LEFT)
        if direction is _enums.LEFT:
            _bind.attach(indicator, first_result_leaf)
        elif direction == _enums.RIGHT:
            _bind.attach(indicator, last_result_leaf)
        elif direction == _enums.MIDDLE:
            _bind.attach(indicator, first_result_leaf)
            indicator_copy = python_copy.copy(indicator)
            _bind.attach(indicator_copy, last_result_leaf)
        else:
            raise ValueError(direction)
    # reattach grace containers
    if before_grace_container is not None:
        _bind.attach(before_grace_container, first_result_leaf)
    if after_grace_container is not None:
        _bind.attach(after_grace_container, last_result_leaf)
    # fuse tuplets
    if isinstance(result_components[0], _score.Tuplet):
        fuse(result_components)
    # tie split notes
    if isinstance(leaf, _score.Note | _score.Chord) and 1 < len(result_leaves):
        _attach_tie_to_leaves(result_leaves)
    if originally_repeat_tied and not result_leaves[0]._has_indicator(
        _indicators.RepeatTie
    ):
        _bind.attach(_indicators.RepeatTie(), result_leaves[0])
    if originally_tied and not result_leaves[-1]._has_indicator(_indicators.Tie):
        _bind.attach(_indicators.Tie(), result_leaves[-1])
    assert isinstance(result_leaves, list)
    assert all(isinstance(_, _score.Leaf) for _ in result_leaves)
    return result_leaves


def copy(argument, n=1) -> list[_score.Component]:
    r"""
    Copies argument.

    ..  container:: example

        Copies explicit clefs:

        >>> staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
        >>> clef = abjad.Clef('treble')
        >>> abjad.attach(clef, staff[0])
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[4])
        >>> copied_notes = abjad.mutate.copy(staff[:2])
        >>> staff.extend(copied_notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "treble"
                c'8
                cs'8
                d'8
                ef'8
                \clef "bass"
                e'8
                f'8
                fs'8
                g'8
                \clef "treble"
                c'8
                cs'8
            }

    ..  container:: example

        Does not copy implicit clefs:

        >>> staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
        >>> clef = abjad.Clef('treble')
        >>> abjad.attach(clef, staff[0])
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[4])
        >>> copied_notes = abjad.mutate.copy(staff[2:4])
        >>> staff.extend(copied_notes)

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "treble"
                c'8
                cs'8
                d'8
                ef'8
                \clef "bass"
                e'8
                f'8
                fs'8
                g'8
                d'8
                ef'8
            }

    ..  container:: example

        Copy components one time:

        >>> staff = abjad.Staff(r"c'8 d'8 e'8 f'8")
        >>> staff.extend(r"g'8 a'8 b'8 c''8")
        >>> score = abjad.Score([staff], name="Score")
        >>> time_signature = abjad.TimeSignature((2, 4))
        >>> abjad.attach(time_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 2/4
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
            }

        >>> selection = staff[2:4]
        >>> result = abjad.mutate.copy(selection)
        >>> new_staff = abjad.Staff(result)
        >>> abjad.show(new_staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(new_staff)
            >>> print(string)
            \new Staff
            {
                e'8
                f'8
            }

        >>> staff[2] is new_staff[0]
        False

    """
    if isinstance(argument, _score.Component):
        selection = [argument]
    else:
        selection = argument
    if n == 1:
        result = _copy_selection(selection)
        if isinstance(argument, _score.Component):
            if len(result) == 1:
                result = result[0]
        return result
    else:
        result = []
        for _ in range(n):
            result_ = copy(argument)
            result.append(result_)
        return result


def eject_contents(container: _score.Container) -> list[_score.Component]:
    r"""
    Ejects ``container`` contents.

    ..  container:: example

        Ejects leaves from container:

        >>> container = abjad.Container("c'4 ~ c'4 d'4 ~ d'4")
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c'4
                ~
                c'4
                d'4
                ~
                d'4
            }

        >>> leaves = abjad.mutate.eject_contents(container)
        >>> leaves
        [Note("c'4"), Note("c'4"), Note("d'4"), Note("d'4")]

        Leaves can be added to a new container:

        >>> staff = abjad.Staff(leaves, lilypond_type="RhythmicStaff")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new RhythmicStaff
            {
                c'4
                ~
                c'4
                d'4
                ~
                d'4
            }

        Old container is empty:

        >>> container
        Container()

    """
    assert isinstance(container, _score.Container), repr(container)
    components = container[:]
    container[:] = []
    return components


def extract(argument):
    r"""
    Extracts ``argument`` from score.

    Leaves children of ``argument`` in score.

    ..  container:: example

        Extract tuplets:

        >>> voice = abjad.Voice()
        >>> voice.append(abjad.Tuplet((3, 2), "c'4 e'4"))
        >>> voice.append(abjad.Tuplet((3, 2), "d'4 f'4"))
        >>> leaves = abjad.select.leaves(voice)
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff], name="Score")
        >>> time_signature = abjad.TimeSignature((3, 4))
        >>> abjad.attach(time_signature, leaves[0])
        >>> abjad.hairpin('p < f', leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \new Voice
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 2/3
                    {
                        \time 3/4
                        c'4
                        \p
                        \<
                        e'4
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 2/3
                    {
                        d'4
                        f'4
                        \f
                    }
                }
            }

        >>> empty_tuplet = abjad.mutate.extract(voice[-1])
        >>> empty_tuplet = abjad.mutate.extract(voice[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \new Voice
                {
                    \time 3/4
                    c'4
                    \p
                    \<
                    e'4
                    d'4
                    f'4
                    \f
                }
            }

    ..  container:: example

        Scales tuplet contents and then extracts tuplet:

        >>> voice = abjad.Voice()
        >>> staff = abjad.Staff([voice])
        >>> voice.append(abjad.Tuplet((3, 2), "c'4 e'4"))
        >>> voice.append(abjad.Tuplet((3, 2), "d'4 f'4"))
        >>> score = abjad.Score([staff], name="Score")
        >>> leaves = abjad.select.leaves(staff)
        >>> abjad.hairpin('p < f', leaves)
        >>> time_signature = abjad.TimeSignature((3, 4))
        >>> abjad.attach(time_signature, leaves[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \new Voice
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 2/3
                    {
                        \time 3/4
                        c'4
                        \p
                        \<
                        e'4
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 2/3
                    {
                        d'4
                        f'4
                        \f
                    }
                }
            }

        >>> abjad.mutate.scale(voice[-1], abjad.Fraction(3, 2))
        >>> empty_tuplet = abjad.mutate.extract(voice[-1])
        >>> abjad.mutate.scale(voice[0], abjad.Fraction(3, 2))
        >>> empty_tuplet = abjad.mutate.extract(voice[0])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \new Voice
                {
                    \time 3/4
                    c'4.
                    \p
                    \<
                    e'4.
                    d'4.
                    f'4.
                    \f
                }
            }

    ..  container:: example

        Extracting out-of-score component does nothing and returns
        component:

        >>> tuplet = abjad.Tuplet((3, 2), "c'4 e'4")
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 2/3
            {
                c'4
                e'4
            }

        >>> abjad.mutate.extract(tuplet)
        Tuplet('2:3', "c'4 e'4")

        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 2/3
            {
                c'4
                e'4
            }

    Returns ``argument``.
    """
    return _extract(argument)


def fuse(argument) -> _score.Tuplet | list[_score.Leaf]:
    r"""
    Fuses ``argument``.

    ..  container:: example

        Fuses in-score leaves:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.mutate.fuse(staff[1:])
        [Note("d'4.")]

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                d'4.
            }

    ..  container:: example

        Fuses parent-contiguous tuplets in selection:

        >>> tuplet_1 = abjad.Tuplet((2, 3), "c'8 d' e'")
        >>> tuplet_2 = abjad.Tuplet((2, 3), "c'16 d' e'")
        >>> voice = abjad.Voice([tuplet_1, tuplet_2])
        >>> staff = abjad.Staff([voice])
        >>> abjad.beam(tuplet_1[:])
        >>> abjad.slur(tuplet_2[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \new Voice
                {
                    \tuplet 3/2
                    {
                        c'8
                        [
                        d'8
                        e'8
                        ]
                    }
                    \tuplet 3/2
                    {
                        c'16
                        (
                        d'16
                        e'16
                        )
                    }
                }
            }

        >>> tuplets = voice[:]
        >>> abjad.mutate.fuse(tuplets)
        Tuplet('3:2', "c'8 d'8 e'8 c'16 d'16 e'16")
        >>> abjad.show(staff) #doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \new Voice
                {
                    \tuplet 3/2
                    {
                        c'8
                        [
                        d'8
                        e'8
                        ]
                        c'16
                        (
                        d'16
                        e'16
                        )
                    }
                }
            }

        Returns new tuplet in selection.

        Fuses zero or more parent-contiguous ``tuplets``.

        Allows in-score ``tuplets``.

        Allows outside-of-score ``tuplets``.

        All ``tuplets`` must carry the same multiplier.

        All ``tuplets`` must be of the same type.

    ..  container:: example

        REGRESSION. Trims tie from fused note:

        >>> staff = abjad.Staff("d'8 ~ d'32 ~ d'16 d'32")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                d'8
                ~
                d'32
                ~
                d'16
                d'32
            }

        >>> logical_tie = abjad.select.logical_tie(staff[0])
        >>> abjad.mutate.fuse(logical_tie)
        [Note("d'8..")]

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                d'8..
                d'32
            }

        >>> abjad.get.has_indicator(staff[0], abjad.Tie)
        False

    """
    _are_contiguous_logical_voice(argument)
    if isinstance(argument, _score.Component):
        result = _fuse([argument])
    else:
        result = _fuse(list(argument))
    assert isinstance(result, list | _score.Tuplet), repr(result)
    return result


def logical_tie_to_tuplet(
    argument, proportions, *, tag: _tag.Tag | None = None
) -> _score.Tuplet:
    r"""
    Changes logical tie to tuplet.

    ..  container:: example

        >>> voice = abjad.Voice(r"df'8 c'8 ~ c'16 cqs''4")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.Dynamic('p'), voice[0])
        >>> abjad.attach(abjad.StartHairpin('<'), voice[0])
        >>> abjad.attach(abjad.Dynamic('f'), voice[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 3
        >>> time_signature = abjad.TimeSignature((9, 16))
        >>> abjad.attach(time_signature, voice[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 3
            }
            {
                \new Voice
                {
                    \time 9/16
                    df'8
                    \p
                    \<
                    c'8
                    ~
                    c'16
                    cqs''4
                    \f
                }
            }

        >>> logical_tie = abjad.select.logical_tie(voice[1])
        >>> abjad.mutate.logical_tie_to_tuplet(logical_tie, [2, 1, 1, 1])
        Tuplet('5:3', "c'8 c'16 c'16 c'16")

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 3
            }
            {
                \new Voice
                {
                    \time 9/16
                    df'8
                    \p
                    \<
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 5/3
                    {
                        c'8
                        c'16
                        c'16
                        c'16
                    }
                    cqs''4
                    \f
                }
            }

        >>> abjad.show(staff) # doctest: +SKIP

    ..  container:: example

        >>> voice = abjad.Voice(r"c'8 ~ c'16 cqs''4")
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.hairpin('p < f', voice[:])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 3
        >>> time_signature = abjad.TimeSignature((7, 16))
        >>> abjad.attach(time_signature, voice[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 3
            }
            {
                \new Voice
                {
                    \time 7/16
                    c'8
                    \p
                    \<
                    ~
                    c'16
                    cqs''4
                    \f
                }
            }

    """
    assert all(isinstance(_, int) for _ in proportions), repr(proportions)
    target_duration = sum(_._get_preprolated_duration() for _ in argument)
    assert isinstance(target_duration, _duration.Duration)
    prolated_duration = target_duration / sum(proportions)
    basic_written_duration = prolated_duration.equal_or_greater_power_of_two
    written_durations = [_ * basic_written_duration for _ in proportions]
    notes: list[_score.Note | _score.Tuplet]
    try:
        notes = [_score.Note(0, _) for _ in written_durations]
    except _exceptions.AssignabilityError:
        denominator = target_duration._denominator
        note_durations = [_duration.Duration(_, denominator) for _ in proportions]
        notes = _makers.make_notes(0, note_durations, tag=tag)
    tuplet = _score.Tuplet.from_duration(target_duration, notes, tag=tag)
    for leaf in argument:
        _bind.detach(_indicators.Tie, leaf)
        _bind.detach(_indicators.RepeatTie, leaf)
    replace(argument, tuplet)
    return tuplet


def replace(argument, recipients, *, wrappers: bool = False) -> None:
    r"""
    Replaces ``argument`` (and contents of ``argument``) with ``recipients``.

    ..  container:: example

        Replaces in-score tuplet (and children of tuplet) with notes. Functions
        exactly the same as container setitem:

        >>> tuplet_1 = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
        >>> tuplet_2 = abjad.Tuplet((2, 3), "d'4 e'4 f'4")
        >>> voice = abjad.Voice([tuplet_1, tuplet_2])
        >>> leaves = abjad.select.leaves(voice)
        >>> abjad.hairpin('p < f', leaves)
        >>> abjad.slur(leaves)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \tuplet 3/2
                {
                    c'4
                    \p
                    (
                    \<
                    d'4
                    e'4
                }
                \tuplet 3/2
                {
                    d'4
                    e'4
                    f'4
                    \f
                    )
                }
            }

        >>> notes = abjad.makers.make_notes("c' d' e' f' c' d' e' f'", (1, 16))
        >>> abjad.mutate.replace([tuplet_1], notes)
        >>> abjad.attach(abjad.Dynamic('p'), voice[0])
        >>> abjad.attach(abjad.StartHairpin('<'), voice[0])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'16
                \p
                \<
                d'16
                e'16
                f'16
                c'16
                d'16
                e'16
                f'16
                \tuplet 3/2
                {
                    d'4
                    e'4
                    f'4
                    \f
                    )
                }
            }

        Preserves both hairpin and slur.

    ..  container:: example

        Copies no wrappers when ``wrappers`` is false:

        >>> staff = abjad.Staff("c'2 f'4 g'")
        >>> abjad.attach(abjad.Clef('alto'), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "alto"
                c'2
                f'4
                g'4
            }

        >>> for leaf in staff:
        ...     leaf, abjad.get.effective(leaf, abjad.Clef)
        ...
        (Note("c'2"), Clef(name='alto', hide=False))
        (Note("f'4"), Clef(name='alto', hide=False))
        (Note("g'4"), Clef(name='alto', hide=False))

        >>> chord = abjad.Chord("<d' e'>2")
        >>> abjad.mutate.replace(staff[0], chord)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <d' e'>2
                f'4
                g'4
            }

        >>> for leaf in staff:
        ...     leaf, abjad.get.effective(leaf, abjad.Clef)
        ...
        (Chord("<d' e'>2"), None)
        (Note("f'4"), None)
        (Note("g'4"), None)

        >>> abjad.wf.wellformed(staff)
        True

    ..  container:: example

        Set ``wrappers`` to true to copy all wrappers from one leaf to
        another leaf (and avoid full-score update). Only works from one
        leaf to another leaf:

        >>> staff = abjad.Staff("c'2 f'4 g'")
        >>> abjad.attach(abjad.Clef('alto'), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "alto"
                c'2
                f'4
                g'4
            }

        >>> for leaf in staff:
        ...     leaf, abjad.get.effective(leaf, abjad.Clef)
        ...
        (Note("c'2"), Clef(name='alto', hide=False))
        (Note("f'4"), Clef(name='alto', hide=False))
        (Note("g'4"), Clef(name='alto', hide=False))

        >>> chord = abjad.Chord("<d' e'>2")
        >>> abjad.mutate.replace(staff[0], chord, wrappers=True)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "alto"
                <d' e'>2
                f'4
                g'4
            }

        >>> for leaf in staff:
        ...     leaf, abjad.get.effective(leaf, abjad.Clef)
        ...
        (Chord("<d' e'>2"), Clef(name='alto', hide=False))
        (Note("f'4"), Clef(name='alto', hide=False))
        (Note("g'4"), Clef(name='alto', hide=False))

        >>> abjad.wf.wellformed(staff)
        True

    ..  container:: example

        ..  todo:: Fix.

        Introduces duplicate ties:

        >>> staff = abjad.Staff("c'2 ~ c'2")
        >>> tied_notes = abjad.makers.make_notes(0, abjad.Duration(5, 8))
        >>> abjad.mutate.replace(staff[:1], tied_notes)

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            c'2
            ~
            c'8
            c'2
        }

    """
    if isinstance(argument, _score.Component):
        donors = [argument]
    else:
        donors = argument
    assert _are_contiguous_same_parent(donors)
    if not isinstance(recipients, list):
        if isinstance(recipients, _score.Component):
            recipients = [recipients]
        else:
            recipients = list(recipients)
    assert _are_contiguous_same_parent(recipients)
    if not donors:
        return
    wrappers_ = []
    if wrappers is True:
        if 1 < len(donors) or not isinstance(donors[0], _score.Leaf):
            raise Exception(f"set wrappers only with single leaf: {donors!r}.")
        if 1 < len(recipients) or not isinstance(recipients[0], _score.Leaf):
            raise Exception(f"set wrappers only with single leaf: {recipients!r}.")
        donor = donors[0]
        wrappers_ = _get.wrappers(donor)
        recipient = recipients[0]
    parent, start, stop = _get_parent_and_start_stop_indices(donors)
    assert parent is not None, repr(donors)
    parent.__setitem__(slice(start, stop + 1), recipients)
    for wrapper in wrappers_:
        # bypass Wrapper._bind_component()
        # to avoid full-score update / traversal;
        # this works because one-to-one leaf replacement
        # including all (persistent) indicators
        # doesn't change score structure:
        donor._wrappers.remove(wrapper)
        wrapper._component = recipient
        recipient._wrappers.append(wrapper)
        context = wrapper._find_correct_effective_context(
            wrapper.component, wrapper.context
        )
        if context is not None:
            context._dependent_wrappers.append(wrapper)


def scale(argument, multiplier) -> None:
    r"""
    Scales ``argument`` by ``multiplier``.

    ..  container:: example

        Scales note duration by dot-generating multiplier:

        >>> staff = abjad.Staff("c'8 ( d'8 e'8 f'8 )")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.mutate.scale(staff[1], abjad.Fraction(3, 2))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                (
                d'8.
                e'8
                f'8
                )
            }

    ..  container:: example

        Scales tied leaves by dot-generating mutliplier:

        >>> staff = abjad.Staff(r"c'8 \accent ~ c'8 d'8")
        >>> score = abjad.Score([staff], name="Score")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(time_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 3/8
                c'8
                - \accent
                ~
                c'8
                d'8
            }

        >>> logical_tie = abjad.select.logical_tie(staff[0])
        >>> logical_tie = abjad.mutate.scale(logical_tie, abjad.Fraction(3, 2))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 3/8
                c'8.
                - \accent
                ~
                c'8.
                d'8
            }

    ..  container:: example

        Scales leaves in container by dot-generating multiplier:

        >>> container = abjad.Container(r"c'8 ( d'8 e'8 f'8 )")
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c'8
                (
                d'8
                e'8
                f'8
                )
            }

        >>> abjad.mutate.scale(container, abjad.Fraction(3, 2))
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c'8.
                (
                d'8.
                e'8.
                f'8.
                )
            }

    ..  container:: example

        Scales leaves in tuplet:

        >>> staff = abjad.Staff()
        >>> score = abjad.Score([staff], name="Score")
        >>> tuplet = abjad.Tuplet((4, 5), "c'8 d'8 e'8 f'8 g'8")
        >>> staff.append(tuplet)
        >>> time_signature = abjad.TimeSignature((4, 8))
        >>> leaf = abjad.get.leaf(staff, 0)
        >>> abjad.attach(time_signature, leaf)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tuplet 5/4
                {
                    \time 4/8
                    c'8
                    d'8
                    e'8
                    f'8
                    g'8
                }
            }

        >>> abjad.mutate.scale(tuplet, abjad.Fraction(2))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tuplet 5/4
                {
                    \time 4/8
                    c'4
                    d'4
                    e'4
                    f'4
                    g'4
                }
            }

    ..  container:: example

        Scales leaves carrying LilyPond multiplier:

        >>> note = abjad.Note("c'8", multiplier=(1, 2))
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'8 * 1/2

        >>> abjad.mutate.scale(note, abjad.Fraction(1, 2))
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'16 * 1/2

    """
    if hasattr(argument, "_scale"):
        argument._scale(multiplier)
    else:
        assert isinstance(argument, list)
        for component in argument:
            component._scale(multiplier)


# TODO: add tests of tupletted notes and rests.
# TODO: add examples that show indicator handling.
# TODO: add example showing grace and after grace handling.
def split(
    argument, durations, *, cyclic: bool = False, tag: _tag.Tag | None = None
) -> list[list[_score.Component]]:
    r"""
    Splits ``argument`` by ``durations``.

    Splits leaves cyclically and ties split notes:

    ..  container:: example

        >>> voice = abjad.Voice("c'1 d'1")
        >>> abjad.hairpin("p < f", voice[:])
        >>> abjad.override(voice).DynamicLineSpanner.staff_padding = 4
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4
            }
            {
                c'1
                \p
                \<
                d'1
                \f
            }

        >>> durations = [(3, 4)]
        >>> result = abjad.mutate.split(
        ...     voice[:],
        ...     durations,
        ...     cyclic=True,
        ...     )
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4
            }
            {
                c'2.
                \p
                \<
                ~
                c'4
                d'2
                \f
                ~
                d'2
            }

    ..  container:: example

        Splits custom voice and preserves context name:

        >>> voice = abjad.Voice(
        ...     "c'4 d' e' f'",
        ...     lilypond_type='CustomVoice',
        ...     name='1',
        ...     )
        >>> staff = abjad.Staff([voice])
        >>> abjad.hairpin('p < f', voice[:])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 3
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 3
            }
            {
                \context CustomVoice = "1"
                {
                    c'4
                    \p
                    \<
                    d'4
                    e'4
                    f'4
                    \f
                }
            }

        >>> durations = [(1, 8)]
        >>> result = abjad.mutate.split(
        ...     staff[:],
        ...     durations,
        ...     cyclic=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 3
            }
            {
                \context CustomVoice = "1"
                {
                    c'8
                    \p
                    \<
                    ~
                }
                \context CustomVoice = "1"
                {
                    c'8
                }
                \context CustomVoice = "1"
                {
                    d'8
                    ~
                }
                \context CustomVoice = "1"
                {
                    d'8
                }
                \context CustomVoice = "1"
                {
                    e'8
                    ~
                }
                \context CustomVoice = "1"
                {
                    e'8
                }
                \context CustomVoice = "1"
                {
                    f'8
                    \f
                    ~
                }
                \context CustomVoice = "1"
                {
                    f'8
                }
            }

        >>> for voice in staff:
        ...     voice
        ...
        Voice("c'8", lilypond_type='CustomVoice', name='1')
        Voice("c'8", lilypond_type='CustomVoice', name='1')
        Voice("d'8", lilypond_type='CustomVoice', name='1')
        Voice("d'8", lilypond_type='CustomVoice', name='1')
        Voice("e'8", lilypond_type='CustomVoice', name='1')
        Voice("e'8", lilypond_type='CustomVoice', name='1')
        Voice("f'8", lilypond_type='CustomVoice', name='1')
        Voice("f'8", lilypond_type='CustomVoice', name='1')

    ..  container:: example

        Splits parallel container:

        >>> voice_1 = abjad.Voice(
        ...     "e''4 ( es'' f'' fs'' )",
        ...     name='Voice_1',
        ...     )
        >>> voice_2 = abjad.Voice(
        ...     r"c'4 \p \< cs' d' ds' \f",
        ...     name='Voice_2',
        ...     )
        >>> abjad.override(voice_1).Stem.direction = abjad.UP
        >>> abjad.override(voice_1).Slur.direction = abjad.UP
        >>> container = abjad.Container(
        ...     [voice_1, voice_2],
        ...     simultaneous=True,
        ...     )
        >>> abjad.override(voice_2).Stem.direction = abjad.DOWN
        >>> staff = abjad.Staff([container])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <<
                    \context Voice = "Voice_1"
                    \with
                    {
                        \override Slur.direction = #up
                        \override Stem.direction = #up
                    }
                    {
                        e''4
                        (
                        es''4
                        f''4
                        fs''4
                        )
                    }
                    \context Voice = "Voice_2"
                    \with
                    {
                        \override Stem.direction = #down
                    }
                    {
                        c'4
                        \p
                        \<
                        cs'4
                        d'4
                        ds'4
                        \f
                    }
                >>
            }

        >>> durations = [(3, 8)]
        >>> result = abjad.mutate.split(
        ...     container,
        ...     durations,
        ...     cyclic=False,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            <<
                \context Voice = "Voice_1"
                \with
                {
                    \override Slur.direction = #up
                    \override Stem.direction = #up
                }
                {
                    e''4
                    (
                    es''8
                    ~
                }
                \context Voice = "Voice_2"
                \with
                {
                    \override Stem.direction = #down
                }
                {
                    c'4
                    \p
                    \<
                    cs'8
                    ~
                }
            >>
            <<
                \context Voice = "Voice_1"
                \with
                {
                    \override Slur.direction = #up
                    \override Stem.direction = #up
                }
                {
                    es''8
                    f''4
                    fs''4
                    )
                }
                \context Voice = "Voice_2"
                \with
                {
                    \override Stem.direction = #down
                }
                {
                    cs'8
                    d'4
                    ds'4
                    \f
                }
            >>
        }

    ..  container:: example

        Splits leaves with articulations:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Articulation('^'), staff[0])
        >>> abjad.attach(abjad.LaissezVibrer(), staff[1])
        >>> abjad.attach(abjad.Articulation('^'), staff[2])
        >>> abjad.attach(abjad.LaissezVibrer(), staff[3])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \marcato
                d'4
                \laissezVibrer
                e'4
                - \marcato
                f'4
                \laissezVibrer
            }

        >>> durations = [(1, 8)]
        >>> result = abjad.mutate.split(
        ...     staff[:],
        ...     durations,
        ...     cyclic=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                - \marcato
                ~
                c'8
                d'8
                ~
                d'8
                \laissezVibrer
                e'8
                - \marcato
                ~
                e'8
                f'8
                ~
                f'8
                \laissezVibrer
            }

    ..  container:: example

        REGRESSION. Preserves tie:

        >>> staff = abjad.Staff("d'2 ~ d'")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                d'2
                ~
                d'2
            }

        >>> result = abjad.mutate.split(staff[0], [(1, 32)])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                d'32
                ~
                d'4...
                ~
                d'2
            }

    ..  container:: example

        REGRESSION. Leaf independent after-grace leaves unchanged:

        >>> music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> container = abjad.IndependentAfterGraceContainer("af'4 gf'4")
        >>> music_voice.insert(3, container)
        >>> staff = abjad.Staff([music_voice])
        >>> lilypond_file = abjad.LilyPondFile([staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'4
                    d'4
                    \afterGrace
                    e'4
                    {
                        af'4
                        gf'4
                    }
                    f'4
                }
            }

        >>> result = abjad.mutate.split(music_voice[:], [(1, 8)], cyclic=True)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \context Voice = "MusicVoice"
                {
                    c'8
                    ~
                    c'8
                    d'8
                    ~
                    d'8
                    e'8
                    ~
                    \afterGrace
                    e'8
                    {
                        af'4
                        gf'4
                    }
                    f'8
                    ~
                    f'8
                }
            }

    """
    components = argument
    if isinstance(components, _score.Component):
        components = [components]
    assert all(isinstance(_, _score.Component) for _ in components)
    durations = [_duration.Duration(_) for _ in durations]
    assert len(durations), repr(durations)
    total_component_duration = _get.duration(components)
    total_split_duration = sum(durations)
    if cyclic:
        durations = _sequence.repeat_to_weight(durations, total_component_duration)
        durations = list(durations)
    elif total_split_duration < total_component_duration:
        final_offset = total_component_duration - sum(durations)
        durations.append(final_offset)
    elif total_component_duration < total_split_duration:
        weight = total_component_duration
        durations = _sequence.truncate(durations, weight=weight)
        durations = list(durations)
    # keep copy of durations to partition result components
    durations_copy = durations[:]
    total_split_duration = sum(durations)
    assert total_split_duration == total_component_duration
    result, shard = [], []
    offset_index = 0
    current_shard_duration = _duration.Duration(0)
    remaining_components = list(components[:])
    advance_to_next_offset = True
    # build shards:
    # grab next component and next duration each time through loop
    while True:
        # grab next split point
        if advance_to_next_offset:
            if not durations:
                break
            next_split_point = durations.pop(0)
        advance_to_next_offset = True
        # grab next component from input stack of components
        if not remaining_components:
            break
        current_component = remaining_components.pop(0)
        # find where current component endpoint will position us
        duration_ = _get.duration(current_component)
        candidate_shard_duration = current_shard_duration + duration_
        # if current component would fill current shard exactly
        if candidate_shard_duration == next_split_point:
            shard.append(current_component)
            result.append(shard)
            shard = []
            current_shard_duration = _duration.Duration(0)
            offset_index += 1
        # if current component would exceed current shard
        elif next_split_point < candidate_shard_duration:
            local_split_duration = next_split_point
            local_split_duration -= current_shard_duration
            if isinstance(current_component, _score.Leaf):
                leaf_split_durations = [local_split_duration]
                duration_ = _get.duration(current_component)
                current_duration = duration_
                additional_required_duration = current_duration
                additional_required_duration -= local_split_duration
                split_durations = _sequence.split(
                    durations,
                    [additional_required_duration],
                    cyclic=False,
                    overhang=True,
                )
                split_durations = [list(_) for _ in split_durations]
                additional_durations = split_durations[0]
                leaf_split_durations.extend(additional_durations)
                durations = split_durations[-1]
                leaf_shards = _split_leaf_by_durations(
                    current_component,
                    leaf_split_durations,
                    cyclic=False,
                    tag=tag,
                )
                shard.extend(leaf_shards)
                result.append(shard)
                offset_index += len(additional_durations)
            else:
                assert isinstance(current_component, _score.Container)
                pair = _split_container_by_duration(
                    current_component,
                    local_split_duration,
                    tag=tag,
                )
                left_list, right_list = pair
                shard.extend(left_list)
                result.append(shard)
                remaining_components.__setitem__(slice(0, 0), right_list)
            shard = []
            offset_index += 1
            current_shard_duration = _duration.Duration(0)
        # if current component would not fill current shard
        elif candidate_shard_duration < next_split_point:
            shard.append(current_component)
            duration_ = _get.duration(current_component)
            current_shard_duration += duration_
            advance_to_next_offset = False
        else:
            message = "can not process candidate duration: {!r}."
            message = message.format(candidate_shard_duration)
            raise ValueError(message)
    # append any stub shard
    if len(shard):
        result.append(shard)
    # append any unexamined components
    if len(remaining_components):
        result.append(remaining_components)
    # partition split components according to input durations
    result = _sequence.flatten(result, depth=-1)
    result = _select.partition_by_durations(result, durations_copy, fill=_enums.EXACT)
    # return list of component lists
    for list_ in result:
        assert isinstance(list_, list), repr(list_)
        assert all(isinstance(_, _score.Component) for _ in list_), repr(list_)
    return result


def swap(argument, container):
    r"""
    Swaps ``argument`` for empty ``container``.

    ..  container:: example

        Swaps containers for tuplet:

        >>> voice = abjad.Voice()
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff], name="Score")
        >>> voice.append(abjad.Container("c'4 d'4 e'4"))
        >>> voice.append(abjad.Container("d'4 e'4 f'4"))
        >>> abjad.attach(abjad.TimeSignature((3, 4)), voice[0][0])
        >>> leaves = abjad.select.leaves(voice)
        >>> abjad.hairpin('p < f', leaves)
        >>> measures = voice[:]
        >>> abjad.slur(leaves)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                {
                    \time 3/4
                    c'4
                    \p
                    (
                    \<
                    d'4
                    e'4
                }
                {
                    d'4
                    e'4
                    f'4
                    \f
                    )
                }
            }

        >>> containers = voice[:]
        >>> tuplet = abjad.Tuplet((2, 3), [])
        >>> tuplet.denominator = 4
        >>> abjad.mutate.swap(containers, tuplet)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \tuplet 6/4
                {
                    \time 3/4
                    c'4
                    \p
                    (
                    \<
                    d'4
                    e'4
                    d'4
                    e'4
                    f'4
                    \f
                    )
                }
            }

        REGRESSION: context indicators survive swap:

        >>> prototype = abjad.TimeSignature
        >>> for component in abjad.iterate.components(voice):
        ...     time_signature = abjad.get.effective(component, prototype)
        ...     print(component, time_signature)
        ...
        Voice("{ 3:2 c'4 d'4 e'4 d'4 e'4 f'4 }") TimeSignature(pair=(3, 4), hide=False, partial=None)
        Tuplet('3:2', "c'4 d'4 e'4 d'4 e'4 f'4") TimeSignature(pair=(3, 4), hide=False, partial=None)
        Note("c'4") TimeSignature(pair=(3, 4), hide=False, partial=None)
        Note("d'4") TimeSignature(pair=(3, 4), hide=False, partial=None)
        Note("e'4") TimeSignature(pair=(3, 4), hide=False, partial=None)
        Note("d'4") TimeSignature(pair=(3, 4), hide=False, partial=None)
        Note("e'4") TimeSignature(pair=(3, 4), hide=False, partial=None)
        Note("f'4") TimeSignature(pair=(3, 4), hide=False, partial=None)

    Returns none.
    """
    if isinstance(argument, list):
        donors = argument
    else:
        assert isinstance(argument, _score.Component)
        donors = [argument]
    assert _are_contiguous_same_parent(donors)
    assert isinstance(container, _score.Container)
    assert not container, repr(container)
    _give_components_to_empty_container(donors, container)
    _give_position_in_parent_to_container(donors, container)


def transpose(argument, interval):
    r"""
    Transposes notes and chords in ``argument`` by ``interval``.

    ..  todo:: Move to abjad.pitch package.

    ..  container:: example

        Transposes notes and chords in staff:

        >>> staff = abjad.Staff()
        >>> score = abjad.Score([staff], name="Score")
        >>> staff.extend("c'4 d'4 e'4 r4")
        >>> abjad.attach(abjad.TimeSignature((4, 4)), staff[0])
        >>> staff.extend("d'4 e'4 <f' a' c''>4")
        >>> abjad.attach(abjad.TimeSignature((3, 4)), staff[4])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 4/4
                c'4
                d'4
                e'4
                r4
                \time 3/4
                d'4
                e'4
                <f' a' c''>4
            }

        >>> abjad.mutate.transpose(staff, "+m3")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 4/4
                ef'4
                f'4
                g'4
                r4
                \time 3/4
                f'4
                g'4
                <af' c'' ef''>4
            }

    Returns none.
    """
    named_interval = _pitch.NamedInterval(interval)
    for item in _iterate.components(argument, (_score.Note, _score.Chord)):
        if isinstance(item, _score.Note):
            old_written_pitch = item.note_head.written_pitch
            new_written_pitch = old_written_pitch.transpose(named_interval)
            item.note_head.written_pitch = new_written_pitch
        else:
            for note_head in item.note_heads:
                old_written_pitch = note_head.written_pitch
                new_written_pitch = old_written_pitch.transpose(named_interval)
                note_head.written_pitch = new_written_pitch


def wrap(argument, container):
    r"""
    Wraps ``argument`` in empty ``container``.

    ..  container:: example

        Wraps in-score notes in tuplet:

        >>> staff = abjad.Staff("c'8 [ ( d' e' ] ) c' [ ( d' e' ] )")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                [
                (
                d'8
                e'8
                )
                ]
                c'8
                [
                (
                d'8
                e'8
                )
                ]
            }

        >>> tuplet = abjad.Tuplet((2, 3), [])
        >>> abjad.mutate.wrap(staff[-3:], tuplet)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                [
                (
                d'8
                e'8
                )
                ]
                \tuplet 3/2
                {
                    c'8
                    [
                    (
                    d'8
                    e'8
                    )
                    ]
                }
            }

    ..  container:: example

        Wraps outside-score notes in tuplet:

        >>> notes = abjad.makers.make_notes([0, 2, 4], [(1, 8)])
        >>> tuplet = abjad.Tuplet((2, 3), [])
        >>> abjad.mutate.wrap(notes, tuplet)
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tuplet 3/2
            {
                c'8
                d'8
                e'8
            }

        (This usage merely substitutes for the tuplet initializer.)

    ..  container:: example

        Wraps leaves in container:

        >>> notes = [abjad.Note(n, (1, 8)) for n in range(8)]
        >>> staff = abjad.Staff(notes)
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((4, 8)), staff[0])
        >>> container = abjad.Container()
        >>> abjad.mutate.wrap(staff[:4], container)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                {
                    \time 4/8
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
                e'8
                f'8
                fs'8
                g'8
            }

    ..  container:: example

        Wraps each leaf in tuplet:

        >>> notes = [abjad.Note(n, (1, 1)) for n in range(4)]
        >>> staff = abjad.Staff(notes)
        >>> for note in staff:
        ...     tuplet = abjad.Tuplet((2, 3))
        ...     abjad.mutate.wrap(note, tuplet)
        ...

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    c'1
                }
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    cs'1
                }
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    d'1
                }
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    ef'1
                }
            }

    ..  container:: example

        Raises exception on nonempty ``container``:

        >>> import pytest
        >>> staff = abjad.Staff("c'8 [ ( d' e' ] ) c' [ ( d' e' ] )")
        >>> tuplet = abjad.Tuplet((2, 3), "g'8 a' fs'")
        >>> abjad.mutate.wrap(staff[-3:], tuplet)
        Traceback (most recent call last):
            ...
        Exception: must be empty container: Tuplet('3:2', "g'8 a'8 fs'8").

    ..  container:: example

        REGRESSION. Contexted indicators (like time signature) survive
        wrap:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff], name="Score")
        >>> leaves = abjad.select.leaves(staff)
        >>> abjad.attach(abjad.TimeSignature((3, 8)), leaves[0])
        >>> container = abjad.Container()
        >>> abjad.mutate.wrap(leaves, container)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                {
                    \time 3/8
                    c'4
                    d'4
                    e'4
                    f'4
                }
            }

        >>> prototype = abjad.TimeSignature
        >>> for component in abjad.iterate.components(staff):
        ...     time_signature = abjad.get.effective(component, prototype)
        ...     print(component, time_signature)
        ...
        Staff("{ c'4 d'4 e'4 f'4 }") TimeSignature(pair=(3, 8), hide=False, partial=None)
        Container("c'4 d'4 e'4 f'4") TimeSignature(pair=(3, 8), hide=False, partial=None)
        Note("c'4") TimeSignature(pair=(3, 8), hide=False, partial=None)
        Note("d'4") TimeSignature(pair=(3, 8), hide=False, partial=None)
        Note("e'4") TimeSignature(pair=(3, 8), hide=False, partial=None)
        Note("f'4") TimeSignature(pair=(3, 8), hide=False, partial=None)

    Returns none.
    """
    if not isinstance(container, _score.Container) or 0 < len(container):
        raise Exception(f"must be empty container: {container!r}.")
    if isinstance(argument, _score.Component):
        selection = [argument]
    else:
        selection = argument
    parent, start, stop = _get_parent_and_start_stop_indices(
        selection, ignore_before_after_grace=True
    )
    if not _are_contiguous_logical_voice(selection, ignore_before_after_grace=True):
        message = "must be contiguous components in same logical voice:\n"
        message += f"   {selection!r}."
        raise Exception(message)
    container._components = list(selection)
    _set_parents(container)
    if parent is not None:
        parent._components.insert(start, container)
        container._set_parent(parent)
