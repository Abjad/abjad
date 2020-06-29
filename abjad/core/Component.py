import abc
import bisect
import collections
import copy
import importlib
import typing

import uqbar.graphs

from .. import enums, exceptions, mathtools, typings
from ..duration import Duration, Multiplier, Offset
from ..formatting import LilyPondFormatManager
from ..indicators.MetronomeMark import MetronomeMark
from ..indicators.StaffChange import StaffChange
from ..indicators.TimeSignature import TimeSignature
from ..markups import Markup
from ..pitch.pitches import NamedPitch
from ..pitch.sets import PitchSet
from ..storage import FormatSpecification, StorageFormatManager
from ..tags import Tag
from ..timespans import AnnotatedTimespan, Timespan, TimespanList
from ..top import attach, detach, iterate, mutate, override, select, setting
from ..utilities.Sequence import Sequence


class Component(object):
    """
    Component baseclass.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_indicators_are_current",
        "_is_forbidden_to_update",
        "_overrides",
        "_lilypond_setting_name_manager",
        "_measure_number",
        "_offsets_are_current",
        "_offsets_in_seconds_are_current",
        "_parent",
        "_start_offset",
        "_start_offset_in_seconds",
        "_stop_offset",
        "_stop_offset_in_seconds",
        "_tag",
        "_timespan",
        "_wrappers",
    )

    _is_abstract = True

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, name: str = None, tag: Tag = None) -> None:
        self._indicators_are_current = False
        self._is_forbidden_to_update = False
        self._measure_number = None
        self._offsets_are_current = False
        self._offsets_in_seconds_are_current = False
        self._overrides = None
        self._parent = None
        self._lilypond_setting_name_manager = None
        self._start_offset = None
        self._start_offset_in_seconds = None
        self._stop_offset = None
        self._stop_offset_in_seconds = None
        if tag is not None:
            assert isinstance(tag, Tag), repr(tag)
        self._tag = tag
        self._timespan = Timespan()
        self._wrappers: typing.List[Wrapper] = []

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies component.

        Copies indicators.

        Does not copy spanners.

        Does not copy children.

        Returns new component.
        """
        new_component = type(self)(*self.__getnewargs__())
        if getattr(self, "_overrides", None) is not None:
            manager = copy.copy(override(self))
            new_component._overrides = manager
        if getattr(self, "_lilypond_setting_name_manager", None) is not None:
            manager = copy.copy(setting(self))
            new_component._lilypond_setting_name_manager = manager
        for wrapper in inspect(self).annotation_wrappers():
            new_wrapper = copy.copy(wrapper)
            attach(new_wrapper, new_component)
        for wrapper in inspect(self).wrappers():
            new_wrapper = copy.copy(wrapper)
            attach(new_wrapper, new_component)
        return new_component

    def __format__(self, format_specification="") -> str:
        """
        Formats component.
        """
        if format_specification in ("", "lilypond"):
            string = self._get_lilypond_format()
        else:
            assert format_specification == "storage"
            string = StorageFormatManager(self).get_storage_format()
        lines = []
        for line in string.split("\n"):
            if line.isspace():
                line = ""
            lines.append(line)
        string = "\n".join(lines)
        return string

    def __getnewargs__(self):
        """
        Gets new arguments.

        Returns tuple.
        """
        return ()

    def __illustrate__(self):
        """
        Illustrates component.

        Returns LilyPond file.
        """
        from ..lilypondfile import LilyPondFile

        lilypond_file = LilyPondFile.new(self)
        return lilypond_file

    def __mul__(self, n):
        """
        Copies component `n` times and detaches spanners.

        Returns list of new components.
        """
        components = []
        for i in range(n):
            component = mutate(self).copy()
            components.append(component)
        result = select(components)
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __rmul__(self, n):
        """
        Copies component `n` times and detach spanners.

        Returns list of new components.
        """
        return self * n

    ### PRIVATE METHODS ###

    def _as_graphviz_node(self):
        score_index = inspect(self).parentage().score_index()
        score_index = "_".join(str(_) for _ in score_index)
        class_name = type(self).__name__
        if score_index:
            name = f"{class_name}_{score_index}"
        else:
            name = class_name
        node = uqbar.graphs.Node(
            name=name, attributes={"margin": 0.05, "style": "rounded"}
        )
        table = uqbar.graphs.Table(attributes={"border": 2, "cellpadding": 5})
        node.append(table)
        return node

    def _cache_named_children(self):
        name_dictionary = {}
        if hasattr(self, "_named_children"):
            for name, children in self._named_children.items():
                name_dictionary[name] = copy.copy(children)
        name = getattr(self, "name", None)
        if name is not None:
            if self.name not in name_dictionary:
                name_dictionary[self.name] = []
            name_dictionary[self.name].append(self)
        return name_dictionary

    def _check_for_cycles(self, components):
        parentage = inspect(self).parentage()
        for component in components:
            if component in parentage:
                return True
        return False

    def _extract(self):
        selection = select([self])
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        if parent is not None:
            components = list(getattr(self, "components", ()))
            parent.__setitem__(slice(start, stop + 1), components)
        return self

    def _format_absolute_after_slot(self, bundle):
        result = []
        result.append(("literals", bundle.absolute_after.commands))
        return result

    def _format_absolute_before_slot(self, bundle):
        result = []
        result.append(("literals", bundle.absolute_before.commands))
        return result

    def _format_after_slot(self, bundle):
        return []

    def _format_before_slot(self, bundle):
        return []

    def _format_close_brackets_slot(self, bundle):
        return []

    def _format_closing_slot(self, bundle):
        return []

    def _format_component(self, pieces=False):
        result = []
        bundle = LilyPondFormatManager.bundle_format_contributions(self)
        result.extend(self._format_absolute_before_slot(bundle))
        result.extend(self._format_before_slot(bundle))
        result.extend(self._format_open_brackets_slot(bundle))
        result.extend(self._format_opening_slot(bundle))
        result.extend(self._format_contents_slot(bundle))
        result.extend(self._format_closing_slot(bundle))
        result.extend(self._format_close_brackets_slot(bundle))
        result.extend(self._format_after_slot(bundle))
        result.extend(self._format_absolute_after_slot(bundle))
        contributions = []
        for contributor, contribution in result:
            contributions.extend(contribution)
        if pieces:
            return contributions
        else:
            return "\n".join(contributions)

    def _format_contents_slot(self, bundle):
        return []

    def _format_open_brackets_slot(self, bundle):
        return []

    def _format_opening_slot(self, bundle):
        return []

    @staticmethod
    def _format_slot_contributions_with_indent(slot):
        result = []
        for contributor, contributions in slot:
            strings = []
            for string in contributions:
                if string.isspace():
                    string = ""
                else:
                    string = LilyPondFormatManager.indent + string
                strings.append(string)
            pair = (contributor, strings)
            result.append(pair)
        return result

    def _get_contents(self):
        result = []
        result.append(self)
        result.extend(getattr(self, "components", []))
        result = select(result)
        return result

    def _get_descendants_starting_with(self):
        from .Container import Container

        result = []
        result.append(self)
        if isinstance(self, Container):
            if self.simultaneous:
                for x in self:
                    result.extend(x._get_descendants_starting_with())
            elif self:
                result.extend(self[0]._get_descendants_starting_with())
        return result

    def _get_descendants_stopping_with(self):
        from .Container import Container

        result = []
        result.append(self)
        if isinstance(self, Container):
            if self.simultaneous:
                for x in self:
                    result.extend(x._get_descendants_stopping_with())
            elif self:
                result.extend(self[-1]._get_descendants_stopping_with())
        return result

    def _get_duration(self, in_seconds=False):
        if in_seconds:
            return self._get_duration_in_seconds()
        elif self._parent is None:
            return self._get_preprolated_duration()
        else:
            parentage = inspect(self._parent).parentage()
            return parentage.prolation * self._get_preprolated_duration()

    def _get_effective(
        self, prototype, *, attributes=None, command=None, n=0, unwrap=True
    ):
        from .Context import Context
        from .Voice import Voice

        self._update_now(indicators=True)
        candidate_wrappers = {}
        parentage = inspect(self).parentage()
        enclosing_voice_name = None
        for component in parentage:
            if isinstance(component, Voice):
                if (
                    enclosing_voice_name is not None
                    and component.name != enclosing_voice_name
                ):
                    continue
                else:
                    enclosing_voice_name = component.name or id(component)
            local_wrappers = []
            for wrapper in component._wrappers:
                if wrapper.annotation:
                    continue
                if isinstance(wrapper.indicator, prototype):
                    append_wrapper = True
                    if command is not None and wrapper.indicator.command != command:
                        continue
                    if attributes is not None:
                        for name, value in attributes.items():
                            if getattr(wrapper.indicator, name, None) != value:
                                append_wrapper = False
                    if not append_wrapper:
                        continue
                    local_wrappers.append(wrapper)
            # active indicator takes precendence over inactive indicator
            if any(_.deactivate is True for _ in local_wrappers) and not all(
                _.deactivate is True for _ in local_wrappers
            ):
                local_wrappers = [_ for _ in local_wrappers if _.deactivate is not True]
            for wrapper in local_wrappers:
                offset = wrapper.start_offset
                candidate_wrappers.setdefault(offset, []).append(wrapper)
            if not isinstance(component, Context):
                continue
            for wrapper in component._dependent_wrappers:
                if wrapper.annotation:
                    continue
                if isinstance(wrapper.indicator, prototype):
                    append_wrapper = True
                    if command is not None and wrapper.indicator.command != command:
                        continue
                    if attributes is not None:
                        for name, value in attributes.items():
                            if getattr(wrapper.indicator, name, None) != value:
                                append_wrapper = False
                    if not append_wrapper:
                        continue
                    offset = wrapper.start_offset
                    candidate_wrappers.setdefault(offset, []).append(wrapper)
        if not candidate_wrappers:
            return
        all_offsets = sorted(candidate_wrappers)
        start_offset = inspect(self).timespan().start_offset
        index = bisect.bisect(all_offsets, start_offset) - 1 + int(n)
        if index < 0:
            return
        elif len(candidate_wrappers) <= index:
            return
        wrapper = candidate_wrappers[all_offsets[index]][0]
        if unwrap:
            return wrapper.indicator
        return wrapper

    def _get_effective_staff(self):
        from .Staff import Staff

        staff_change = self._get_effective(StaffChange)
        if staff_change is not None:
            effective_staff = staff_change.staff
        else:
            effective_staff = inspect(self).parentage().get(Staff)
        return effective_staff

    def _get_format_contributions_for_slot(self, slot_identifier, bundle=None):
        result = []
        if bundle is None:
            manager = LilyPondFormatManager
            bundle = manager.bundle_format_contributions(self)
        slot_names = (
            "before",
            "open_brackets",
            "opening",
            "contents",
            "closing",
            "close_brackets",
            "after",
        )
        if isinstance(slot_identifier, int):
            assert slot_identifier in range(1, 7 + 1)
            slot_index = slot_identifier - 1
            slot_name = slot_names[slot_index]
        elif isinstance(slot_identifier, str):
            slot_name = slot_identifier.replace(" ", "_")
            assert slot_name in slot_names
        method_name = f"_format_{slot_name}_slot"
        method = getattr(self, method_name)
        for source, contributions in method(bundle):
            result.extend(contributions)
        return result

    def _get_format_pieces(self):
        return self._format_component(pieces=True)

    def _get_format_specification(self):
        values = []
        summary = self._get_contents_summary()
        if summary:
            values.append(summary)
        return FormatSpecification(
            client=self, repr_args_values=values, storage_format_kwargs_names=[],
        )

    def _get_indicator(self, prototype=None, *, attributes=None, unwrap=True):
        indicators = self._get_indicators(
            prototype=prototype, attributes=attributes, unwrap=unwrap
        )
        if not indicators:
            raise ValueError(f"no attached indicators found matching {prototype!r}.")
        if 1 < len(indicators):
            raise ValueError(
                f"multiple attached indicators found matching {prototype!r}."
            )
        return indicators[0]

    def _get_indicators(self, prototype=None, *, attributes=None, unwrap=True):
        prototype = prototype or (object,)
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        prototype_objects, prototype_classes = [], []
        for indicator_prototype in prototype:
            if isinstance(indicator_prototype, type):
                prototype_classes.append(indicator_prototype)
            else:
                prototype_objects.append(indicator_prototype)
        prototype_objects = tuple(prototype_objects)
        prototype_classes = tuple(prototype_classes)
        result = []
        for wrapper in self._wrappers:
            if wrapper.annotation:
                continue
            if isinstance(wrapper, prototype_classes):
                result.append(wrapper)
            elif any(wrapper == _ for _ in prototype_objects):
                result.append(wrapper)
            elif isinstance(wrapper, Wrapper):
                if isinstance(wrapper.indicator, prototype_classes):
                    result.append(wrapper)
                elif any(wrapper.indicator == _ for _ in prototype_objects):
                    result.append(wrapper)
        if attributes is not None:
            result_ = []
            for wrapper in result:
                for name, value in attributes.items():
                    if getattr(wrapper.indicator, name, None) != value:
                        break
                else:
                    result_.append(wrapper)
            result = result_
        if unwrap:
            result = [_.indicator for _ in result]
        result = tuple(result)
        return result

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    def _get_markup(self, direction=None):
        markup = self._get_indicators(Markup)
        if direction is enums.Up:
            return tuple(x for x in markup if x.direction is enums.Up)
        elif direction is enums.Down:
            return tuple(x for x in markup if x.direction is enums.Down)
        return markup

    def _get_sibling(self, n):
        assert n in (-1, 0, 1), repr(self, n)
        if n == 0:
            return self
        if self._parent is None:
            return None
        if self._parent.simultaneous:
            return None
        index = self._parent.index(self) + n
        if 0 <= index < len(self._parent):
            return self._parent[index]

    def _get_sibling_with_graces(self, n):
        from .OnBeatGraceContainer import OnBeatGraceContainer

        assert n in (-1, 0, 1), repr(self, n)
        if n == 0:
            return self
        if self._parent is None:
            return None
        if self._parent.simultaneous:
            return None
        if (
            n == 1
            and getattr(self._parent, "_main_leaf", None)
            and self._parent._main_leaf._before_grace_container is self._parent
            and self is self._parent[-1]
        ):
            return self._parent._main_leaf
        # last leaf in on-beat grace redo
        if (
            n == 1
            and self is self._parent[-1]
            and isinstance(self._parent, OnBeatGraceContainer)
        ):
            return self._parent._get_on_beat_anchor_leaf()
        if (
            n == 1
            and getattr(self._parent, "_main_leaf", None)
            and self._parent._main_leaf._after_grace_container is self._parent
            and self is self._parent[-1]
        ):
            main_leaf = self._parent._main_leaf
            if main_leaf is main_leaf._parent[-1]:
                return None
            index = main_leaf._parent.index(main_leaf)
            return main_leaf._parent[index + 1]
        if n == 1 and getattr(self, "_after_grace_container", None):
            return self._after_grace_container[0]
        if (
            n == -1
            and getattr(self._parent, "_main_leaf", None)
            and self._parent._main_leaf._after_grace_container is self._parent
            and self is self._parent[0]
        ):
            return self._parent._main_leaf
        if (
            n == -1
            and getattr(self._parent, "_main_leaf", None)
            and self._parent._main_leaf._before_grace_container is self._parent
            and self is self._parent[0]
        ):
            main_leaf = self._parent._main_leaf
            if main_leaf is main_leaf._parent[0]:
                return None
            index = main_leaf._parent.index(main_leaf)
            return main_leaf._parent[index - 1]
        # self is main leaf in main voice (simultaneous with on-beat graces)
        if (
            n == -1
            and self is self._parent[0]
            and self._parent._get_on_beat_anchor_voice() is not None
        ):
            on_beat = self._parent._get_on_beat_anchor_voice()
            return on_beat[-1]
        if n == -1 and hasattr(self, "_get_on_beat_anchor_voice"):
            raise Exception(repr(self))
            on_beat = self._get_on_beat_anchor_voice()
            if on_beat is not None:
                return on_beat[-1]
        if n == -1 and getattr(self, "_before_grace_container", None):
            return self._before_grace_container[-1]
        index = self._parent.index(self) + n
        if not (0 <= index < len(self._parent)):
            return None
        candidate = self._parent[index]
        if n == 1 and getattr(candidate, "_before_grace_container", None):
            return candidate._before_grace_container[0]
        if n == -1 and getattr(candidate, "_after_grace_container", None):
            return candidate._after_grace_container[-1]
        return candidate

    def _get_timespan(self, in_seconds=False):
        if in_seconds:
            self._update_now(offsets_in_seconds=True)
            if self._start_offset_in_seconds is None:
                raise exceptions.MissingMetronomeMarkError
            return Timespan(
                start_offset=self._start_offset_in_seconds,
                stop_offset=self._stop_offset_in_seconds,
            )
        else:
            self._update_now(offsets=True)
            return self._timespan

    def _has_effective_indicator(self, prototype, *, attributes=None, command=None):
        indicator = self._get_effective(
            prototype, attributes=attributes, command=command
        )
        return indicator is not None

    def _has_indicator(self, prototype=None, *, attributes=None):
        indicators = self._get_indicators(prototype=prototype, attributes=attributes)
        return bool(indicators)

    def _immediately_precedes(self, component, ignore_before_after_grace=None):
        from .AfterGraceContainer import AfterGraceContainer
        from .BeforeGraceContainer import BeforeGraceContainer

        successors = []
        current = self
        # do not include OnBeatGraceContainer here because
        # OnBeatGraceContainer is a proper container
        grace_prototype = (AfterGraceContainer, BeforeGraceContainer)
        while current is not None:
            sibling = current._get_sibling_with_graces(1)
            while (
                ignore_before_after_grace
                and sibling is not None
                and isinstance(sibling._parent, grace_prototype)
            ):
                sibling = sibling._get_sibling_with_graces(1)
            if sibling is None:
                current = current._parent
            else:
                descendants = sibling._get_descendants_starting_with()
                successors = descendants
                break
        return component in successors

    def _move_indicators(self, recipient_component):
        for wrapper in inspect(self).wrappers():
            detach(wrapper, self)
            attach(wrapper, recipient_component)

    def _remove_from_parent(self):
        from .Context import Context

        self._update_later(offsets=True)
        for component in inspect(self).parentage()[1:]:
            if not isinstance(component, Context):
                continue
            for wrapper in component._dependent_wrappers[:]:
                if wrapper.component is self:
                    component._dependent_wrappers.remove(wrapper)
        if self._parent is not None:
            self._parent._components.remove(self)
        self._parent = None

    def _remove_named_children_from_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in inspect(self).parentage()[1:]:
                named_children = parent._named_children
                for name in name_dictionary:
                    for component in name_dictionary[name]:
                        named_children[name].remove(component)
                    if not named_children[name]:
                        del named_children[name]

    def _restore_named_children_to_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in inspect(self).parentage()[1:]:
                named_children = parent._named_children
                for name in name_dictionary:
                    if name in named_children:
                        named_children[name].extend(name_dictionary[name])
                    else:
                        named_children[name] = copy.copy(name_dictionary[name])

    def _set_parent(self, new_parent):
        """
        Not composer-safe.
        """
        named_children = self._cache_named_children()
        self._remove_named_children_from_parentage(named_children)
        self._remove_from_parent()
        self._parent = new_parent
        self._restore_named_children_to_parentage(named_children)
        self._update_later(offsets=True)

    def _sibling(self, n):
        assert n in (-1, 0, 1), repr(n)
        if n == 0:
            return self
        for parent in inspect(self).parentage():
            sibling = parent._get_sibling(mathtools.sign(n))
            if sibling is not None:
                return sibling

    def _tag_strings(self, strings):
        return LilyPondFormatManager.tag(strings, tag=self.tag)

    def _update_later(self, offsets=False, offsets_in_seconds=False):
        assert offsets or offsets_in_seconds
        for component in inspect(self).parentage():
            if offsets:
                component._offsets_are_current = False
            elif offsets_in_seconds:
                component._offsets_in_seconds_are_current = False

    def _update_measure_numbers(self):
        update_manager = UpdateManager()
        update_manager._update_measure_numbers(self)

    def _update_now(self, offsets=False, offsets_in_seconds=False, indicators=False):
        update_manager = UpdateManager()
        return update_manager._update_now(
            self,
            offsets=offsets,
            offsets_in_seconds=offsets_in_seconds,
            indicators=indicators,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self) -> typing.Optional[Tag]:
        """
        Gets component tag.
        """
        return self._tag


class UpdateManager(object):
    """
    Update manager.

    Updates start offsets, stop offsets and indicators everywhere in score.

    ..  note:: This is probably the most important part of Abjad to optimize.
        Use the profiler to figure out how many unnecessary updates are
        happening. Then reimplement. As a hint, the update manager implements
        a weird version of the "observer pattern." It may make sense to revisit
        a textbook example of the observer pattern and review the
        implementation of the update manager.

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Managers"

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Delegates to storage format manager.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_after_grace_leaf_offsets(leaf):
        container = leaf._parent
        main_leaf = container._main_leaf
        main_leaf_stop_offset = main_leaf._stop_offset
        assert main_leaf_stop_offset is not None
        displacement = -inspect(leaf).duration()
        sibling = leaf._sibling(1)
        while sibling is not None and sibling._parent is container:
            displacement -= inspect(sibling).duration()
            sibling = sibling._sibling(1)
        if leaf._parent is not None and leaf._parent._main_leaf is not None:
            main_leaf = leaf._parent._main_leaf
            sibling = main_leaf._sibling(1)
            if (
                sibling is not None
                and hasattr(sibling, "_before_grace_container")
                and sibling._before_grace_container is not None
            ):
                before_grace_container = sibling._before_grace_container
                duration = inspect(before_grace_container).duration()
                displacement -= duration
        start_offset = Offset(main_leaf_stop_offset, displacement=displacement)
        displacement += inspect(leaf).duration()
        stop_offset = Offset(main_leaf_stop_offset, displacement=displacement)
        return start_offset, stop_offset

    @staticmethod
    def _get_before_grace_leaf_offsets(leaf):
        container = leaf._parent
        main_leaf = container._main_leaf
        main_leaf_start_offset = main_leaf._start_offset
        assert main_leaf_start_offset is not None
        displacement = -inspect(leaf).duration()
        sibling = leaf._sibling(1)
        while sibling is not None and sibling._parent is container:
            displacement -= inspect(sibling).duration()
            sibling = sibling._sibling(1)
        start_offset = Offset(main_leaf_start_offset, displacement=displacement)
        displacement += inspect(leaf).duration()
        stop_offset = Offset(main_leaf_start_offset, displacement=displacement)
        return start_offset, stop_offset

    def _get_measure_start_offsets(self, component):
        wrappers = []
        prototype = TimeSignature
        root = inspect(component).parentage().root
        for component_ in self._iterate_entire_score(root):
            wrappers_ = inspect(component_).wrappers(prototype)
            wrappers.extend(wrappers_)
        pairs = []
        for wrapper in wrappers:
            component = wrapper.component
            start_offset = inspect(component).timespan().start_offset
            time_signature = wrapper.indicator
            pair = start_offset, time_signature
            pairs.append(pair)
        offset_zero = Offset(0)
        default_time_signature = TimeSignature((4, 4))
        default_pair = (offset_zero, default_time_signature)
        if pairs and not pairs[0] == offset_zero:
            pairs.insert(0, default_pair)
        elif not pairs:
            pairs = [default_pair]
        pairs.sort(key=lambda x: x[0])
        score_stop_offset = inspect(root).timespan().stop_offset
        dummy_last_pair = (score_stop_offset, None)
        pairs.append(dummy_last_pair)
        measure_start_offsets = []
        for current_pair, next_pair in Sequence(pairs).nwise():
            current_start_offset, current_time_signature = current_pair
            next_start_offset, next_time_signature = next_pair
            measure_start_offset = current_start_offset
            while measure_start_offset < next_start_offset:
                measure_start_offsets.append(measure_start_offset)
                measure_start_offset += current_time_signature.duration
        return measure_start_offsets

    @staticmethod
    def _get_on_beat_grace_leaf_offsets(leaf):
        container = leaf._parent
        anchor_leaf = container._get_on_beat_anchor_leaf()
        anchor_leaf_start_offset = anchor_leaf._start_offset
        assert anchor_leaf_start_offset is not None
        anchor_leaf_start_offset = Offset(anchor_leaf_start_offset.pair)
        start_displacement = Duration(0)
        sibling = leaf._sibling(-1)
        while sibling is not None and sibling._parent is container:
            start_displacement += inspect(sibling).duration()
            sibling = sibling._sibling(-1)
        stop_displacement = start_displacement + inspect(leaf).duration()
        if start_displacement == 0:
            start_displacement = None
        start_offset = Offset(
            anchor_leaf_start_offset.pair, displacement=start_displacement
        )
        stop_offset = Offset(
            anchor_leaf_start_offset.pair, displacement=stop_displacement
        )
        return start_offset, stop_offset

    @staticmethod
    def _get_score_tree_state_flags(parentage):
        offsets_are_current = True
        indicators_are_current = True
        offsets_in_seconds_are_current = True
        for component in parentage:
            if offsets_are_current:
                if not component._offsets_are_current:
                    offsets_are_current = False
            if indicators_are_current:
                if not component._indicators_are_current:
                    indicators_are_current = False
            if offsets_in_seconds_are_current:
                if not component._offsets_in_seconds_are_current:
                    offsets_in_seconds_are_current = False
        return (
            offsets_are_current,
            indicators_are_current,
            offsets_in_seconds_are_current,
        )

    @staticmethod
    def _iterate_entire_score(root):
        """
        NOTE: RETURNS GRACE NOTES LAST (AND OUT-OF-ORDER).
        """
        components = list(iterate(root).components(grace=False))
        graces = iterate(root).components(grace=True)
        components.extend(graces)
        return components

    def _make_metronome_mark_map(self, root):
        pairs = []
        all_stop_offsets = set()
        for component in self._iterate_entire_score(root):
            indicators = component._get_indicators(MetronomeMark)
            if len(indicators) == 1:
                metronome_mark = indicators[0]
                if not metronome_mark.is_imprecise:
                    pair = (component._start_offset, metronome_mark)
                    pairs.append(pair)
            if component._stop_offset is not None:
                all_stop_offsets.add(component._stop_offset)
        pairs.sort(key=lambda _: _[0])
        if not pairs:
            return
        if pairs[0][0] != 0:
            return
        score_stop_offset = max(all_stop_offsets)
        timespans = TimespanList()
        clocktime_start_offset = Offset(0)
        for left, right in Sequence(pairs).nwise(wrapped=True):
            metronome_mark = left[-1]
            start_offset = left[0]
            stop_offset = right[0]
            # last timespan
            if stop_offset == 0:
                stop_offset = score_stop_offset
            duration = stop_offset - start_offset
            multiplier = Multiplier(60, metronome_mark.units_per_minute)
            clocktime_duration = duration / metronome_mark.reference_duration
            clocktime_duration *= multiplier
            timespan = AnnotatedTimespan(
                start_offset=start_offset,
                stop_offset=stop_offset,
                annotation=(clocktime_start_offset, clocktime_duration),
            )
            timespans.append(timespan)
            clocktime_start_offset += clocktime_duration
        return timespans

    # TODO: reimplement with some type of bisection
    def _to_measure_number(self, component, measure_start_offsets):
        component_start_offset = inspect(component).timespan().start_offset
        displacement = component_start_offset.displacement
        if displacement is not None:
            component_start_offset = Offset(component_start_offset, displacement=None)
            # score-initial grace music only:
            if displacement < 0 and component_start_offset == 0:
                measure_number = 0
                return measure_number
        measure_start_offsets = measure_start_offsets[:]
        measure_start_offsets.append(mathtools.Infinity())
        pairs = Sequence(measure_start_offsets)
        pairs = pairs.nwise()
        for measure_index, pair in enumerate(pairs):
            if pair[0] <= component_start_offset < pair[-1]:
                measure_number = measure_index + 1
                return measure_number
        message = f"can not find measure number for {repr(component)}:\n"
        message += f"   {repr(measure_start_offsets)}"
        raise ValueError(message)

    def _update_all_indicators(self, root):
        """
        Updating indicators does not update offsets.
        On the other hand, getting an effective indicator does update
        offsets when at least one indicator of the appropriate type
        attaches to score.
        """
        components = self._iterate_entire_score(root)
        for component in components:
            for wrapper in inspect(component).wrappers():
                if wrapper.context is not None:
                    wrapper._update_effective_context()
            component._indicators_are_current = True

    def _update_all_offsets(self, root):
        """
        Updating offsets does not update indicators.
        Updating offsets does not update offsets in seconds.
        """
        from ..core.OnBeatGraceContainer import OnBeatGraceContainer

        on_beat_grace_music = []
        for component in self._iterate_entire_score(root):
            if isinstance(component, OnBeatGraceContainer) or isinstance(
                component._parent, OnBeatGraceContainer
            ):
                on_beat_grace_music.append(component)
            else:
                self._update_component_offsets(component)
                component._offsets_are_current = True
        for component in on_beat_grace_music:
            self._update_component_offsets(component)
            component._offsets_are_current = True

    def _update_all_offsets_in_seconds(self, root):
        self._update_all_offsets(root)
        timespans = self._make_metronome_mark_map(root)
        for component in self._iterate_entire_score(root):
            self._update_clocktime_offsets(component, timespans)
            component._offsets_in_seconds_are_current = True

    @staticmethod
    def _update_clocktime_offsets(component, timespans):
        if not timespans:
            return
        for timespan in timespans:
            if timespan.start_offset <= component._start_offset < timespan.stop_offset:
                pair = timespan.annotation
                clocktime_start_offset, clocktime_duration = pair
                local_offset = component._start_offset - timespan.start_offset
                multiplier = local_offset / timespan.duration
                duration = multiplier * clocktime_duration
                offset = clocktime_start_offset + duration
                component._start_offset_in_seconds = Offset(offset)
            if timespan.start_offset <= component._stop_offset < timespan.stop_offset:
                pair = timespan.annotation
                clocktime_start_offset, clocktime_duration = pair
                local_offset = component._stop_offset - timespan.start_offset
                multiplier = local_offset / timespan.duration
                duration = multiplier * clocktime_duration
                offset = clocktime_start_offset + duration
                component._stop_offset_in_seconds = Offset(offset)
                return
        if component._stop_offset == timespans[-1].stop_offset:
            pair = timespans[-1].annotation
            clocktime_start_offset, clocktime_duration = pair
            offset = clocktime_start_offset + clocktime_duration
            component._stop_offset_in_seconds = Offset(offset)
            return
        raise Exception(f"can not find {offset} in {timespans}.")

    @classmethod
    def _update_component_offsets(class_, component):
        from ..core.AfterGraceContainer import AfterGraceContainer
        from ..core.BeforeGraceContainer import BeforeGraceContainer
        from ..core.OnBeatGraceContainer import OnBeatGraceContainer

        if isinstance(component, BeforeGraceContainer):
            pair = class_._get_before_grace_leaf_offsets(component[0])
            start_offset = pair[0]
            pair = class_._get_before_grace_leaf_offsets(component[-1])
            stop_offset = pair[-1]
        elif isinstance(component._parent, BeforeGraceContainer):
            pair = class_._get_before_grace_leaf_offsets(component)
            start_offset, stop_offset = pair
        elif isinstance(component, OnBeatGraceContainer):
            pair = class_._get_on_beat_grace_leaf_offsets(component[0])
            start_offset = pair[0]
            pair = class_._get_on_beat_grace_leaf_offsets(component[-1])
            stop_offset = pair[-1]
        elif isinstance(component._parent, OnBeatGraceContainer):
            pair = class_._get_on_beat_grace_leaf_offsets(component)
            start_offset, stop_offset = pair
        elif isinstance(component, AfterGraceContainer):
            pair = class_._get_after_grace_leaf_offsets(component[0])
            start_offset = pair[0]
            pair = class_._get_after_grace_leaf_offsets(component[-1])
            stop_offset = pair[-1]
        elif isinstance(component._parent, AfterGraceContainer):
            pair = class_._get_after_grace_leaf_offsets(component)
            start_offset, stop_offset = pair
        else:
            previous = component._sibling(-1)
            if previous is not None:
                start_offset = previous._stop_offset
            else:
                start_offset = Offset(0)
            # on-beat anchor leaf:
            if (
                component._parent is not None
                and component._parent._is_on_beat_anchor_voice()
                and component is component._parent[0]
            ):
                anchor_voice = component._parent
                assert anchor_voice._is_on_beat_anchor_voice()
                on_beat_grace_container = None
                on_beat_wrapper = anchor_voice._parent
                assert on_beat_wrapper._is_on_beat_wrapper()
                index = on_beat_wrapper.index(anchor_voice)
                if index == 0:
                    on_beat_grace_container = on_beat_wrapper[1]
                else:
                    on_beat_grace_container = on_beat_wrapper[0]
                if on_beat_grace_container is not None:
                    durations = [inspect(_).duration() for _ in on_beat_grace_container]
                    start_displacement = sum(durations)
                    start_offset = Offset(start_offset, displacement=start_displacement)
            stop_offset = start_offset + component._get_duration()
        component._start_offset = start_offset
        component._stop_offset = stop_offset
        component._timespan._start_offset = start_offset
        component._timespan._stop_offset = stop_offset

    def _update_measure_numbers(self, component):
        measure_start_offsets = self._get_measure_start_offsets(component)
        root = inspect(component).parentage().root
        for component in self._iterate_entire_score(root):
            measure_number = self._to_measure_number(component, measure_start_offsets)
            component._measure_number = measure_number

    def _update_now(
        self, component, offsets=False, offsets_in_seconds=False, indicators=False,
    ):
        assert offsets or offsets_in_seconds or indicators
        if component._is_forbidden_to_update:
            return
        parentage = inspect(component).parentage()
        for parent in parentage:
            if parent._is_forbidden_to_update:
                return
            (
                offsets_are_current,
                indicators_are_current,
                offsets_in_seconds_are_current,
            ) = self._get_score_tree_state_flags(parentage)
        root = parentage.root
        if offsets and not offsets_are_current:
            self._update_all_offsets(root)
        if offsets_in_seconds and not offsets_in_seconds_are_current:
            self._update_all_offsets_in_seconds(root)
        if indicators and not indicators_are_current:
            self._update_all_indicators(root)


class Inspection(object):
    """
    Inspection.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.inspect(staff)
        Inspection(client=Staff("c'4 e'4 d'4 f'4"))

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Collaborators"

    __slots__ = ("_client",)

    ### INITIALIZER ###

    def __init__(
        self, client: typing.Union[Component, typing.Iterable[Component]] = None,
    ) -> None:
        assert not isinstance(client, str), repr(client)
        prototype = (Component, collections.abc.Iterable, type(None))
        if not isinstance(client, prototype):
            message = "must be component, nonstring iterable or none:"
            message += f" (not {client!r})."
            raise TypeError(message)
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Delegates to storage format manager.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def client(self,) -> typing.Union[Component, typing.Iterable[Component], None]:
        r"""
        Gets client.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> abjad.inspect(staff).client
            Staff("c'4 d'4 e'4 f'4")

        """
        return self._client

    ### PUBLIC METHODS ###

    def after_grace_container(self):
        r"""
        Gets after grace containers attached to component.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     container = abjad.inspect(component).after_grace_container()
            ...     print(f"{repr(component):30} {repr(container)}")
            <Staff{1}>                     None
            <Voice-"Music_Voice"{4}>       None
            Note("c'4")                    None
            BeforeGraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    None
            <<<2>>>                        None
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") None
            Chord("<e' g'>16")             None
            Note("gs'16")                  None
            Note("a'16")                   None
            Note("as'16")                  None
            Voice("e'4", name='Music_Voice') None
            Note("e'4")                    None
            Note("f'4")                    AfterGraceContainer("fs'16")
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  None

        """
        return getattr(self.client, "_after_grace_container", None)

    def annotation(
        self, annotation: typing.Any, default: typing.Any = None, unwrap: bool = True,
    ) -> typing.Any:
        r"""
        Gets annotation.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e' e' f'")
            >>> abjad.annotate(staff[0], 'default_instrument', abjad.Cello())
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    e'4
                    e'4
                    f'4
                }

            >>> string = 'default_instrument'
            >>> abjad.inspect(staff[0]).annotation(string)
            Cello()

            >>> abjad.inspect(staff[1]).annotation(string) is None
            True

            >>> abjad.inspect(staff[2]).annotation(string) is None
            True

            >>> abjad.inspect(staff[3]).annotation(string) is None
            True

            Returns default when no annotation is found:

            >>> abjad.inspect(staff[3]).annotation(string, abjad.Violin())
            Violin()

        ..  container:: example

            REGRESSION: annotation is not picked up as effective indicator:

            >>> prototype = abjad.Instrument
            >>> abjad.inspect(staff[0]).effective(prototype) is None
            True

            >>> abjad.inspect(staff[1]).effective(prototype) is None
            True

            >>> abjad.inspect(staff[2]).effective(prototype) is None
            True

            >>> abjad.inspect(staff[3]).effective(prototype) is None
            True

        """
        assert isinstance(annotation, str), repr(annotation)
        for wrapper in self.annotation_wrappers():
            if wrapper.annotation == annotation:
                if unwrap is True:
                    return wrapper.indicator
                else:
                    return wrapper
        return default

    def annotation_wrappers(self) -> typing.List["Wrapper"]:
        r"""
        Gets annotation wrappers.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e' e' f'")
            >>> abjad.annotate(staff[0], 'default_instrument', abjad.Cello())
            >>> abjad.annotate(staff[0], 'default_clef', abjad.Clef('tenor'))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    e'4
                    e'4
                    f'4
                }

            >>> for wrapper in abjad.inspect(staff[0]).annotation_wrappers():
            ...     abjad.f(wrapper)
            ...
            abjad.Wrapper(
                annotation='default_instrument',
                indicator=abjad.Cello(
                    name='cello',
                    short_name='vc.',
                    markup=abjad.Markup(
                        contents=['Cello'],
                        ),
                    short_markup=abjad.Markup(
                        contents=['Vc.'],
                        ),
                    allowable_clefs=('bass', 'tenor', 'treble'),
                    context='Staff',
                    default_tuning=abjad.Tuning(
                        pitches=abjad.PitchSegment(
                            (
                                abjad.NamedPitch('c,'),
                                abjad.NamedPitch('g,'),
                                abjad.NamedPitch('d'),
                                abjad.NamedPitch('a'),
                                ),
                            item_class=abjad.NamedPitch,
                            ),
                        ),
                    middle_c_sounding_pitch=abjad.NamedPitch("c'"),
                    pitch_range=abjad.PitchRange('[C2, G5]'),
                    primary=True,
                    ),
                tag=abjad.Tag(),
                )
            abjad.Wrapper(
                annotation='default_clef',
                indicator=abjad.Clef('tenor'),
                tag=abjad.Tag(),
                )

        """
        result = []
        for wrapper in getattr(self.client, "_wrappers", []):
            if wrapper.annotation:
                result.append(wrapper)
        return result

    def badly_formed_components(self) -> typing.List[Component]:
        r"""
        Gets badly formed components.
        """
        from .Wellformedness import Wellformedness

        manager = Wellformedness()
        violators: typing.List[Component] = []
        for violators_, total, check_name in manager(self.client):
            violators.extend(violators_)
        return violators

    def bar_line_crossing(self) -> bool:
        r"""
        Is true when client crosses bar line.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4")
            >>> time_signature = abjad.TimeSignature((3, 8))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 3/8
                    c'4
                    d'4
                    e'4
                }

            >>> for note in staff:
            ...     result = abjad.inspect(note).bar_line_crossing()
            ...     print(note, result)
            ...
            c'4 False
            d'4 True
            e'4 False

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get indicator on component.")
        time_signature = self.client._get_effective(TimeSignature)
        if time_signature is None:
            time_signature_duration = Duration(4, 4)
        else:
            time_signature_duration = time_signature.duration
        partial = getattr(time_signature, "partial", 0)
        partial = partial or 0
        start_offset = Inspection(self.client).timespan().start_offset
        shifted_start = start_offset - partial
        shifted_start %= time_signature_duration
        stop_offset = self.client._get_duration() + shifted_start
        if time_signature_duration < stop_offset:
            return True
        return False

    def before_grace_container(self):
        r"""
        Gets before-grace container attached to leaf.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     container = abjad.inspect(component).before_grace_container()
            ...     print(f"{repr(component):30} {repr(container)}")
            <Staff{1}>                     None
            <Voice-"Music_Voice"{4}>       None
            Note("c'4")                    None
            BeforeGraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    BeforeGraceContainer("cs'16")
            <<<2>>>                        None
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") None
            Chord("<e' g'>16")             None
            Note("gs'16")                  None
            Note("a'16")                   None
            Note("as'16")                  None
            Voice("e'4", name='Music_Voice') None
            Note("e'4")                    None
            Note("f'4")                    None
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  None

        """
        return getattr(self.client, "_before_grace_container", None)

    # def contents(self) -> typing.Optional["Selection"]:
    def contents(self):
        r"""
        Gets contents.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     contents = abjad.inspect(component).contents()
            ...     print(f"{repr(component)}:")
            ...     for component_ in contents:
            ...         print(f"    {repr(component_)}")
            <Staff{1}>:
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
            <Voice-"Music_Voice"{4}>:
                <Voice-"Music_Voice"{4}>
                Note("c'4")
                Note("d'4")
                <<<2>>>
                Note("f'4")
            Note("c'4"):
                Note("c'4")
            BeforeGraceContainer("cs'16"):
                BeforeGraceContainer("cs'16")
                Note("cs'16")
            Note("cs'16"):
                Note("cs'16")
            Note("d'4"):
                Note("d'4")
            <<<2>>>:
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Voice("e'4", name='Music_Voice')
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
            Chord("<e' g'>16"):
                Chord("<e' g'>16")
            Note("gs'16"):
                Note("gs'16")
            Note("a'16"):
                Note("a'16")
            Note("as'16"):
                Note("as'16")
            Voice("e'4", name='Music_Voice'):
                Voice("e'4", name='Music_Voice')
                Note("e'4")
            Note("e'4"):
                Note("e'4")
            Note("f'4"):
                Note("f'4")
            AfterGraceContainer("fs'16"):
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("fs'16"):
                Note("fs'16")

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     contents = abjad.inspect(component).contents()
            ...     print(f"{repr(component)}:")
            ...     for component_ in contents:
            ...         print(f"    {repr(component_)}")
            <Staff{4}>:
                <Staff{4}>
                TremoloContainer("c'16 e'16")
                Note("cs'4")
                TremoloContainer("d'16 f'16")
                Note("ds'4")
            TremoloContainer("c'16 e'16"):
                TremoloContainer("c'16 e'16")
                Note("c'16")
                Note("e'16")
            Note("c'16"):
                Note("c'16")
            Note("e'16"):
                Note("e'16")
            Note("cs'4"):
                Note("cs'4")
            TremoloContainer("d'16 f'16"):
                TremoloContainer("d'16 f'16")
                Note("d'16")
                Note("f'16")
            Note("d'16"):
                Note("d'16")
            Note("f'16"):
                Note("f'16")
            Note("ds'4"):
                Note("ds'4")

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get contents of component.")
        return self.client._get_contents()

    # def descendants(self) -> typing.Union["Descendants", "Selection"]:
    def descendants(self):
        r"""
        Gets descendants.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     descendants = abjad.inspect(component).descendants()
            ...     print(f"{repr(component)}:")
            ...     for component_ in descendants:
            ...         print(f"    {repr(component_)}")
            <Staff{1}>:
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("c'4")
                BeforeGraceContainer("cs'16")
                Note("cs'16")
                Note("d'4")
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
                Note("f'4")
                AfterGraceContainer("fs'16")
                Note("fs'16")
            <Voice-"Music_Voice"{4}>:
                <Voice-"Music_Voice"{4}>
                Note("c'4")
                BeforeGraceContainer("cs'16")
                Note("cs'16")
                Note("d'4")
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
                Note("f'4")
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("c'4"):
                Note("c'4")
            BeforeGraceContainer("cs'16"):
                BeforeGraceContainer("cs'16")
                Note("cs'16")
            Note("cs'16"):
                Note("cs'16")
            Note("d'4"):
                Note("d'4")
            <<<2>>>:
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
            Chord("<e' g'>16"):
                Chord("<e' g'>16")
            Note("gs'16"):
                Note("gs'16")
            Note("a'16"):
                Note("a'16")
            Note("as'16"):
                Note("as'16")
            Voice("e'4", name='Music_Voice'):
                Voice("e'4", name='Music_Voice')
                Note("e'4")
            Note("e'4"):
                Note("e'4")
            Note("f'4"):
                Note("f'4")
            AfterGraceContainer("fs'16"):
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("fs'16"):
                Note("fs'16")

        """
        from .Descendants import Descendants
        from .Selection import Selection

        if isinstance(self.client, Component):
            return Descendants(self.client)
        descendants: typing.List[Component] = []
        assert isinstance(self.client, Selection)
        for argument in self.client:
            descendants_ = Inspection(argument).descendants()
            for descendant_ in descendants_:
                if descendant_ not in descendants:
                    descendants.append(descendant_)
        result = Selection(descendants)
        return result

    def duration(self, in_seconds: bool = False) -> Duration:
        r"""
        Gets duration.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     duration = abjad.inspect(component).duration()
            ...     print(f"{repr(component):30} {repr(duration)}")
            <Staff{1}>                     Duration(1, 1)
            <Voice-"Music_Voice"{4}>       Duration(1, 1)
            Note("c'4")                    Duration(1, 4)
            BeforeGraceContainer("cs'16")        Duration(1, 16)
            Note("cs'16")                  Duration(1, 16)
            Note("d'4")                    Duration(1, 4)
            <<<2>>>                        Duration(1, 4)
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") Duration(1, 4)
            Chord("<e' g'>16")             Duration(1, 16)
            Note("gs'16")                  Duration(1, 16)
            Note("a'16")                   Duration(1, 16)
            Note("as'16")                  Duration(1, 16)
            Voice("e'4", name='Music_Voice') Duration(1, 4)
            Note("e'4")                    Duration(1, 4)
            Note("f'4")                    Duration(1, 4)
            AfterGraceContainer("fs'16")   Duration(1, 16)
            Note("fs'16")                  Duration(1, 16)

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     duration = abjad.inspect(component).duration()
            ...     print(f"{repr(component):30} {repr(duration)}")
            <Staff{4}>                     Duration(1, 1)
            TremoloContainer("c'16 e'16")  Duration(1, 4)
            Note("c'16")                   Duration(1, 8)
            Note("e'16")                   Duration(1, 8)
            Note("cs'4")                   Duration(1, 4)
            TremoloContainer("d'16 f'16")  Duration(1, 4)
            Note("d'16")                   Duration(1, 8)
            Note("f'16")                   Duration(1, 8)
            Note("ds'4")                   Duration(1, 4)

        ..  container:: example

            REGRESSION. Works with selections:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> selection = staff[:3]
            >>> abjad.inspect(selection).duration()
            Duration(3, 4)

        """
        if isinstance(self.client, Component):
            return self.client._get_duration(in_seconds=in_seconds)
        assert isinstance(self.client, collections.abc.Iterable), repr(self.client)
        durations = [Inspection(_).duration(in_seconds=in_seconds) for _ in self.client]
        return Duration(sum(durations))

    def effective(
        self,
        prototype: typings.Prototype,
        *,
        attributes: typing.Dict = None,
        default: bool = None,
        n: int = 0,
        unwrap: bool = True,
    ) -> typing.Any:
        r"""
        Gets effective indicator.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     clef = abjad.inspect(component).effective(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(clef)}")
            <Staff{1}>                     None
            <Voice-"Music_Voice"{4}>       None
            Note("c'4")                    None
            BeforeGraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    None
            <<<2>>>                        Clef('alto')
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") Clef('alto')
            Chord("<e' g'>16")             Clef('alto')
            Note("gs'16")                  Clef('alto')
            Note("a'16")                   Clef('alto')
            Note("as'16")                  Clef('alto')
            Voice("e'4", name='Music_Voice') Clef('alto')
            Note("e'4")                    Clef('alto')
            Note("f'4")                    Clef('alto')
            AfterGraceContainer("fs'16")   Clef('alto')
            Note("fs'16")                  Clef('alto')

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        \clef "alto"
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     clef = abjad.inspect(component).effective(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(clef)}")
            <Staff{4}>                     None
            TremoloContainer("c'16 e'16")  None
            Note("c'16")                   None
            Note("e'16")                   None
            Note("cs'4")                   None
            TremoloContainer("d'16 f'16")  Clef('alto')
            Note("d'16")                   Clef('alto')
            Note("f'16")                   Clef('alto')
            Note("ds'4")                   Clef('alto')

        ..  container:: example

            Arbitrary objects (like strings) can be contexted:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> abjad.attach('color', staff[1], context='Staff')
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> for component in abjad.iterate(staff).components():
            ...     string = abjad.inspect(component).effective(str)
            ...     print(component, repr(string))
            ...
            Staff("c'8 d'8 e'8 f'8") None
            c'8 None
            d'8 'color'
            e'8 'color'
            f'8 'color'

        ..  container:: example

            Scans forwards or backwards when ``n`` is set:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8")
            >>> abjad.attach('red', staff[0], context='Staff')
            >>> abjad.attach('blue', staff[2], context='Staff')
            >>> abjad.attach('yellow', staff[4], context='Staff')
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                    g'8
                }

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[0]).effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 None
            0 'red'
            1 'blue'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[1]).effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 None
            0 'red'
            1 'blue'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[2]).effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 'red'
            0 'blue'
            1 'yellow'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[3]).effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 'red'
            0 'blue'
            1 'yellow'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[4]).effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 'blue'
            0 'yellow'
            1 None

        ..  container:: example

            Use synthetic offsets to hide a clef before the start of a staff
            like this:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.attach(
            ...     abjad.Clef("treble", hide=True),
            ...     staff[0],
            ...     synthetic_offset=-1,
            ...     )
            >>> abjad.attach(abjad.Clef("alto"), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> for leaf in staff:
            ...     clef = abjad.inspect(leaf).effective(abjad.Clef)
            ...     (leaf, clef)
            ...
            (Note("c'4"), Clef('alto'))
            (Note("d'4"), Clef('alto'))
            (Note("e'4"), Clef('alto'))
            (Note("f'4"), Clef('alto'))

            >>> abjad.inspect(staff[0]).effective(abjad.Clef)
            Clef('alto')

            >>> abjad.inspect(staff[0]).effective(abjad.Clef, n=-1)
            Clef('treble', hide=True)

            >>> abjad.inspect(staff[0]).effective(abjad.Clef, n=-2) is None
            True

            Note that ``hide=True`` is set on the offset clef to prevent
            duplicate clef commands in LilyPond output.

            Note also that the order of attachment (offset versus non-offset)
            makes no difference.

        ..  container:: example

            Here's how to hide a clef after the end of a staff:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.attach(abjad.Clef("treble"), staff[0])
            >>> abjad.attach(
            ...     abjad.Clef("alto", hide=True),
            ...     staff[-1],
            ...     synthetic_offset=1,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "treble"
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> for leaf in staff:
            ...     clef = abjad.inspect(leaf).effective(abjad.Clef)
            ...     (leaf, clef)
            ...
            (Note("c'4"), Clef('treble'))
            (Note("d'4"), Clef('treble'))
            (Note("e'4"), Clef('treble'))
            (Note("f'4"), Clef('treble'))

            >>> abjad.inspect(staff[-1]).effective(abjad.Clef)
            Clef('treble')

            >>> abjad.inspect(staff[-1]).effective(abjad.Clef, n=1)
            Clef('alto', hide=True)

            >>> abjad.inspect(staff[-1]).effective(abjad.Clef, n=2) is None
            True

        ..  container:: example

            Gets effective time signature:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> leaves = abjad.select(staff).leaves()
            >>> abjad.attach(abjad.TimeSignature((3, 8)), leaves[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 3/8
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> prototype = abjad.TimeSignature
            >>> for component in abjad.iterate(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     time_signature = inspection.effective(prototype)
            ...     print(component, time_signature)
            ...
            Staff("c'4 d'4 e'4 f'4") 3/8
            c'4 3/8
            d'4 3/8
            e'4 3/8
            f'4 3/8

        ..  container:: example

            Test attributes like this:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> staff = abjad.Staff([voice])
            >>> start_text_span = abjad.StartTextSpan()
            >>> abjad.attach(start_text_span, voice[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, voice[2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \new Voice
                    {
                        c'4
                        \startTextSpan
                        d'4
                        e'4
                        \stopTextSpan
                        f'4
                    }
                }

            >>> for note in abjad.select(staff).notes():
            ...     note, abjad.inspect(note).effective(abjad.StartTextSpan)
            ...
            (Note("c'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("d'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("e'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("f'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))

            >>> for note in abjad.select(staff).notes():
            ...     note, abjad.inspect(note).effective(abjad.StopTextSpan)
            ...
            (Note("c'4"), None)
            (Note("d'4"), None)
            (Note("e'4"), StopTextSpan(command='\\stopTextSpan'))
            (Note("f'4"), StopTextSpan(command='\\stopTextSpan'))

            >>> attributes = {'parameter': 'TEXT_SPANNER'}
            >>> for note in abjad.select(staff).notes():
            ...     indicator = abjad.inspect(note).effective(
            ...         object,
            ...         attributes=attributes,
            ...         )
            ...     note, indicator
            ...
            (Note("c'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("d'4"), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5))
            (Note("e'4"), StopTextSpan(command='\\stopTextSpan'))
            (Note("f'4"), StopTextSpan(command='\\stopTextSpan'))

        ..  container:: example

            REGRESSION. Matching start-beam and stop-beam indicators work
            correctly:

            >>> voice = abjad.Voice("c'8 d'8 e'8 f'8 g'4 a'4")
            >>> abjad.attach(abjad.StartBeam(), voice[0])
            >>> abjad.attach(abjad.StopBeam(), voice[3])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'8
                    [
                    d'8
                    e'8
                    f'8
                    ]
                    g'4
                    a'4
                }

            >>> for leaf in abjad.select(voice).leaves():
            ...     start_beam = abjad.inspect(leaf).effective(abjad.StartBeam)
            ...     stop_beam = abjad.inspect(leaf).effective(abjad.StopBeam)
            ...     leaf, start_beam, stop_beam
            (Note("c'8"), StartBeam(), None)
            (Note("d'8"), StartBeam(), None)
            (Note("e'8"), StartBeam(), None)
            (Note("f'8"), StartBeam(), StopBeam())
            (Note("g'4"), StartBeam(), StopBeam())
            (Note("a'4"), StartBeam(), StopBeam())

            # TODO: make this work.

        ..  container:: example

            REGRESSION. Bar lines work like this:

            >>> voice = abjad.Voice("c'2 d'2 e'2 f'2")
            >>> score = abjad.Score([voice])
            >>> abjad.attach(abjad.BarLine("||"), voice[1])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Voice
                    {
                        c'2
                        d'2
                        \bar "||"
                        e'2
                        f'2
                    }
                >>

            >>> for leaf in abjad.select(score).leaves():
            ...     bar_line = abjad.inspect(leaf).effective(abjad.BarLine)
            ...     leaf, bar_line
            (Note("c'2"), None)
            (Note("d'2"), BarLine('||', format_slot='after'))
            (Note("e'2"), BarLine('||', format_slot='after'))
            (Note("f'2"), BarLine('||', format_slot='after'))

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get effective on components.")
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        result = self.client._get_effective(
            prototype, attributes=attributes, n=n, unwrap=unwrap
        )
        if result is None:
            result = default
        return result

    # def effective_staff(self) -> typing.Optional["Staff"]:
    def effective_staff(self):
        r"""
        Gets effective staff.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     staff = abjad.inspect(component).effective_staff()
            ...     print(f"{repr(component):30} {repr(staff)}")
            <Staff{1}>                     <Staff{1}>
            <Voice-"Music_Voice"{4}>       <Staff{1}>
            Note("c'4")                    <Staff{1}>
            BeforeGraceContainer("cs'16")        <Staff{1}>
            Note("cs'16")                  <Staff{1}>
            Note("d'4")                    <Staff{1}>
            <<<2>>>                        <Staff{1}>
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") <Staff{1}>
            Chord("<e' g'>16")             <Staff{1}>
            Note("gs'16")                  <Staff{1}>
            Note("a'16")                   <Staff{1}>
            Note("as'16")                  <Staff{1}>
            Voice("e'4", name='Music_Voice') <Staff{1}>
            Note("e'4")                    <Staff{1}>
            Note("f'4")                    <Staff{1}>
            AfterGraceContainer("fs'16")   <Staff{1}>
            Note("fs'16")                  <Staff{1}>

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get effective staff on components.")
        return self.client._get_effective_staff()

    def effective_wrapper(
        self,
        prototype: typings.Prototype,
        *,
        attributes: typing.Dict = None,
        n: int = 0,
    ) -> typing.Optional["Wrapper"]:
        r"""
        Gets effective wrapper.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     wrapper = inspection.effective_wrapper(abjad.Clef)
            ...     print(f"{repr(component):}")
            ...     print(f"    {repr(wrapper)}")
            <Staff{1}>
                None
            <Voice-"Music_Voice"{4}>
                None
            Note("c'4")
                None
            BeforeGraceContainer("cs'16")
                None
            Note("cs'16")
                None
            Note("d'4")
                None
            <<<2>>>
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Chord("<e' g'>16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("gs'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("a'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("as'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Voice("e'4", name='Music_Voice')
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("e'4")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("f'4")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            AfterGraceContainer("fs'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            Note("fs'16")
                Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())

        """
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.effective(prototype, attributes=attributes, n=n, unwrap=False)

    def grace(self) -> bool:
        r"""
        Is true when client is grace music.

        Grace music defined equal to grace container, after-grace container and
        contents of those containers.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).grace()
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     False
            <Voice-"Music_Voice"{4}>       False
            Note("c'4")                    False
            BeforeGraceContainer("cs'16")        True
            Note("cs'16")                  True
            Note("d'4")                    False
            <<<2>>>                        False
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") True
            Chord("<e' g'>16")             True
            Note("gs'16")                  True
            Note("a'16")                   True
            Note("as'16")                  True
            Voice("e'4", name='Music_Voice') False
            Note("e'4")                    False
            Note("f'4")                    False
            AfterGraceContainer("fs'16")   True
            Note("fs'16")                  True


        """
        from .AfterGraceContainer import AfterGraceContainer
        from .BeforeGraceContainer import BeforeGraceContainer
        from .OnBeatGraceContainer import OnBeatGraceContainer

        prototype = (
            AfterGraceContainer,
            BeforeGraceContainer,
            OnBeatGraceContainer,
        )
        if isinstance(self.client, prototype):
            return True
        for component in Inspection(self.client).parentage():
            if isinstance(component, prototype):
                return True
        return False

    def has_effective_indicator(
        self, prototype: typings.Prototype = None, *, attributes: typing.Dict = None,
    ) -> bool:
        r"""
        Is true when client has effective indicator.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     result = inspection.has_effective_indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     False
            <Voice-"Music_Voice"{4}>       False
            Note("c'4")                    False
            BeforeGraceContainer("cs'16")        False
            Note("cs'16")                  False
            Note("d'4")                    False
            <<<2>>>                        True
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") True
            Chord("<e' g'>16")             True
            Note("gs'16")                  True
            Note("a'16")                   True
            Note("as'16")                  True
            Voice("e'4", name='Music_Voice') True
            Note("e'4")                    True
            Note("f'4")                    True
            AfterGraceContainer("fs'16")   True
            Note("fs'16")                  True

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        \clef "alto"
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     result = inspection.has_effective_indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{4}>                     False
            TremoloContainer("c'16 e'16")  False
            Note("c'16")                   False
            Note("e'16")                   False
            Note("cs'4")                   False
            TremoloContainer("d'16 f'16")  True
            Note("d'16")                   True
            Note("f'16")                   True
            Note("ds'4")                   True

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get effective indicator on component.")
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.client._has_effective_indicator(
            prototype=prototype, attributes=attributes
        )

    def has_indicator(
        self, prototype: typings.Prototype = None, *, attributes: typing.Dict = None,
    ) -> bool:
        r"""
        Is true when client has one or more indicators.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     result = inspection.has_indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     False
            <Voice-"Music_Voice"{4}>       False
            Note("c'4")                    False
            BeforeGraceContainer("cs'16")        False
            Note("cs'16")                  False
            Note("d'4")                    False
            <<<2>>>                        False
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") False
            Chord("<e' g'>16")             True
            Note("gs'16")                  False
            Note("a'16")                   False
            Note("as'16")                  False
            Voice("e'4", name='Music_Voice') False
            Note("e'4")                    False
            Note("f'4")                    False
            AfterGraceContainer("fs'16")   False
            Note("fs'16")                  False

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        \clef "alto"
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     result = inspection.has_indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{4}>                     False
            TremoloContainer("c'16 e'16")  False
            Note("c'16")                   False
            Note("e'16")                   False
            Note("cs'4")                   False
            TremoloContainer("d'16 f'16")  False
            Note("d'16")                   True
            Note("f'16")                   False
            Note("ds'4")                   False

        ..  container:: example

            Set ``attributes`` dictionary to test indicator attributes:

            >>> voice = abjad.Voice("c'4 c'4 c'4 c'4")
            >>> abjad.attach(abjad.Clef('treble'), voice[0])
            >>> abjad.attach(abjad.Clef('alto'), voice[2])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    \clef "treble"
                    c'4
                    c'4
                    \clef "alto"
                    c'4
                    c'4
                }

            >>> attributes = {'name': 'alto'}
            >>> abjad.inspect(voice[0]).has_indicator(abjad.Clef)
            True

            >>> abjad.inspect(voice[0]).has_indicator(
            ...     abjad.Clef,
            ...     attributes=attributes,
            ...     )
            False

            >>> abjad.inspect(voice[2]).has_indicator(abjad.Clef)
            True

            >>> abjad.inspect(voice[2]).has_indicator(
            ...     abjad.Clef,
            ...     attributes=attributes,
            ...     )
            True


        """
        if isinstance(prototype, Tag):
            raise Exception("do not attach tags; use tag=None keyword.")
        if not isinstance(self.client, Component):
            raise Exception("can only get indicator on component.")
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.client._has_indicator(prototype=prototype, attributes=attributes)

    def indicator(
        self,
        prototype: typings.Prototype = None,
        *,
        default: typing.Any = None,
        unwrap: bool = True,
    ) -> typing.Any:
        r"""
        Gets indicator.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     None
            <Voice-"Music_Voice"{4}>       None
            Note("c'4")                    None
            BeforeGraceContainer("cs'16")        None
            Note("cs'16")                  None
            Note("d'4")                    None
            <<<2>>>                        None
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") None
            Chord("<e' g'>16")             Clef('alto')
            Note("gs'16")                  None
            Note("a'16")                   None
            Note("as'16")                  None
            Voice("e'4", name='Music_Voice') None
            Note("e'4")                    None
            Note("f'4")                    None
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  None

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        \clef "alto"
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).indicator(abjad.Clef)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{4}>                     None
            TremoloContainer("c'16 e'16")  None
            Note("c'16")                   None
            Note("e'16")                   None
            Note("cs'4")                   None
            TremoloContainer("d'16 f'16")  None
            Note("d'16")                   Clef('alto')
            Note("f'16")                   None
            Note("ds'4")                   None

        Raises exception when more than one indicator of ``prototype`` attach
        to client.

        Returns default when no indicator of ``prototype`` attaches to client.
        """
        if not isinstance(self.client, Component):
            raise Exception("can only get indicator on component.")
        indicators = self.client._get_indicators(prototype=prototype, unwrap=unwrap)
        if not indicators:
            return default
        elif len(indicators) == 1:
            return list(indicators)[0]
        else:
            raise Exception("multiple indicators attached to client.")

    def indicators(
        self,
        prototype: typings.Prototype = None,
        *,
        attributes: typing.Dict = None,
        unwrap: bool = True,
    ) -> typing.List:
        r"""
        Get indicators.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> for note in abjad.select(staff).notes():
            ...     abjad.attach(abjad.Staccato(), note)

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \staccato
                        \grace {
                            cs'16
                            \staccato
                        }
                        d'4
                        \staccato
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                \staccato
                                a'16
                                \staccato
                                as'16
                                )
                                ]
                                \staccato
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                                \staccato
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        \staccato
                        {
                            fs'16
                            \staccato
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).indicators()
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     []
            <Voice-"Music_Voice"{4}>       []
            Note("c'4")                    [Staccato()]
            BeforeGraceContainer("cs'16")  []
            Note("cs'16")                  [Staccato()]
            Note("d'4")                    [Staccato()]
            <<<2>>>                        []
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") [LilyPondLiteral('\\set fontSize = #-3', format_slot='opening')]
            Chord("<e' g'>16")             [StartBeam(), LilyPondLiteral('\\slash', format_slot='opening'), StartSlur(), LilyPondLiteral('\\voiceOne', format_slot='opening'), Clef('alto'), Articulation('>')]
            Note("gs'16")                  [Staccato()]
            Note("a'16")                   [Staccato()]
            Note("as'16")                  [StopBeam(), StopSlur(), Staccato()]
            Voice("e'4", name='Music_Voice') []
            Note("e'4")                    [LilyPondLiteral('\\voiceTwo', format_slot='opening'), Staccato()]
            Note("f'4")                    [LilyPondLiteral('\\oneVoice', format_slot='absolute_before'), Staccato()]
            AfterGraceContainer("fs'16")   []
            Note("fs'16")                  [Staccato()]

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> abjad.attach(abjad.Clef("alto"), staff[-1][0])
            >>> staff.append("ds'4")
            >>> for note in abjad.select(staff).notes():
            ...     abjad.attach(abjad.Staccato(), note)

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        \staccato
                        e'16
                        \staccato
                    }
                    cs'4
                    \staccato
                    \repeat tremolo 2 {
                        \clef "alto"
                        d'16
                        \staccato
                        f'16
                        \staccato
                    }
                    ds'4
                    \staccato
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).indicators()
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{4}>                     []
            TremoloContainer("c'16 e'16")  []
            Note("c'16")                   [Staccato()]
            Note("e'16")                   [Staccato()]
            Note("cs'4")                   [Staccato()]
            TremoloContainer("d'16 f'16")  []
            Note("d'16")                   [Clef('alto'), Staccato()]
            Note("f'16")                   [Staccato()]
            Note("ds'4")                   [Staccato()]

        """
        # TODO: extend to any non-none client
        if not isinstance(self.client, Component):
            message = "can only get indicators on component"
            message += f" (not {self.client!r})."
            raise Exception(message)
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        result = self.client._get_indicators(
            prototype=prototype, attributes=attributes, unwrap=unwrap
        )
        return list(result)

    # def leaf(self, n: int = 0) -> typing.Optional["Leaf"]:
    def leaf(self, n: int = 0):
        r"""
        Gets leaf ``n``.

        :param n: constrained to -1, 0, 1 for previous, current, next leaf.

        ..  container:: example

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Voice("c'8 d'8 e'8 f'8"))
            >>> staff.append(abjad.Voice("g'8 a'8 b'8 c''8"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \new Voice
                    {
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                }

        ..  container:: example

            Gets leaf **FROM** client when client is a leaf:

            >>> leaf = staff[0][1]

            >>> abjad.inspect(leaf).leaf(-1)
            Note("c'8")

            >>> abjad.inspect(leaf).leaf(0)
            Note("d'8")

            >>> abjad.inspect(leaf).leaf(1)
            Note("e'8")

        ..  container:: example

            Gets leaf **IN** client when client is a container:

            >>> voice = staff[0]

            >>> abjad.inspect(voice).leaf(-1)
            Note("f'8")

            >>> abjad.inspect(voice).leaf(0)
            Note("c'8")

            >>> abjad.inspect(voice).leaf(1)
            Note("d'8")

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for current_leaf in abjad.select(staff).leaves():
            ...     previous_leaf = abjad.inspect(current_leaf).leaf(-1)
            ...     next_leaf = abjad.inspect(current_leaf).leaf(1)
            ...     print(f"previous leaf: {repr(previous_leaf)}")
            ...     print(f"current leaf:  {repr(current_leaf)}")
            ...     print(f"next leaf:     {repr(next_leaf)}")
            ...     print("---")
            previous leaf: None
            current leaf:  Note("c'4")
            next leaf:     Note("cs'16")
            ---
            previous leaf: Note("c'4")
            current leaf:  Note("cs'16")
            next leaf:     Note("d'4")
            ---
            previous leaf: Note("cs'16")
            current leaf:  Note("d'4")
            next leaf:     Chord("<e' g'>16")
            ---
            previous leaf: Note("d'4")
            current leaf:  Chord("<e' g'>16")
            next leaf:     Note("gs'16")
            ---
            previous leaf: Chord("<e' g'>16")
            current leaf:  Note("gs'16")
            next leaf:     Note("a'16")
            ---
            previous leaf: Note("gs'16")
            current leaf:  Note("a'16")
            next leaf:     Note("as'16")
            ---
            previous leaf: Note("a'16")
            current leaf:  Note("as'16")
            next leaf:     Note("e'4")
            ---
            previous leaf: Note("as'16")
            current leaf:  Note("e'4")
            next leaf:     Note("f'4")
            ---
            previous leaf: Note("e'4")
            current leaf:  Note("f'4")
            next leaf:     Note("fs'16")
            ---
            previous leaf: Note("f'4")
            current leaf:  Note("fs'16")
            next leaf:     None
            ---

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for current_leaf in abjad.select(staff).leaves():
            ...     previous_leaf = abjad.inspect(current_leaf).leaf(-1)
            ...     next_leaf = abjad.inspect(current_leaf).leaf(1)
            ...     print(f"previous leaf: {repr(previous_leaf)}")
            ...     print(f"current leaf:  {repr(current_leaf)}")
            ...     print(f"next leaf:     {repr(next_leaf)}")
            ...     print("---")
            previous leaf: None
            current leaf:  Note("c'16")
            next leaf:     Note("e'16")
            ---
            previous leaf: Note("c'16")
            current leaf:  Note("e'16")
            next leaf:     Note("cs'4")
            ---
            previous leaf: Note("e'16")
            current leaf:  Note("cs'4")
            next leaf:     Note("d'16")
            ---
            previous leaf: Note("cs'4")
            current leaf:  Note("d'16")
            next leaf:     Note("f'16")
            ---
            previous leaf: Note("d'16")
            current leaf:  Note("f'16")
            next leaf:     Note("ds'4")
            ---
            previous leaf: Note("f'16")
            current leaf:  Note("ds'4")
            next leaf:     None
            ---

        """
        from .Leaf import Leaf

        if n not in (-1, 0, 1):
            message = "n must be -1, 0 or 1:\n"
            message += f"   {repr(n)}"
            raise Exception(message)
        if isinstance(self.client, Leaf):
            candidate = self.client._get_sibling_with_graces(n)
            if isinstance(candidate, Leaf):
                return candidate
            return self.client._leaf(n)
        if 0 <= n:
            reverse = False
        else:
            reverse = True
            n = abs(n) - 1
        leaves = iterate(self.client).leaves(reverse=reverse)
        for i, leaf in enumerate(leaves):
            if i == n:
                return leaf
        return None

    # def lineage(self) -> "Lineage":
    def lineage(self):
        r"""
        Gets lineage.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     lineage = abjad.inspect(component).lineage()
            ...     print(f"{repr(component)}:")
            ...     for component_ in lineage:
            ...         print(f"    {repr(component_)}")
            <Staff{1}>:
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("c'4")
                BeforeGraceContainer("cs'16")
                Note("cs'16")
                Note("d'4")
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
                Note("f'4")
                AfterGraceContainer("fs'16")
                Note("fs'16")
            <Voice-"Music_Voice"{4}>:
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("c'4")
                BeforeGraceContainer("cs'16")
                Note("cs'16")
                Note("d'4")
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
                Note("f'4")
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("c'4"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("c'4")
            BeforeGraceContainer("cs'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                BeforeGraceContainer("cs'16")
                Note("cs'16")
            Note("cs'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                BeforeGraceContainer("cs'16")
                Note("cs'16")
            Note("d'4"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("d'4")
            <<<2>>>:
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
                Voice("e'4", name='Music_Voice')
                Note("e'4")
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
                Note("gs'16")
                Note("a'16")
                Note("as'16")
            Chord("<e' g'>16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Chord("<e' g'>16")
            Note("gs'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Note("gs'16")
            Note("a'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Note("a'16")
            Note("as'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                Note("as'16")
            Voice("e'4", name='Music_Voice'):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                Voice("e'4", name='Music_Voice')
                Note("e'4")
            Note("e'4"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                <<<2>>>
                Voice("e'4", name='Music_Voice')
                Note("e'4")
            Note("f'4"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                Note("f'4")
            AfterGraceContainer("fs'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                AfterGraceContainer("fs'16")
                Note("fs'16")
            Note("fs'16"):
                <Staff{1}>
                <Voice-"Music_Voice"{4}>
                AfterGraceContainer("fs'16")
                Note("fs'16")

        """
        from .Lineage import Lineage

        if not isinstance(self.client, Component):
            raise Exception("can only get lineage on component.")
        return Lineage(self.client)

    # def logical_tie(self) -> "LogicalTie":
    def logical_tie(self):
        r"""
        Gets logical tie.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for leaf in abjad.select(staff).leaves():
            ...     lt = abjad.inspect(leaf).logical_tie()
            ...     print(f"{repr(leaf):30} {repr(lt)}")
            Note("c'4")                    LogicalTie([Note("c'4")])
            Note("cs'16")                  LogicalTie([Note("cs'16")])
            Note("d'4")                    LogicalTie([Note("d'4")])
            Chord("<e' g'>16")             LogicalTie([Chord("<e' g'>16")])
            Note("gs'16")                  LogicalTie([Note("gs'16")])
            Note("a'16")                   LogicalTie([Note("a'16")])
            Note("as'16")                  LogicalTie([Note("as'16")])
            Note("e'4")                    LogicalTie([Note("e'4")])
            Note("f'4")                    LogicalTie([Note("f'4")])
            Note("fs'16")                  LogicalTie([Note("fs'16")])

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for leaf in abjad.select(staff).leaves():
            ...     lt = abjad.inspect(leaf).logical_tie()
            ...     print(f"{repr(leaf):30} {repr(lt)}")
            Note("c'16")                   LogicalTie([Note("c'16")])
            Note("e'16")                   LogicalTie([Note("e'16")])
            Note("cs'4")                   LogicalTie([Note("cs'4")])
            Note("d'16")                   LogicalTie([Note("d'16")])
            Note("f'16")                   LogicalTie([Note("f'16")])
            Note("ds'4")                   LogicalTie([Note("ds'4")])

        """
        from .Leaf import Leaf

        if not isinstance(self.client, Leaf):
            raise Exception("can only get logical tie on leaf.")
        return self.client._get_logical_tie()

    def markup(
        self, *, direction: enums.VerticalAlignment = None
    ) -> typing.List[Markup]:
        """
        Gets markup.
        """
        # TODO: extend to any non-none client
        if not isinstance(self.client, Component):
            raise Exception("can only get markup on component.")
        result = self.client._get_markup(direction=direction)
        return list(result)

    def measure_number(self) -> int:
        r"""
        Gets measure number.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     measure_number = abjad.inspect(component).measure_number()
            ...     print(f"{repr(component):30} {measure_number}")
            <Staff{1}>                     1
            <Voice-"Music_Voice"{4}>       1
            Note("c'4")                    1
            BeforeGraceContainer("cs'16")        1
            Note("cs'16")                  1
            Note("d'4")                    1
            <<<2>>>                        1
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") 1
            Chord("<e' g'>16")             1
            Note("gs'16")                  1
            Note("a'16")                   1
            Note("as'16")                  1
            Voice("e'4", name='Music_Voice') 1
            Note("e'4")                    1
            Note("f'4")                    1
            AfterGraceContainer("fs'16")   1
            Note("fs'16")                  1

        ..  container:: example

            REGRESSION. Measure number of score-initial grace notes is set
            equal to 0:

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> container = abjad.BeforeGraceContainer("b16")
            >>> abjad.attach(container, voice[0])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    \grace {
                        b16
                    }
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> for component in abjad.select(voice).components():
            ...     measure_number = abjad.inspect(component).measure_number()
            ...     print(f"{repr(component):30} {measure_number}")
            Voice("c'4 d'4 e'4 f'4")       1
            BeforeGraceContainer('b16')          0
            Note('b16')                    0
            Note("c'4")                    1
            Note("d'4")                    1
            Note("e'4")                    1
            Note("f'4")                    1

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     measure_number = abjad.inspect(component).measure_number()
            ...     print(f"{repr(component):30} {measure_number}")
            <Staff{4}>                     1
            TremoloContainer("c'16 e'16")  1
            Note("c'16")                   1
            Note("e'16")                   1
            Note("cs'4")                   1
            TremoloContainer("d'16 f'16")  1
            Note("d'16")                   1
            Note("f'16")                   1
            Note("ds'4")                   1

        """
        if not isinstance(self.client, Component):
            raise Exception("can only get measure number on component.")
        self.client._update_measure_numbers()
        assert isinstance(self.client._measure_number, int)
        return self.client._measure_number

    # def parentage(self) -> "Parentage":
    def parentage(self):
        r"""
        Gets parentage.

        ..  container:: example

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.inspect(component).parentage()
            ...     print(f"{repr(component)}:")
            ...     for component_ in parentage[:]:
            ...         print(f"    {repr(component_)}")
            <Staff{1}>:
                <Staff{1}>
            <Voice-"Music_Voice"{4}>:
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("c'4"):
                Note("c'4")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            BeforeGraceContainer("cs'16"):
                BeforeGraceContainer("cs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("cs'16"):
                Note("cs'16")
                BeforeGraceContainer("cs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("d'4"):
                Note("d'4")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            <<<2>>>:
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16"):
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Chord("<e' g'>16"):
                Chord("<e' g'>16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("gs'16"):
                Note("gs'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("a'16"):
                Note("a'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("as'16"):
                Note("as'16")
                OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16")
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Voice("e'4", name='Music_Voice'):
                Voice("e'4", name='Music_Voice')
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("e'4"):
                Note("e'4")
                Voice("e'4", name='Music_Voice')
                <<<2>>>
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("f'4"):
                Note("f'4")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            AfterGraceContainer("fs'16"):
                AfterGraceContainer("fs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>
            Note("fs'16"):
                Note("fs'16")
                AfterGraceContainer("fs'16")
                <Voice-"Music_Voice"{4}>
                <Staff{1}>

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.inspect(component).parentage()
            ...     print(f"{repr(component)}:")
            ...     print(f"    {repr(parentage[:])}")
            <Staff{4}>:
                (<Staff{4}>,)
            TremoloContainer("c'16 e'16"):
                (TremoloContainer("c'16 e'16"), <Staff{4}>)
            Note("c'16"):
                (Note("c'16"), TremoloContainer("c'16 e'16"), <Staff{4}>)
            Note("e'16"):
                (Note("e'16"), TremoloContainer("c'16 e'16"), <Staff{4}>)
            Note("cs'4"):
                (Note("cs'4"), <Staff{4}>)
            TremoloContainer("d'16 f'16"):
                (TremoloContainer("d'16 f'16"), <Staff{4}>)
            Note("d'16"):
                (Note("d'16"), TremoloContainer("d'16 f'16"), <Staff{4}>)
            Note("f'16"):
                (Note("f'16"), TremoloContainer("d'16 f'16"), <Staff{4}>)
            Note("ds'4"):
                (Note("ds'4"), <Staff{4}>)

        """
        from .Parentage import Parentage

        if not isinstance(self.client, Component):
            message = "can only get parentage on component"
            message += f" (not {self.client})."
            raise Exception(message)
        return Parentage(self.client)

    def pitches(self) -> typing.Optional[PitchSet]:
        r"""
        Gets pitches.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     pitches = abjad.inspect(component).pitches()
            ...     print(f"{repr(component):30} {repr(pitches)}")
            <Staff{1}>                     PitchSet(["c'", "cs'", "d'", "e'", "f'", "fs'", "g'", "gs'", "a'", "as'"])
            <Voice-"Music_Voice"{4}>       PitchSet(["c'", "cs'", "d'", "e'", "f'", "fs'", "g'", "gs'", "a'", "as'"])
            Note("c'4")                    PitchSet(["c'"])
            BeforeGraceContainer("cs'16")        PitchSet(["cs'"])
            Note("cs'16")                  PitchSet(["cs'"])
            Note("d'4")                    PitchSet(["d'"])
            <<<2>>>                        PitchSet(["e'", "g'", "gs'", "a'", "as'"])
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") PitchSet(["e'", "g'", "gs'", "a'", "as'"])
            Chord("<e' g'>16")             PitchSet(["e'", "g'"])
            Note("gs'16")                  PitchSet(["gs'"])
            Note("a'16")                   PitchSet(["a'"])
            Note("as'16")                  PitchSet(["as'"])
            Voice("e'4", name='Music_Voice') PitchSet(["e'"])
            Note("e'4")                    PitchSet(["e'"])
            Note("f'4")                    PitchSet(["f'"])
            AfterGraceContainer("fs'16")   PitchSet(["fs'"])
            Note("fs'16")                  PitchSet(["fs'"])

        """
        from .Selection import Selection

        if not self.client:
            return None
        selection = Selection(self.client)
        return PitchSet.from_selection(selection)

    def report_modifications(self) -> str:
        r"""
        Reports modifications.

        ..  container:: example

            Reports container modifications:

            >>> container = abjad.Container("c'8 d'8 e'8 f'8")
            >>> abjad.override(container).note_head.color = 'red'
            >>> abjad.override(container).note_head.style = 'harmonic'
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    \override NoteHead.color = #red
                    \override NoteHead.style = #'harmonic
                    c'8
                    d'8
                    e'8
                    f'8
                    \revert NoteHead.color
                    \revert NoteHead.style
                }

            >>> report = abjad.inspect(container).report_modifications()
            >>> print(report)
            {
                \override NoteHead.color = #red
                \override NoteHead.style = #'harmonic
                %%% 4 components omitted %%%
                \revert NoteHead.color
                \revert NoteHead.style
            }

        ..  container:: example

            Reports leaf modifications:

            >>> container = abjad.Container("c'8 d'8 e'8 f'8")
            >>> abjad.attach(abjad.Clef('alto'), container[0])
            >>> abjad.override(container[0]).note_head.color = 'red'
            >>> abjad.override(container[0]).stem.color = 'red'
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    \clef "alto"
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> report = abjad.inspect(container[0]).report_modifications()
            >>> print(report)
            slot "absolute before":
            slot "before":
                grob overrides:
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
            slot "opening":
                commands:
                    \clef "alto"
            slot "contents slot":
                leaf body:
                    c'8
            slot "closing":
            slot "after":
            slot "absolute after":

        """
        from .Container import Container
        from .Leaf import Leaf

        if isinstance(self.client, Container):
            bundle = LilyPondFormatManager.bundle_format_contributions(self.client)
            result: typing.List[str] = []
            for slot in ("before", "open brackets", "opening"):
                lines = self.client._get_format_contributions_for_slot(slot, bundle)
                result.extend(lines)
            line = f"    %%% {len(self.client)} components omitted %%%"
            result.append(line)
            for slot in ("closing", "close brackets", "after"):
                lines = self.client._get_format_contributions_for_slot(slot, bundle)
                result.extend(lines)
            return "\n".join(result)
        elif isinstance(self.client, Leaf):
            return self.client._report_format_contributions()
        else:
            return f"only defined for components: {self.client}."

    def sounding_pitch(self) -> NamedPitch:
        r"""
        Gets sounding pitch of note.

        ..  container:: example

            >>> staff = abjad.Staff("d''8 e''8 f''8 g''8")
            >>> piccolo = abjad.Piccolo()
            >>> abjad.attach(piccolo, staff[0])
            >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    d'8
                    e'8
                    f'8
                    g'8
                }

            >>> for note in abjad.select(staff).notes():
            ...     pitch = abjad.inspect(note).sounding_pitch()
            ...     print(f"{repr(note):10} {repr(pitch)}")
            Note("d'8") NamedPitch("d''")
            Note("e'8") NamedPitch("e''")
            Note("f'8") NamedPitch("f''")
            Note("g'8") NamedPitch("g''")

        """
        from .Note import Note

        if not isinstance(self.client, Note):
            raise Exception("can only get sounding pitch of note.")
        return self.client._get_sounding_pitch()

    def sounding_pitches(self) -> PitchSet:
        r"""
        Gets sounding pitches.

        ..  container:: example

            >>> staff = abjad.Staff("<c''' e'''>4 <d''' fs'''>4")
            >>> glockenspiel = abjad.Glockenspiel()
            >>> abjad.attach(glockenspiel, staff[0])
            >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    <c' e'>4
                    <d' fs'>4
                }

            >>> for chord in abjad.select(staff).chords():
            ...     pitches = abjad.inspect(chord).sounding_pitches()
            ...     print(f"{repr(chord):20} {repr(pitches)}")
            Chord("<c' e'>4")    PitchSet(["c'''", "e'''"])
            Chord("<d' fs'>4")   PitchSet(["d'''", "fs'''"])

        """
        from .Chord import Chord

        # TODO: extend to any non-none client
        if not isinstance(self.client, Chord):
            raise Exception("can only get sounding pitches of chord.")
        result = self.client._get_sounding_pitches()
        return PitchSet(result)

    def tabulate_wellformedness(
        self,
        check_beamed_long_notes: bool = True,
        check_duplicate_ids: bool = True,
        check_empty_containers: bool = True,
        check_missing_parents: bool = True,
        check_notes_on_wrong_clef: bool = True,
        check_out_of_range_pitches: bool = True,
        check_overlapping_text_spanners: bool = True,
        check_unmatched_stop_text_spans: bool = True,
        check_unterminated_hairpins: bool = True,
        check_unterminated_text_spanners: bool = True,
    ) -> str:
        r"""
        Tabulates wellformedness.
        """
        from .Wellformedness import Wellformedness

        manager = Wellformedness()
        triples = manager(self.client)
        strings = []
        for violators, total, check_name in triples:
            if eval(check_name) is not True:
                continue
            violator_count = len(violators)
            check_name = check_name.replace("check_", "")
            check_name = check_name.replace("_", " ")
            string = f"{violator_count} /\t{total} {check_name}"
            strings.append(string)
        return "\n".join(strings)

    def timespan(self, in_seconds: bool = False) -> Timespan:
        r"""
        Gets timespan.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

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
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \grace {
                            cs'16
                        }
                        d'4
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                a'16
                                as'16
                                )
                                ]
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        {
                            fs'16
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     timespan = abjad.inspect(component).timespan()
            ...     print(f"{repr(component):30} {repr(timespan)}")
            <Staff{1}>                     Timespan(Offset((0, 1)), Offset((1, 1)))
            <Voice-"Music_Voice"{4}>       Timespan(Offset((0, 1)), Offset((1, 1)))
            Note("c'4")                    Timespan(Offset((0, 1)), Offset((1, 4)))
            BeforeGraceContainer("cs'16")        Timespan(Offset((1, 4), displacement=Duration(-1, 16)), Offset((1, 4)))
            Note("cs'16")                  Timespan(Offset((1, 4), displacement=Duration(-1, 16)), Offset((1, 4)))
            Note("d'4")                    Timespan(Offset((1, 4)), Offset((1, 2)))
            <<<2>>>                        Timespan(Offset((1, 2)), Offset((3, 4)))
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") Timespan(Offset((1, 2)), Offset((1, 2), displacement=Duration(1, 4)))
            Chord("<e' g'>16")             Timespan(Offset((1, 2)), Offset((1, 2), displacement=Duration(1, 16)))
            Note("gs'16")                  Timespan(Offset((1, 2), displacement=Duration(1, 16)), Offset((1, 2), displacement=Duration(1, 8)))
            Note("a'16")                   Timespan(Offset((1, 2), displacement=Duration(1, 8)), Offset((1, 2), displacement=Duration(3, 16)))
            Note("as'16")                  Timespan(Offset((1, 2), displacement=Duration(3, 16)), Offset((1, 2), displacement=Duration(1, 4)))
            Voice("e'4", name='Music_Voice') Timespan(Offset((1, 2)), Offset((3, 4)))
            Note("e'4")                    Timespan(Offset((1, 2), displacement=Duration(1, 4)), Offset((3, 4)))
            Note("f'4")                    Timespan(Offset((3, 4)), Offset((1, 1)))
            AfterGraceContainer("fs'16")   Timespan(Offset((1, 1), displacement=Duration(-1, 16)), Offset((1, 1)))
            Note("fs'16")                  Timespan(Offset((1, 1), displacement=Duration(-1, 16)), Offset((1, 1)))

        ..  container:: example

            REGRESSSION. Works with tremolo containers:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
            >>> staff.append("cs'4")
            >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
            >>> staff.append("ds'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \repeat tremolo 2 {
                        c'16
                        e'16
                    }
                    cs'4
                    \repeat tremolo 2 {
                        d'16
                        f'16
                    }
                    ds'4
                }

            >>> for component in abjad.select(staff).components():
            ...     timespan = abjad.inspect(component).timespan()
            ...     print(f"{repr(component):30} {repr(timespan)}")
            <Staff{4}>                     Timespan(Offset((0, 1)), Offset((1, 1)))
            TremoloContainer("c'16 e'16")  Timespan(Offset((0, 1)), Offset((1, 4)))
            Note("c'16")                   Timespan(Offset((0, 1)), Offset((1, 8)))
            Note("e'16")                   Timespan(Offset((1, 8)), Offset((1, 4)))
            Note("cs'4")                   Timespan(Offset((1, 4)), Offset((1, 2)))
            TremoloContainer("d'16 f'16")  Timespan(Offset((1, 2)), Offset((3, 4)))
            Note("d'16")                   Timespan(Offset((1, 2)), Offset((5, 8)))
            Note("f'16")                   Timespan(Offset((5, 8)), Offset((3, 4)))
            Note("ds'4")                   Timespan(Offset((3, 4)), Offset((1, 1)))

        ..  container:: example

            REGRESION. Works with selection:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> abjad.inspect(staff[:3]).timespan()
            Timespan(Offset((0, 1)), Offset((3, 4)))

        """
        if isinstance(self.client, Component):
            return self.client._get_timespan(in_seconds=in_seconds)
        assert isinstance(self.client, collections.abc.Iterable), repr(self.client)
        remaining_items = []
        for i, item in enumerate(self.client):
            if i == 0:
                first_item = item
            else:
                remaining_items.append(item)
        timespan = Inspection(first_item).timespan(in_seconds=in_seconds)
        start_offset = timespan.start_offset
        stop_offset = timespan.stop_offset
        for item in remaining_items:
            timespan = Inspection(item).timespan(in_seconds=in_seconds)
            if timespan.start_offset < start_offset:
                start_offset = timespan.start_offset
            if stop_offset < timespan.stop_offset:
                stop_offset = timespan.stop_offset
        return Timespan(start_offset, stop_offset)

    def wellformed(
        self,
        check_beamed_long_notes: bool = True,
        check_duplicate_ids: bool = True,
        check_empty_containers: bool = True,
        check_missing_parents: bool = True,
        check_notes_on_wrong_clef: bool = True,
        check_out_of_range_pitches: bool = True,
        check_overlapping_text_spanners: bool = True,
        check_unmatched_stop_text_spans: bool = True,
        check_unterminated_hairpins: bool = True,
        check_unterminated_text_spanners: bool = True,
    ) -> bool:
        """
        Is true when client is wellformed.
        """
        from .Wellformedness import Wellformedness

        manager = Wellformedness()
        for violators, total, check_name in manager(self.client):
            if eval(check_name) is not True:
                continue
            if violators:
                return False
        return True

    def wrapper(
        self, prototype: typings.Prototype = None, *, attributes: typing.Dict = None,
    ) -> typing.Optional["Wrapper"]:
        r"""
        Gets wrapper.

        ..  container:: example

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> for note in abjad.select(staff).notes():
            ...     abjad.attach(abjad.Staccato(), note)

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \staccato
                        \grace {
                            cs'16
                            \staccato
                        }
                        d'4
                        \staccato
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                \staccato
                                a'16
                                \staccato
                                as'16
                                )
                                ]
                                \staccato
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                                \staccato
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        \staccato
                        {
                            fs'16
                            \staccato
                        }
                    }
                }

            REGRESSION. Works with grace notes (and containers):

            >>> for component in abjad.select(staff).components():
            ...     wrapper = abjad.inspect(component).wrapper(abjad.Staccato)
            ...     print(f"{repr(component):30} {repr(wrapper)}")
            <Staff{1}>                     None
            <Voice-"Music_Voice"{4}>       None
            Note("c'4")                    Wrapper(indicator=Staccato(), tag=Tag())
            BeforeGraceContainer("cs'16")        None
            Note("cs'16")                  Wrapper(indicator=Staccato(), tag=Tag())
            Note("d'4")                    Wrapper(indicator=Staccato(), tag=Tag())
            <<<2>>>                        None
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") None
            Chord("<e' g'>16")             None
            Note("gs'16")                  Wrapper(indicator=Staccato(), tag=Tag())
            Note("a'16")                   Wrapper(indicator=Staccato(), tag=Tag())
            Note("as'16")                  Wrapper(indicator=Staccato(), tag=Tag())
            Voice("e'4", name='Music_Voice') None
            Note("e'4")                    Wrapper(indicator=Staccato(), tag=Tag())
            Note("f'4")                    Wrapper(indicator=Staccato(), tag=Tag())
            AfterGraceContainer("fs'16")   None
            Note("fs'16")                  Wrapper(indicator=Staccato(), tag=Tag())

        Raises exception when more than one indicator of ``prototype`` attach
        to client.
        """
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.indicator(prototype=prototype, unwrap=False)

    def wrappers(
        self, prototype: typings.Prototype = None, *, attributes: typing.Dict = None,
    ) -> typing.Optional[typing.List["Wrapper"]]:
        r"""
        Gets wrappers.

        ..  container:: example

            REGRESSION. Works with grace notes (and containers):

            >>> music_voice = abjad.Voice("c'4 d' e' f'", name="Music_Voice")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, music_voice[1])
            >>> container = abjad.on_beat_grace_container(
            ...     "g'16 gs' a' as'", music_voice[2:3]
            ... )
            >>> abjad.attach(abjad.Clef("alto"), container[0])
            >>> abjad.attach(abjad.Articulation(">"), container[0])
            >>> container = abjad.AfterGraceContainer("fs'16")
            >>> abjad.attach(container, music_voice[3])
            >>> staff = abjad.Staff([music_voice])
            >>> for note in abjad.select(staff).notes():
            ...     abjad.attach(abjad.Staccato(), note)

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \context Voice = "Music_Voice"
                    {
                        c'4
                        \staccato
                        \grace {
                            cs'16
                            \staccato
                        }
                        d'4
                        \staccato
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3 %! abjad.on_beat_grace_container(1)
                                \clef "alto"
                                \slash %! abjad.on_beat_grace_container(2)
                                \voiceOne %! abjad.on_beat_grace_container(3)
                                <
                                    \tweak font-size #0
                                    \tweak transparent ##t
                                    e'
                                    g'
                                >16
                                - \accent
                                [
                                (
                                gs'16
                                \staccato
                                a'16
                                \staccato
                                as'16
                                )
                                ]
                                \staccato
                            }
                            \context Voice = "Music_Voice"
                            {
                                \voiceTwo %! abjad.on_beat_grace_container(4)
                                e'4
                                \staccato
                            }
                        >>
                        \oneVoice %! abjad.on_beat_grace_container(5)
                        \afterGrace
                        f'4
                        \staccato
                        {
                            fs'16
                            \staccato
                        }
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     result = abjad.inspect(component).wrappers(abjad.Staccato)
            ...     print(f"{repr(component):30} {repr(result)}")
            <Staff{1}>                     []
            <Voice-"Music_Voice"{4}>       []
            Note("c'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            BeforeGraceContainer("cs'16")        []
            Note("cs'16")                  [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("d'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            <<<2>>>                        []
            OnBeatGraceContainer("<e' g'>16 gs'16 a'16 as'16") []
            Chord("<e' g'>16")             []
            Note("gs'16")                  [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("a'16")                   [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("as'16")                  [Wrapper(indicator=Staccato(), tag=Tag())]
            Voice("e'4", name='Music_Voice') []
            Note("e'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            Note("f'4")                    [Wrapper(indicator=Staccato(), tag=Tag())]
            AfterGraceContainer("fs'16")   []
            Note("fs'16")                  [Wrapper(indicator=Staccato(), tag=Tag())]

        """
        if attributes is not None:
            assert isinstance(attributes, dict), repr(attributes)
        return self.indicators(prototype=prototype, unwrap=False)


### FUNCTIONS ###


def inspect(client):
    r"""
    Makes inspection agent.

    ..  container:: example

        Example staff:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Gets duration of first note in staff:

        >>> abjad.inspect(staff[0]).duration()
        Duration(1, 4)

    ..  container:: example

        Returns inspection agent:

        >>> abjad.inspect(staff)
        Inspection(client=Staff("c'4 e'4 d'4 f'4"))

    """
    return Inspection(client=client)


class Wrapper(object):
    r"""
    Wrapper.

    ..  container:: example

        >>> component = abjad.Note("c'4")
        >>> articulation = abjad.Articulation('accent', direction=abjad.Up)
        >>> abjad.attach(articulation, component)
        >>> wrapper = abjad.inspect(component).wrapper()

        >>> abjad.f(wrapper)
        abjad.Wrapper(
            indicator=abjad.Articulation('accent', Up),
            tag=abjad.Tag(),
            )

    ..  container:: example

        Duplicate indicator warnings take two forms.

        >>> voice_1 = abjad.Voice("c''4 d'' e'' f''", name='VoiceI')
        >>> voice_2 = abjad.Voice("c'4 d' e' f'", name='VoiceII')
        >>> abjad.attach(abjad.Clef('alto'), voice_2[0])
        >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            <<
                \context Voice = "VoiceI"
                {
                    c''4
                    d''4
                    e''4
                    f''4
                }
                \context Voice = "VoiceII"
                {
                    \clef "alto"
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>

        First form when attempting to attach a contexted indicator to a leaf
        that already carries a contexted indicator of the same type:

        >>> abjad.attach(abjad.Clef('treble'), voice_2[0])
        Traceback (most recent call last):
            ...
        abjad...PersistentIndicatorError:
        <BLANKLINE>
        Can not attach ...
        <BLANKLINE>
        abjad.Wrapper(
            context='Staff',
            indicator=abjad.Clef('treble'),
            tag=abjad.Tag(),
            )
        <BLANKLINE>
            ... to Note("c'4") in VoiceII because ...
        <BLANKLINE>
        abjad.Wrapper(
            context='Staff',
            indicator=abjad.Clef('alto'),
            tag=abjad.Tag(),
            )
        <BLANKLINE>
            ... is already attached to the same leaf.
        <BLANKLINE>

        Second form when attempting to attach a contexted indicator to a leaf
        governed by some other component carrying a contexted indicator of the
        same type.

        >>> abjad.attach(abjad.Clef('treble'), voice_1[0])
        Traceback (most recent call last):
            ...
        abjad...PersistentIndicatorError:
        <BLANKLINE>
        Can not attach ...
        <BLANKLINE>
            abjad.Wrapper(
                context='Staff',
                indicator=abjad.Clef('treble'),
                tag=abjad.Tag(),
                )
        <BLANKLINE>
            ... to Note("c''4") in VoiceI because ...
        <BLANKLINE>
        abjad.Wrapper(
            context='Staff',
            indicator=abjad.Clef('alto'),
            tag=abjad.Tag(),
            )
        <BLANKLINE>
            ... is already attached to Note("c'4") in VoiceII.
        <BLANKLINE>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Internals"

    __slots__ = (
        "_annotation",
        "_component",
        "_context",
        "_deactivate",
        "_effective_context",
        "_indicator",
        "_synthetic_offset",
        "_tag",
    )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        annotation: str = None,
        component=None,
        context: str = None,
        deactivate: bool = None,
        indicator: typing.Any = None,
        synthetic_offset: int = None,
        tag: typing.Union[str, Tag] = None,
    ) -> None:
        from ..core.Component import Component

        assert not isinstance(indicator, type(self)), repr(indicator)
        if annotation is not None:
            assert isinstance(annotation, str), repr(annotation)
        self._annotation = annotation
        if component is not None:
            assert isinstance(component, Component), repr(component)
        self._component = component
        if deactivate is not None:
            deactivate = bool(deactivate)
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if deactivate is not None:
            deactivate = bool(deactivate)
        self._deactivate = deactivate
        self._effective_context = None
        self._indicator = indicator
        if synthetic_offset is not None:
            synthetic_offset = Offset(synthetic_offset)
        self._synthetic_offset = synthetic_offset
        if tag is not None:
            assert isinstance(tag, (str, Tag))
        tag = Tag(tag)
        self._tag: Tag = tag
        if component is not None:
            self._bind_component(component)

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments) -> "Wrapper":
        r"""
        Copies wrapper.

        ..  container:: example

            Preserves annotation flag:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.annotate(old_staff[0], 'bow_direction', abjad.Down)
            >>> abjad.f(old_staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = old_staff[0]
            >>> abjad.inspect(leaf).annotation('bow_direction')
            Down

            >>> new_staff = abjad.mutate(old_staff).copy()
            >>> abjad.f(new_staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = new_staff[0]
            >>> abjad.inspect(leaf).annotation("bow_direction")
            Down

        ..  container:: example

            Preserves tag:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> clef = abjad.Clef("alto")
            >>> abjad.attach(clef, old_staff[0], tag=abjad.Tag("RED:M1"))
            >>> abjad.f(old_staff)
            \new Staff {
                \clef "alto" %! RED:M1
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = old_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                context='Staff',
                indicator=abjad.Clef('alto'),
                tag=abjad.Tag('RED:M1'),
                )

            >>> new_staff = abjad.mutate(old_staff).copy()
            >>> abjad.f(new_staff)
            \new Staff {
                \clef "alto" %! RED:M1
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = new_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                context='Staff',
                indicator=abjad.Clef('alto'),
                tag=abjad.Tag('RED:M1'),
                )

        ..  container:: example

            Preserves deactivate flag:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.attach(
            ...     abjad.Clef('alto'),
            ...     old_staff[0],
            ...     deactivate=True,
            ...     tag=abjad.Tag("RED:M1"),
            ...     )
            >>> abjad.f(old_staff)
            \new Staff {
                %@% \clef "alto" %! RED:M1
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = old_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                context='Staff',
                deactivate=True,
                indicator=abjad.Clef('alto'),
                tag=abjad.Tag('RED:M1'),
                )

            >>> new_staff = abjad.mutate(old_staff).copy()
            >>> abjad.f(new_staff)
            \new Staff {
                %@% \clef "alto" %! RED:M1
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = new_staff[0]
            >>> wrapper = abjad.inspect(leaf).wrapper()
            >>> abjad.f(wrapper)
            abjad.Wrapper(
                context='Staff',
                deactivate=True,
                indicator=abjad.Clef('alto'),
                tag=abjad.Tag('RED:M1'),
                )

        Copies all properties except component.

        Copy operations must supply component after wrapper copy.
        """
        new = type(self)(
            annotation=self.annotation,
            component=None,
            context=self.context,
            deactivate=self.deactivate,
            indicator=copy.copy(self.indicator),
            synthetic_offset=self.synthetic_offset,
            tag=self.tag,
        )
        return new

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Formats Abjad object.

        Set ``format_specification`` to ``''`` or ``'storage'``.
        Interprets ``''`` equal to ``'storage'``.
        """
        if format_specification in ("", "storage"):
            return StorageFormatManager(self).get_storage_format()
        return str(self)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _bind_component(self, component):
        if getattr(self.indicator, "context", None) is not None:
            self._warn_duplicate_indicator(component)
            self._unbind_component()
            self._component = component
            self._update_effective_context()
            if getattr(self.indicator, "_mutates_offsets_in_seconds", False):
                self._component._update_later(offsets_in_seconds=True)
        component._wrappers.append(self)

    def _bind_effective_context(self, correct_effective_context):
        self._unbind_effective_context()
        if correct_effective_context is not None:
            correct_effective_context._dependent_wrappers.append(self)
        self._effective_context = correct_effective_context
        self._update_effective_context()
        if getattr(self.indicator, "_mutates_offsets_in_seconds", False):
            correct_effective_context._update_later(offsets_in_seconds=True)

    def _detach(self):
        self._unbind_component()
        self._unbind_effective_context()
        return self

    def _find_correct_effective_context(self):
        abjad = importlib.import_module("abjad")
        if self.context is None:
            return None
        context = getattr(abjad, self.context, self.context)
        candidate = None
        parentage = inspect(self.component).parentage()
        if isinstance(context, type):
            for component in parentage:
                if not hasattr(component, "_lilypond_type"):
                    continue
                if isinstance(component, context):
                    candidate = component
                    break
        elif isinstance(context, str):
            for component in parentage:
                if not hasattr(component, "_lilypond_type"):
                    continue
                if component.name == context or component.lilypond_type == context:
                    candidate = component
                    break
        else:
            raise TypeError("must be context or string: {context!r}.")
        if candidate.__class__.__name__ == "Voice":
            for component in reversed(parentage):
                if not component.__class__.__name__ == "Voice":
                    continue
                if component.name == candidate.name:
                    candidate = component
                    break
        return candidate

    def _get_effective_context(self):
        if self.component is not None:
            self.component._update_now(indicators=True)
        return self._effective_context

    def _get_format_pieces(self):
        result = []
        if self.annotation:
            return result
        if hasattr(self.indicator, "_get_lilypond_format_bundle"):
            bundle = self.indicator._get_lilypond_format_bundle(self.component)
            bundle.tag_format_contributions(self.tag, deactivate=self.deactivate)
            return bundle
        try:
            context = self._get_effective_context()
            lilypond_format = self.indicator._get_lilypond_format(context=context)
        except TypeError:
            lilypond_format = self.indicator._get_lilypond_format()
        if isinstance(lilypond_format, str):
            lilypond_format = [lilypond_format]
        assert isinstance(lilypond_format, (tuple, list))
        lilypond_format = LilyPondFormatManager.tag(
            lilypond_format, self.tag, deactivate=self.deactivate
        )
        result.extend(lilypond_format)
        if self._get_effective_context() is not None:
            return result
        result = [rf"%%% {_} %%%" for _ in result]
        return result

    def _get_format_specification(self):
        keywords = [
            "annotation",
            "context",
            "deactivate",
            "indicator",
            "synthetic_offset",
            "tag",
        ]
        return FormatSpecification(
            client=self,
            storage_format_args_values=None,
            storage_format_kwargs_names=keywords,
        )

    def _unbind_component(self):
        if self._component is not None and self in self._component._wrappers:
            self._component._wrappers.remove(self)
        self._component = None

    def _unbind_effective_context(self):
        if (
            self._effective_context is not None
            and self in self._effective_context._dependent_wrappers
        ):
            self._effective_context._dependent_wrappers.remove(self)
        self._effective_context = None

    def _update_effective_context(self):
        correct_effective_context = self._find_correct_effective_context()
        # print(correct_effective_context)
        if self._effective_context is not correct_effective_context:
            self._bind_effective_context(correct_effective_context)

    def _warn_duplicate_indicator(self, component):
        from ..core.Context import Context

        if self.deactivate is True:
            return
        prototype = type(self.indicator)
        command = getattr(self.indicator, "command", None)
        wrapper = inspect(component).effective_wrapper(
            prototype, attributes={"command": command}
        )
        wrapper_format_slot = None
        if wrapper is not None:
            wrapper_format_slot = getattr(wrapper.indicator, "format_slot", None)
        my_format_slot = getattr(self.indicator, "format_slot", None)
        if (
            wrapper is None
            or wrapper.context is None
            or wrapper.deactivate is True
            or wrapper.start_offset != self.start_offset
            or wrapper_format_slot != my_format_slot
        ):
            return
        my_leak = getattr(self.indicator, "leak", None)
        if getattr(wrapper.indicator, "leak", None) != my_leak:
            return
        context = inspect(component).parentage().get(Context)
        parentage = inspect(wrapper.component).parentage()
        wrapper_context = parentage.get(Context)
        if wrapper.indicator == self.indicator and context is not wrapper_context:
            return
        message = f"\n\nCan not attach ...\n\n{self}\n\n..."
        message += f" to {repr(component)}"
        message += f" in {getattr(context, 'name', None)} because ..."
        message += f"\n\n{format(wrapper)}\n\n"
        message += "... is already attached"
        if component is wrapper.component:
            message += " to the same leaf."
        else:
            message += f" to {repr(wrapper.component)}"
            message += f" in {wrapper_context.name}."
        message += "\n"
        raise exceptions.PersistentIndicatorError(message)

    ### PUBLIC PROPERTIES ###

    @property
    def annotation(self) -> typing.Optional[str]:
        """
        Gets wrapper annotation.

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation('accent', direction=abjad.Up)
            >>> abjad.attach(articulation, note)
            >>> wrapper = abjad.inspect(note).wrapper()
            >>> wrapper.annotation is None
            True

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation('accent', direction=abjad.Up)
            >>> abjad.annotate(note, 'foo', articulation)
            >>> abjad.inspect(note).annotation('foo')
            Articulation('accent', Up)

        """
        return self._annotation

    @property
    def component(self):
        """
        Gets start component.

        Returns component or none.
        """
        return self._component

    @property
    def context(self) -> typing.Optional[str]:
        """
        Gets context (name).
        """
        return self._context

    @property
    def deactivate(self) -> typing.Optional[bool]:
        """
        Is true when wrapper deactivates tag.
        """
        assert self._deactivate in (True, False, None)
        return self._deactivate

    @deactivate.setter
    def deactivate(self, argument):
        assert argument in (True, False, None)
        self._deactivate: typing.Optional[bool] = argument

    @property
    def indicator(self) -> typing.Any:
        """
        Gets indicator.
        """
        return self._indicator

    @property
    def leaked_start_offset(self):
        r"""
        Gets start offset and checks to see whether indicator leaks to the
        right.

        This is either the wrapper's synthetic offset (if set); or the START
        offset of the wrapper's component (if indicator DOES NOT leak); or else
        the STOP offset of the wrapper's component (if indicator DOES leak).

        ..  container:: example

            Start- and stop-text-spans attach to the same leaf. But
            stop-text-span leaks to the right:

            >>> voice = abjad.Voice("c'2 d'2")
            >>> start_text_span = abjad.StartTextSpan()
            >>> abjad.attach(start_text_span, voice[0])
            >>> stop_text_span = abjad.StopTextSpan(leak=True)
            >>> abjad.attach(stop_text_span, voice[0])
            >>> abjad.show(voice) # doctest: +SKIP

            >>> abjad.f(voice)
            \new Voice
            {
                c'2
                \startTextSpan
                <> \stopTextSpan
                d'2
            }

            Start offset and leaked start offset are the same for
            start-text-span:

            >>> wrapper = abjad.inspect(voice[0]).wrapper(abjad.StartTextSpan)
            >>> wrapper.start_offset, wrapper.leaked_start_offset
            (Offset((0, 1)), Offset((0, 1)))

            Start offset and leaked start offset differ for stop-text-span:

            >>> wrapper = abjad.inspect(voice[0]).wrapper(abjad.StopTextSpan)
            >>> wrapper.start_offset, wrapper.leaked_start_offset
            (Offset((0, 1)), Offset((1, 2)))

        Returns offset.
        """
        if self._synthetic_offset is not None:
            return self._synthetic_offset
        if not getattr(self.indicator, "leak", False):
            return inspect(self._component).timespan().start_offset
        else:
            return inspect(self._component).timespan().stop_offset

    @property
    def start_offset(self):
        """
        Gets start offset.

        This is either the wrapper's synthetic offset or the start offset of
        the wrapper's component.

        Returns offset.
        """
        if self._synthetic_offset is not None:
            return self._synthetic_offset
        return inspect(self._component).timespan().start_offset

    @property
    def synthetic_offset(self):
        """
        Gets synthetic offset.

        Returns offset or none.
        """
        return self._synthetic_offset

    @property
    def tag(self) -> Tag:
        """
        Gets and sets tag.
        """
        assert isinstance(self._tag, Tag), repr(self._tag)
        return self._tag

    @tag.setter
    def tag(self, argument):
        if not isinstance(argument, (str, Tag)):
            raise Exception(f"string or tag: {argument!r}.")
        tag = Tag(argument)
        self._tag = tag
