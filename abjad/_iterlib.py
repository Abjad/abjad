import collections
import enum
import typing

from . import _getlib
from . import indicators as _indicators
from . import score as _score
from . import select as _select


def _coerce_exclude(exclude):
    if exclude is None:
        exclude = ()
    elif isinstance(exclude, str | enum.Enum):
        exclude = (exclude,)
    else:
        exclude = tuple(exclude)
    assert isinstance(exclude, tuple), repr(exclude)
    return exclude


def _get_leaf(argument, n: int = 0):
    if n not in (-1, 0, 1):
        message = "n must be -1, 0 or 1:\n"
        message += f"   {repr(n)}"
        raise Exception(message)
    if isinstance(argument, _score.Leaf):
        candidate = _get_sibling_with_graces(argument, n)
        if isinstance(candidate, _score.Leaf):
            return candidate
        return _getlib._get_leaf_from_leaf(argument, n)
    if 0 <= n:
        reverse = False
    else:
        reverse = True
        n = abs(n) - 1
    leaves = _public_iterate_leaves(argument, reverse=reverse)
    for i, leaf in enumerate(leaves):
        if i == n:
            return leaf
    return None


def _get_logical_tie_leaves(leaf):
    if _is_unpitched(leaf):
        return [leaf]
    leaves_before, leaves_after = [], []
    current_leaf = leaf
    while True:
        previous_leaf = _get_leaf(current_leaf, -1)
        if previous_leaf is None:
            break
        if _is_unpitched(previous_leaf):
            break
        if current_leaf._has_indicator(
            _indicators.RepeatTie
        ) or previous_leaf._has_indicator(_indicators.Tie):
            leaves_before.insert(0, previous_leaf)
        else:
            break
        current_leaf = previous_leaf
    current_leaf = leaf
    while True:
        next_leaf = _get_leaf(current_leaf, 1)
        if next_leaf is None:
            break
        if _is_unpitched(next_leaf):
            break
        if current_leaf._has_indicator(_indicators.Tie) or next_leaf._has_indicator(
            _indicators.RepeatTie
        ):
            leaves_after.append(next_leaf)
        else:
            break
        current_leaf = next_leaf
    leaves = leaves_before + [leaf] + leaves_after
    return leaves


def _is_obgc_nongrace_voice(argument):
    if (
        type(argument).__name__ == "Voice"
        and type(argument._parent).__name__ == "Container"
        and type(argument._parent[0]).__name__ == "OnBeatGraceContainer"
    ):
        return True
    return False


def _get_sibling_with_graces(component, n):
    assert n in (-1, 0, 1), repr(component, n)
    if n == 0:
        return component
    if component._parent is None:
        return None
    if component._parent.simultaneous:
        return None
    if (
        n == 1
        and getattr(component._parent, "_main_leaf", None)
        and component._parent._main_leaf._before_grace_container is component._parent
        and component is component._parent[-1]
    ):
        return component._parent._main_leaf
    # component is final leaf in obgc
    if (
        n == 1
        and component is component._parent[-1]
        and component._parent.__class__.__name__ == "OnBeatGraceContainer"
    ):
        return component._parent.get_first_nongrace_leaf()
    if (
        n == 1
        and getattr(component._parent, "_main_leaf", None)
        and component._parent._main_leaf._after_grace_container is component._parent
        and component is component._parent[-1]
    ):
        main_leaf = component._parent._main_leaf
        if main_leaf is main_leaf._parent[-1]:
            return None
        index = main_leaf._parent.index(main_leaf)
        return main_leaf._parent[index + 1]
    if n == 1 and getattr(component, "_after_grace_container", None):
        return component._after_grace_container[0]
    if (
        n == -1
        and getattr(component._parent, "_main_leaf", None)
        and component._parent._main_leaf._after_grace_container is component._parent
        and component is component._parent[0]
    ):
        return component._parent._main_leaf
    if (
        n == -1
        and getattr(component._parent, "_main_leaf", None)
        and component._parent._main_leaf._before_grace_container is component._parent
        and component is component._parent[0]
    ):
        main_leaf = component._parent._main_leaf
        if main_leaf is main_leaf._parent[0]:
            return None
        index = main_leaf._parent.index(main_leaf)
        return main_leaf._parent[index - 1]
    # component is first leaf in obgc nongrace voice
    if (
        n == -1
        and component is component._parent[0]
        and type(component._parent).__name__ == "Voice"
        and type(component._parent._parent).__name__ == "Container"
        and type(component._parent._parent[0]).__name__ == "OnBeatGraceContainer"
    ):
        obgc = component._parent._parent[0]
        return obgc[-1]
    if n == -1 and getattr(component, "_before_grace_container", None):
        return component._before_grace_container[-1]
    index = component._parent.index(component) + n
    if not (0 <= index < len(component._parent)):
        return None
    candidate = component._parent[index]
    if n == 1 and getattr(candidate, "_before_grace_container", None):
        return candidate._before_grace_container[0]
    if n == 1 and candidate.__class__.__name__ == "IndependentAfterGraceContainer":
        return candidate[0]
    if n == -1 and getattr(candidate, "_after_grace_container", None):
        return candidate._after_grace_container[-1]
    if n == -1 and candidate.__class__.__name__ == "IndependentAfterGraceContainer":
        return candidate[-1]
    return candidate


def _is_unpitched(leaf):
    if hasattr(leaf, "written_pitch"):
        return False
    if hasattr(leaf, "written_pitches"):
        return False
    return True


def _iterate_components(
    argument,
    prototype=None,
    *,
    exclude=None,
    do_not_iterate_grace_containers=None,
    grace=None,
    reverse=None,
):
    prototype = prototype or _score.Component
    before_grace_container = None
    after_grace_container = None
    exclude = _coerce_exclude(exclude)
    assert isinstance(exclude, tuple), repr(exclude)
    if grace is not False and isinstance(argument, _score.Leaf):
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
                or (grace is True and _getlib._get_grace_container(argument))
                or (grace is False and not _getlib._get_grace_container(argument))
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
                or (grace is True and _getlib._get_grace_container(argument))
                or (grace is False and not _getlib._get_grace_container(argument))
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
    assert isinstance(component, _score.Component), repr(component)
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
    argument,
    *,
    exclude=None,
    grace=None,
    nontrivial=None,
    pitched=None,
    reverse=None,
) -> typing.Iterator[_select.LogicalTie]:
    yielded_logical_ties = set()
    for leaf in _public_iterate_leaves(
        argument, exclude=exclude, grace=grace, pitched=pitched, reverse=reverse
    ):
        leaves = _get_logical_tie_leaves(leaf)
        if leaf is not leaves[0]:
            continue
        if (
            nontrivial is None
            or (nontrivial is True and not len(leaves) == 1)
            or (nontrivial is False and len(leaves) == 1)
        ):
            logical_tie = _select.LogicalTie(leaves)
            if logical_tie not in yielded_logical_ties:
                yielded_logical_ties.add(logical_tie)
                yield logical_tie


def _public_iterate_components(
    argument, prototype=None, *, exclude=None, grace=None, reverse=None
):
    if isinstance(argument, _score.Container):
        for component in _iterate_components(
            argument,
            prototype,
            exclude=exclude,
            do_not_iterate_grace_containers=False,
            grace=grace,
            reverse=reverse,
        ):
            yield component
    elif isinstance(argument, collections.abc.Iterable):
        if not reverse:
            for item in argument:
                generator = _public_iterate_components(
                    item,
                    prototype,
                    exclude=exclude,
                    grace=grace,
                    reverse=reverse,
                )
                yield from generator
        else:
            for item in reversed(argument):
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
            argument,
            prototype,
            exclude=exclude,
            do_not_iterate_grace_containers=True,
            grace=grace,
            reverse=reverse,
        ):
            yield component


def _public_iterate_leaves(
    argument,
    prototype=None,
    *,
    exclude=None,
    grace=None,
    pitched=None,
    reverse=None,
):
    prototype = prototype or _score.Leaf
    if pitched is True:
        prototype = (_score.Chord, _score.Note)
    elif pitched is False:
        prototype = (_score.MultimeasureRest, _score.Rest, _score.Skip)
    return _public_iterate_components(
        argument, prototype=prototype, exclude=exclude, grace=grace, reverse=reverse
    )


def _should_exclude(argument, exclude):
    assert isinstance(exclude, tuple)
    for string in exclude:
        if argument._has_indicator(string):
            return True
    return False
