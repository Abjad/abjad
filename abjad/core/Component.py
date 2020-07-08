import abc
import bisect
import copy
import importlib
import typing

from .. import enums, exceptions, mathtools
from ..bundle import LilyPondFormatBundle
from ..duration import Multiplier, Offset
from ..markups import Markup
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
        for wrapper in self._wrappers:
            if not wrapper.annotation:
                continue
            new_wrapper = copy.copy(wrapper)
            attach(new_wrapper, new_component)
        for wrapper in self._get_indicators(unwrap=False):
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

    def _extract(self):
        from .Selection import Selection

        selection = Selection([self])
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
        from ..formatting import LilyPondFormatManager

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

    def _get_contents(self):
        from .Selection import Selection

        result = []
        result.append(self)
        result.extend(getattr(self, "components", []))
        result = Selection(result)
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
        duration = self._get_preprolated_duration()
        if self._parent is None:
            return duration
        for parent in self._parent._get_parentage():
            multiplier = getattr(parent, "implied_prolation", Multiplier(1))
            duration *= multiplier
        return duration

    def _get_effective(
        self, prototype, *, attributes=None, command=None, n=0, unwrap=True
    ):
        from .Context import Context
        from .Voice import Voice

        self._update_now(indicators=True)
        candidate_wrappers = {}
        parentage = self._get_parentage()
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
        start_offset = self._get_timespan().start_offset
        index = bisect.bisect(all_offsets, start_offset) - 1 + int(n)
        if index < 0:
            return
        elif len(candidate_wrappers) <= index:
            return
        wrapper = candidate_wrappers[all_offsets[index]][0]
        if unwrap:
            return wrapper.indicator
        return wrapper

    def _get_format_contributions_for_slot(self, slot_identifier, bundle=None):
        from ..formatting import LilyPondFormatManager

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
        from .update import UpdateManager

        UpdateManager()._update_measure_numbers(self)

    def _update_now(self, offsets=False, offsets_in_seconds=False, indicators=False):
        from .update import UpdateManager

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
        parentage = self.component._get_parentage()
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
        lilypond_format = Tag.tag(lilypond_format, self.tag, deactivate=self.deactivate)
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
        if self.deactivate is True:
            return
        prototype = type(self.indicator)
        command = getattr(self.indicator, "command", None)
        wrapper = component._get_effective(
            prototype, attributes={"command": command}, unwrap=False,
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
        context = None
        for parent in component._get_parentage():
            if hasattr(parent, "_lilypond_type"):
                context = parent
                break
        wrapper_context = None
        for parent in wrapper.component._get_parentage():
            if hasattr(parent, "_lilypond_type"):
                wrapper_context = parent
                break
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
    def leaked_start_offset(self) -> Offset:
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
            return self._component._get_timespan().start_offset
        else:
            return self._component._get_timespan().stop_offset

    @property
    def start_offset(self) -> Offset:
        """
        Gets start offset.

        This is either the wrapper's synthetic offset or the start offset of
        the wrapper's component.
        """
        if self._synthetic_offset is not None:
            return self._synthetic_offset
        return self._component._get_timespan().start_offset

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


### FUNCTIONS ###


def annotate(component, annotation, indicator) -> None:
    r"""
    Annotates ``component`` with ``indicator``.

    ..  container:: example

        Annotates first note in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.annotate(staff[0], 'bow_direction', abjad.Down)
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

        >>> abjad.inspect(staff[0]).annotation('bow_direction')
        Down

        >>> abjad.inspect(staff[0]).annotation('bow_fraction') is None
        True

        >>> abjad.inspect(staff[0]).annotation('bow_fraction', 99)
        99

    """
    if isinstance(annotation, Tag):
        message = "use the tag=None keyword instead of annotate():\n"
        message += f"   {repr(annotation)}"
        raise Exception(message)
    assert isinstance(annotation, str), repr(annotation)
    Wrapper(annotation=annotation, component=component, indicator=indicator)


def attach(  # noqa: 302
    attachable,
    target,
    context=None,
    deactivate=None,
    do_not_test=None,
    synthetic_offset=None,
    tag=None,
    wrapper=None,
):
    r"""
    Attaches ``attachable`` to ``target``.

    First form attaches indicator ``attachable`` to single leaf ``target``.

    Second for attaches grace container ``attachable`` to leaf ``target``.

    Third form attaches wrapper ``attachable`` to unknown (?) ``target``.

    ..  container:: example

        Attaches clef to first note in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Clef('alto'), staff[0])
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

    ..  container:: example

        Attaches accent to last note in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Articulation('>'), staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                - \accent
            }

    ..  container:: example

        Works with context names:

        >>> voice = abjad.Voice("c'4 d' e' f'", name='MusicVoice')
        >>> staff = abjad.Staff([voice], name='MusicStaff')
        >>> abjad.attach(abjad.Clef('alto'), voice[0], context='MusicStaff')
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \context Staff = "MusicStaff"
            {
                \context Voice = "MusicVoice"
                {
                    \clef "alto"
                    c'4
                    d'4
                    e'4
                    f'4
                }
            }

        >>> for leaf in abjad.select(staff).leaves():
        ...     leaf, abjad.inspect(leaf).effective(abjad.Clef)
        ...
        (Note("c'4"), Clef('alto'))
        (Note("d'4"), Clef('alto'))
        (Note("e'4"), Clef('alto'))
        (Note("f'4"), Clef('alto'))

        Derives context from default ``attachable`` context when ``context`` is
        none.

    ..  container:: example

        Two contexted indicators can not be attached at the same offset if both
        indicators are active:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> abjad.attach(abjad.Clef('alto'), staff[0])
        Traceback (most recent call last):
            ...
        abjad...PersistentIndicatorError: Can not attach ...

        But simultaneous contexted indicators are allowed if only one is active
        (and all others are inactive):

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> abjad.attach(
        ...     abjad.Clef('alto'),
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.tags.ONLY_PARTS,
        ...     )
        >>> abjad.attach(
        ...     abjad.Clef('tenor'),
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.tags.ONLY_PARTS,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \clef "treble"
            %@% \clef "alto" %! +PARTS
            %@% \clef "tenor" %! +PARTS
                c'4
                d'4
                e'4
                f'4
            }

        Active indicator is always effective when competing inactive indicators
        are present:

        >>> for note in staff:
        ...     clef = abjad.inspect(staff[0]).effective(abjad.Clef)
        ...     note, clef
        ...
        (Note("c'4"), Clef('treble'))
        (Note("d'4"), Clef('treble'))
        (Note("e'4"), Clef('treble'))
        (Note("f'4"), Clef('treble'))

        But a lone inactivate indicator is effective when no active indicator
        is present:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(
        ...     abjad.Clef('alto'),
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.tags.ONLY_PARTS,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
            %@% \clef "alto" %! +PARTS
                c'4
                d'4
                e'4
                f'4
            }

        >>> for note in staff:
        ...     clef = abjad.inspect(staff[0]).effective(abjad.Clef)
        ...     note, clef
        ...
        (Note("c'4"), Clef('alto'))
        (Note("d'4"), Clef('alto'))
        (Note("e'4"), Clef('alto'))
        (Note("f'4"), Clef('alto'))

    ..  container:: example

        Tag must exist when ``deactivate`` is true:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Clef('alto'), staff[0], deactivate=True)
        Traceback (most recent call last):
            ...
        Exception: tag must exist when deactivate is true.

    ..  container:: example

        Returns wrapper when ``wrapper`` is true:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> wrapper = abjad.attach(abjad.Clef('alto'), staff[0], wrapper=True)
        >>> abjad.f(wrapper)
        abjad.Wrapper(
            context='Staff',
            indicator=abjad.Clef('alto'),
            tag=abjad.Tag(),
            )

    Otherwise returns none.
    """
    if isinstance(attachable, Tag):
        message = "use the tag=None keyword instead of attach():\n"
        message += f"   {repr(attachable)}"
        raise Exception(message)

    if tag is not None and not isinstance(tag, Tag):
        raise Exception(f"must be be tag: {repr(tag)}")

    if isinstance(attachable, Multiplier):
        message = "use the Leaf.multiplier property to multiply leaf duration."
        raise Exception(message)

    assert attachable is not None, repr(attachable)
    assert target is not None, repr(target)

    if context is not None and hasattr(attachable, "_main_leaf"):
        raise Exception(f"set context only for indicators, not {attachable!r}.")

    if deactivate is True and tag is None:
        raise Exception("tag must exist when deactivate is true.")

    if hasattr(attachable, "_before_attach"):
        attachable._before_attach(target)

    if hasattr(attachable, "_attachment_test_all") and not do_not_test:
        result = attachable._attachment_test_all(target)
        if result is not True:
            assert isinstance(result, list), repr(result)
            result = ["  " + _ for _ in result]
            message = f"{attachable!r}._attachment_test_all():"
            result.insert(0, message)
            message = "\n".join(result)
            raise Exception(message)

    if hasattr(attachable, "_main_leaf"):
        if not hasattr(target, "written_duration"):
            raise Exception("grace containers attach to single leaf only.")
        attachable._attach(target)
        return

    # target is component
    assert hasattr(target, "_parent"), repr(target)

    # if target is container
    if hasattr(target, "__iter__"):
        acceptable = False
        if isinstance(attachable, (dict, str, Tag, Wrapper)):
            acceptable = True
        if getattr(attachable, "_can_attach_to_containers", False):
            acceptable = True
        if not acceptable:
            message = f"can not attach {attachable!r} to containers: {target!r}"
            raise Exception(message)
    elif not hasattr(target, "written_duration"):
        raise Exception(
            f"indicator {attachable!r} must attach to leaf, not {target!r}."
        )

    component = target
    assert hasattr(component, "_parent")

    annotation = None
    if isinstance(attachable, Wrapper):
        annotation = attachable.annotation
        context = context or attachable.context
        deactivate = deactivate or attachable.deactivate
        synthetic_offset = synthetic_offset or attachable.synthetic_offset
        tag = tag or attachable.tag
        attachable._detach()
        attachable = attachable.indicator

    if hasattr(attachable, "context"):
        context = context or attachable.context

    wrapper_ = Wrapper(
        annotation=annotation,
        component=component,
        context=context,
        deactivate=deactivate,
        indicator=attachable,
        synthetic_offset=synthetic_offset,
        tag=tag,
    )

    if wrapper is True:
        return wrapper_


def detach(argument, target=None, by_id=False):
    r"""
    Detaches indicators-equal-to-``argument`` from ``target``.

    Set ``by_id`` to true to detach exact ``argument`` from ``target`` (rather
    than detaching all indicators-equal-to-``argument``).

    ..  container:: example

        Detaches articulations from first note in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Articulation('>'), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \accent
                d'4
                e'4
                f'4
            }

        >>> abjad.detach(abjad.Articulation, staff[0])
        (Articulation('>'),)
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

    ..  container:: example

        The use of ``by_id`` is motivated by the following.

        Consider the three document-specifier markups below:

        >>> markup_1 = abjad.Markup('tutti', direction=abjad.Up)
        >>> markup_2 = abjad.Markup('with the others', direction=abjad.Up)
        >>> markup_3 = abjad.Markup('with the others', direction=abjad.Up)

        Markups two and three compare equal:

        >>> markup_2 == markup_3
        True

        But document-tagging like this makes sense for score and two diferent
        parts:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(markup_1, staff[0], tag=abjad.tags.ONLY_SCORE)
        >>> abjad.attach(
        ...     markup_2,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("+PARTS_VIOLIN_1"),
        ...     )
        >>> abjad.attach(
        ...     markup_3,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("+PARTS_VIOLIN_2"),
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff, strict=50)
        \new Staff
        {
            c'4
            ^ \markup { tutti }                           %! +SCORE
        %@% ^ \markup { "with the others" }               %! +PARTS_VIOLIN_1
        %@% ^ \markup { "with the others" }               %! +PARTS_VIOLIN_2
            d'4
            e'4
            f'4
        }

        The question is then how to detach just one of the two markups that
        compare equal to each other?

        Passing in one of the markup objects directory doesn't work. This is
        because detach tests for equality to input argument:

        >>> abjad.detach(markup_2, staff[0])
        (Markup(contents=['with the others'], direction=Up), Markup(contents=['with the others'], direction=Up))

        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff, strict=50)
        \new Staff
        {
            c'4
            ^ \markup { tutti }                           %! +SCORE
            d'4
            e'4
            f'4
        }

        We start again:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(markup_1, staff[0], tag=abjad.tags.ONLY_SCORE)
        >>> abjad.attach(
        ...     markup_2,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("+PARTS_VIOLIN_1"),
        ...     )
        >>> abjad.attach(
        ...     markup_3,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("+PARTS_VIOLIN_2"),
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff, strict=50)
        \new Staff
        {
            c'4
            ^ \markup { tutti }                           %! +SCORE
        %@% ^ \markup { "with the others" }               %! +PARTS_VIOLIN_1
        %@% ^ \markup { "with the others" }               %! +PARTS_VIOLIN_2
            d'4
            e'4
            f'4
        }

        This time we set ``by_id`` to true. Now detach checks the exact id of
        its input argument (rather than just testing for equality). This gives
        us what we want:

        >>> abjad.detach(markup_2, staff[0], by_id=True)
        (Markup(contents=['with the others'], direction=Up),)

        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff, strict=50)
        \new Staff
        {
            c'4
            ^ \markup { tutti }                           %! +SCORE
        %@% ^ \markup { "with the others" }               %! +PARTS_VIOLIN_2
            d'4
            e'4
            f'4
        }

    ..  container:: example

        REGRESSION. Attach-detach-attach pattern works correctly when detaching
        wrappers:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Clef('alto'), staff[0])
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

        >>> wrapper = abjad.inspect(staff[0]).wrappers()[0]
        >>> abjad.detach(wrapper, wrapper.component)
        (Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag()),)

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

        >>> abjad.attach(abjad.Clef('tenor'), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \clef "tenor"
                c'4
                d'4
                e'4
                f'4
            }

    Returns tuple of zero or more detached items.
    """
    assert target is not None
    after_grace_container = None
    before_grace_container = None
    if isinstance(argument, type):
        if "AfterGraceContainer" in argument.__name__:
            after_grace_container = target._after_grace_container
        elif "BeforeGraceContainer" in argument.__name__:
            before_grace_container = target._before_grace_container
        else:
            assert hasattr(target, "_wrappers")
            result = []
            for wrapper in target._wrappers[:]:
                if isinstance(wrapper, argument):
                    target._wrappers.remove(wrapper)
                    result.append(wrapper)
                elif isinstance(wrapper.indicator, argument):
                    wrapper._detach()
                    result.append(wrapper.indicator)
            result = tuple(result)
            return result
    else:
        if "AfterGraceContainer" in argument.__class__.__name__:
            after_grace_container = target._after_grace_container
        elif "BeforeGraceContainer" in argument.__class__.__name__:
            before_grace_container = target._before_grace_container
        else:
            assert hasattr(target, "_wrappers")
            result = []
            for wrapper in target._wrappers[:]:
                if wrapper is argument:
                    wrapper._detach()
                    result.append(wrapper)
                elif wrapper.indicator == argument:
                    if by_id is True and id(argument) != id(wrapper.indicator):
                        pass
                    else:
                        wrapper._detach()
                        result.append(wrapper.indicator)
            result = tuple(result)
            return result
    items = []
    if after_grace_container is not None:
        items.append(after_grace_container)
    if before_grace_container is not None:
        items.append(before_grace_container)
    if by_id is True:
        items = [_ for _ in items if id(_) == id(argument)]
    for item in items:
        item._detach()
    items = tuple(items)
    return items
