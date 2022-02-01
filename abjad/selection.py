import abc
import collections.abc
import itertools
import operator
import typing

from . import _inspect, _iterate
from . import bind as _bind
from . import cyclictuple as _cyclictuple
from . import duration as _duration
from . import enums as _enums
from . import format as _format
from . import indicators as _indicators
from . import math as _math
from . import parentage as _parentage
from . import pattern as _pattern
from . import pitch as _pitch
from . import ratio as _ratio
from . import score as _score
from . import sequence as _sequence
from . import typings as _typings


class Inequality:
    """
    Inequality.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Inequalities"

    __slots__ = ("_operator_string", "_operator_function")

    _operator_strings = ("!=", "<", "<=", "==", ">", ">=")

    ### INITIALIZER ###

    def __init__(self, operator_string="<"):
        assert operator_string in self._operator_strings
        self._operator_string = operator_string
        self._operator_function = {
            "!=": operator.ne,
            "<": operator.lt,
            "<=": operator.le,
            "==": operator.eq,
            ">": operator.gt,
            ">=": operator.ge,
        }[self._operator_string]

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, argument):
        """
        Calls inequality on ``argument``.

        Returns true or false.
        """
        raise NotImplementedError

    def __hash__(self) -> int:
        """
        Hashes inequality.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PUBLIC PROPERTIES ###

    @property
    def operator_string(self) -> str:
        """
        Gets operator string.

        Returns string.
        """
        return self._operator_string


class DurationInequality(Inequality):
    """
    Duration inequality.

    ..  container:: example

        >>> inequality = abjad.DurationInequality('<', (3, 4))
        >>> string = abjad.storage(inequality)
        >>> print(string)
        abjad.DurationInequality(
            operator_string='<',
            duration=abjad.Duration(3, 4),
            )

        >>> inequality(abjad.Duration(1, 2))
        True

        >>> inequality(abjad.Note("c'4"))
        True

        >>> inequality(abjad.Container("c'1 d'1"))
        False

    ..  container:: example

        Has clean interpreter representation:

        >>> abjad.DurationInequality('<', (3, 4))
        DurationInequality(operator_string='<', duration=Duration(3, 4))

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Inequalities"

    __slots__ = ("_duration", "_preprolated")

    ### INITIALIZER ###

    def __init__(
        self,
        operator_string: str = "<",
        duration=None,
        *,
        preprolated: bool = None,
    ) -> None:
        Inequality.__init__(self, operator_string=operator_string)
        if duration is None:
            duration = _math.Infinity()
        infinities = (_math.Infinity(), _math.NegativeInfinity())
        if duration not in infinities:
            duration = _duration.Duration(duration)
            assert 0 <= duration
        self._duration = duration
        self._preprolated = preprolated

    ### SPECIAL METHODS ###

    def __call__(self, argument) -> bool:
        """
        Calls inequality on ``argument``.
        """
        if self.preprolated and hasattr(argument, "_get_preprolated_duration"):
            duration = argument._get_preprolated_duration()
        else:
            try:
                duration = _duration.Duration(argument)
            except Exception:
                duration = _inspect._get_duration(argument)
        return self._operator_function(duration, self.duration)

    def __eq__(self, argument) -> bool:
        """
        Compares ``operator_string``, ``duration``.
        """
        if isinstance(argument, type(self)):
            return (
                self.operator_string == argument.operator_string
                and self.duration == argument.duration
            )
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self) -> _duration.Duration:
        """
        Gets duration.
        """
        return self._duration

    @property
    def preprolated(self) -> typing.Optional[bool]:
        """
        Is true when inequality evaluates preprolated duration.
        """
        return self._preprolated


class LengthInequality(Inequality):
    """
    Length inequality.

    ..  container:: example

        >>> inequality = abjad.LengthInequality('<', 4)
        >>> string = abjad.storage(inequality)
        >>> print(string)
        abjad.LengthInequality(
            operator_string='<',
            length=4,
            )

        >>> inequality([1, 2, 3])
        True

        >>> inequality([1, 2, 3, 4])
        False

        >>> inequality([1, 2, 3, 4, 5])
        False

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Inequalities"

    __slots__ = ("_length",)

    ### INITIALIZER ###

    def __init__(self, operator_string="<", length=None):
        Inequality.__init__(self, operator_string=operator_string)
        if length is None:
            length = _math.Infinity()
        assert 0 <= length
        infinities = (_math.Infinity(), _math.NegativeInfinity())
        if length not in infinities:
            length = int(length)
        self._length = length

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        """
        Calls inequality on ``argument``.

        Returns true or false.
        """
        return self._operator_function(len(argument), self.length)

    def __eq__(self, argument) -> bool:
        """
        Compares ``operator_string``, ``length``.
        """
        if isinstance(argument, type(self)):
            return (
                self.operator_string == argument.operator_string
                and self.length == argument.length
            )
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        """
        Gets length.

        Returns integer.
        """
        return self._length


class PitchInequality:
    """
    Pitch inequality.

    ..  container:: example

        >>> inequality = abjad.PitchInequality('&', 'C4 E4')
        >>> string = abjad.storage(inequality)
        >>> print(string)
        abjad.PitchInequality(
            operator_string='&',
            pitches=abjad.PitchSet(
                [0, 4]
                ),
            )

        >>> inequality(abjad.Staff("d'8 e' f' g'"))
        True

        >>> inequality(abjad.Staff("e'8 f' g' a'"))
        True

        >>> inequality(abjad.Staff("f'8 g' a' b'"))
        False

    .. note:: only intersection currently implemented.

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Inequalities"

    __slots__ = ("_operator_string", "_pitches")

    _set_theoretic_operator_strings = ("&", "|", "^")

    ### INITIALIZER ###

    def __init__(self, operator_string="&", pitches=None):
        assert operator_string in self._set_theoretic_operator_strings
        self._operator_string = operator_string
        # only intersection is currently implemented
        if not isinstance(pitches, collections.abc.Iterable):
            pitches = [pitches]
        pitches = _pitch.PitchSet(items=pitches, item_class=_pitch.NumberedPitch)
        self._pitches = pitches

    ### SPECIAL METHODS ###

    def __call__(self, argument) -> bool:
        """
        Calls inequality on ``argument``.
        """
        if not self.pitches:
            return False
        selection = Selection(argument)
        pitch_set = _pitch.PitchSet.from_selection(
            selection, item_class=_pitch.NumberedPitch
        )
        if self.operator_string == "&":
            return bool(self.pitches.intersection(pitch_set))
        else:
            raise NotImplementedError(f"implement {self.operator_string!r}.")

    def __eq__(self, argument) -> bool:
        """
        Compares ``operator_string``, ``pitches``.
        """
        if isinstance(argument, type(self)):
            return (
                self.operator_string == argument.operator_string
                and self.pitches == argument.pitches
            )
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def operator_string(self):
        """
        Gets operator string.

        Returns string.
        """
        return self._operator_string

    @property
    def pitches(self):
        """
        Gets pitches.

        Returns numbered pitch set.
        """
        return self._pitches


class Selection(collections.abc.Sequence):
    r"""
    Selection of items (components / or other selections).

    ..  container:: example

        >>> string = r"c'4 \times 2/3 { d'8 r8 e'8 } r16 f'16 g'8 a'4"
        >>> staff = abjad.Staff(string)
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.show(staff) # doctest: +SKIP

        >>> result = abjad.select(staff).runs()

        >>> for item in result:
        ...     item
        ...
        Selection([Note("c'4"), Note("d'8")])
        Selection([Note("e'8")])
        Selection([Note("f'16"), Note("g'8"), Note("a'4")])

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Selections"

    __slots__ = ("_items", "_previous")

    ### INITIALIZER ###

    def __init__(self, items=None, previous=None):
        if items is None:
            items = []
        if isinstance(items, _score.Component):
            items = [items]
        items = tuple(items)
        self._check(items)
        self._items = tuple(items)
        self._previous = previous

    ### SPECIAL METHODS ###

    def __add__(self, argument) -> "Selection":
        r"""
        Cocatenates ``argument`` to selection.

        ..  container:: example

            Adds selections:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).autoBeaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> left = abjad.select(staff).leaves()[:2]
                >>> right = abjad.select(staff).leaves()[-2:]
                >>> result = left + right

                >>> for item in result:
                ...     item
                ...
                Note("c'8")
                Rest('r8')
                Note("g'8")
                Note("a'8")

        """
        assert isinstance(argument, collections.abc.Iterable)
        items = self.items + tuple(argument)
        return type(self)(items=items)

    def __contains__(self, argument) -> bool:
        """
        Is true when ``argument`` is in selection.
        """
        return argument in self.items

    def __eq__(self, argument) -> bool:
        """
        Is true when selection and ``argument`` are of the same type
        and when items in selection equal item in ``argument``.
        """
        if isinstance(argument, type(self)):
            return self.items == argument.items
        elif isinstance(argument, collections.abc.Sequence):
            return self.items == tuple(argument)
        return False

    def __getitem__(self, argument):
        """
        Gets item, slice or pattern ``argument`` in selection.

        Returns a single item when ``argument`` is an integer.

        Returns new selection when ``argument`` is a slice.
        """
        result = self.items.__getitem__(argument)
        if isinstance(result, tuple):
            result = type(self)(result, previous=self._previous)
        return result

    def __getstate__(self) -> dict:
        """
        Gets state of selection.
        """
        if hasattr(self, "__dict__"):
            state = vars(self).copy()
        else:
            state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, "__slots__", ()):
                try:
                    state[slot] = getattr(self, slot)
                except AttributeError:
                    pass
        return state

    def __hash__(self) -> int:
        """
        Hashes selection.
        """
        return hash(self.__class__.__name__ + str(self))

    def __len__(self) -> int:
        """
        Gets number of items in selection.
        """
        return len(self.items)

    def __radd__(self, argument) -> "Selection":
        """
        Concatenates selection to ``argument``.
        """
        assert isinstance(argument, collections.abc.Iterable)
        items = tuple(argument) + self.items
        return type(self)(items=items)

    def __repr__(self) -> str:
        """
        Gets interpreter representation of selection.
        """
        return _format.get_repr(self)

    def __setstate__(self, state) -> None:
        """
        Sets state of selection.
        """
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE METHODS ###

    def _attach_tie_to_leaves(self):
        for leaf in self[:-1]:
            _bind.detach(_indicators.Tie, leaf)
            _bind.attach(_indicators.Tie(), leaf)

    @staticmethod
    def _check(items):
        for item in items:
            if not isinstance(item, (_score.Component, Selection)):
                message = "components / selections only:\n"
                message += f"   {items!r}"
                raise TypeError(message)

    @classmethod
    def _components(
        class_,
        argument,
        prototype=None,
        *,
        exclude=None,
        grace=None,
        head=None,
        tail=None,
        trim=None,
    ):
        prototype = prototype or _score.Component
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        result = []
        generator = _iterate._public_iterate_components(
            argument, prototype, exclude=exclude, grace=grace
        )
        components = list(generator)
        if components:
            if trim in (True, _enums.Left):
                components = Selection._trim_subresult(components, trim)
            if head is not None:
                components = Selection._head_filter_subresult(components, head)
            if tail is not None:
                components = Selection._tail_filter_subresult(components, tail)
            result.extend(components)
        return class_(result)

    def _copy(self):
        assert self.are_contiguous_logical_voice()
        new_components = []
        for component in self:
            if isinstance(component, _score.Container):
                new_component = component._copy_with_children()
            else:
                new_component = component.__copy__()
            new_components.append(new_component)
        new_components = type(self)(new_components)
        return new_components

    def _get_component(self, prototype=None, n=0, recurse=True):
        prototype = prototype or (_score.Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        if 0 <= n:
            if recurse:
                components = _iterate._public_iterate_components(self, prototype)
            else:
                components = self.items
            for i, x in enumerate(components):
                if i == n:
                    return x
        else:
            if recurse:
                components = _iterate._public_iterate_components(
                    self, prototype, reverse=True
                )
            else:
                components = reversed(self.items)
            for i, x in enumerate(components):
                if i == abs(n) - 1:
                    return x

    def _get_format_specification(self):
        values = []
        if self.items:
            values = [list(self.items)]
        return _format.FormatSpecification(storage_format_args_values=values)

    def _get_offset_lists(self):
        start_offsets, stop_offsets = [], []
        for component in self:
            start_offsets.append(component._get_timespan().start_offset)
            stop_offsets.append(component._get_timespan().stop_offset)
        return start_offsets, stop_offsets

    def _get_parent_and_start_stop_indices(self, ignore_before_after_grace=None):
        assert self.are_contiguous_same_parent(
            ignore_before_after_grace=ignore_before_after_grace
        )
        if self:
            first, last = self[0], self[-1]
            parent = first._parent
            if parent is not None:
                first_index = parent.index(first)
                last_index = parent.index(last)
                return parent, first_index, last_index
        return None, None, None

    def _get_preprolated_duration(self):
        return sum(component._get_preprolated_duration() for component in self)

    def _give_components_to_empty_container(self, container):
        """
        Not composer-safe.
        """
        assert self.are_contiguous_same_parent()
        assert isinstance(container, _score.Container)
        assert not container
        components = []
        for component in self:
            components.extend(getattr(component, "components", ()))
        container._components.extend(components)
        container[:]._set_parents(container)

    def _give_position_in_parent_to_container(self, container):
        """
        Not composer-safe.
        """
        assert self.are_contiguous_same_parent()
        assert isinstance(container, _score.Container)
        parent, start, stop = self._get_parent_and_start_stop_indices()
        if parent is not None:
            parent._components.__setitem__(slice(start, start), [container])
            container._set_parent(parent)
            self._set_parents(None)

    @staticmethod
    def _head_filter_subresult(result, head):
        result_ = []
        for item in result:
            if isinstance(item, _score.Component):
                leaves = _iterate._get_logical_tie_leaves(item)
                if head == (item is leaves[0]):
                    result_.append(item)
                else:
                    pass
            elif isinstance(item, Selection):
                if not all(isinstance(_, _score.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    leaves = _iterate._get_logical_tie_leaves(component)
                    if head == leaves[0]:
                        selection.append(item)
                    else:
                        pass
                selection = Selection(selection)
                result_.append(selection)
            else:
                raise TypeError(item)
        assert isinstance(result_, list), repr(result_)
        return Selection(result_)

    @staticmethod
    def _immediately_precedes(component_1, component_2, ignore_before_after_grace=None):
        successors = []
        current = component_1
        # do not include OnBeatGraceContainer here because
        # OnBeatGraceContainer is a proper container
        grace_prototype = (_score.AfterGraceContainer, _score.BeforeGraceContainer)
        while current is not None:
            sibling = _inspect._get_sibling_with_graces(current, 1)
            while (
                ignore_before_after_grace
                and sibling is not None
                and isinstance(sibling._parent, grace_prototype)
            ):
                sibling = _inspect._get_sibling_with_graces(sibling, 1)
            if sibling is None:
                current = current._parent
            else:
                descendants = sibling._get_descendants_starting_with()
                successors = descendants
                break
        return component_2 in successors

    @staticmethod
    def _is_immediate_child_of_outermost_voice(component):
        parentage = _parentage.Parentage(component)
        context = parentage.get(_score.Voice, -1) or parentage.get(_score.Context)
        if context is not None:
            return parentage.component._parent is context
        return None

    # TODO: remove this in favor of the abjad.iterpitches module;
    #       force users to initialize pitch segments expicitly after iteration.
    def _pitch_segment(self) -> _pitch.PitchSegment:
        pitches = []
        for leaf in _iterate._public_iterate_leaves(self, pitched=True):
            try:
                pitches.extend(leaf.written_pitches)
            except AttributeError:
                pass
            try:
                pitches.append(leaf.written_pitch)
            except AttributeError:
                pass
        return _pitch.PitchSegment(items=pitches, item_class=_pitch.NamedPitch)

    def _set_parents(self, new_parent):
        """
        Not composer-safe.
        """
        for component in self.items:
            component._set_parent(new_parent)

    @staticmethod
    def _tail_filter_subresult(result, tail):
        result_ = []
        for item in result:
            if isinstance(item, _score.Component):
                leaves = _iterate._get_logical_tie_leaves(item)
                if tail == (item is leaves[-1]):
                    result_.append(item)
                else:
                    pass
            elif isinstance(item, Selection):
                if not all(isinstance(_, _score.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    leaves = _iterate._get_logical_tie_leaves(component)
                    if tail == leaves[-1]:
                        selection.append(item)
                    else:
                        pass
                selection = Selection(selection)
                result_.append(selection)
            else:
                raise TypeError(item)
        assert isinstance(result_, list), repr(result_)
        return Selection(result_)

    @staticmethod
    def _trim_subresult(result, trim):
        assert trim in (True, _enums.Left)
        prototype = (_score.MultimeasureRest, _score.Rest, _score.Skip)
        result_ = []
        found_good_component = False
        for item in result:
            if isinstance(item, _score.Component):
                if not isinstance(item, prototype):
                    found_good_component = True
            elif isinstance(item, Selection):
                if not all(isinstance(_, _score.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    if not isinstance(component, prototype):
                        found_good_component = True
                    if found_good_component:
                        selection.append(component)
                item = Selection(selection)
            else:
                raise TypeError(item)
            if found_good_component:
                result_.append(item)
        if trim is _enums.Left:
            result = Selection(result_)
        else:
            result__ = []
            found_good_component = False
            for item in reversed(result_):
                if isinstance(item, _score.Component):
                    if not isinstance(item, prototype):
                        found_good_component = True
                elif isinstance(item, Selection):
                    if not all(isinstance(_, _score.Component) for _ in item):
                        raise NotImplementedError(item)
                    selection = []
                    for component in reversed(item):
                        if not isinstance(component, prototype):
                            found_good_component = True
                        if found_good_component:
                            selection.insert(0, component)
                    item = Selection(selection)
                else:
                    raise TypeError(item)
                if found_good_component:
                    result__.insert(0, item)
            assert isinstance(result__, list), repr(result__)
            result = Selection(result__)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def items(self) -> typing.Tuple:
        """
        Gets items.

        ..  container:: example

            >>> abjad.Staff("c'4 d'4 e'4 f'4")[:].items
            (Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4"))

        """
        return self._items

    ### PUBLIC METHODS ###

    def are_contiguous_logical_voice(
        self, prototype=None, *, ignore_before_after_grace=None
    ) -> bool:
        r"""
        Is true when items in selection are contiguous components in the
        same logical voice.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> staff[:].are_contiguous_logical_voice()
            True

            >>> selection = staff[:1] + staff[-1:]
            >>> selection.are_contiguous_logical_voice()
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
            Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])

            >>> voice[:].are_contiguous_logical_voice()
            False

            >>> voice[:].are_contiguous_logical_voice(
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
            Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])

            >>> voice[:].are_contiguous_logical_voice()
            False

            >>> voice[:].are_contiguous_logical_voice(
            ...     ignore_before_after_grace=True
            ... )
            True

        """
        if not isinstance(self, collections.abc.Iterable):
            return False
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
        first_parentage = _parentage.Parentage(first)
        first_logical_voice = first_parentage.logical_voice()
        first_root = first_parentage.root
        previous = first
        for current in self[1:]:
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
                if not self._immediately_precedes(
                    previous,
                    current,
                    ignore_before_after_grace=ignore_before_after_grace,
                ):
                    return False
            previous = current
        return True

    def are_contiguous_same_parent(
        self, prototype=None, *, ignore_before_after_grace=None
    ) -> bool:
        r"""
        Is true when items in selection are all contiguous components in
        the same parent.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> staff[:].are_contiguous_same_parent()
            True

            >>> selection = staff[:1] + staff[-1:]
            >>> selection.are_contiguous_same_parent()
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
            Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])

            >>> voice[:].are_contiguous_same_parent()
            False

            >>> voice[:].are_contiguous_same_parent(
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
            Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])

            >>> voice[:].are_contiguous_same_parent()
            False

            >>> voice[:].are_contiguous_same_parent(
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
            if not self._immediately_precedes(
                previous,
                current,
                ignore_before_after_grace=ignore_before_after_grace,
            ):
                strictly_contiguous = False
            if current._parent is not None and (
                not same_parent or not strictly_contiguous
            ):
                return False
            previous = current
        return True

    def are_leaves(self) -> bool:
        """
        Is true when items in selection are all leaves.

        ..  container:: example

            >>> abjad.Staff("c'4 d'4 e'4 f'4")[:].are_leaves()
            True

        """
        return all(isinstance(_, _score.Leaf) for _ in self)

    def are_logical_voice(self, prototype=None) -> bool:
        """
        Is true when items in selection are all components in the same
        logical voice.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> staff[:].are_logical_voice()
            True

            >>> selection = staff[:1] + staff[-1:]
            >>> selection.are_logical_voice()
            True

        """
        return _inspect._are_logical_voice(self, prototype=prototype)

    def chord(
        self, n: int, *, exclude: _typings.Strings = None, grace: bool = None
    ) -> _score.Chord:
        r"""
        Selects chord ``n``.

        ..  container:: example

            Selects chord -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).chord(-1)
            >>> result
            Chord("<fs' gs'>16")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'green
                            <fs' gs'>16
                        }
                    }
                >>

        """
        return self.chords(exclude=exclude, grace=grace)[n]

    def chords(
        self, *, exclude: _typings.Strings = None, grace: bool = None
    ) -> "Selection":
        r"""
        Selects chords.

        ..  container:: example

            Selects chords:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).chords()
            >>> for item in result:
            ...     item
            ...
            Chord("<a'' b''>16")
            Chord("<d' e'>4")
            Chord("<d' e'>16")
            Chord("<a'' b''>16")
            Chord("<e' fs'>4")
            Chord("<e' fs'>16")
            Chord("<a'' b''>16")
            Chord("<fs' gs'>4")
            Chord("<fs' gs'>16")

            >>> abjad.label.by_selector(result, True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            r16
                            bf'16
                            \abjad-color-music #'red
                            <a'' b''>16
                            c'16
                            \abjad-color-music #'blue
                            <d' e'>4
                            ~
                            \abjad-color-music #'red
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            r16
                            bf'16
                            \abjad-color-music #'blue
                            <a'' b''>16
                            d'16
                            \abjad-color-music #'red
                            <e' fs'>4
                            ~
                            \abjad-color-music #'blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            r16
                            bf'16
                            \abjad-color-music #'red
                            <a'' b''>16
                            e'16
                            \abjad-color-music #'blue
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'red
                            <fs' gs'>16
                        }
                    }
                >>

        """
        return self.components(_score.Chord, exclude=exclude, grace=grace)

    def components(
        self,
        prototype=None,
        *,
        exclude: _typings.Strings = None,
        grace: bool = None,
        reverse: bool = None,
    ) -> "Selection":
        r"""
        Selects components.

        ..  container:: example

            Selects notes:

            >>> staff = abjad.Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 r4 g'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).components(abjad.Note)
            >>> for item in result:
            ...     item
            ...
            Note("c'4")
            Note("d'8")
            Note("d'16")
            Note("e'16")
            Note("e'8")
            Note("g'8")

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'4
                    \abjad-color-music #'blue
                    d'8
                    ~
                    \abjad-color-music #'red
                    d'16
                    \abjad-color-music #'blue
                    e'16
                    ~
                    \abjad-color-music #'red
                    e'8
                    r4
                    \abjad-color-music #'blue
                    g'8
                }

        ..  container:: example

            Selects both main notes and graces when ``grace=None``:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).components(
            ...     abjad.Leaf,
            ...     grace=None,
            ...     )

            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Note("cf''16")
            Note("bf'16")
            Note("d'8")
            Note("af'16")
            Note("gf'16")
            Note("e'8")
            Note("f'8")

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \grace {
                        \abjad-color-music #'blue
                        cf''16
                        \abjad-color-music #'red
                        bf'16
                    }
                    \abjad-color-music #'blue
                    \afterGrace
                    d'8
                    {
                        \abjad-color-music #'red
                        af'16
                        \abjad-color-music #'blue
                        gf'16
                    }
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }

        ..  container:: example

            Excludes grace notes when ``grace=False``:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).components(
            ...     abjad.Leaf,
            ...     grace=False,
            ...     )

            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'8")

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \grace {
                        cf''16
                        bf'16
                    }
                    \abjad-color-music #'blue
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }

        ..  container:: example

            Selects only grace notes when ``grace=True``:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).components(
            ...     abjad.Leaf,
            ...     grace=True,
            ...     )

            >>> for item in result:
            ...     item
            ...
            Note("cf''16")
            Note("bf'16")
            Note("af'16")
            Note("gf'16")

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \grace {
                        \abjad-color-music #'red
                        cf''16
                        \abjad-color-music #'blue
                        bf'16
                    }
                    \afterGrace
                    d'8
                    {
                        \abjad-color-music #'red
                        af'16
                        \abjad-color-music #'blue
                        gf'16
                    }
                    e'8
                    f'8
                }

        """
        generator = _iterate._public_iterate_components(
            self, prototype=prototype, exclude=exclude, grace=grace, reverse=reverse
        )
        return type(self)(generator, previous=self._previous)

    def exclude(self, indices: typing.Sequence[int], period: int = None) -> "Selection":
        r"""
        Gets patterned items.

        ..  container:: example

            Excludes every other leaf:

            >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves().exclude([0], 2)
            >>> for item in result:
            ...     item
            ...
            Note("d'8")
            Note("e'8")
            Note("e'8")
            Note("f'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \abjad-color-music #'red
                    d'8
                    ~
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    ~
                    e'8
                    ~
                    \abjad-color-music #'red
                    e'8
                    r8
                    \abjad-color-music #'blue
                    f'8
                }

        ..  container:: example

            Excludes every other logical tie:

            >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> selection = abjad.select(staff).logical_ties(pitched=True)
            >>> result = selection.exclude([0], 2)
            >>> for item in result:
            ...     item
            ...
            LogicalTie([Note("d'8"), Note("d'8")])
            LogicalTie([Note("f'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \abjad-color-music #'red
                    d'8
                    ~
                    \abjad-color-music #'red
                    d'8
                    e'8
                    ~
                    e'8
                    ~
                    e'8
                    r8
                    \abjad-color-music #'blue
                    f'8
                }

        ..  container:: example

            Excludes note 1 (or nothing) in each pitched logical tie:

            >>> staff = abjad.Staff(r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties(pitched=True)
            >>> result = [abjad.select(_).leaves().exclude([1]) for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])
            Selection([Note("d'8")])
            Selection([Note("e'8"), Note("e'8")])
            Selection([Note("f'8")])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    d'8
                    ~
                    d'8
                    \abjad-color-music #'red
                    e'8
                    ~
                    e'8
                    ~
                    \abjad-color-music #'red
                    e'8
                    r8
                    \abjad-color-music #'blue
                    f'8
                }

        """
        pattern = _pattern.Pattern(indices, period=period, inverted=True)
        pattern = pattern.advance(self._previous)
        self._previous = None
        items = _sequence.Sequence(self.items).retain_pattern(pattern)
        result = type(self)(items, previous=self._previous)
        return result

    def filter(self, predicate=None) -> "Selection":
        r"""
        Filters selection by ``predicate``.

        ..  container:: example

            Selects runs with duration equal to 2/8:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> inequality = abjad.DurationInequality('==', (2, 8))
            >>> result = abjad.select(staff).runs().filter(inequality)
            >>> for item in result:
            ...     item
            ...
            Selection([Note("d'8"), Note("e'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        """
        if predicate is None:
            return type(self)(self)
        return type(self)([_ for _ in self if predicate(_)])

    def filter_duration(
        self,
        operator,
        duration: _typings.DurationTyping,
        *,
        preprolated: bool = None,
    ) -> "Selection":
        r"""
        Filters selection by ``operator`` and ``duration``.

        ..  container:: example

            Selects runs with duration equal to 2/8:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).runs()
            >>> result = result.filter_duration('==', (2, 8))
            >>> for item in result:
            ...     item
            ...
            Selection([Note("d'8"), Note("e'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        ..  container:: example

            Selects runs with duration less than 3/8:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).runs()
            >>> result = result.filter_duration('<', (3, 8))
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])
            Selection([Note("d'8"), Note("e'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        """
        inequality = DurationInequality(operator, duration, preprolated=preprolated)
        return self.filter(inequality)

    def filter_length(self, operator, length: int) -> "Selection":
        r"""
        Filters selection by ``operator`` and ``length``.

        ..  container:: example

            Selects notes runs with length greater than 1:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).runs().filter_length('>', 1)
            >>> for item in result:
            ...     item
            ...
            Selection([Note("d'8"), Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    r8
                    \abjad-color-music #'blue
                    f'8
                    \abjad-color-music #'blue
                    g'8
                    \abjad-color-music #'blue
                    a'8
                }

        ..  container:: example

            Selects runs with length less than 3:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).runs().filter_length('<', 3)
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])
            Selection([Note("d'8"), Note("e'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        """
        return self.filter(LengthInequality(operator, length))

    def filter_pitches(self, operator, pitches) -> "Selection":
        r"""
        Filters selection by ``operator`` and ``pitches``.

        ..  container:: example

            Selects leaves with pitches intersecting C4:

            >>> staff = abjad.Staff("c'8 d'8 ~ d'8 e'8")
            >>> abjad.setting(staff).autoBeaming = False
            >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")

            >>> result = abjad.select(staff).leaves()
            >>> result = result.filter_pitches('&', 'C4')
            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Chord("<c' e' g'>8")
            Chord("<c' e' g'>4")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    d'8
                    ~
                    d'8
                    e'8
                    r8
                    \abjad-color-music #'blue
                    <c' e' g'>8
                    ~
                    \abjad-color-music #'red
                    <c' e' g'>4
                }

        ..  container:: example

            Selects leaves with pitches intersecting C4 or E4:

            >>> staff = abjad.Staff("c'8 d'8 ~ d'8 e'8")
            >>> abjad.setting(staff).autoBeaming = False
            >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")

            >>> result = abjad.select(staff).leaves()
            >>> result = result.filter_pitches('&', 'C4 E4')
            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Note("e'8")
            Chord("<c' e' g'>8")
            Chord("<c' e' g'>4")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    d'8
                    ~
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    r8
                    \abjad-color-music #'red
                    <c' e' g'>8
                    ~
                    \abjad-color-music #'blue
                    <c' e' g'>4
                }

        ..  container:: example

            Selects logical ties with pitches intersecting C4:

            >>> staff = abjad.Staff("c'8 d'8 ~ d'8 e'8")
            >>> abjad.setting(staff).autoBeaming = False
            >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")

            >>> result = abjad.select(staff).logical_ties()
            >>> result = result.filter_pitches('&', 'C4')
            >>> for item in result:
            ...     item
            ...
            LogicalTie([Note("c'8")])
            LogicalTie([Chord("<c' e' g'>8"), Chord("<c' e' g'>4")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    d'8
                    ~
                    d'8
                    e'8
                    r8
                    \abjad-color-music #'blue
                    <c' e' g'>8
                    ~
                    \abjad-color-music #'blue
                    <c' e' g'>4
                }

        """
        return self.filter(PitchInequality(operator, pitches))

    def filter_preprolated(
        self, operator, duration: _typings.DurationTyping
    ) -> "Selection":
        r"""
        Filters selection by ``operator`` and preprolated ``duration``.

        ..  container:: example

            Selects runs with duration equal to 2/8:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).runs()
            >>> result = result.filter_preprolated('==', (2, 8))
            >>> for item in result:
            ...     item
            ...
            Selection([Note("d'8"), Note("e'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        ..  container:: example

            Selects runs with duration less than 3/8:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).runs()
            >>> result = result.filter_preprolated('<', (3, 8))
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])
            Selection([Note("d'8"), Note("e'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        """
        inequality = DurationInequality(operator, duration, preprolated=True)
        return self.filter(inequality)

    def flatten(self, depth: int = 1) -> "Selection":
        r"""
        Flattens selection to ``depth``.

        ..  container:: example

            Selects first two leaves of each tuplet:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).tuplets()
            >>> result = [abjad.select(_).leaves()[:2] for _ in result]
            >>> for item in result:
            ...     item
            Selection([Rest('r16'), Note("bf'16")])
            Selection([Rest('r16'), Note("bf'16")])
            Selection([Rest('r16'), Note("bf'16")])

            >>> abjad.label.by_selector(result, True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            \abjad-color-music #'red
                            r16
                            \abjad-color-music #'red
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            \abjad-color-music #'blue
                            r16
                            \abjad-color-music #'blue
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \abjad-color-music #'red
                            r16
                            \abjad-color-music #'red
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                >>

        ..  container:: example

            Selects first two leaves of all tuplets:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).tuplets()
            >>> result = abjad.select(abjad.select(_).leaves()[:2] for _ in result)
            >>> result = result.flatten()
            >>> for item in result:
            ...     item
            Rest('r16')
            Note("bf'16")
            Rest('r16')
            Note("bf'16")
            Rest('r16')
            Note("bf'16")

            >>> abjad.label.by_selector(result, True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            \abjad-color-music #'red
                            r16
                            \abjad-color-music #'blue
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            \abjad-color-music #'red
                            r16
                            \abjad-color-music #'blue
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \abjad-color-music #'red
                            r16
                            \abjad-color-music #'blue
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                >>

        """
        return type(self)(_sequence.Sequence(self).flatten(depth=depth))

    def get(
        self,
        indices: typing.Union[typing.Sequence[int], _pattern.Pattern],
        period: int = None,
    ) -> "Selection":
        r"""
        Gets patterned items.

        ..  container:: example

            Gets every other leaf:

            >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves().get([0], 2)
            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Rest('r8')

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    d'8
                    ~
                    \abjad-color-music #'blue
                    d'8
                    e'8
                    ~
                    \abjad-color-music #'red
                    e'8
                    ~
                    e'8
                    \abjad-color-music #'blue
                    r8
                    f'8
                }

        ..  container:: example

            Gets every other logical tie:

            >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> selection = abjad.select(staff).logical_ties(pitched=True)
            >>> result = selection.get([0], 2)
            >>> for item in result:
            ...     item
            ...
            LogicalTie([Note("c'8")])
            LogicalTie([Note("e'8"), Note("e'8"), Note("e'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    d'8
                    ~
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    ~
                    \abjad-color-music #'blue
                    e'8
                    ~
                    \abjad-color-music #'blue
                    e'8
                    r8
                    f'8
                }

        ..  container:: example

            Gets note 1 (or nothing) in each pitched logical tie:

            >>> staff = abjad.Staff(r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties(pitched=True)
            >>> result = [abjad.select(_).leaves().get([1]) for _ in result]
            >>> for item in result:
            ...     item
            Selection(items=())
            Selection([Note("d'8")])
            Selection([Note("e'8")])
            Selection(items=())

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    d'8
                    ~
                    \abjad-color-music #'blue
                    d'8
                    e'8
                    ~
                    \abjad-color-music #'red
                    e'8
                    ~
                    e'8
                    r8
                    f'8
                }

        """
        if isinstance(indices, _pattern.Pattern):
            assert period is None
            pattern = indices
        else:
            pattern = _pattern.Pattern(indices, period=period)
        pattern = pattern.advance(self._previous)
        self._previous = None
        items = _sequence.Sequence(self.items).retain_pattern(pattern)
        result = type(self)(items, previous=self._previous)
        return result

    def group(self) -> "Selection":
        r"""
        Groups selection.

        ..  container:: example

            >>> staff = abjad.Staff(r'''
            ...     c'8 ~ c'16 c'16 r8 c'16 c'16
            ...     d'8 ~ d'16 d'16 r8 d'16 d'16
            ...     ''')
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves(pitched=True).group()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16"), Note("d'8"), Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])

            >>> abjad.label.by_selector(result, lone=True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'green
                    c'8
                    ~
                    \abjad-color-music #'green
                    c'16
                    \abjad-color-music #'green
                    c'16
                    r8
                    \abjad-color-music #'green
                    c'16
                    \abjad-color-music #'green
                    c'16
                    \abjad-color-music #'green
                    d'8
                    ~
                    \abjad-color-music #'green
                    d'16
                    \abjad-color-music #'green
                    d'16
                    r8
                    \abjad-color-music #'green
                    d'16
                    \abjad-color-music #'green
                    d'16
                }

        """
        return self.group_by()

    def group_by(self, predicate=None) -> "Selection":
        r'''
        Groups items in selection by ``predicate``.

        ..  container:: example

            Wraps selection in selection when ``predicate`` is none:

            >>> staff = abjad.Staff(r"""
            ...     c'8 ~ c'16 c'16 r8 c'16 c'16
            ...     d'8 ~ d'16 d'16 r8 d'16 d'16
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves(pitched=True)
            >>> result = result.group_by()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16"), Note("d'8"), Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])

            >>> abjad.label.by_selector(result, lone=True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'green
                    c'8
                    ~
                    \abjad-color-music #'green
                    c'16
                    \abjad-color-music #'green
                    c'16
                    r8
                    \abjad-color-music #'green
                    c'16
                    \abjad-color-music #'green
                    c'16
                    \abjad-color-music #'green
                    d'8
                    ~
                    \abjad-color-music #'green
                    d'16
                    \abjad-color-music #'green
                    d'16
                    r8
                    \abjad-color-music #'green
                    d'16
                    \abjad-color-music #'green
                    d'16
                }

        '''
        items = []
        if predicate is None:

            def predicate(argument):
                return True

        pairs = itertools.groupby(self, predicate)
        for count, group in pairs:
            item = type(self)(group)
            items.append(item)
        return type(self)(items)

    def group_by_contiguity(self) -> "Selection":
        r'''
        Groups items in selection by contiguity.

        ..  container:: example

            Groups pitched leaves by contiguity:

            >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False
            >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")

            >>> result = abjad.select(staff).leaves(pitched=True)
            >>> result = result.group_by_contiguity()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])
            Selection([Chord("<c' e' g'>8"), Chord("<c' e' g'>4")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    d'8
                    r8
                    \times 2/3
                    {
                        \abjad-color-music #'blue
                        e'8
                        r8
                        \abjad-color-music #'red
                        f'8
                    }
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'red
                    a'8
                    r8
                    r8
                    \abjad-color-music #'blue
                    <c' e' g'>8
                    ~
                    \abjad-color-music #'blue
                    <c' e' g'>4
                }

        ..  container:: example

            Groups sixteenths by contiguity:

            >>> staff = abjad.Staff("c'4 d'16 d' d' d' e'4 f'16 f' f' f'")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves()
            >>> result = result.filter_duration('==', (1, 16))
            >>> result = result.group_by_contiguity()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])
            Selection([Note("f'16"), Note("f'16"), Note("f'16"), Note("f'16")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'4
                    \abjad-color-music #'red
                    d'16
                    \abjad-color-music #'red
                    d'16
                    \abjad-color-music #'red
                    d'16
                    \abjad-color-music #'red
                    d'16
                    e'4
                    \abjad-color-music #'blue
                    f'16
                    \abjad-color-music #'blue
                    f'16
                    \abjad-color-music #'blue
                    f'16
                    \abjad-color-music #'blue
                    f'16
                }

        ..  container:: example

            Groups short-duration logical ties by contiguity; then gets leaf 0 in each
            group:

            >>> staff = abjad.Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 f'4 g'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties()
            >>> result = result.filter_duration('<', (1, 4))
            >>> result = result.group_by_contiguity()
            >>> result = [abjad.select(_).leaves()[0] for _ in result]
            >>> for item in result:
            ...     item
            Note("d'8")
            Note("g'8")

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'4
                    \abjad-color-music #'red
                    d'8
                    ~
                    d'16
                    e'16
                    ~
                    e'8
                    f'4
                    \abjad-color-music #'blue
                    g'8
                }

        ..  container:: example

            Groups pitched leaves pitch; then regroups each group by contiguity:

            >>> staff = abjad.Staff(r"""
            ...     c'8 ~ c'16 c'16 r8 c'16 c'16
            ...     d'8 ~ d'16 d'16 r8 d'16 d'16
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves(pitched=True)
            >>> result = result.group_by_pitch()
            >>> result = [abjad.select(_).group_by_contiguity() for _ in result]
            >>> result = abjad.select(result).flatten()
            >>> for item in result:
            ...     item
            Selection([Note("c'8"), Note("c'16"), Note("c'16")])
            Selection([Note("c'16"), Note("c'16")])
            Selection([Note("d'8"), Note("d'16"), Note("d'16")])
            Selection([Note("d'16"), Note("d'16")])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    ~
                    \abjad-color-music #'red
                    c'16
                    \abjad-color-music #'red
                    c'16
                    r8
                    \abjad-color-music #'blue
                    c'16
                    \abjad-color-music #'blue
                    c'16
                    \abjad-color-music #'red
                    d'8
                    ~
                    \abjad-color-music #'red
                    d'16
                    \abjad-color-music #'red
                    d'16
                    r8
                    \abjad-color-music #'blue
                    d'16
                    \abjad-color-music #'blue
                    d'16
                }

        ..  container:: example

            Groups pitched logical ties by contiguity; then regroups each group by pitch:

            >>> staff = abjad.Staff(r"""
            ...     c'8 ~ c'16 c'16 r8 c'16 c'16
            ...     d'8 ~ d'16 d'16 r8 d'16 d'16
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties(pitched=True)
            >>> result = result.group_by_contiguity()
            >>> result = abjad.select(abjad.select(_).group_by_pitch() for _ in result)
            >>> result = result.flatten()
            >>> for item in result:
            ...     item
            ...
            Selection([LogicalTie([Note("c'8"), Note("c'16")]), LogicalTie([Note("c'16")])])
            Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
            Selection([LogicalTie([Note("d'8"), Note("d'16")]), LogicalTie([Note("d'16")])])
            Selection([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")])])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    ~
                    \abjad-color-music #'red
                    c'16
                    \abjad-color-music #'red
                    c'16
                    r8
                    \abjad-color-music #'blue
                    c'16
                    \abjad-color-music #'blue
                    c'16
                    \abjad-color-music #'red
                    d'8
                    ~
                    \abjad-color-music #'red
                    d'16
                    \abjad-color-music #'red
                    d'16
                    r8
                    \abjad-color-music #'blue
                    d'16
                    \abjad-color-music #'blue
                    d'16
                }

        '''
        result = []
        selection: typing.List[typing.Union[_score.Component, Selection]] = []
        selection.extend(self[:1])
        for item in self[1:]:
            this_timespan = _inspect._get_timespan(selection[-1])
            that_timespan = _inspect._get_timespan(item)
            # remove displacement
            this_stop_offset = this_timespan.stop_offset
            this_stop_offset = _duration.Offset(this_stop_offset.pair)
            that_start_offset = that_timespan.start_offset
            that_start_offset = _duration.Offset(that_start_offset.pair)
            # if this_timespan.stop_offset == that_timespan.start_offset:
            if this_stop_offset == that_start_offset:
                selection.append(item)
            else:
                result.append(type(self)(selection))
                selection = [item]
        if selection:
            result.append(type(self)(selection))
        return type(self)(result)

    def group_by_duration(self) -> "Selection":
        r"""
        Groups items in selection by duration.

        ..  container:: example

            Groups logical ties by duration:

            >>> string = "c'4 ~ c'16 d' ~ d' d' e'4 ~ e'16 f' ~ f' f'"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties()
            >>> result = result.group_by_duration()
            >>> for item in result:
            ...     item
            ...
            Selection([LogicalTie([Note("c'4"), Note("c'16")])])
            Selection([LogicalTie([Note("d'16"), Note("d'16")])])
            Selection([LogicalTie([Note("d'16")])])
            Selection([LogicalTie([Note("e'4"), Note("e'16")])])
            Selection([LogicalTie([Note("f'16"), Note("f'16")])])
            Selection([LogicalTie([Note("f'16")])])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'4
                    ~
                    \abjad-color-music #'red
                    c'16
                    \abjad-color-music #'blue
                    d'16
                    ~
                    \abjad-color-music #'blue
                    d'16
                    \abjad-color-music #'red
                    d'16
                    \abjad-color-music #'blue
                    e'4
                    ~
                    \abjad-color-music #'blue
                    e'16
                    \abjad-color-music #'red
                    f'16
                    ~
                    \abjad-color-music #'red
                    f'16
                    \abjad-color-music #'blue
                    f'16
                }

        """

        def predicate(argument):
            return _inspect._get_duration(argument)

        return self.group_by(predicate)

    def group_by_length(self) -> "Selection":
        r"""
        Groups items in selection by length.

        ..  container:: example

            Groups logical ties by length:

            >>> string = "c'4 ~ c'16 d' ~ d' d' e'4 ~ e'16 f' ~ f' f'"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties().group_by_length()
            >>> for item in result:
            ...     item
            ...
            Selection([LogicalTie([Note("c'4"), Note("c'16")]), LogicalTie([Note("d'16"), Note("d'16")])])
            Selection([LogicalTie([Note("d'16")])])
            Selection([LogicalTie([Note("e'4"), Note("e'16")]), LogicalTie([Note("f'16"), Note("f'16")])])
            Selection([LogicalTie([Note("f'16")])])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'4
                    ~
                    \abjad-color-music #'red
                    c'16
                    \abjad-color-music #'red
                    d'16
                    ~
                    \abjad-color-music #'red
                    d'16
                    \abjad-color-music #'blue
                    d'16
                    \abjad-color-music #'red
                    e'4
                    ~
                    \abjad-color-music #'red
                    e'16
                    \abjad-color-music #'red
                    f'16
                    ~
                    \abjad-color-music #'red
                    f'16
                    \abjad-color-music #'blue
                    f'16
                }

        """

        def predicate(argument):
            if isinstance(argument, _score.Leaf):
                return 1
            return len(argument)

        return self.group_by(predicate)

    def group_by_measure(self) -> "Selection":
        r"""
        Groups items in selection by measure.

        ..  container:: example

            Groups leaves by measure:

            >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = abjad.select(staff).leaves()
            >>> result = result.group_by_measure()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("d'8")])
            Selection([Note("e'8"), Note("f'8")])
            Selection([Note("g'8"), Note("a'8"), Note("b'8")])
            Selection([Note("c''8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'blue
                    f'8
                    \time 3/8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'red
                    a'8
                    \abjad-color-music #'red
                    b'8
                    \time 1/8
                    \abjad-color-music #'blue
                    c''8
                }

        ..  container:: example

            Groups leaves by measure and joins pairs of consecutive groups:

            >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = abjad.select(staff).leaves()
            >>> result = result.group_by_measure()
            >>> result = result.partition_by_counts([2], cyclic=True)
            >>> result = [abjad.select(_).flatten() for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")])
            Selection([Note("g'8"), Note("a'8"), Note("b'8"), Note("c''8")])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'red
                    f'8
                    \time 3/8
                    \abjad-color-music #'blue
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'blue
                    b'8
                    \time 1/8
                    \abjad-color-music #'blue
                    c''8
                }

        ..  container:: example

            Groups leaves by measure; then gets item 0 in each group:

            >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = abjad.select(staff).leaves()
            >>> result = result.group_by_measure()
            >>> result = [abjad.select(_)[0] for _ in result]
            >>> for item in result:
            ...     item
            Note("c'8")
            Note("e'8")
            Note("g'8")
            Note("c''8")

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    c'8
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    f'8
                    \time 3/8
                    \abjad-color-music #'red
                    g'8
                    a'8
                    b'8
                    \time 1/8
                    \abjad-color-music #'blue
                    c''8
                }

        ..  container:: example

            Groups leaves by measure; then gets item -1 in each group:

            >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = abjad.select(staff).leaves()
            >>> result = result.group_by_measure()
            >>> result = [abjad.select(_)[-1] for _ in result]
            >>> for item in result:
            ...     item
            ...
            Note("d'8")
            Note("f'8")
            Note("b'8")
            Note("c''8")

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    c'8
                    \abjad-color-music #'red
                    d'8
                    e'8
                    \abjad-color-music #'blue
                    f'8
                    \time 3/8
                    g'8
                    a'8
                    \abjad-color-music #'red
                    b'8
                    \time 1/8
                    \abjad-color-music #'blue
                    c''8
                }

        ..  container:: example

            Works with implicit time signatures:

            >>> staff = abjad.Staff("c'4 d' e' f' g' a' b' c''")
            >>> abjad.setting(staff).autoBeaming = False
            >>> score = abjad.Score([staff])
            >>> string = "#(ly:make-moment 1 16)"
            >>> abjad.setting(score).proportionalNotationDuration = string

            >>> result = abjad.select(score).leaves()
            >>> result = result.group_by_measure()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])
            Selection([Note("g'4"), Note("a'4"), Note("b'4"), Note("c''4")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'4
                    \abjad-color-music #'red
                    d'4
                    \abjad-color-music #'red
                    e'4
                    \abjad-color-music #'red
                    f'4
                    \abjad-color-music #'blue
                    g'4
                    \abjad-color-music #'blue
                    a'4
                    \abjad-color-music #'blue
                    b'4
                    \abjad-color-music #'blue
                    c''4
                }

        ..  container:: example

            Groups logical ties by measure:

            >>> staff = abjad.Staff("c'8 d' ~ d' e' ~ e' f' g' ~ g'")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = abjad.select(staff).logical_ties()
            >>> result = result.group_by_measure()
            >>> for item in result:
            ...     item
            ...
            Selection([LogicalTie([Note("c'8")]), LogicalTie([Note("d'8"), Note("d'8")])])
            Selection([LogicalTie([Note("e'8"), Note("e'8")])])
            Selection([LogicalTie([Note("f'8")]), LogicalTie([Note("g'8"), Note("g'8")])])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    d'8
                    ~
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    ~
                    \time 3/8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'red
                    f'8
                    \abjad-color-music #'red
                    g'8
                    ~
                    \time 1/8
                    \abjad-color-music #'red
                    g'8
                }

        ..  container:: example

            REGRESSION: works for pickup measure:

            >>> staff = abjad.Staff(r"c'4 | d'4 e'4 f'4 | g'4 a'4 b'4")
            >>> time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
            >>> abjad.attach(time_signature, staff[0])

            >>> for measure in abjad.select(staff).leaves().group_by_measure():
            ...     print(measure)
            ...
            Selection([Note("c'4")])
            Selection([Note("d'4"), Note("e'4"), Note("f'4")])
            Selection([Note("g'4"), Note("a'4"), Note("b'4")])

        """

        def _get_first_component(argument):
            component = Selection(argument).components()[0]
            assert isinstance(component, _score.Component)
            return component

        def _get_measure_number(argument):
            first_component = _get_first_component(argument)
            assert first_component._measure_number is not None
            return first_component._measure_number

        selections = []
        first_component = _get_first_component(self)
        first_component._update_measure_numbers()
        pairs = itertools.groupby(self, _get_measure_number)
        for value, group in pairs:
            selection = type(self)(group)
            selections.append(selection)
        return type(self)(selections)

    def group_by_pitch(self) -> "Selection":
        r"""
        Groups items in selection by pitches.

        ..  container:: example

            Groups logical ties by pitches:

            >>> string = "c'4 ~ c'16 d' ~ d' d' e'4 ~ e'16 f' ~ f' f'"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties().group_by_pitch()
            >>> for item in result:
            ...     item
            ...
            Selection([LogicalTie([Note("c'4"), Note("c'16")])])
            Selection([LogicalTie([Note("d'16"), Note("d'16")]), LogicalTie([Note("d'16")])])
            Selection([LogicalTie([Note("e'4"), Note("e'16")])])
            Selection([LogicalTie([Note("f'16"), Note("f'16")]), LogicalTie([Note("f'16")])])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'4
                    ~
                    \abjad-color-music #'red
                    c'16
                    \abjad-color-music #'blue
                    d'16
                    ~
                    \abjad-color-music #'blue
                    d'16
                    \abjad-color-music #'blue
                    d'16
                    \abjad-color-music #'red
                    e'4
                    ~
                    \abjad-color-music #'red
                    e'16
                    \abjad-color-music #'blue
                    f'16
                    ~
                    \abjad-color-music #'blue
                    f'16
                    \abjad-color-music #'blue
                    f'16
                }

        """

        def predicate(argument):
            selection = Selection(argument)
            return _pitch.PitchSet.from_selection(selection)

        return self.group_by(predicate)

    def leaf(
        self,
        n: int,
        *,
        exclude: _typings.Strings = None,
        grace: bool = None,
        head: bool = None,
        pitched: bool = None,
        prototype=None,
        reverse: bool = None,
        tail: bool = None,
        trim: typing.Union[bool, int] = None,
    ) -> _score.Leaf:
        r"""
        Selects leaf ``n``.

        ..  container:: example

            Selects leaf -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).leaf(-1)
            >>> result
            Chord("<fs' gs'>16")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'green
                            <fs' gs'>16
                        }
                    }
                >>

        """
        return self.leaves(
            exclude=exclude,
            grace=grace,
            head=head,
            pitched=pitched,
            prototype=prototype,
            reverse=reverse,
            tail=tail,
            trim=trim,
        )[n]

    def leaves(
        self,
        prototype=None,
        *,
        exclude: _typings.Strings = None,
        grace: bool = None,
        head: bool = None,
        pitched: bool = None,
        reverse: bool = None,
        tail: bool = None,
        trim: typing.Union[bool, int] = None,
    ) -> "Selection":
        r'''
        Selects leaves (without grace notes).

        ..  container:: example

            Selects leaves:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves()
            >>> for item in result:
            ...     item
            ...
            Rest('r8')
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Rest('r8')
            Rest('r8')
            Note("f'8")
            Note("e'8")
            Note("d'8")
            Rest('r8')

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        r8
                        \abjad-color-music #'blue
                        d'8
                        \abjad-color-music #'red
                        e'8
                    }
                    \abjad-color-music #'blue
                    f'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'red
                    f'8
                    \times 2/3
                    {
                        \abjad-color-music #'blue
                        e'8
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'blue
                        r8
                    }
                }

        ..  container:: example

            Selects pitched leaves:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves(pitched=True)
            >>> for item in result:
            ...     item
            ...
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Note("f'8")
            Note("e'8")
            Note("d'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        r8
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'blue
                        e'8
                    }
                    \abjad-color-music #'red
                    f'8
                    r8
                    r8
                    \abjad-color-music #'blue
                    f'8
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'blue
                        d'8
                        r8
                    }
                }

        ..  container:: example

            Trimmed leaves are the correct selection for ottava brackets.

            Selects trimmed leaves:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves(trim=True)
            >>> for item in result:
            ...     item
            ...
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Rest('r8')
            Rest('r8')
            Note("f'8")
            Note("e'8")
            Note("d'8")

            >>> abjad.ottava(result)
            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        r8
                        \ottava 1
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'blue
                        e'8
                    }
                    \abjad-color-music #'red
                    f'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    f'8
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'blue
                        d'8
                        \ottava 0
                        r8
                    }
                }

        ..  container:: example

            Set ``trim`` to ``abjad.Left`` to trim rests at left (and preserve rests at
            right):

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves(trim=abjad.Left)
            >>> for item in result:
            ...     item
            ...
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Rest('r8')
            Rest('r8')
            Note("f'8")
            Note("e'8")
            Note("d'8")
            Rest('r8')

            >>> abjad.ottava(result)
            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        r8
                        \ottava 1
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'blue
                        e'8
                    }
                    \abjad-color-music #'red
                    f'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    f'8
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'blue
                        d'8
                        \abjad-color-music #'red
                        r8
                        \ottava 0
                    }
                }

        ..  container:: example

            REGRESSION: selects trimmed leaves (even when there are no rests to trim):

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { c'8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' c' }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves(trim=True)
            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Rest('r8')
            Rest('r8')
            Note("f'8")
            Note("e'8")
            Note("d'8")
            Note("c'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        c'8
                        \abjad-color-music #'blue
                        d'8
                        \abjad-color-music #'red
                        e'8
                    }
                    \abjad-color-music #'blue
                    f'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'red
                    f'8
                    \times 2/3
                    {
                        \abjad-color-music #'blue
                        e'8
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'blue
                        c'8
                    }
                }

        ..  container:: example

            Selects leaves in tuplets:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).components(abjad.Tuplet)
            >>> result = result.leaves()
            >>> for item in result:
            ...     item
            ...
            Rest('r8')
            Note("d'8")
            Note("e'8")
            Note("e'8")
            Note("d'8")
            Rest('r8')

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        r8
                        \abjad-color-music #'blue
                        d'8
                        \abjad-color-music #'red
                        e'8
                    }
                    f'8
                    r8
                    r8
                    f'8
                    \times 2/3
                    {
                        \abjad-color-music #'blue
                        e'8
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'blue
                        r8
                    }
                }

        ..  container:: example

            Selects trimmed leaves in tuplets:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).components(abjad.Tuplet)
            >>> result = result.leaves(trim=True)
            >>> for item in result:
            ...     item
            ...
            Note("d'8")
            Note("e'8")
            Note("e'8")
            Note("d'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        r8
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'blue
                        e'8
                    }
                    f'8
                    r8
                    r8
                    f'8
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'blue
                        d'8
                        r8
                    }
                }

        ..  container:: example

            Pitched heads is the correct selection for most articulations.

            Selects pitched heads in tuplets:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { c'8 d' ~ d' } e' r
            ...     r e' \times 2/3 { d' ~ d' c' }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).components(abjad.Tuplet)
            >>> result = result.leaves(head=True, pitched=True)
            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Note("d'8")
            Note("d'8")
            Note("c'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        c'8
                        \abjad-color-music #'blue
                        d'8
                        ~
                        d'8
                    }
                    e'8
                    r8
                    r8
                    e'8
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        d'8
                        ~
                        d'8
                        \abjad-color-music #'blue
                        c'8
                    }
                }

        ..  container:: example

            Pitched tails in the correct selection for laissez vibrer.

            Selects pitched tails in tuplets:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { c'8 d' ~ d' } e' r
            ...     r e' \times 2/3 { d' ~ d' c' }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).components(abjad.Tuplet)
            >>> result = result.leaves(tail=True, pitched=True)
            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Note("d'8")
            Note("d'8")
            Note("c'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        c'8
                        d'8
                        ~
                        \abjad-color-music #'blue
                        d'8
                    }
                    e'8
                    r8
                    r8
                    e'8
                    \times 2/3
                    {
                        d'8
                        ~
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'blue
                        c'8
                    }
                }

        ..  container:: example

            Chord heads are the correct selection for arpeggios.

            Selects chord heads in tuplets:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { <c' e' g'>8 ~ <c' e' g'> d' } e' r
            ...     r <g d' fs'> \times 2/3 { e' <c' d'> ~ <c' d'> }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).components(abjad.Tuplet)
            >>> result = result.leaves(abjad.Chord, head=True)
            >>> for item in result:
            ...     item
            ...
            Chord("<c' e' g'>8")
            Chord("<c' d'>8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        <c' e' g'>8
                        ~
                        <c' e' g'>8
                        d'8
                    }
                    e'8
                    r8
                    r8
                    <g d' fs'>8
                    \times 2/3
                    {
                        e'8
                        \abjad-color-music #'blue
                        <c' d'>8
                        ~
                        <c' d'>8
                    }
                }

        ..  container:: example

            Excludes leaves with ``"HIDDEN"`` indicator:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> abjad.attach("HIDDEN", staff[-1][-2])
            >>> abjad.attach("HIDDEN", staff[-1][-1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves(exclude="HIDDEN")
            >>> for item in result:
            ...     item
            ...
            Rest('r8')
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Rest('r8')
            Rest('r8')
            Note("f'8")
            Note("e'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        r8
                        \abjad-color-music #'blue
                        d'8
                        \abjad-color-music #'red
                        e'8
                    }
                    \abjad-color-music #'blue
                    f'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'red
                    f'8
                    \times 2/3
                    {
                        \abjad-color-music #'blue
                        e'8
                        d'8
                        r8
                    }
                }

        ..  container:: example

            Selects both main notes and graces when ``grace=None``:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves(grace=None)
            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Note("cf''16")
            Note("bf'16")
            Note("d'8")
            Note("af'16")
            Note("gf'16")
            Note("e'8")
            Note("f'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \grace {
                        \abjad-color-music #'blue
                        cf''16
                        \abjad-color-music #'red
                        bf'16
                    }
                    \abjad-color-music #'blue
                    \afterGrace
                    d'8
                    {
                        \abjad-color-music #'red
                        af'16
                        \abjad-color-music #'blue
                        gf'16
                    }
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }

        ..  container:: example

            Excludes grace notes when ``grace=False``:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves(grace=False)
            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \grace {
                        cf''16
                        bf'16
                    }
                    \abjad-color-music #'blue
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }

        ..  container:: example

            Selects only grace notes when ``grace=True``:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves(grace=True)
            >>> for item in result:
            ...     item
            ...
            Note("cf''16")
            Note("bf'16")
            Note("af'16")
            Note("gf'16")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \grace {
                        \abjad-color-music #'red
                        cf''16
                        \abjad-color-music #'blue
                        bf'16
                    }
                    \afterGrace
                    d'8
                    {
                        \abjad-color-music #'red
                        af'16
                        \abjad-color-music #'blue
                        gf'16
                    }
                    e'8
                    f'8
                }

        '''
        assert trim in (True, False, _enums.Left, None)
        if pitched:
            prototype = (_score.Chord, _score.Note)
        elif prototype is None:
            prototype = _score.Leaf
        return self._components(
            self,
            prototype=prototype,
            exclude=exclude,
            grace=grace,
            head=head,
            tail=tail,
            trim=trim,
        )

    def logical_tie(
        self,
        n: int = 0,
        *,
        exclude: _typings.Strings = None,
        grace: bool = None,
        nontrivial: bool = None,
        pitched: bool = None,
        reverse: bool = None,
    ) -> _score.Leaf:
        """
        Selects logical tie ``n``.

        ..  todo:: Make work on nonhead leaves.

        ..  todo:: Write examples.

        ..  todo:: Remove ``abjad.get.logical_tie()``.

        """
        return self.logical_ties(
            exclude=exclude,
            grace=grace,
            nontrivial=nontrivial,
            pitched=pitched,
            reverse=reverse,
        )[n]

    def logical_ties(
        self,
        *,
        exclude: _typings.Strings = None,
        grace: bool = None,
        nontrivial: bool = None,
        pitched: bool = None,
        reverse: bool = None,
    ) -> "Selection":
        r'''
        Selects logical ties (without grace notes).

        ..  container:: example

            Selects logical ties:

            >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties()
            >>> for item in result:
            ...     item
            ...
            LogicalTie([Note("c'8")])
            LogicalTie([Note("d'8"), Note("d'8")])
            LogicalTie([Note("e'8")])
            LogicalTie([Rest('r8')])
            LogicalTie([Note("f'8"), Note("f'8")])
            LogicalTie([Rest('r8')])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    d'8
                    ~
                    {
                        \abjad-color-music #'blue
                        d'8
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'blue
                        r8
                        \abjad-color-music #'red
                        f'8
                        ~
                    }
                    \abjad-color-music #'red
                    f'8
                    \abjad-color-music #'blue
                    r8
                }

        ..  container:: example

            Selects pitched logical ties:

            >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties(pitched=True)
            >>> for item in result:
            ...     item
            ...
            LogicalTie([Note("c'8")])
            LogicalTie([Note("d'8"), Note("d'8")])
            LogicalTie([Note("e'8")])
            LogicalTie([Note("f'8"), Note("f'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    d'8
                    ~
                    {
                        \abjad-color-music #'blue
                        d'8
                        \abjad-color-music #'red
                        e'8
                        r8
                        \abjad-color-music #'blue
                        f'8
                        ~
                    }
                    \abjad-color-music #'blue
                    f'8
                    r8
                }

        ..  container:: example

            Selects pitched nontrivial logical ties:

            >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties(
            ...     pitched=True,
            ...     nontrivial=True,
            ...     )
            >>> for item in result:
            ...     item
            LogicalTie([Note("d'8"), Note("d'8")])
            LogicalTie([Note("f'8"), Note("f'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \abjad-color-music #'red
                    d'8
                    ~
                    {
                        \abjad-color-music #'red
                        d'8
                        e'8
                        r8
                        \abjad-color-music #'blue
                        f'8
                        ~
                    }
                    \abjad-color-music #'blue
                    f'8
                    r8
                }

        ..  container:: example

            Selects pitched logical ties (starting) in each tuplet:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { c'8 d' e'  ~ } e' f' ~
            ...     \times 2/3 { f' g' a' ~ } a' b' ~
            ...     \times 2/3 { b' c'' d'' }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).components(abjad.Tuplet)
            >>> result = [abjad.select(_).logical_ties(pitched=True) for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([LogicalTie([Note("c'8")]), LogicalTie([Note("d'8")]), LogicalTie([Note("e'8"), Note("e'8")])])
            Selection([LogicalTie([Note("g'8")]), LogicalTie([Note("a'8"), Note("a'8")])])
            Selection([LogicalTie([Note("c''8")]), LogicalTie([Note("d''8")])])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        c'8
                        \abjad-color-music #'red
                        d'8
                        \abjad-color-music #'red
                        e'8
                        ~
                    }
                    \abjad-color-music #'red
                    e'8
                    f'8
                    ~
                    \times 2/3
                    {
                        f'8
                        \abjad-color-music #'blue
                        g'8
                        \abjad-color-music #'blue
                        a'8
                        ~
                    }
                    \abjad-color-music #'blue
                    a'8
                    b'8
                    ~
                    \times 2/3
                    {
                        b'8
                        \abjad-color-music #'red
                        c''8
                        \abjad-color-music #'red
                        d''8
                    }
                }

        ..  container:: example

            Selects pitched logical ties (starting) in each of the last two tuplets:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { c'8 d' e'  ~ } e' f' ~
            ...     \times 2/3 { f' g' a' ~ } a' b' ~
            ...     \times 2/3 { b' c'' d'' }
            ...     """)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).components(abjad.Tuplet)[-2:]
            >>> result = [abjad.select(_).logical_ties(pitched=True) for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([LogicalTie([Note("g'8")]), LogicalTie([Note("a'8"), Note("a'8")])])
            Selection([LogicalTie([Note("c''8")]), LogicalTie([Note("d''8")])])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \times 2/3
                    {
                        c'8
                        d'8
                        e'8
                        ~
                    }
                    e'8
                    f'8
                    ~
                    \times 2/3
                    {
                        f'8
                        \abjad-color-music #'red
                        g'8
                        \abjad-color-music #'red
                        a'8
                        ~
                    }
                    \abjad-color-music #'red
                    a'8
                    b'8
                    ~
                    \times 2/3
                    {
                        b'8
                        \abjad-color-music #'blue
                        c''8
                        \abjad-color-music #'blue
                        d''8
                    }
                }

        ..  container:: example

            Selects both main notes and graces when ``grace=None``:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties(grace=None)
            >>> for item in result:
            ...     item
            ...
            LogicalTie([Note("c'8")])
            LogicalTie([Note("cf''16")])
            LogicalTie([Note("bf'16")])
            LogicalTie([Note("d'8")])
            LogicalTie([Note("af'16")])
            LogicalTie([Note("gf'16")])
            LogicalTie([Note("e'8")])
            LogicalTie([Note("f'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \grace {
                        \abjad-color-music #'blue
                        cf''16
                        \abjad-color-music #'red
                        bf'16
                    }
                    \abjad-color-music #'blue
                    \afterGrace
                    d'8
                    {
                        \abjad-color-music #'red
                        af'16
                        \abjad-color-music #'blue
                        gf'16
                    }
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }

        ..  container:: example

            Excludes grace notes when ``grace=False``:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties(grace=False)
            >>> for item in result:
            ...     item
            ...
            LogicalTie([Note("c'8")])
            LogicalTie([Note("d'8")])
            LogicalTie([Note("e'8")])
            LogicalTie([Note("f'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \grace {
                        cf''16
                        bf'16
                    }
                    \abjad-color-music #'blue
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }

        ..  container:: example

            Selects only grace notes when ``grace=True``:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False


            >>> result = abjad.select(staff).logical_ties(grace=True)
            >>> for item in result:
            ...     item
            ...
            LogicalTie([Note("cf''16")])
            LogicalTie([Note("bf'16")])
            LogicalTie([Note("af'16")])
            LogicalTie([Note("gf'16")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \grace {
                        \abjad-color-music #'red
                        cf''16
                        \abjad-color-music #'blue
                        bf'16
                    }
                    \afterGrace
                    d'8
                    {
                        \abjad-color-music #'red
                        af'16
                        \abjad-color-music #'blue
                        gf'16
                    }
                    e'8
                    f'8
                }

        ..  container:: example

            STATAL SELECTOR WITH PATTERN.  Note that this currently only works with
            pattern objects; slices and integer indices do not work yet.

            Selector configured for logical ties 4, 5, 6, 7:

            >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties()
            >>> result = result.get([4, 5, 6, 7])
            >>> for item in result:
            ...     item
            ...
            LogicalTie([Note("f'8"), Note("f'8")])
            LogicalTie([Rest('r8')])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    d'8
                    ~
                    {
                        d'8
                        e'8
                        r8
                        \abjad-color-music #'red
                        f'8
                        ~
                    }
                    \abjad-color-music #'red
                    f'8
                    \abjad-color-music #'blue
                    r8
                }

            Selects logical ties 4 and 5 on first call.

            Setting ``previous`` effects statal outcome:

            >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
            >>> abjad.setting(staff).autoBeaming = False

            >>> logical_ties = abjad.select(staff).logical_ties()
            >>> previous = len(logical_ties)
            >>> previous
            6

            >>> result = abjad.select(staff, previous=previous)
            >>> result = result.logical_ties().get([4, 5, 6, 7])
            >>> for item in result:
            ...     item
            ...
            LogicalTie([Note("c'8")])
            LogicalTie([Note("d'8"), Note("d'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    d'8
                    ~
                    {
                        \abjad-color-music #'blue
                        d'8
                        e'8
                        r8
                        f'8
                        ~
                    }
                    f'8
                    r8
                }

            Selects logical ties 6 and 7 on second call.

        '''
        generator = _iterate._iterate_logical_ties(
            self,
            exclude=exclude,
            grace=grace,
            nontrivial=nontrivial,
            pitched=pitched,
            reverse=reverse,
            wrapper_class=LogicalTie,
        )
        return type(self)(generator, previous=self._previous)

    def nontrivial(self) -> "Selection":
        r"""
        Filters selection by length greater than 1.

        ..  container:: example

            Selects nontrivial runs:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).runs().nontrivial()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("d'8"), Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    r8
                    \abjad-color-music #'blue
                    f'8
                    \abjad-color-music #'blue
                    g'8
                    \abjad-color-music #'blue
                    a'8
                }

        """
        return self.filter_length(">", 1)

    def note(
        self, n: int, *, exclude: _typings.Strings = None, grace: bool = None
    ) -> _score.Note:
        r"""
        Selects note ``n``.

        ..  container:: example

            Selects note -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).note(-1)
            >>> result
            Note("e'16")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            \abjad-color-music #'green
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                >>

        """
        return self.notes(exclude=exclude, grace=grace)[n]

    def notes(
        self, *, exclude: _typings.Strings = None, grace: bool = None
    ) -> "Selection":
        r"""
        Selects notes.

        ..  container:: example

            Selects notes:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).notes()
            >>> for item in result:
            ...     item
            ...
            Note("bf'16")
            Note("c'16")
            Note("bf'16")
            Note("d'16")
            Note("bf'16")
            Note("e'16")

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            r16
                            \abjad-color-music #'red
                            bf'16
                            <a'' b''>16
                            \abjad-color-music #'blue
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            r16
                            \abjad-color-music #'red
                            bf'16
                            <a'' b''>16
                            \abjad-color-music #'blue
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            r16
                            \abjad-color-music #'red
                            bf'16
                            <a'' b''>16
                            \abjad-color-music #'blue
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                >>

        """
        return self.components(_score.Note, exclude=exclude, grace=grace)

    def partition_by_counts(
        self,
        counts,
        *,
        cyclic=False,
        enchain=False,
        fuse_overhang=False,
        nonempty=False,
        overhang=False,
    ) -> "Selection":
        r"""
        Partitions selection by ``counts``.

        ..  container:: example

            Partitions leaves into a single part of length 3; truncates overhang:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_counts(
            ...     [3],
            ...     cyclic=False,
            ...     overhang=False,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Rest('r8'), Note("d'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

        ..  container:: example

            Cyclically partitions leaves into parts of length 3; truncates overhang:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves().partition_by_counts(
            ...     [3],
            ...     cyclic=True,
            ...     overhang=False,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Rest('r8'), Note("d'8")])
            Selection([Note("e'8"), Rest('r8'), Note("f'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    f'8
                    g'8
                    a'8
                }

        ..  container:: example

            Cyclically partitions leaves into parts of length 3; returns overhang at end:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves().partition_by_counts(
            ...     [3],
            ...     cyclic=True,
            ...     overhang=True,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Rest('r8'), Note("d'8")])
            Selection([Note("e'8"), Rest('r8'), Note("f'8")])
            Selection([Note("g'8"), Note("a'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    f'8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'red
                    a'8
                }

        ..  container:: example

            Cyclically partitions leaves into parts of length 3; fuses overhang to last
            part:

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves().partition_by_counts(
            ...     [3],
            ...     cyclic=True,
            ...     fuse_overhang=True,
            ...     overhang=True,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Rest('r8'), Note("d'8")])
            Selection([Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    f'8
                    \abjad-color-music #'blue
                    g'8
                    \abjad-color-music #'blue
                    a'8
                }

        ..  container:: example

            Cyclically partitions leaves into parts of length 3; returns overhang at end:

            >>> string = "c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves().partition_by_counts(
            ...     [1, 2, 3],
            ...     cyclic=True,
            ...     overhang=True,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])
            Selection([Rest('r8'), Note("d'8")])
            Selection([Note("e'8"), Rest('r8'), Note("f'8")])
            Selection([Note("g'8")])
            Selection([Note("a'8"), Note("b'8")])
            Selection([Rest('r8'), Note("c''8")])

            >>> abjad.label.by_selector(result, colors=["#red", "#blue", "#cyan"])
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'cyan
                    e'8
                    \abjad-color-music #'cyan
                    r8
                    \abjad-color-music #'cyan
                    f'8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'blue
                    b'8
                    \abjad-color-music #'cyan
                    r8
                    \abjad-color-music #'cyan
                    c''8
                }

        ..  container:: example

            With negative ``counts``.

            Partitions leaves alternately into parts 2 and -3 (without overhang):

            >>> string = "c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves().partition_by_counts(
            ...     [2, -3],
            ...     cyclic=True,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Rest('r8')])
            Selection([Note("f'8"), Note("g'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    r8
                    d'8
                    e'8
                    r8
                    \abjad-color-music #'blue
                    f'8
                    \abjad-color-music #'blue
                    g'8
                    a'8
                    b'8
                    r8
                    c''8
                }

        ..  container:: example

            With negative ``counts``.

            Partitions leaves alternately into parts 2 and -3 (with overhang):

            >>> string = "c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves().partition_by_counts(
            ...     [2, -3],
            ...     cyclic=True,
            ...     overhang=True,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Rest('r8')])
            Selection([Note("f'8"), Note("g'8")])
            Selection([Note("c''8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    r8
                    d'8
                    e'8
                    r8
                    \abjad-color-music #'blue
                    f'8
                    \abjad-color-music #'blue
                    g'8
                    a'8
                    b'8
                    r8
                    \abjad-color-music #'red
                    c''8
                }

        ..  container:: example

            REGRESSION. Noncyclic counts work when ``overhang`` is true:

            >>> string = "c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves().partition_by_counts(
            ...     [3],
            ...     overhang=True,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Rest('r8'), Note("d'8")])
            Selection([Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8"), Note("b'8"), Rest('r8'), Note("c''8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    f'8
                    \abjad-color-music #'blue
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'blue
                    b'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    c''8
                }

        """
        result = []
        groups_ = _sequence.Sequence(self).partition_by_counts(
            [abs(_) for _ in counts],
            cyclic=cyclic,
            enchain=enchain,
            overhang=overhang,
        )
        groups = list(groups_)
        total = len(groups)
        if overhang and fuse_overhang and 1 < len(groups):
            last_count = counts[(len(groups) - 1) % len(counts)]
            if len(groups[-1]) != last_count:
                last_group = groups.pop()
                groups[-1] += last_group
        subresult = []
        if cyclic:
            counts = _cyclictuple.CyclicTuple(counts)
        for i, group in enumerate(groups):
            if overhang and i == total - 1:
                pass
            else:
                try:
                    count = counts[i]
                except Exception:
                    raise Exception(counts, i)
                if count < 0:
                    continue
            items = type(self)(group)
            subresult.append(items)
        if nonempty and not subresult:
            group = type(self)(groups[0])
            subresult.append(group)
        result.extend(subresult)
        return type(self)(result)

    def partition_by_durations(
        self,
        durations,
        *,
        cyclic=False,
        fill=None,
        in_seconds=False,
        overhang=False,
    ) -> "Selection":
        r"""
        Partitions selection by ``durations``.

        ..  container:: example

            Cyclically partitions leaves into parts equal to exactly 3/8; returns
            overhang at end:

            >>> staff = abjad.Staff([
            ...     abjad.Container("c'8 d'"),
            ...     abjad.Container("e'8 f'"),
            ...     abjad.Container("g'8 a'"),
            ...     abjad.Container("b'8 c''"),
            ... ])
            >>> for container in staff:
            ...     time_signature = abjad.TimeSignature((2, 8))
            ...     abjad.attach(time_signature, container[0])
            ...
            >>> abjad.setting(staff).autoBeaming = False
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).leaves().partition_by_durations(
            ...     [abjad.Duration(3, 8)],
            ...     cyclic=True,
            ...     fill=abjad.Exact,
            ...     in_seconds=False,
            ...     overhang=True,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])
            Selection([Note("b'8"), Note("c''8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        c'8
                        \abjad-color-music #'red
                        d'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'blue
                        f'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'blue
                        g'8
                        \abjad-color-music #'blue
                        a'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        b'8
                        \abjad-color-music #'red
                        c''8
                    }
                }

        ..  container:: example

            Partitions leaves into one part equal to exactly 3/8; truncates overhang:

            >>> staff = abjad.Staff([
            ...     abjad.Container("c'8 d'"),
            ...     abjad.Container("e'8 f'"),
            ...     abjad.Container("g'8 a'"),
            ...     abjad.Container("b'8 c''"),
            ... ])
            >>> for container in staff:
            ...     time_signature = abjad.TimeSignature((2, 8))
            ...     abjad.attach(time_signature, container[0])
            ...
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_durations(
            ...     [abjad.Duration(3, 8)],
            ...     cyclic=False,
            ...     fill=abjad.Exact,
            ...     in_seconds=False,
            ...     overhang=False,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        c'8
                        \abjad-color-music #'red
                        d'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        e'8
                        f'8
                    }
                    {
                        \time 2/8
                        g'8
                        a'8
                    }
                    {
                        \time 2/8
                        b'8
                        c''8
                    }
                }

        ..  container:: example

            Cyclically partitions leaves into parts equal to (or just less than) 3/16 and
            1/16; returns overhang at end:

            >>> staff = abjad.Staff([
            ...     abjad.Container("c'8 d'"),
            ...     abjad.Container("e'8 f'"),
            ...     abjad.Container("g'8 a'"),
            ...     abjad.Container("b'8 c''"),
            ... ])
            >>> for container in staff:
            ...     time_signature = abjad.TimeSignature((2, 8))
            ...     abjad.attach(time_signature, container[0])
            ...
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_durations(
            ...     [abjad.Duration(3, 16), abjad.Duration(1, 16)],
            ...     cyclic=True,
            ...     fill=abjad.More,
            ...     in_seconds=False,
            ...     overhang=True,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'8"), Note("g'8")])
            Selection([Note("a'8")])
            Selection([Note("b'8"), Note("c''8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        c'8
                        \abjad-color-music #'red
                        d'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'blue
                        e'8
                        \abjad-color-music #'red
                        f'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        g'8
                        \abjad-color-music #'blue
                        a'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        b'8
                        \abjad-color-music #'red
                        c''8
                    }
                }

        ..  container:: example

            Cyclically partitions leaves into parts equal to (or just less than) 3/16;
            truncates overhang:

            >>> staff = abjad.Staff([
            ...     abjad.Container("c'8 d'"),
            ...     abjad.Container("e'8 f'"),
            ...     abjad.Container("g'8 a'"),
            ...     abjad.Container("b'8 c''"),
            ... ])
            >>> for container in staff:
            ...     time_signature = abjad.TimeSignature((2, 8))
            ...     abjad.attach(time_signature, container[0])
            ...
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_durations(
            ...     [abjad.Duration(3, 16)],
            ...     cyclic=True,
            ...     fill=abjad.Less,
            ...     in_seconds=False,
            ...     overhang=False,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])
            Selection([Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'8")])
            Selection([Note("g'8")])
            Selection([Note("a'8")])
            Selection([Note("b'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        c'8
                        \abjad-color-music #'blue
                        d'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'blue
                        f'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        g'8
                        \abjad-color-music #'blue
                        a'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        b'8
                        c''8
                    }
                }

        ..  container:: example

            Partitions leaves into a single part equal to (or just less than) 3/16;
            truncates overhang:

            >>> staff = abjad.Staff([
            ...     abjad.Container("c'8 d'"),
            ...     abjad.Container("e'8 f'"),
            ...     abjad.Container("g'8 a'"),
            ...     abjad.Container("b'8 c''"),
            ... ])
            >>> for container in staff:
            ...     time_signature = abjad.TimeSignature((2, 8))
            ...     abjad.attach(time_signature, container[0])
            ...
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_durations(
            ...     [abjad.Duration(3, 16)],
            ...     cyclic=False,
            ...     fill=abjad.Less,
            ...     in_seconds=False,
            ...     overhang=False,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        c'8
                        d'8
                    }
                    {
                        \time 2/8
                        e'8
                        f'8
                    }
                    {
                        \time 2/8
                        g'8
                        a'8
                    }
                    {
                        \time 2/8
                        b'8
                        c''8
                    }
                }

        ..  container:: example

            Cyclically partitions leaves into parts equal to exactly 1.5 seconds;
            truncates overhang:

            >>> staff = abjad.Staff([
            ...     abjad.Container("c'8 d'"),
            ...     abjad.Container("e'8 f'"),
            ...     abjad.Container("g'8 a'"),
            ...     abjad.Container("b'8 c''"),
            ... ])
            >>> for container in staff:
            ...     time_signature = abjad.TimeSignature((2, 8))
            ...     abjad.attach(time_signature, container[0])
            ...
            >>> abjad.setting(staff).autoBeaming = False
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> leaf = abjad.get.leaf(staff, 0)
            >>> abjad.attach(mark, leaf, context='Staff')

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_durations(
            ...     [1.5],
            ...     cyclic=True,
            ...     fill=abjad.Exact,
            ...     in_seconds=True,
            ...     overhang=False,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {
                        \tempo 4=60
                        \time 2/8
                        \abjad-color-music #'red
                        c'8
                        \abjad-color-music #'red
                        d'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'blue
                        f'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'blue
                        g'8
                        \abjad-color-music #'blue
                        a'8
                    }
                    {
                        \time 2/8
                        b'8
                        c''8
                    }
                }

        ..  container:: example

            Cyclically partitions leaves into parts equal to exactly 1.5 seconds; returns
            overhang at end:

            >>> staff = abjad.Staff([
            ...     abjad.Container("c'8 d'"),
            ...     abjad.Container("e'8 f'"),
            ...     abjad.Container("g'8 a'"),
            ...     abjad.Container("b'8 c''"),
            ... ])
            >>> for container in staff:
            ...     time_signature = abjad.TimeSignature((2, 8))
            ...     abjad.attach(time_signature, container[0])
            ...
            >>> abjad.setting(staff).autoBeaming = False
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> leaf = abjad.get.leaf(staff, 0)
            >>> abjad.attach(mark, leaf, context='Staff')

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_durations(
            ...     [1.5],
            ...     cyclic=True,
            ...     fill=abjad.Exact,
            ...     in_seconds=True,
            ...     overhang=True,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])
            Selection([Note("b'8"), Note("c''8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {
                        \tempo 4=60
                        \time 2/8
                        \abjad-color-music #'red
                        c'8
                        \abjad-color-music #'red
                        d'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'blue
                        f'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'blue
                        g'8
                        \abjad-color-music #'blue
                        a'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        b'8
                        \abjad-color-music #'red
                        c''8
                    }
                }

        ..  container:: example

            Partitions leaves into a single part equal to exactly 1.5 seconds; truncates
            overhang:

            >>> staff = abjad.Staff([
            ...     abjad.Container("c'8 d'"),
            ...     abjad.Container("e'8 f'"),
            ...     abjad.Container("g'8 a'"),
            ...     abjad.Container("b'8 c''"),
            ... ])
            >>> for container in staff:
            ...     time_signature = abjad.TimeSignature((2, 8))
            ...     abjad.attach(time_signature, container[0])
            ...
            >>> abjad.setting(staff).autoBeaming = False
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> leaf = abjad.get.leaf(staff, 0)
            >>> abjad.attach(mark, leaf, context='Staff')

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_durations(
            ...     [1.5],
            ...     cyclic=False,
            ...     fill=abjad.Exact,
            ...     in_seconds=True,
            ...     overhang=False,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {
                        \tempo 4=60
                        \time 2/8
                        \abjad-color-music #'red
                        c'8
                        \abjad-color-music #'red
                        d'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        e'8
                        f'8
                    }
                    {
                        \time 2/8
                        g'8
                        a'8
                    }
                    {
                        \time 2/8
                        b'8
                        c''8
                    }
                }

        ..  container:: example

            Cyclically partitions leaves into parts equal to (or just less than) 0.75
            seconds; truncates overhang:

            >>> staff = abjad.Staff([
            ...     abjad.Container("c'8 d'"),
            ...     abjad.Container("e'8 f'"),
            ...     abjad.Container("g'8 a'"),
            ...     abjad.Container("b'8 c''"),
            ... ])
            >>> for container in staff:
            ...     time_signature = abjad.TimeSignature((2, 8))
            ...     abjad.attach(time_signature, container[0])
            ...
            >>> abjad.setting(staff).autoBeaming = False
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> leaf = abjad.get.leaf(staff, 0)
            >>> abjad.attach(mark, leaf, context='Staff')

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_durations(
            ...     [0.75],
            ...     cyclic=True,
            ...     fill=abjad.Less,
            ...     in_seconds=True,
            ...     overhang=False,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])
            Selection([Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'8")])
            Selection([Note("g'8")])
            Selection([Note("a'8")])
            Selection([Note("b'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {
                        \tempo 4=60
                        \time 2/8
                        \abjad-color-music #'red
                        c'8
                        \abjad-color-music #'blue
                        d'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'blue
                        f'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        g'8
                        \abjad-color-music #'blue
                        a'8
                    }
                    {
                        \time 2/8
                        \abjad-color-music #'red
                        b'8
                        c''8
                    }
                }

        ..  container:: example

            Partitions leaves into one part equal to (or just less than) 0.75 seconds;
            truncates overhang:

            >>> staff = abjad.Staff([
            ...     abjad.Container("c'8 d'"),
            ...     abjad.Container("e'8 f'"),
            ...     abjad.Container("g'8 a'"),
            ...     abjad.Container("b'8 c''"),
            ... ])
            >>> for container in staff:
            ...     time_signature = abjad.TimeSignature((2, 8))
            ...     abjad.attach(time_signature, container[0])
            ...
            >>> abjad.setting(staff).autoBeaming = False
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> leaf = abjad.get.leaf(staff, 0)
            >>> abjad.attach(mark, leaf, context='Staff')

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_durations(
            ...     [0.75],
            ...     cyclic=False,
            ...     fill=abjad.Less,
            ...     in_seconds=True,
            ...     overhang=False,
            ...     )
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    {
                        \tempo 4=60
                        \time 2/8
                        \abjad-color-music #'red
                        c'8
                        d'8
                    }
                    {
                        \time 2/8
                        e'8
                        f'8
                    }
                    {
                        \time 2/8
                        g'8
                        a'8
                    }
                    {
                        \time 2/8
                        b'8
                        c''8
                    }
                }

        Interprets ``fill`` as ``Exact`` when ``fill`` is none.

        Parts must equal ``durations`` exactly when ``fill`` is ``Exact``.

        Parts must be less than or equal to ``durations`` when ``fill`` is ``Less``.

        Parts must be greater or equal to ``durations`` when ``fill`` is ``More``.

        Reads ``durations`` cyclically when ``cyclic`` is true.

        Reads component durations in seconds when ``in_seconds`` is true.

        Returns remaining components at end in final part when ``overhang`` is true.
        """
        fill = fill or _enums.Exact
        durations = [_duration.Duration(_) for _ in durations]
        if cyclic:
            durations = _cyclictuple.CyclicTuple(durations)
        result = []
        part = []
        current_duration_index = 0
        target_duration = durations[current_duration_index]
        cumulative_duration = _duration.Duration(0)
        components_copy = list(self)
        while True:
            try:
                component = components_copy.pop(0)
            except IndexError:
                break
            component_duration = component._get_duration()
            if in_seconds:
                component_duration = _inspect._get_duration_in_seconds(component)
            candidate_duration = cumulative_duration + component_duration
            if candidate_duration < target_duration:
                part.append(component)
                cumulative_duration = candidate_duration
            elif candidate_duration == target_duration:
                part.append(component)
                result.append(part)
                part = []
                cumulative_duration = _duration.Duration(0)
                current_duration_index += 1
                try:
                    target_duration = durations[current_duration_index]
                except IndexError:
                    break
            elif target_duration < candidate_duration:
                if fill is _enums.Exact:
                    raise Exception("must partition exactly.")
                elif fill is _enums.Less:
                    result.append(part)
                    part = [component]
                    if in_seconds:
                        sum_ = sum([_inspect._get_duration_in_seconds(_) for _ in part])
                        cumulative_duration = _duration.Duration(sum_)
                    else:
                        sum_ = sum([_inspect._get_duration(_) for _ in part])
                        cumulative_duration = _duration.Duration(sum_)
                    current_duration_index += 1
                    try:
                        target_duration = durations[current_duration_index]
                    except IndexError:
                        break
                    if target_duration < cumulative_duration:
                        message = f"target duration {target_duration} is less"
                        message += " than cumulative duration"
                        message += f" {cumulative_duration}."
                        raise Exception(message)
                elif fill is _enums.More:
                    part.append(component)
                    result.append(part)
                    part = []
                    cumulative_duration = _duration.Duration(0)
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
        selections = [type(self)(_) for _ in result]
        return type(self)(selections)

    def partition_by_ratio(self, ratio) -> "Selection":
        r"""
        Partitions selection by ``ratio``.

        ..  container:: example

            Partitions leaves by a ratio of 1:1:

            >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_ratio((1, 1))
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("d'8"), Rest('r8'), Note("e'8"), Rest('r8')])
            Selection([Note("f'8"), Note("g'8"), Note("a'8"), Rest('r8')])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    r8
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        e'8
                        \abjad-color-music #'red
                        r8
                        \abjad-color-music #'blue
                        f'8
                    }
                    \abjad-color-music #'blue
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'blue
                    r8
                }

        ..  container:: example

            Partitions leaves by a ratio of 1:1:1:

            >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves()
            >>> result = result.partition_by_ratio((1, 1, 1))
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Note("d'8"), Rest('r8')])
            Selection([Note("e'8"), Rest('r8'), Note("f'8")])
            Selection([Note("g'8"), Note("a'8"), Rest('r8')])

            >>> abjad.label.by_selector(result, colors=["#red", "#blue", "#cyan"])
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    r8
                    \times 2/3
                    {
                        \abjad-color-music #'blue
                        e'8
                        \abjad-color-music #'blue
                        r8
                        \abjad-color-music #'blue
                        f'8
                    }
                    \abjad-color-music #'cyan
                    g'8
                    \abjad-color-music #'cyan
                    a'8
                    \abjad-color-music #'cyan
                    r8
                }

        """
        ratio = ratio or _ratio.Ratio((1,))
        ratio = _ratio.Ratio(ratio)
        counts = ratio.partition_integer(len(self))
        parts = _sequence.Sequence(self).partition_by_counts(counts=counts)
        selections = [type(self)(_) for _ in parts]
        return type(self)(selections)

    def rest(
        self, n: int, *, exclude: _typings.Strings = None, grace: bool = None
    ) -> _score.Rest:
        r"""
        Selects rest ``n``.

        ..  container:: example

            Selects rest -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).rest(-1)
            >>> result
            Rest('r16')

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \abjad-color-music #'green
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                >>

        """
        return self.rests(grace=grace)[n]

    def rests(
        self, *, exclude: _typings.Strings = None, grace: bool = None
    ) -> "Selection":
        r"""
        Selects rests.

        ..  container:: example

            Selects rests:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).rests()
            >>> for item in result:
            ...     item
            ...
            Rest('r16')
            Rest('r16')
            Rest('r16')

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            \abjad-color-music #'red
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            \abjad-color-music #'blue
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \abjad-color-music #'red
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }
                >>

        """
        return self.components(
            (_score.MultimeasureRest, _score.Rest), exclude=exclude, grace=grace
        )

    def run(self, n: int, *, exclude: _typings.Strings = None) -> "Selection":
        r"""
        Selects run ``n``.

        ..  container:: example

            Selects run -1:

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).run(-1)
            >>> result
            Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            r16
                            c'16
                            c'16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            r16
                            d'16
                            d'16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            r16
                            \abjad-color-music #'green
                            e'16
                            \abjad-color-music #'green
                            e'16
                            \abjad-color-music #'green
                            e'16
                            \abjad-color-music #'green
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'green
                            <fs' gs'>16
                        }
                    }
                >>

        """
        return self.runs(exclude=exclude)[n]

    def runs(self, *, exclude: _typings.Strings = None) -> "Selection":
        r"""
        Selects runs.

        ..  container:: example

            Selects runs:

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).runs()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16")])
            Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16")])
            Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            r16
                            \abjad-color-music #'red
                            c'16
                            \abjad-color-music #'red
                            c'16
                            \abjad-color-music #'red
                            c'16
                            \abjad-color-music #'red
                            <d' e'>4
                            ~
                            \abjad-color-music #'red
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            r16
                            \abjad-color-music #'blue
                            d'16
                            \abjad-color-music #'blue
                            d'16
                            \abjad-color-music #'blue
                            d'16
                            \abjad-color-music #'blue
                            <e' fs'>4
                            ~
                            \abjad-color-music #'blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            r16
                            \abjad-color-music #'red
                            e'16
                            \abjad-color-music #'red
                            e'16
                            \abjad-color-music #'red
                            e'16
                            \abjad-color-music #'red
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'red
                            <fs' gs'>16
                        }
                    }
                >>

        ..  container:: example

            REGRESSION. Works with grace note (and containers):

            >>> music_voice = abjad.Voice(
            ...     "c'16 d' e' r d'4 e' r8 f'", name="Music_Voice"
            ... )
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[4])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[5:7]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[-1])
            >>> staff = abjad.Staff([music_voice])

            >>> result = abjad.select(staff).runs()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'16"), Note("d'16"), Note("e'16")])
            Selection([Note("cs'16"), Note("d'4"), Chord("<e' g'>16"), Note("gs'16"), Note("a'16"), Note("as'16"), Note("e'4")])
            Selection([Note("f'8"), Note("fs'16")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'red
                        e'16
                        r16
                        \grace {
                            \abjad-color-music #'blue
                            cs'16
                        }
                        \abjad-color-music #'blue
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                \abjad-color-music #'blue
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                \abjad-color-music #'blue
                                gs'16
                                \abjad-color-music #'blue
                                a'16
                                \abjad-color-music #'blue
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo
                                \abjad-color-music #'blue
                                e'4
                                r8
                            }
                        >>
                        \oneVoice
                        \abjad-color-music #'red
                        \afterGrace
                        f'8
                        {
                            \abjad-color-music #'red
                            fs'16
                        }
                    }
                }

        """
        result = Selection.leaves(self, exclude=exclude, pitched=True)
        result = result.group_by_contiguity()
        assert isinstance(result, Selection)
        items = [Selection(_) for _ in result]
        result = type(self)(items)
        return result

    def top(self, *, exclude: _typings.Strings = None) -> "Selection":
        r"""
        Selects top components.

        ..  container:: example

            Selects top components (up from leaves):

            >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
            >>> staff = abjad.Staff(string)
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).leaves().top()
            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Note("d'8")
            Rest('r8')
            Tuplet('3:2', "e'8 r8 f'8")
            Note("g'8")
            Note("a'8")
            Rest('r8')

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    r8
                    \times 2/3
                    {
                        \abjad-color-music #'blue
                        e'8
                        \abjad-color-music #'blue
                        r8
                        \abjad-color-music #'blue
                        f'8
                    }
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'red
                    r8
                }

        """
        result: typing.List[typing.Union[_score.Component, Selection]] = []
        for component in _iterate._public_iterate_components(self, exclude=exclude):
            for component_ in _parentage.Parentage(component):
                if (
                    self._is_immediate_child_of_outermost_voice(component_)
                    and component_ not in result
                ):
                    result.append(component_)
        return type(self)(result)

    def tuplet(
        self, n: int, *, exclude: _typings.Strings = None, level: int = None
    ) -> _score.Component:
        r"""
        Selects tuplet ``n``.

        ..  container:: example

            Selects tuplet -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ...     ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = abjad.select(staff).tuplet(-1)
            >>> result
            Tuplet('9:10', "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 <fs' gs'>16")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    \with
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 3
                        autoBeaming = ##f
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \time 7/4
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9
                        {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9
                        {
                            \abjad-color-music #'green
                            r16
                            \abjad-color-music #'green
                            bf'16
                            \abjad-color-music #'green
                            <a'' b''>16
                            \abjad-color-music #'green
                            e'16
                            \abjad-color-music #'green
                            <fs' gs'>4
                            ~
                            \abjad-color-music #'green
                            <fs' gs'>16
                        }
                    }
                >>

        """
        return self.tuplets(exclude=exclude, level=level)[n]

    def tuplets(
        self, *, exclude: _typings.Strings = None, level: int = None
    ) -> "Selection":
        r"""
        Selects tuplets.

        ..  container:: example

            Selects tuplets at every level:

            >>> staff = abjad.Staff(
            ...     r"\times 2/3 { c'2 \times 2/3 { d'8 e' f' } } \times 2/3 { c'4 d' e' }"
            ... )

            >>> result = abjad.select(staff).tuplets()
            >>> for item in result:
            ...     item
            ...
            Tuplet('3:2', "c'2 { 2/3 d'8 e'8 f'8 }")
            Tuplet('3:2', "d'8 e'8 f'8")
            Tuplet('3:2', "c'4 d'4 e'4")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        c'2
                        \times 2/3
                        {
                            \abjad-color-music #'red
                            \abjad-color-music #'blue
                            d'8
                            \abjad-color-music #'red
                            \abjad-color-music #'blue
                            e'8
                            \abjad-color-music #'red
                            \abjad-color-music #'blue
                            f'8
                        }
                    }
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        c'4
                        \abjad-color-music #'red
                        d'4
                        \abjad-color-music #'red
                        e'4
                    }
                }

        ..  container:: example

            Selects tuplets at level -1:

            >>> staff = abjad.Staff(
            ...     r"\times 2/3 { c'2 \times 2/3 { d'8 e' f' } } \times 2/3 { c'4 d' e' }"
            ... )

            >>> result = abjad.select(staff).tuplets(level=-1)
            >>> for item in result:
            ...     item
            ...
            Tuplet('3:2', "d'8 e'8 f'8")
            Tuplet('3:2', "c'4 d'4 e'4")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \times 2/3
                    {
                        c'2
                        \times 2/3
                        {
                            \abjad-color-music #'red
                            d'8
                            \abjad-color-music #'red
                            e'8
                            \abjad-color-music #'red
                            f'8
                        }
                    }
                    \times 2/3
                    {
                        \abjad-color-music #'blue
                        c'4
                        \abjad-color-music #'blue
                        d'4
                        \abjad-color-music #'blue
                        e'4
                    }
                }

            Tuplets at level -1 are bottom-level tuplet: tuplets at level -1 contain only
            one tuplet (themselves) and do not contain any other tuplets.

        ..  container:: example

            Selects tuplets at level 1:

            >>> staff = abjad.Staff(
            ...     r"\times 2/3 { c'2 \times 2/3 { d'8 e' f' } } \times 2/3 { c'4 d' e' }"
            ... )

            >>> result = abjad.select(staff).tuplets(level=1)
            >>> for item in result:
            ...     item
            ...
            Tuplet('3:2', "c'2 { 2/3 d'8 e'8 f'8 }")
            Tuplet('3:2', "c'4 d'4 e'4")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \times 2/3
                    {
                        \abjad-color-music #'red
                        c'2
                        \times 2/3
                        {
                            \abjad-color-music #'red
                            d'8
                            \abjad-color-music #'red
                            e'8
                            \abjad-color-music #'red
                            f'8
                        }
                    }
                    \times 2/3
                    {
                        \abjad-color-music #'blue
                        c'4
                        \abjad-color-music #'blue
                        d'4
                        \abjad-color-music #'blue
                        e'4
                    }
                }

            Tuplets at level 1 are top-level tuplets: level-1 tuplets contain only 1
            tuplet (themselves) and are not contained by any other tuplets.

        """
        tuplets = self.components(_score.Tuplet, exclude=exclude)
        assert isinstance(tuplets, Selection)
        if level is None:
            return tuplets
        elif level < 0:
            result = []
            for tuplet in tuplets:
                count = 0
                for component in _iterate._iterate_descendants(tuplet):
                    if isinstance(component, _score.Tuplet):
                        count += 1
                if -count == level:
                    result.append(tuplet)
        else:
            result = []
            for tuplet in tuplets:
                if _parentage.Parentage(tuplet).count(_score.Tuplet) == level:
                    result.append(tuplet)
        return type(self)(result)

    # TODO: write grace examples
    def with_next_leaf(self, *, grace: bool = None) -> "Selection":
        r"""
        Extends selection with next leaf.

        ..  container:: example

            Selects runs (each with next leaf):

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).runs()
            >>> result = [abjad.select(_).with_next_leaf() for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Rest('r8')])
            Selection([Note("d'8"), Note("e'8"), Rest('r8')])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'red
                    f'8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'red
                    a'8
                }

        ..  container:: example

            Selects pitched tails (each with next leaf):

            >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties(pitched=True)
            >>> result = [abjad.select(_)[-1:].with_next_leaf() for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Rest('r8')])
            Selection([Note("d'8"), Note("e'8")])
            Selection([Note("e'8"), Rest('r8')])
            Selection([Note("f'8")])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    r8
                    d'8
                    ~
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    ~
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    f'8
                }

        ..  container:: example

            Pitched logical ties (each with next leaf) is the correct selection
            for single-pitch sustain pedal applications.

            Selects pitched logical ties (each with next leaf):

            >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.setting(staff).pedalSustainStyle = "#'mixed"

            >>> result = abjad.select(staff).logical_ties(pitched=True)
            >>> result = [abjad.select(_).with_next_leaf() for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Rest('r8')])
            Selection([Note("d'8"), Note("d'8"), Note("e'8")])
            Selection([Note("e'8"), Note("e'8"), Rest('r8')])
            Selection([Note("f'8")])

            >>> for item in result:
            ...     abjad.piano_pedal(item)
            ...

            >>> abjad.label.by_selector(result, True)
            >>> abjad.override(staff).SustainPedalLineSpanner.staff_padding = 6
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override SustainPedalLineSpanner.staff-padding = 6
                    autoBeaming = ##f
                    pedalSustainStyle = #'mixed
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \sustainOn
                    \abjad-color-music #'red
                    r8
                    \sustainOff
                    \abjad-color-music #'blue
                    d'8
                    ~
                    \sustainOn
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'blue
                    \abjad-color-music #'red
                    e'8
                    \sustainOff
                    ~
                    \sustainOn
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'red
                    r8
                    \sustainOff
                    \abjad-color-music #'blue
                    f'8
                    \sustainOff
                    \sustainOn
                }

        ..  container:: example

            REGRESSION. Works with grace note (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])

            >>> prototype = (
            ...     abjad.BeforeGraceContainer,
            ...     abjad.OnBeatGraceContainer,
            ...     abjad.AfterGraceContainer,
            ... )
            >>> result = abjad.select(staff).components(prototype)
            >>> result = [abjad.select(_).leaves().with_next_leaf() for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([Note("cs'16"), Note("d'4")])
            Selection([Chord("<e' g'>16"), Note("gs'16"), Note("a'16"), Note("as'16"), Note("e'4")])
            Selection([Note("fs'16")])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            \abjad-color-music #'red
                            cs'16
                        }
                        \abjad-color-music #'red
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                \abjad-color-music #'blue
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                \abjad-color-music #'blue
                                gs'16
                                \abjad-color-music #'blue
                                a'16
                                \abjad-color-music #'blue
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo
                                \abjad-color-music #'blue
                                e'4
                            }
                        >>
                        \oneVoice
                        \afterGrace
                        f'4
                        {
                            \abjad-color-music #'red
                            fs'16
                        }
                    }
                }

        """
        leaves = list(self.leaves())
        previous_leaf = leaves[-1]
        while True:
            next_leaf = _iterate._get_leaf(previous_leaf, n=1)
            if next_leaf is None:
                break
            if (
                grace is None
                or (grace is True and _inspect._get_grace_container(next_leaf))
                or (grace is False and not _inspect._get_grace_container(next_leaf))
            ):
                leaves.append(next_leaf)
                break
            previous_leaf = next_leaf
        return type(self)(leaves)

    def with_previous_leaf(self) -> "Selection":
        r"""
        Extends selection with previous leaf.

        ..  container:: example

            Selects runs (each with previous leaf):

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).runs()
            >>> result = [abjad.select(_).with_previous_leaf() for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])
            Selection([Rest('r8'), Note("d'8"), Note("e'8")])
            Selection([Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    f'8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'red
                    a'8
                }

        ..  container:: example

            Selects pitched heads (each with previous leaf):

            >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = abjad.select(staff).logical_ties(pitched=True)
            >>> result = [abjad.select(_)[:1].with_previous_leaf() for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])
            Selection([Rest('r8'), Note("d'8")])
            Selection([Note("d'8"), Note("e'8")])
            Selection([Rest('r8'), Note("f'8")])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    d'8
                    ~
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    ~
                    e'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    f'8
                }

        ..  container:: example

            REGRESSION. Works with grace note (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])

            >>> prototype = (
            ...     abjad.BeforeGraceContainer,
            ...     abjad.OnBeatGraceContainer,
            ...     abjad.AfterGraceContainer,
            ... )
            >>> result = abjad.select(staff).components(prototype)
            >>> result = [abjad.select(_).leaves().with_previous_leaf() for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'4"), Note("cs'16")])
            Selection([Note("d'4"), Chord("<e' g'>16"), Note("gs'16"), Note("a'16"), Note("as'16")])
            Selection([Note("f'4"), Note("fs'16")])

            >>> abjad.label.by_selector(result, True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        \abjad-color-music #'red
                        c'4
                        \grace {
                            \abjad-color-music #'red
                            cs'16
                        }
                        \abjad-color-music #'blue
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                \abjad-color-music #'blue
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                \abjad-color-music #'blue
                                gs'16
                                \abjad-color-music #'blue
                                a'16
                                \abjad-color-music #'blue
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo
                                e'4
                            }
                        >>
                        \oneVoice
                        \abjad-color-music #'red
                        \afterGrace
                        f'4
                        {
                            \abjad-color-music #'red
                            fs'16
                        }
                    }
                }

        """
        leaves = list(self.leaves())
        previous_leaf = _iterate._get_leaf(leaves[0], n=-1)
        if previous_leaf is not None:
            leaves.insert(0, previous_leaf)
        return type(self)(leaves)


class LogicalTie(Selection):
    """
    Logical tie of a component.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' ~ e'")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.select(staff[2]).logical_tie()
        LogicalTie([Note("e'4"), Note("e'4")])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets ``argument``.

        Returns component or vanilla selection (not logical tie).
        """
        result = self.items.__getitem__(argument)
        if isinstance(result, tuple):
            result = Selection(result)
        return result

    ### PRIVATE METHODS ###

    def _scale(self, multiplier):
        for leaf in list(self):
            leaf._scale(multiplier)

    ### PUBLIC PROPERTIES ###

    @property
    def head(self):
        """
        Reference to element ``0`` in logical tie.

        Returns component.
        """
        if self.items:
            return self.items[0]

    @property
    def is_pitched(self):
        """
        Is true when logical tie head is a note or chord.

        Returns true or false.
        """
        return hasattr(self.head, "written_pitch") or hasattr(
            self.head, "written_pitches"
        )

    @property
    def is_trivial(self):
        """
        Is true when length of logical tie is less than or equal to ``1``.

        Returns true or false.
        """
        return len(self) <= 1

    @property
    def leaves(self):
        """
        Gets leaves in logical tie.

        Returns selection.
        """
        return Selection(self)

    @property
    def tail(self):
        """
        Gets last leaf in logical tie.

        Returns leaf.
        """
        if self.items:
            return self.items[-1]

    @property
    def written_duration(self):
        """
        Sum of written duration of all components in logical tie.

        Returns duration.
        """
        return sum([_.written_duration for _ in self])


def select(items=None, previous=None):
    r"""
    Deprecated. Use ``abjad.Selection()`` instead.

    ..  container:: example

        Selects first two notes in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> selection = abjad.select(staff[:2]).leaves(pitched=True)
        >>> for note in selection:
        ...     abjad.override(note).NoteHead.color = "#red"

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override NoteHead.color = #red
                c'4
                \once \override NoteHead.color = #red
                d'4
                e'4
                f'4
            }

    """
    assert items is not None, repr(items)
    return Selection(items=items, previous=previous)
