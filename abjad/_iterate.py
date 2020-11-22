import collections
import typing

from . import _inspect, score
from .indicators.RepeatTie import RepeatTie
from .indicators.Tie import Tie


def _coerce_exclude(exclude):
    if exclude is None:
        exclude = ()
    elif isinstance(exclude, str):
        exclude = (exclude,)
    else:
        exclude = tuple(exclude)
    assert isinstance(exclude, tuple), repr(exclude)
    return exclude


def _is_unpitched(LEAF):
    if hasattr(LEAF, "written_pitch"):
        return False
    if hasattr(LEAF, "written_pitches"):
        return False
    return True


def _get_logical_tie_leaves(LEAF):
    if _is_unpitched(LEAF):
        return [LEAF]
    leaves_before, leaves_after = [], []
    current_leaf = LEAF
    while True:
        previous_leaf = _get_leaf(current_leaf, -1)
        if previous_leaf is None:
            break
        if _is_unpitched(previous_leaf):
            break
        if current_leaf._has_indicator(RepeatTie) or previous_leaf._has_indicator(Tie):
            leaves_before.insert(0, previous_leaf)
        else:
            break
        current_leaf = previous_leaf
    current_leaf = LEAF
    while True:
        next_leaf = _get_leaf(current_leaf, 1)
        if next_leaf is None:
            break
        if _is_unpitched(next_leaf):
            break
        if current_leaf._has_indicator(Tie) or next_leaf._has_indicator(RepeatTie):
            leaves_after.append(next_leaf)
        else:
            break
        current_leaf = next_leaf
    leaves = leaves_before + [LEAF] + leaves_after
    return leaves


def _iterate_components(
    client,
    prototype=None,
    *,
    exclude=None,
    do_not_iterate_grace_containers=None,
    grace=None,
    reverse=None,
):
    argument = client
    prototype = prototype or score.Component
    before_grace_container = None
    after_grace_container = None
    exclude = _coerce_exclude(exclude)
    assert isinstance(exclude, tuple), repr(exclude)
    if grace is not False and isinstance(argument, score.Leaf):
        before_grace_container = argument._before_grace_container
        after_grace_container = argument._after_grace_container
    if not reverse:
        if (
            not do_not_iterate_grace_containers
            and grace is not False
            and before_grace_container
        ):
            yield from _iterate_components(
                before_grace_container,
                prototype,
                do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                grace=grace,
                reverse=reverse,
            )
        if isinstance(argument, prototype):
            if (
                grace is None
                or (grace is True and _inspect._get_grace_container(argument))
                or (grace is False and not _inspect._get_grace_container(argument))
            ):
                if not _should_exclude(argument, exclude):
                    yield argument
        if (
            not do_not_iterate_grace_containers
            and grace is not False
            and after_grace_container
        ):
            yield from _iterate_components(
                after_grace_container,
                prototype,
                exclude=exclude,
                do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                grace=grace,
                reverse=reverse,
            )
        if isinstance(argument, collections.abc.Iterable):
            for item in argument:
                yield from _iterate_components(
                    item,
                    prototype,
                    exclude=exclude,
                    do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                    grace=grace,
                    reverse=reverse,
                )
    else:
        if (
            not do_not_iterate_grace_containers
            and grace is not False
            and after_grace_container
        ):
            yield from _iterate_components(
                after_grace_container,
                prototype,
                exclude=exclude,
                do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                grace=grace,
                reverse=reverse,
            )
        if isinstance(argument, prototype):
            if (
                grace is None
                or (grace is True and _inspect._get_grace_container(argument))
                or (grace is False and not _inspect._get_grace_container(argument))
            ):
                if not _should_exclude(argument, exclude):
                    yield argument
        if (
            not do_not_iterate_grace_containers
            and grace is not False
            and before_grace_container
        ):
            yield from _iterate_components(
                before_grace_container,
                prototype,
                exclude=exclude,
                do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                grace=grace,
                reverse=reverse,
            )
        if isinstance(argument, collections.abc.Iterable):
            for item in reversed(argument):
                yield from _iterate_components(
                    item,
                    prototype,
                    exclude=exclude,
                    do_not_iterate_grace_containers=do_not_iterate_grace_containers,
                    grace=grace,
                    reverse=reverse,
                )


def _iterate_descendants(component, cross_offset=None):
    assert isinstance(component, score.Component), repr(component)
    if component is None:
        components = ()
    else:
        generator = _public_iterate_components(component)
        components = list(generator)
    result = []
    if cross_offset is None:
        result = components
    else:
        for component in components:
            append_x = True
            if not (
                component._get_timespan().start_offset < cross_offset
                and cross_offset < component._get_timespan().stop_offset
            ):
                append_x = False
            if append_x:
                result.append(component)
    return tuple(result)


def _iterate_logical_ties(
    ARGUMENT,
    *,
    exclude=None,
    grace=None,
    nontrivial=None,
    pitched=None,
    reverse=None,
    wrapper_class=None,
) -> typing.Generator:
    yielded_logical_ties = set()
    for leaf in _public_iterate_leaves(
        ARGUMENT, exclude=exclude, grace=grace, pitched=pitched, reverse=reverse
    ):
        leaves = _get_logical_tie_leaves(leaf)
        # logical_tie = LogicalTie(leaves)
        # if leaf is not logical_tie.head:
        if leaf is not leaves[0]:
            continue
        if (
            nontrivial is None
            or (nontrivial is True and not len(leaves) == 1)
            or (nontrivial is False and len(leaves) == 1)
        ):
            # if logical_tie not in yielded_logical_ties:
            if wrapper_class is not None:
                leaves = wrapper_class(leaves)
            if leaves not in yielded_logical_ties:
                # yielded_logical_ties.add(logical_tie)
                yielded_logical_ties.add(leaves)
                # yield logical_tie
                yield leaves


def _get_leaf(ARGUMENT, n: int = 0):
    if n not in (-1, 0, 1):
        message = "n must be -1, 0 or 1:\n"
        message += f"   {repr(n)}"
        raise Exception(message)
    if isinstance(ARGUMENT, score.Leaf):
        candidate = _inspect._get_sibling_with_graces(ARGUMENT, n)
        if isinstance(candidate, score.Leaf):
            return candidate
        return _inspect._get_leaf_from_leaf(ARGUMENT, n)
    if 0 <= n:
        reverse = False
    else:
        reverse = True
        n = abs(n) - 1
    leaves = _public_iterate_leaves(ARGUMENT, reverse=reverse)
    for i, leaf in enumerate(leaves):
        if i == n:
            return leaf
    return None


def _public_iterate_components(
    ARGUMENT, prototype=None, *, exclude=None, grace=None, reverse=None
):
    if isinstance(ARGUMENT, score.Container):
        for component in _iterate_components(
            ARGUMENT,
            prototype,
            exclude=exclude,
            do_not_iterate_grace_containers=False,
            grace=grace,
            reverse=reverse,
        ):
            yield component
    elif isinstance(ARGUMENT, collections.abc.Iterable):
        if not reverse:
            for item in ARGUMENT:
                generator = _public_iterate_components(
                    item,
                    prototype,
                    exclude=exclude,
                    grace=grace,
                    reverse=reverse,
                )
                yield from generator
        else:
            for item in reversed(ARGUMENT):
                generator = _public_iterate_components(
                    item,
                    prototype,
                    exclude=exclude,
                    grace=grace,
                    reverse=reverse,
                )
                yield from generator
    else:
        for component in _iterate_components(
            ARGUMENT,
            prototype,
            exclude=exclude,
            do_not_iterate_grace_containers=True,
            grace=grace,
            reverse=reverse,
        ):
            yield component


def _public_iterate_leaves(
    ARGUMENT,
    prototype=None,
    *,
    exclude=None,
    grace=None,
    pitched=None,
    reverse=None,
):
    prototype = prototype or score.Leaf
    if pitched is True:
        prototype = (score.Chord, score.Note)
    elif pitched is False:
        prototype = (score.MultimeasureRest, score.Rest, score.Skip)
    return _public_iterate_components(
        ARGUMENT, prototype=prototype, exclude=exclude, grace=grace, reverse=reverse
    )


def _should_exclude(argument, exclude):
    assert isinstance(exclude, tuple)
    for string in exclude:
        if argument._has_indicator(string):
            return True
    return False
