import abc
import copy
import typing

from .. import enums, exceptions, mathtools
from ..bundle import LilyPondFormatBundle
from ..duration import Multiplier
from ..markups import Markup
from ..new import new
from ..overrides import override, setting
from ..storage import FormatSpecification, StorageFormatManager
from ..tags import Tag
from ..timespans import Timespan


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

    @staticmethod
    def _parse_lilypond_string(string):
        from ..parsers.parse import parse

        return parse(string)

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
        self._wrappers: typing.List = []

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies component.

        Copies indicators.

        Does not copy spanners.

        Does not copy children.

        Returns new component.
        """
        component = type(self)(*self.__getnewargs__())
        if getattr(self, "_overrides", None) is not None:
            component._overrides = copy.copy(override(self))
        if getattr(self, "_lilypond_setting_name_manager", None) is not None:
            component._lilypond_setting_name_manager = copy.copy(setting(self))
        for wrapper in self._wrappers:
            if not wrapper.annotation:
                continue
            wrapper_ = copy.copy(wrapper)
            new(wrapper_, component=component)
        for wrapper in self._get_indicators(unwrap=False):
            wrapper_ = copy.copy(wrapper)
            new(wrapper_, component=component)
        return component

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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

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
        parentage = [self]
        parent = self._parent
        while parent is not None:
            parentage.append(parent)
            parent = parent._parent
        for component in components:
            if component in parentage:
                return True
        return False

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
        from ..formatx import LilyPondFormatManager

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
                    string = LilyPondFormatBundle.indent + string
                strings.append(string)
            pair = (contributor, strings)
            result.append(pair)
        return result

    @staticmethod
    def _get_components(argument):
        result = []
        if isinstance(argument, Component):
            result.extend(argument._get_subtree())
        else:
            for item in argument:
                result.extend(Component._get_components(item))
        return result

    def _get_descendants_starting_with(self):
        return [self]

    def _get_descendants_stopping_with(self):
        return [self]

    def _get_duration(self):
        duration = self._get_preprolated_duration()
        if self._parent is None:
            return duration
        for parent in self._parent._get_parentage():
            multiplier = getattr(parent, "implied_prolation", Multiplier(1))
            duration *= multiplier
        return duration

    def _get_format_contributions_for_slot(self, slot_identifier, bundle=None):
        from ..formatx import LilyPondFormatManager

        result = []
        if bundle is None:
            bundle = LilyPondFormatManager.bundle_format_contributions(self)
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
            message = f"multiple attached indicators found matching {prototype!r}."
            raise ValueError(message)
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
            elif isinstance(wrapper.indicator, prototype_classes):
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

    def _get_parentage(self):
        parentage = []
        parent = self
        while parent is not None:
            parentage.append(parent)
            if hasattr(parent, "_main_leaf"):
                if parent._main_leaf is not None:
                    parent = parent._main_leaf._parent
                else:
                    parent = None
            else:
                parent = parent._parent
        return parentage

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

    def _has_indicator(self, prototype=None, *, attributes=None):
        indicators = self._get_indicators(prototype=prototype, attributes=attributes)
        return bool(indicators)

    def _remove_from_parent(self):
        self._update_later(offsets=True)
        for component in self._get_parentage()[1:]:
            if not hasattr(component, "_lilypond_type"):
                continue
            for wrapper in component._dependent_wrappers[:]:
                if wrapper.component is self:
                    component._dependent_wrappers.remove(wrapper)
        if self._parent is not None:
            self._parent._components.remove(self)
        self._parent = None

    def _remove_named_children_from_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self._get_parentage()[1:]:
                named_children = parent._named_children
                for name in name_dictionary:
                    for component in name_dictionary[name]:
                        named_children[name].remove(component)
                    if not named_children[name]:
                        del named_children[name]

    def _restore_named_children_to_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self._get_parentage()[1:]:
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
        for parent in self._get_parentage():
            sibling = parent._get_sibling(mathtools.sign(n))
            if sibling is not None:
                return sibling

    def _tag_strings(self, strings):
        return Tag.tag(strings, tag=self.tag)

    def _update_later(self, offsets=False, offsets_in_seconds=False):
        assert offsets or offsets_in_seconds
        for component in self._get_parentage():
            if offsets:
                component._offsets_are_current = False
            elif offsets_in_seconds:
                component._offsets_in_seconds_are_current = False

    def _update_measure_numbers(self):
        from ..update import UpdateManager

        UpdateManager()._update_measure_numbers(self)

    def _update_now(self, offsets=False, offsets_in_seconds=False, indicators=False):
        from ..update import UpdateManager

        return UpdateManager()._update_now(
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
