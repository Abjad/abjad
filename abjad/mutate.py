import copy as python_copy
import itertools

from . import enums, exceptions, get
from .attach import attach, detach
from .duration import Duration
from .indicators.RepeatTie import RepeatTie
from .indicators.Tie import Tie
from .iterate import Iteration
from .makers import NoteMaker
from .pitch.intervals import NamedInterval
from .ratio import Ratio
from .score import BeforeGraceContainer, Chord, Component, Container, Leaf, Note, Tuplet
from .select import Selection
from .sequence import Sequence
from .spanners import tie

### PRIVATE FUNCTIONS ###


def _extract(COMPONENT):
    selection = Selection([COMPONENT])
    parent, start, stop = selection._get_parent_and_start_stop_indices()
    if parent is not None:
        components = list(getattr(COMPONENT, "components", ()))
        parent.__setitem__(slice(start, stop + 1), components)
    return COMPONENT


def _fuse(SELECTION):
    assert SELECTION.are_contiguous_logical_voice()
    if SELECTION.are_leaves():
        return _fuse_leaves(SELECTION)
    elif all(isinstance(_, Tuplet) for _ in SELECTION):
        return _fuse_tuplets(SELECTION)
    else:
        raise Exception(f"can only fuse leaves and tuplets (not {SELECTION}).")


def _fuse_leaves(SELECTION):
    assert SELECTION.are_leaves()
    assert SELECTION.are_contiguous_logical_voice()
    leaves = SELECTION
    if len(leaves) <= 1:
        return leaves
    originally_tied = SELECTION[-1]._has_indicator(Tie)
    total_preprolated = leaves._get_preprolated_duration()
    for leaf in leaves[1:]:
        parent = leaf._parent
        if parent:
            index = parent.index(leaf)
            del parent[index]
    result = _set_leaf_duration(leaves[0], total_preprolated)
    if not originally_tied:
        last_leaf = Selection(result).leaf(-1)
        detach(Tie, last_leaf)
    return result


def _fuse_leaves_by_immediate_parent(SELECTION):
    result = []
    parts = _get_leaves_grouped_by_immediate_parents(SELECTION)
    for part in parts:
        fused = _fuse(part)
        result.append(fused)
    return result


def _fuse_tuplets(SELECTION):
    assert SELECTION.are_contiguous_same_parent(prototype=Tuplet)
    if len(SELECTION) == 0:
        return None
    first = SELECTION[0]
    first_multiplier = first.multiplier
    for tuplet in SELECTION[1:]:
        if tuplet.multiplier != first_multiplier:
            raise ValueError("tuplets must carry same multiplier.")
    assert isinstance(first, Tuplet)
    new_tuplet = Tuplet(first_multiplier, [])
    wrapped = False
    if get.parentage(SELECTION[0]).root is not get.parentage(SELECTION[-1]).root:
        dummy_container = Container(SELECTION)
        wrapped = True
    swap(SELECTION, new_tuplet)
    if wrapped:
        del dummy_container[:]
    return new_tuplet


def _get_leaves_grouped_by_immediate_parents(SELECTION):
    result = []
    pairs_generator = itertools.groupby(SELECTION, lambda x: id(x._parent))
    for key, values_generator in pairs_generator:
        group = Selection(list(values_generator))
        result.append(group)
    return result


def _move_indicators(donor_component, recipient_component):
    for wrapper in get.wrappers(donor_component):
        detach(wrapper, donor_component)
        attach(wrapper, recipient_component)


def _set_leaf_duration(leaf, new_duration):
    new_duration = Duration(new_duration)
    if leaf.multiplier is not None:
        multiplier = new_duration.__div__(leaf.written_duration)
        leaf.multiplier = multiplier
        return Selection(leaf)
    try:
        leaf.written_duration = new_duration
        return Selection(leaf)
    except exceptions.AssignabilityError:
        pass
    maker = NoteMaker()
    components = maker(0, new_duration)
    new_leaves = Selection(components).leaves()
    following_leaf_count = len(new_leaves) - 1
    following_leaves = []
    for i in range(following_leaf_count):
        following_leaf = copy(leaf)
        for indicator in get.indicators(following_leaf):
            if i != following_leaf_count - 1:
                if getattr(indicator, "_time_orientation", enums.Left) != enums.Middle:
                    detach(indicator, following_leaf)
            elif (
                getattr(indicator, "_time_orientation", enums.Left) != enums.Right
                and getattr(indicator, "_time_orientation", enums.Left) != enums.Middle
            ):
                detach(indicator, following_leaf)
        detach(BeforeGraceContainer, following_leaf)
        following_leaves.append(following_leaf)
    if following_leaf_count > 0:
        for indicator in get.indicators(leaf):
            if getattr(indicator, "_time_orientation", enums.Left) == enums.Right:
                detach(indicator, leaf)
    all_leaves = [leaf] + following_leaves
    assert len(all_leaves) == len(new_leaves)
    for all_leaf, new_leaf in zip(all_leaves, new_leaves):
        all_leaf.written_duration = new_leaf.written_duration
    logical_tie = get.logical_tie(leaf)
    logical_tie_leaves = list(logical_tie.leaves)
    for leaf_ in logical_tie:
        detach(Tie, leaf_)
        detach(RepeatTie, leaf_)
    if leaf._parent is not None:
        index = leaf._parent.index(leaf)
        next_ = index + 1
        leaf._parent[next_:next_] = following_leaves
    index = logical_tie_leaves.index(leaf)
    next_ = index + 1
    logical_tie_leaves[next_:next_] = following_leaves
    if 1 < len(logical_tie_leaves) and isinstance(leaf, (Note, Chord)):
        tie(logical_tie_leaves)
    if isinstance(components[0], Leaf):
        return Selection(all_leaves)
    else:
        assert isinstance(components[0], Tuplet)
        assert len(components) == 1
        tuplet = components[0]
        multiplier = tuplet.multiplier
        tuplet = Tuplet(multiplier, [])
        if not isinstance(all_leaves, Selection):
            all_leaves = Selection(all_leaves)
        wrap(all_leaves, tuplet)
        return Selection(tuplet)


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
    if isinstance(CONTAINER, Tuplet):
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
    selection = Selection(CONTAINER)
    parent, start, stop = selection._get_parent_and_start_stop_indices()
    if parent is not None:
        parent._components.__setitem__(slice(start, stop + 1), nonempty_halves)
        for part in nonempty_halves:
            part._set_parent(parent)
    else:
        left._set_parent(None)
        right._set_parent(None)
    # return new left and right containers
    return halves


def _split_container_by_duration(CONTAINER, duration):
    if CONTAINER.simultaneous:
        return _split_simultaneous_by_duration(CONTAINER, duration=duration)
    duration = Duration(duration)
    assert 0 <= duration, repr(duration)
    if duration == 0:
        # TODO: disallow and raise Exception
        return [], CONTAINER
    # get split point score offset
    timespan = get.timespan(CONTAINER)
    global_split_point = timespan.start_offset + duration
    # get any duration-crossing descendents
    cross_offset = timespan.start_offset + duration
    duration_crossing_descendants = []
    for descendant in get.descendants(CONTAINER):
        timespan = get.timespan(descendant)
        start_offset = timespan.start_offset
        stop_offset = timespan.stop_offset
        if start_offset < cross_offset < stop_offset:
            duration_crossing_descendants.append(descendant)
    # any duration-crossing leaf will be at end of list
    bottom = duration_crossing_descendants[-1]
    did_split_leaf = False
    # if split point necessitates leaf split
    if isinstance(bottom, Leaf):
        assert isinstance(bottom, Leaf)
        original_bottom_parent = bottom._parent
        did_split_leaf = True
        timespan = get.timespan(bottom)
        split_point_in_bottom = global_split_point - timespan.start_offset
        new_leaves = _split_leaf_by_durations(
            bottom,
            [split_point_in_bottom],
        )
        if new_leaves[0]._parent is not original_bottom_parent:
            new_leaves_tuplet_wrapper = new_leaves[0]._parent
            assert isinstance(new_leaves_tuplet_wrapper, Tuplet)
            assert new_leaves_tuplet_wrapper._parent is original_bottom_parent
            _split_container_by_duration(
                new_leaves_tuplet_wrapper,
                split_point_in_bottom,
            )
        for leaf in new_leaves:
            timespan = get.timespan(leaf)
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
        for leaf in Iteration(bottom).leaves():
            timespan = get.timespan(leaf)
            if timespan.start_offset == global_split_point:
                leaf_right_of_split = leaf
                leaf_left_of_split = get.leaf(leaf, -1)
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
        assert isinstance(container, Container)
        index = container.index(previous)
        left, right = _split_container_at_index(container, index)
        previous = right
    # reapply tie here if crawl above killed tie applied to leaves
    if did_split_leaf:
        if isinstance(leaf_left_of_split, Note):
            if (
                get.parentage(leaf_left_of_split).root
                is get.parentage(leaf_right_of_split).root
            ):
                leaves_around_split = (
                    leaf_left_of_split,
                    leaf_right_of_split,
                )
                selection = Selection(leaves_around_split)
                selection._attach_tie_to_leaves()
    # return list-wrapped halves of container
    return [left], [right]


def _split_simultaneous_by_duration(CONTAINER, duration):
    assert CONTAINER.simultaneous
    left_components, right_components = [], []
    for component in CONTAINER[:]:
        halves = _split_container_by_duration(component, duration=duration)
        left_components_, right_components_ = halves
        left_components.extend(left_components_)
        right_components.extend(right_components_)
    left_components = Selection(left_components)
    right_components = Selection(right_components)
    left_container = CONTAINER.__copy__()
    right_container = CONTAINER.__copy__()
    left_container.extend(left_components)
    right_container.extend(right_components)
    if get.parentage(CONTAINER).parent is not None:
        containers = Selection([left_container, right_container])
        replace(CONTAINER, containers)
    # return list-wrapped halves of container
    return [left_container], [right_container]


def _split_leaf_by_durations(LEAF, durations, cyclic=False):
    durations = [Duration(_) for _ in durations]
    durations = Sequence(durations)
    leaf_duration = get.duration(LEAF)
    if cyclic:
        durations = durations.repeat_to_weight(leaf_duration)
    if sum(durations) < leaf_duration:
        last_duration = leaf_duration - sum(durations)
        durations = list(durations)
        durations.append(last_duration)
        durations = Sequence(durations)
    durations = durations.truncate(weight=leaf_duration)
    originally_tied = LEAF._has_indicator(Tie)
    originally_repeat_tied = LEAF._has_indicator(RepeatTie)
    result_selections = []
    # detach grace containers
    before_grace_container = LEAF._before_grace_container
    if before_grace_container is not None:
        detach(before_grace_container, LEAF)
    after_grace_container = LEAF._after_grace_container
    if after_grace_container is not None:
        detach(after_grace_container, LEAF)
    # do other things
    leaf_prolation = get.parentage(LEAF).prolation
    for duration in durations:
        new_leaf = python_copy.copy(LEAF)
        preprolated_duration = duration / leaf_prolation
        selection = _set_leaf_duration(new_leaf, preprolated_duration)
        result_selections.append(selection)
    result_components = Sequence(result_selections).flatten(depth=-1)
    result_components = Selection(result_components)
    result_leaves = Selection(result_components).leaves(grace=False)
    assert all(isinstance(_, Selection) for _ in result_selections)
    assert all(isinstance(_, Component) for _ in result_components)
    assert result_leaves.are_leaves()
    # strip result leaves of all indicators
    for leaf in result_leaves:
        detach(object, leaf)
    # replace leaf with flattened result
    if get.parentage(LEAF).parent is not None:
        replace(LEAF, result_components)
    # move indicators
    first_result_leaf = result_leaves[0]
    last_result_leaf = result_leaves[-1]
    for indicator in get.indicators(LEAF):
        detach(indicator, LEAF)
        direction = getattr(indicator, "_time_orientation", enums.Left)
        if direction is enums.Left:
            attach(indicator, first_result_leaf)
        elif direction == enums.Right:
            attach(indicator, last_result_leaf)
        elif direction == enums.Middle:
            attach(indicator, first_result_leaf)
            indicator_copy = python_copy.copy(indicator)
            attach(indicator_copy, last_result_leaf)
        else:
            raise ValueError(direction)
    # reattach grace containers
    if before_grace_container is not None:
        attach(before_grace_container, first_result_leaf)
    if after_grace_container is not None:
        attach(after_grace_container, last_result_leaf)
    # fuse tuplets
    if isinstance(result_components[0], Tuplet):
        fuse(result_components)
    # tie split notes
    if isinstance(LEAF, (Note, Chord)) and 1 < len(result_leaves):
        result_leaves._attach_tie_to_leaves()
    if originally_repeat_tied and not result_leaves[0]._has_indicator(RepeatTie):
        attach(RepeatTie(), result_leaves[0])
    if originally_tied and not result_leaves[-1]._has_indicator(Tie):
        attach(Tie(), result_leaves[-1])
    assert isinstance(result_leaves, Selection)
    assert all(isinstance(_, Leaf) for _ in result_leaves)
    return result_leaves


### PUBLIC FUNCTIONS ###


def copy(argument, n=1):
    r"""
    Copies client.

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
        >>> result = selection._copy()
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

    Returns selection of new components.
    """
    if isinstance(argument, Component):
        selection = Selection(argument)
    else:
        selection = argument
    if n == 1:
        result = selection._copy()
        if isinstance(argument, Component):
            if len(result) == 1:
                result = result[0]
        return result
    else:
        result = []
        for _ in range(n):
            result_ = copy(argument)
            result.append(result_)
        return result


def eject_contents(argument):
    r"""
    Ejects contents from outside-of-score container.

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

        Returns container contents as a selection with spanners preserved:

        >>> contents = abjad.mutate.eject_contents(container)
        >>> contents
        Selection([Note("c'4"), Note("c'4"), Note("d'4"), Note("d'4")])

        Container contents can be safely added to a new container:

        >>> staff = abjad.Staff(contents, lilypond_type='RhythmicStaff')
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

        New container is well formed:

        >>> abjad.wf.wellformed(staff)
        True

        Old container is empty:

        >>> container
        Container()

    Returns container contents as selection.
    """
    return argument._eject_contents()


def extract(argument):
    r"""
    Extracts mutation client from score.

    Leaves children of mutation client in score.

    ..  container:: example

        Extract tuplets:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.Tuplet((3, 2), "c'4 e'4"))
        >>> staff.append(abjad.Tuplet((3, 2), "d'4 f'4"))
        >>> leaves = abjad.select(staff).leaves()
        >>> time_signature = abjad.TimeSignature((3, 4))
        >>> abjad.attach(time_signature, leaves[0])
        >>> abjad.hairpin('p < f', leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    \time 3/4
                    c'4
                    \p
                    \<
                    e'4
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    d'4
                    f'4
                    \f
                }
            }

        >>> empty_tuplet = abjad.mutate.extract(staff[-1])
        >>> empty_tuplet = abjad.mutate.extract(staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
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

    ..  container:: example

        Scales tuplet contents and then extracts tuplet:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.Tuplet((3, 2), "c'4 e'4"))
        >>> staff.append(abjad.Tuplet((3, 2), "d'4 f'4"))
        >>> leaves = abjad.select(staff).leaves()
        >>> abjad.hairpin('p < f', leaves)
        >>> time_signature = abjad.TimeSignature((3, 4))
        >>> abjad.attach(time_signature, leaves[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    \time 3/4
                    c'4
                    \p
                    \<
                    e'4
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    d'4
                    f'4
                    \f
                }
            }

        >>> abjad.mutate.scale(staff[-1], abjad.Multiplier((3, 2)))
        >>> empty_tuplet = abjad.mutate.extract(staff[-1])
        >>> abjad.mutate.scale(staff[0], abjad.Multiplier((3, 2)))
        >>> empty_tuplet = abjad.mutate.extract(staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
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

    ..  container:: example

        Extracting out-of-score component does nothing and returns
        component:

        >>> tuplet = abjad.Tuplet((3, 2), "c'4 e'4")
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak text #tuplet-number::calc-fraction-text
            \times 3/2 {
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
            \times 3/2 {
                c'4
                e'4
            }

    Returns mutation client.
    """
    return _extract(argument)


def fuse(argument):
    r"""
    Fuses mutation client.

    ..  container:: example

        Fuses in-score leaves:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.mutate.fuse(staff[1:])
        Selection([Note("d'4.")])
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
        >>> abjad.beam(tuplet_1[:])
        >>> tuplet_2 = abjad.Tuplet((2, 3), "c'16 d' e'")
        >>> abjad.slur(tuplet_2[:])
        >>> staff = abjad.Staff([tuplet_1, tuplet_2])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \times 2/3 {
                    c'8
                    [
                    d'8
                    e'8
                    ]
                }
                \times 2/3 {
                    c'16
                    (
                    d'16
                    e'16
                    )
                }
            }

        >>> tuplets = staff[:]
        >>> abjad.mutate.fuse(tuplets)
        Tuplet('3:2', "c'8 d'8 e'8 c'16 d'16 e'16")
        >>> abjad.show(staff) #doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \times 2/3 {
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

        >>> logical_tie = abjad.select(staff[0]).logical_tie()
        >>> abjad.mutate.fuse(logical_tie)
        Selection([Note("d'8..")])

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

    Returns selection.
    """
    if isinstance(argument, Component):
        selection = Selection(argument)
        return _fuse(selection)
    elif isinstance(argument, Selection) and argument.are_contiguous_logical_voice():
        selection = Selection(argument)
        return _fuse(selection)


def logical_tie_to_tuplet(argument, proportions) -> Tuplet:
    r"""
    Changes logical tie to tuplet.

    ..  container:: example

        >>> staff = abjad.Staff(r"df'8 c'8 ~ c'16 cqs''4")
        >>> abjad.attach(abjad.Dynamic('p'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('<'), staff[0])
        >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 3
        >>> time_signature = abjad.TimeSignature((9, 16))
        >>> abjad.attach(time_signature, staff[0])
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

        >>> logical_tie = abjad.select(staff[1]).logical_tie()
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
                \time 9/16
                df'8
                \p
                \<
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    c'8
                    c'16
                    c'16
                    c'16
                }
                cqs''4
                \f
            }

        >>> abjad.show(staff) # doctest: +SKIP

    ..  container:: example

        >>> staff = abjad.Staff(r"c'8 ~ c'16 cqs''4")
        >>> abjad.hairpin('p < f', staff[:])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 3
        >>> time_signature = abjad.TimeSignature((7, 16))
        >>> abjad.attach(time_signature, staff[0])
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
                \time 7/16
                c'8
                \p
                \<
                ~
                c'16
                cqs''4
                \f
            }

    """
    proportions = Ratio(proportions)
    target_duration = argument._get_preprolated_duration()
    prolated_duration = target_duration / sum(proportions.numbers)
    basic_written_duration = prolated_duration.equal_or_greater_power_of_two
    written_durations = [_ * basic_written_duration for _ in proportions.numbers]
    maker = NoteMaker()
    try:
        notes = Selection([Note(0, _) for _ in written_durations])
    except exceptions.AssignabilityError:
        denominator = target_duration._denominator
        note_durations = [Duration(_, denominator) for _ in proportions.numbers]
        notes = maker(0, note_durations)
    tuplet = Tuplet.from_duration(target_duration, notes)
    for leaf in argument:
        detach(Tie, leaf)
        detach(RepeatTie, leaf)
    replace(argument, tuplet)
    return tuplet


def replace(argument, recipients, wrappers=False):
    r"""
    Replaces mutation client (and contents of mutation client) with
    ``recipients``.

    ..  container:: example

        Replaces in-score tuplet (and children of tuplet) with notes.
        Functions exactly the same as container setitem:

        >>> tuplet_1 = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
        >>> tuplet_2 = abjad.Tuplet((2, 3), "d'4 e'4 f'4")
        >>> staff = abjad.Staff([tuplet_1, tuplet_2])
        >>> leaves = abjad.select(staff).leaves()
        >>> abjad.hairpin('p < f', leaves)
        >>> abjad.slur(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \times 2/3 {
                    c'4
                    \p
                    \<
                    (
                    d'4
                    e'4
                }
                \times 2/3 {
                    d'4
                    e'4
                    f'4
                    \f
                    )
                }
            }

        >>> maker = abjad.NoteMaker()
        >>> notes = maker("c' d' e' f' c' d' e' f'", (1, 16))
        >>> abjad.mutate.replace([tuplet_1], notes)
        >>> abjad.attach(abjad.Dynamic('p'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('<'), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
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
                \times 2/3 {
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
        (Note("c'2"), Clef('alto'))
        (Note("f'4"), Clef('alto'))
        (Note("g'4"), Clef('alto'))

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
        (Note("c'2"), Clef('alto'))
        (Note("f'4"), Clef('alto'))
        (Note("g'4"), Clef('alto'))

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
        (Chord("<d' e'>2"), Clef('alto'))
        (Note("f'4"), Clef('alto'))
        (Note("g'4"), Clef('alto'))

        >>> abjad.wf.wellformed(staff)
        True

    ..  container:: example

        ..  todo:: Fix.

        Introduces duplicate ties:

        >>> staff = abjad.Staff("c'2 ~ c'2")
        >>> maker = abjad.NoteMaker()
        >>> tied_notes = maker(0, abjad.Duration(5, 8))
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

    Returns none.
    """
    if isinstance(argument, Selection):
        donors = argument
    else:
        donors = Selection(argument)
    assert donors.are_contiguous_same_parent()
    if not isinstance(recipients, Selection):
        recipients = Selection(recipients)
    assert recipients.are_contiguous_same_parent()
    if not donors:
        return
    if wrappers is True:
        if 1 < len(donors) or not isinstance(donors[0], Leaf):
            raise Exception(f"set wrappers only with single leaf: {donors!r}.")
        if 1 < len(recipients) or not isinstance(recipients[0], Leaf):
            raise Exception(f"set wrappers only with single leaf: {recipients!r}.")
        donor = donors[0]
        wrappers = get.wrappers(donor)
        recipient = recipients[0]
    parent, start, stop = donors._get_parent_and_start_stop_indices()
    assert parent is not None, repr(donors)
    parent.__setitem__(slice(start, stop + 1), recipients)
    if not wrappers:
        return
    for wrapper in wrappers:
        # bypass Wrapper._bind_component()
        # to avoid full-score update / traversal;
        # this works because one-to-one leaf replacement
        # including all (persistent) indicators
        # doesn't change score structure:
        donor._wrappers.remove(wrapper)
        wrapper._component = recipient
        recipient._wrappers.append(wrapper)
        context = wrapper._find_correct_effective_context()
        if context is not None:
            context._dependent_wrappers.append(wrapper)


def scale(argument, multiplier) -> None:
    r"""
    Scales mutation client by ``multiplier``.

    ..  container:: example

        Scales note duration by dot-generating multiplier:

        >>> staff = abjad.Staff("c'8 ( d'8 e'8 f'8 )")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.mutate.scale(staff[1], abjad.Multiplier(3, 2))
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

        >>> logical_tie = abjad.select(staff[0]).logical_tie()
        >>> logical_tie = abjad.mutate.scale(logical_tie, abjad.Multiplier(3, 2))
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

        >>> abjad.mutate.scale(container, abjad.Multiplier(3, 2))
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
                \times 4/5 {
                    \time 4/8
                    c'8
                    d'8
                    e'8
                    f'8
                    g'8
                }
            }

        >>> abjad.mutate.scale(tuplet, abjad.Multiplier(2))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \times 4/5 {
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

        >>> abjad.mutate.scale(note, abjad.Multiplier(1, 2))
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'16 * 1/2

    """
    if hasattr(argument, "_scale"):
        argument._scale(multiplier)
    else:
        assert isinstance(argument, Selection)
        for component in argument:
            component._scale(multiplier)


# TODO: add tests of tupletted notes and rests.
# TODO: add examples that show indicator handling.
# TODO: add example showing grace and after grace handling.
def split(argument, durations, cyclic=False):
    r"""
    Splits mutation client by ``durations``.

    ..  container:: example

        Splits leaves cyclically and ties split notes:

        >>> staff = abjad.Staff("c'1 d'1")
        >>> abjad.hairpin('p < f', staff[:])
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
                c'1
                \p
                \<
                d'1
                \f
            }

        >>> durations = [(3, 4)]
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
                c'2.
                \p
                ~
                c'4
                \<
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
                    ~
                }
                \context CustomVoice = "1"
                {
                    c'8
                    \<
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
        >>> abjad.override(voice_1).Stem.direction = abjad.Up
        >>> abjad.override(voice_1).Slur.direction = abjad.Up
        >>> container = abjad.Container(
        ...     [voice_1, voice_2],
        ...     simultaneous=True,
        ...     )
        >>> abjad.override(voice_2).Stem.direction = abjad.Down
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

    Returns list of selections.
    """
    components = argument
    if isinstance(components, Component):
        components = Selection(components)
    assert all(isinstance(_, Component) for _ in components)
    if not isinstance(components, Selection):
        components = Selection(components)
    durations = [Duration(_) for _ in durations]
    assert len(durations), repr(durations)
    total_component_duration = get.duration(components)
    total_split_duration = sum(durations)
    if cyclic:
        durations = Sequence(durations)
        durations = durations.repeat_to_weight(total_component_duration)
        durations = list(durations)
    elif total_split_duration < total_component_duration:
        final_offset = total_component_duration - sum(durations)
        durations.append(final_offset)
    elif total_component_duration < total_split_duration:
        weight = total_component_duration
        durations = Sequence(durations).truncate(weight=weight)
        durations = list(durations)
    # keep copy of durations to partition result components
    durations_copy = durations[:]
    total_split_duration = sum(durations)
    assert total_split_duration == total_component_duration
    result, shard = [], []
    offset_index = 0
    current_shard_duration = Duration(0)
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
        duration_ = get.duration(current_component)
        candidate_shard_duration = current_shard_duration + duration_
        # if current component would fill current shard exactly
        if candidate_shard_duration == next_split_point:
            shard.append(current_component)
            result.append(shard)
            shard = []
            current_shard_duration = Duration(0)
            offset_index += 1
        # if current component would exceed current shard
        elif next_split_point < candidate_shard_duration:
            local_split_duration = next_split_point
            local_split_duration -= current_shard_duration
            if isinstance(current_component, Leaf):
                leaf_split_durations = [local_split_duration]
                duration_ = get.duration(current_component)
                current_duration = duration_
                additional_required_duration = current_duration
                additional_required_duration -= local_split_duration
                split_durations = Sequence(durations)
                split_durations = split_durations.split(
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
                )
                shard.extend(leaf_shards)
                result.append(shard)
                offset_index += len(additional_durations)
            else:
                assert isinstance(current_component, Container)
                pair = _split_container_by_duration(
                    current_component,
                    local_split_duration,
                )
                left_list, right_list = pair
                shard.extend(left_list)
                result.append(shard)
                remaining_components.__setitem__(slice(0, 0), right_list)
            shard = []
            offset_index += 1
            current_shard_duration = Duration(0)
        # if current component would not fill current shard
        elif candidate_shard_duration < next_split_point:
            shard.append(current_component)
            duration_ = get.duration(current_component)
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
    result = Sequence(result).flatten(depth=-1)
    result = Selection(result).partition_by_durations(durations_copy, fill=enums.Exact)
    # return list of shards
    assert all(isinstance(_, Selection) for _ in result)
    return result


def swap(argument, container):
    r"""
    Swaps mutation client for empty ``container``.

    ..  container:: example

        Swaps containers for tuplet:

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.Container("c'4 d'4 e'4"))
        >>> staff.append(abjad.Container("d'4 e'4 f'4"))
        >>> abjad.attach(abjad.TimeSignature((3, 4)), staff[0][0])
        >>> leaves = abjad.select(staff).leaves()
        >>> abjad.hairpin('p < f', leaves)
        >>> measures = staff[:]
        >>> abjad.slur(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                {
                    \time 3/4
                    c'4
                    \p
                    \<
                    (
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

        >>> containers = staff[:]
        >>> tuplet = abjad.Tuplet((2, 3), [])
        >>> tuplet.denominator = 4
        >>> abjad.mutate.swap(containers, tuplet)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \times 4/6 {
                    \time 3/4
                    c'4
                    \p
                    \<
                    (
                    d'4
                    e'4
                    d'4
                    e'4
                    f'4
                    \f
                    )
                }
            }

    Returns none.
    """
    if isinstance(argument, Selection):
        donors = argument
    else:
        donors = Selection(argument)
    assert donors.are_contiguous_same_parent()
    assert isinstance(container, Container)
    assert not container, repr(container)
    donors._give_components_to_empty_container(container)
    # donors._give_dominant_spanners([container])
    donors._give_position_in_parent_to_container(container)


def transpose(argument, interval):
    r"""
    Transposes notes and chords in ``argument`` by ``interval``.

    ..  todo:: Move to abjad.pitch package.

    ..  container:: example

        Transposes notes and chords in staff:

        >>> staff = abjad.Staff()
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
    named_interval = NamedInterval(interval)
    for x in Iteration(argument).components((Note, Chord)):
        if isinstance(x, Note):
            old_written_pitch = x.note_head.written_pitch
            new_written_pitch = old_written_pitch.transpose(named_interval)
            x.note_head.written_pitch = new_written_pitch
        else:
            for note_head in x.note_heads:
                old_written_pitch = note_head.written_pitch
                new_written_pitch = old_written_pitch.transpose(named_interval)
                note_head.written_pitch = new_written_pitch


def wrap(argument, container):
    r"""
    Wraps mutation client in empty ``container``.

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
                \times 2/3 {
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

        >>> maker = abjad.NoteMaker()
        >>> notes = maker([0, 2, 4], [(1, 8)])
        >>> tuplet = abjad.Tuplet((2, 3), [])
        >>> abjad.mutate.wrap(notes, tuplet)
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \times 2/3 {
                c'8
                d'8
                e'8
            }

        (This usage merely substitutes for the tuplet initializer.)

    ..  container:: example

        Wraps leaves in container:

        >>> notes = [abjad.Note(n, (1, 8)) for n in range(8)]
        >>> staff = abjad.Staff(notes)
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
                \times 2/3 {
                    c'1
                }
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    cs'1
                }
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    d'1
                }
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
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
        >>> leaves = abjad.select(staff).leaves()
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
        >>> for component in abjad.iterate(staff).components():
        ...     time_signature = abjad.get.effective(component, prototype)
        ...     print(component, time_signature)
        ...
        <Staff{1}> 3/8
        Container("c'4 d'4 e'4 f'4") 3/8
        c'4 3/8
        d'4 3/8
        e'4 3/8
        f'4 3/8

    Returns none.
    """
    if not isinstance(container, Container) or 0 < len(container):
        raise Exception(f"must be empty container: {container!r}.")
    if isinstance(argument, Component):
        selection = Selection(argument)
    else:
        selection = argument
    assert isinstance(selection, Selection), repr(selection)
    parent, start, stop = selection._get_parent_and_start_stop_indices(
        ignore_before_after_grace=True
    )
    if not selection.are_contiguous_logical_voice(ignore_before_after_grace=True):
        message = "must be contiguous components in same logical voice:\n"
        message += f"   {selection!r}."
        raise Exception(message)
    container._components = list(selection)
    container[:]._set_parents(container)
    if parent is not None:
        parent._components.insert(start, container)
        container._set_parent(parent)
    for component in selection:
        for wrapper in component._wrappers:
            wrapper._effective_context = None
            wrapper._update_effective_context()
