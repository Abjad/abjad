"""
Classes to model score components.
"""

import collections
import copy
import fractions
import functools
import typing

from . import _contributions, _indentlib, _updatelib
from . import duration as _duration
from . import enums as _enums
from . import exceptions as _exceptions
from . import format as _format
from . import indicators as _indicators
from . import lyconst as _lyconst
from . import lyproxy as _lyproxy
from . import math as _math
from . import overrides as _overrides
from . import pitch as _pitch
from . import tag as _tag
from . import timespan as _timespan
from . import tweaks as _tweaks


def _indent_strings(strings):
    result = []
    for string in strings:
        assert isinstance(string, str)
        if string.isspace():
            result.append("")
        else:
            result.append(_indentlib.INDENT + string)
    assert all(isinstance(_, str) for _ in result), repr(result)
    return result


class Component:
    """
    Component.
    """

    ### CLASS VARIABLES ###

    _allowable_sites: tuple[str, ...] = ()

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
    def _parse_lilypond_string(string, language="english"):
        from .parsers.parse import parse

        return parse(string, language=language)

    def __init__(self, *, tag: _tag.Tag | None = None) -> None:
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
            assert isinstance(tag, _tag.Tag), repr(tag)
        self._tag = tag
        self._timespan = _timespan.Timespan()
        self._wrappers: list = []

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies component.

        Copies indicators.

        Does not copy spanners.

        Does not copy children.

        Returns new component.
        """
        component = type(self)(*self.__getnewargs__(), tag=self.tag())
        if hasattr(self, "identifier"):
            component.set_identifier(self.identifier())
        if hasattr(self, "lilypond_type"):
            component.set_lilypond_type(self.lilypond_type())
        if hasattr(self, "name"):
            component.set_name(self.name())
        if hasattr(self, "simultaneous"):
            component.set_simultaneous(self.simultaneous())
        if getattr(self, "_overrides", None) is not None:
            component._overrides = copy.copy(_overrides.override(self))
        if getattr(self, "_lilypond_setting_name_manager", None) is not None:
            component._lilypond_setting_name_manager = copy.copy(
                _overrides.setting(self)
            )
        for wrapper in self._wrappers:
            if not wrapper.annotation():
                continue
            wrapper_ = copy.copy(wrapper)
            wrapper_._component = component
            wrapper_._bind_component(component)
        for wrapper in self._get_wrappers():
            wrapper_ = copy.copy(wrapper)
            wrapper_._component = component
            wrapper_._bind_component(component)
        return component

    def __getnewargs__(self):
        """
        Gets new arguments.

        Returns tuple.
        """
        return ()

    ### PRIVATE METHODS ###

    def _cache_named_children(self):
        name_dictionary = {}
        if hasattr(self, "_named_children"):
            for name, children in self._named_children.items():
                name_dictionary[name] = copy.copy(children)
        name = None
        if hasattr(self, "name"):
            name = self.name()
        if name is not None:
            if self.name() not in name_dictionary:
                name_dictionary[self.name()] = []
            name_dictionary[self.name()].append(self)
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

    def _format_absolute_after_site(self, contributions):
        result = []
        strings = contributions.alphabetize(contributions.absolute_after.commands)
        if strings:
            assert isinstance(
                self, AfterGraceContainer | BeforeGraceContainer | Leaf
            ), repr(self)
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        return result

    def _format_absolute_before_site(self, contributions):
        result = []
        strings = contributions.alphabetize(contributions.absolute_before.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
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
            if hasattr(parent, "_get_prolation"):
                prolation = parent._get_prolation()
                duration *= prolation
        return duration

    def _get_indicators(self, prototype=None, *, attributes=None):
        wrappers = self._get_wrappers(prototype, attributes=attributes)
        indicators = []
        for wrapper_ in wrappers:
            indicators.append(wrapper_.unbundle_indicator())
        return indicators

    def _get_lilypond_format(self):
        _updatelib._update_now(self, indicators=True)
        string = _format.format_component(self)
        return string

    def _get_markup(self, direction=None):
        wrappers = self._get_wrappers(_indicators.Markup)
        if direction is _enums.UP:
            return tuple(_.indicator() for _ in wrappers if _.direction() is _enums.UP)
        elif direction is _enums.DOWN:
            return tuple(
                _.indicator() for _ in wrappers if _.direction() is _enums.DOWN
            )
        indicators = [_.indicator() for _ in wrappers]
        return indicators

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
        if self._parent.simultaneous():
            return None
        index = self._parent.index(self) + n
        if 0 <= index < len(self._parent):
            return self._parent[index]

    def _get_timespan(self, in_seconds=False):
        if in_seconds:
            _updatelib._update_now(self, offsets_in_seconds=True)
            if self._start_offset_in_seconds is None:
                raise _exceptions.MissingMetronomeMarkError
            return _timespan.Timespan(
                start_offset=self._start_offset_in_seconds,
                stop_offset=self._stop_offset_in_seconds,
            )
        else:
            _updatelib._update_now(self, offsets=True)
            return self._timespan

    def _get_wrappers(self, prototype=None, *, attributes=None):
        if prototype is None:
            prototype = object
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
        wrappers = []
        for wrapper in self._wrappers:
            if wrapper.annotation():
                continue
            if isinstance(wrapper, prototype_classes):
                wrappers.append(wrapper)
            elif any(wrapper == _ for _ in prototype_objects):
                wrappers.append(wrapper)
            elif isinstance(wrapper.unbundle_indicator(), prototype_classes):
                wrappers.append(wrapper)
            elif any(wrapper.indicator() == _ for _ in prototype_objects):
                wrappers.append(wrapper)
            elif any(wrapper.unbundle_indicator() == _ for _ in prototype_objects):
                wrappers.append(wrapper)
        if attributes is not None:
            wrappers_ = []
            for wrapper in wrappers:
                for name, value in attributes.items():
                    if getattr(wrapper.unbundle_indicator(), name, None) != value:
                        break
                else:
                    wrappers_.append(wrapper)
            wrappers = wrappers_
        return wrappers

    def _has_indicator(self, prototype=None, *, attributes=None):
        indicators = self._get_indicators(prototype=prototype, attributes=attributes)
        return bool(indicators)

    def _remove_from_parent(self):
        self._update_later(offsets=True)
        for component in self._get_parentage()[1:]:
            if not hasattr(component, "_lilypond_type"):
                continue
            for wrapper in component._dependent_wrappers[:]:
                if wrapper.component() is self:
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
            sibling = parent._get_sibling(_math.sign(n))
            if sibling is not None:
                return sibling

    def _tag_strings(self, strings):
        if self.tag() is not None:
            strings = _tag.double_tag(strings, self.tag())
        return strings

    def _update_later(self, offsets=False, offsets_in_seconds=False):
        assert offsets or offsets_in_seconds
        for component in self._get_parentage():
            if offsets:
                component._offsets_are_current = False
            elif offsets_in_seconds:
                component._offsets_in_seconds_are_current = False

    def tag(self) -> _tag.Tag | None:
        """
        Gets component tag.
        """
        if self._tag is not None:
            assert isinstance(self._tag, _tag.Tag), repr(self._tag)
        return self._tag

    def set_tag(self, argument):
        """
        Sets component tag.
        """
        if argument is not None:
            assert isinstance(argument, _tag.Tag), repr(argument)
        self._tag = argument


class Leaf(Component):
    """
    Leaf.
    """

    ### CLASS VARIABLES ##

    _allowable_sites = (
        "absolute_before",
        "before",
        "after",
        "absolute_after",
    )

    __slots__ = (
        "_after_grace_container",
        "_before_grace_container",
        "_multiplier",
        "_written_duration",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        written_duration: _duration.Duration,
        *,
        multiplier=None,
        tag: _tag.Tag | None = None,
    ) -> None:
        Component.__init__(self, tag=tag)
        self._after_grace_container = None
        self._before_grace_container = None
        self.set_multiplier(multiplier)
        self.set_written_duration(written_duration)

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies leaf.
        """
        leaf = Component.__copy__(self, *arguments)
        leaf.set_multiplier(self.multiplier())
        before_grace_container = self._before_grace_container
        if before_grace_container is not None:
            grace_container = before_grace_container._copy_with_children()
            grace_container._attach(leaf)
        after_grace_container = self._after_grace_container
        if after_grace_container is not None:
            grace_container = after_grace_container._copy_with_children()
            grace_container._attach(leaf)
        return leaf

    def __getnewargs__(self):
        """
        Gets new arguments.

        Returns tuple.
        """
        return (self.written_duration(),)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self._get_compact_representation()!r})"

    ### PRIVATE METHODS ###

    def _copy_override_and_set_from_leaf(self, leaf):
        if getattr(leaf, "_overrides", None) is not None:
            self._overrides = copy.copy(_overrides.override(leaf))
        if getattr(leaf, "_lilypond_setting_name_manager", None) is not None:
            self._lilypond_setting_name_manager = copy.copy(_overrides.setting(leaf))
        for wrapper in leaf._wrappers:
            wrapper_ = copy.copy(wrapper)
            wrapper_._component = self
            wrapper_._bind_component(self)

    def _format_after_site(self, contributions):
        result = []
        strings = contributions.alphabetize(contributions.after.stem_tremolos)
        if strings:
            result.append(f"% {_contributions.Types.STEM_TREMOLOS.name}:")
            result.extend(strings)
        strings = contributions.alphabetize(contributions.after.articulations)
        if strings:
            result.append(f"% {_contributions.Types.ARTICULATIONS.name}:")
            result.extend(strings)
        strings = contributions.alphabetize(contributions.after.markup)
        if strings:
            result.append(f"% {_contributions.Types.MARKUP.name}:")
            result.extend(strings)
        strings = contributions.alphabetize(contributions.after.spanner_stops)
        if strings:
            result.append(f"% {_contributions.Types.SPANNER_STOPS.name}:")
            result.extend(strings)
        strings = contributions.alphabetize(contributions.after.start_beam)
        if strings:
            result.append(f"% {_contributions.Types.START_BEAM.name}:")
            result.extend(strings)
        strings = contributions.alphabetize(contributions.after.stop_beam)
        if strings:
            result.append(f"% {_contributions.Types.STOP_BEAM.name}:")
            result.extend(strings)
        strings = contributions.alphabetize(contributions.after.spanner_starts)
        if strings:
            result.append(f"% {_contributions.Types.SPANNER_STARTS.name}:")
            result.extend(strings)
        # NOTE: LilyPond demands \startTrillSpan appear after almost all
        #       other contributions; pitched trills dangerously
        #       suppress markup and the starts of other spanners when
        #       \startTrillSpan appears lexically prior to those commands;
        #       but \startTrillSpan must appear before calls to \set.
        strings = contributions.alphabetize(contributions.after.trill_spanner_starts)
        if strings:
            result.append(f"% {_contributions.Types.TRILL_SPANNER_STARTS.name}:")
            result.extend(strings)
        strings = contributions.alphabetize(contributions.after.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        strings = contributions.alphabetize(contributions.after.leak)
        if strings:
            result.append(f"% {_contributions.Types.LEAK.name}:")
            result.extend(strings)
        strings = contributions.alphabetize(contributions.after.leaks)
        if strings:
            result.append(f"% {_contributions.Types.LEAKS.name}:")
            result.extend(strings)
        if self._after_grace_container is not None:
            string = self._after_grace_container._get_lilypond_format()
            result.append(string)
        return result

    def _format_before_site(self, contributions):
        result = []
        if self._before_grace_container is not None:
            string = self._before_grace_container._get_lilypond_format()
            result.append(string)
        strings = contributions.alphabetize(contributions.before.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        strings = contributions.grob_reverts
        if strings:
            result.append(f"% {_contributions.Types.GROB_REVERTS.name}:")
            result.extend(strings)
        strings = contributions.grob_overrides
        if strings:
            result.append(f"% {_contributions.Types.GROB_OVERRIDES.name}:")
            result.extend(strings)
        strings = contributions.context_settings
        if strings:
            result.append(f"% {_contributions.Types.CONTEXT_SETTINGS.name}:")
            result.extend(strings)
        return result

    def _format_closing_site(self, contributions):
        result = []
        strings = contributions.alphabetize(contributions.closing.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        result = _indent_strings(result)
        return result

    def _format_contents(self):
        result = []
        strings = self._format_leaf_nucleus()
        result.extend(strings)
        return result

    def _format_leaf_nucleus(self):
        strings = self._get_body()
        if self.tag() is not None and self.tag().string:
            strings = _tag.double_tag(strings, self.tag())
        return strings

    def _format_opening_site(self, contributions):
        result = []
        strings = contributions.alphabetize(contributions.opening.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        if self._after_grace_container is not None:
            assert not self._is_followed_by_after_grace_container()
            string = r"\afterGrace"
            if self._after_grace_container.fraction() is not None:
                n, d = self._after_grace_container.fraction()
                string = f"{string} {n}/{d}"
            result.append(string)
        if self._is_followed_by_after_grace_container():
            assert self._after_grace_container is None, repr(
                self._after_grace_container
            )
            string = r"\afterGrace"
            container = self._get_following_after_grace_container()
            if container.fraction() is not None:
                n, d = container.fraction()
                string = f"{string} {n}/{d}"
            result.append(string)
        strings = contributions.alphabetize(contributions.before.pitched_trill)
        if strings:
            result.append(f"% {_contributions.Types.PITCHED_TRILL.name}:")
            result.extend(strings)
        return result

    def _get_compact_representation(self):
        return f"({self._get_formatted_duration()})"

    def _get_following_after_grace_container(self):
        if self._parent is not None:
            index = self._parent.index(self)
            try:
                component = self._parent[index + 1]
            except IndexError:
                component = None
            if isinstance(component, IndependentAfterGraceContainer):
                return component
            else:
                return False

    def _get_formatted_duration(self):
        strings = [self.written_duration().lilypond_duration_string()]
        if self.multiplier() is not None:
            string = f"{self.multiplier()[0]}/{self.multiplier()[1]}"
            strings.append(string)
        result = " * ".join(strings)
        return result

    def _get_preprolated_duration(self):
        duration = self.written_duration()
        if self.multiplier() is not None:
            duration *= fractions.Fraction(*self.multiplier())
        return duration

    def _get_subtree(self):
        result = []
        if self._before_grace_container is not None:
            result.extend(self._before_grace_container._get_subtree())
        result.append(self)
        if self._after_grace_container is not None:
            result.extend(self._after_grace_container._get_subtree())
        return result

    def _is_followed_by_after_grace_container(self):
        if self._parent is not None:
            index = self._parent.index(self)
            try:
                component = self._parent[index + 1]
            except IndexError:
                component = None
            if isinstance(component, IndependentAfterGraceContainer):
                return True
            else:
                return False

    def _process_contribution_packet(self, contribution_packet):
        result = ""
        for contributor, contributions in contribution_packet:
            if contributions:
                if isinstance(contributor, tuple):
                    contributor = _indentlib.INDENT + contributor[0] + ":\n"
                else:
                    contributor = _indentlib.INDENT + contributor + ":\n"
                result += contributor
                for contribution in contributions:
                    contribution = (_indentlib.INDENT * 2) + contribution + "\n"
                    result += contribution
        return result

    def _scale(self, multiplier):
        assert isinstance(multiplier, fractions.Fraction), repr(multiplier)
        self_written_duration = self.written_duration() * multiplier
        self.set_written_duration(self_written_duration)

    ### PUBLIC PROPERTIES ###

    def multiplier(self) -> tuple[int, int] | None:
        """
        Gets leaf duration multiplier.
        """
        return self._multiplier

    def set_multiplier(self, argument):
        """
        Sets leaf duration multiplier.
        """
        if argument is not None:
            assert isinstance(argument, tuple), repr(argument)
            assert len(argument) == 2, repr(argument)
        self._multiplier = argument

    def written_duration(self) -> _duration.Duration:
        """
        Gets leaf written duration.
        """
        return self._written_duration

    def set_written_duration(self, argument):
        duration = _duration.Duration(argument)
        if not duration.is_assignable():
            message = f"not assignable duration: {duration!r}."
            raise _exceptions.AssignabilityError(message)
        self._written_duration = duration


class Container(Component):
    r"""
    Container.

    ..  container:: example

        Intializes from string:

        >>> container = abjad.Container("c'4 e'4 d'4 e'8 f'8")
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c'4
                e'4
                d'4
                e'8
                f'8
            }

    ..  container:: example

        Intializes from components:

        >>> notes = [
        ...     abjad.Note("c'4"),
        ...     abjad.Note("e'4"),
        ...     abjad.Note("d'4"),
        ...     abjad.Note("e'8"),
        ...     abjad.Note("f'8"),
        ... ]
        >>> container = abjad.Container(notes)
        >>> abjad.show(container) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c'4
                e'4
                d'4
                e'8
                f'8
            }

    ..  container:: example

        Containers are iterables:

        >>> import collections
        >>> container = abjad.Container("c'4 e'4 d'4 e'8 f'8")
        >>> isinstance(container, collections.abc.Iterable)
        True

    ..  container:: example

        Containers are not sequences because containers do not implement
        reverse:

        >>> container = abjad.Container("c'4 e'4 d'4 e'8 f'8")
        >>> isinstance(container, collections.abc.Sequence)
        False

    ..  container:: example

        Formatting positions contributions strictly one-per-line:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Articulation('^'), staff[0])
        >>> markup = abjad.Markup(r'\markup Allegro')
        >>> abjad.attach(markup, staff[0], direction=abjad.UP)
        >>> abjad.attach(abjad.StemTremolo(), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            c'4
            :16
            - \marcato
            ^ \markup Allegro
            d'4
            e'4
            f'4
        }

    """

    ### CLASS VARIABLES ###

    _allowable_sites = (
        "absolute_before",
        "before",
        "opening",
        "closing",
        "after",
    )

    __slots__ = (
        "_identifier",
        "_components",
        "_formatter",
        "_named_children",
        "_name",
        "_is_simultaneous",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        *,
        identifier: str | None = None,
        language: str = "english",
        name: str | None = None,
        simultaneous: bool = False,
        tag: _tag.Tag | None = None,
    ) -> None:
        components = components or []
        if not isinstance(components, str):
            prototype = (Component, str)
            assert all(isinstance(_, prototype) for _ in components), repr(components)
        Component.__init__(self, tag=tag)
        self._named_children: dict = {}
        self._is_simultaneous = None
        # sets name temporarily for _find_correct_effective_context:
        self._name = name
        self._initialize_components(components, language=language)
        self.set_identifier(identifier)
        self.set_simultaneous(bool(simultaneous))
        # sets name permanently after _initalize_components:
        self.set_name(name)

    ### SPECIAL METHODS ###

    def __contains__(self, argument) -> bool:
        """
        Is true when ``argument`` appears in container.
        """
        if isinstance(argument, str):
            return argument in self._named_children
        else:
            for component in self.components():
                if component is argument:
                    return True
            else:
                return False

    def __delitem__(self, i) -> None:
        r"""
        Deletes components(s) at index ``i`` in container.

        ..  container:: example

            Deletes first tuplet in voice:

            >>> voice = abjad.Voice()
            >>> voice.append(abjad.Tuplet("6:4", "c'4 d'4 e'4"))
            >>> voice.append(abjad.Tuplet("3:2", "e'4 d'4 c'4"))
            >>> leaves = abjad.select.leaves(voice)
            >>> abjad.slur(leaves)
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    \tuplet 6/4
                    {
                        c'4
                        (
                        d'4
                        e'4
                    }
                    \tuplet 3/2
                    {
                        e'4
                        d'4
                        c'4
                        )
                    }
                }

            >>> tuplet_1 = voice[0]
            >>> del(voice[0])
            >>> start_slur = abjad.StartSlur()
            >>> leaf = abjad.select.leaf(voice, 0)
            >>> abjad.attach(start_slur, leaf)

            First tuplet no longer appears in voice:

            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    \tuplet 3/2
                    {
                        e'4
                        (
                        d'4
                        c'4
                        )
                    }
                }

            >>> abjad.wf.is_wellformed(voice)
            True

            First tuplet must have start slur removed:

            >>> abjad.detach(abjad.StartSlur, tuplet_1[0])
            (StartSlur(),)

            >>> abjad.show(tuplet_1) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet_1)
                >>> print(string)
                \tuplet 6/4
                {
                    c'4
                    d'4
                    e'4
                }

            >>> abjad.wf.is_wellformed(tuplet_1)
            True

        """
        result = self[i]
        wrappers = []
        for component in self._get_components(result):
            wrappers_ = component._get_wrappers()
            wrappers.extend(wrappers_)
        if isinstance(result, Component):
            result._set_parent(None)
        else:
            for component in result:
                component._set_parent(None)
        for wrapper in wrappers:
            wrapper._update_effective_context()

    @typing.overload
    def __getitem__(self, argument: typing.SupportsIndex | str) -> Component:
        pass

    @typing.overload
    def __getitem__(self, argument: slice) -> list[Component]:
        pass

    def __getitem__(
        self, argument: typing.SupportsIndex | str | slice
    ) -> Component | list[Component]:
        """
        Gets top-level item or slice identified by ``argument``.
        """
        if isinstance(argument, int):
            return self.components().__getitem__(argument)
        elif isinstance(argument, slice):
            result = self.components().__getitem__(argument)
            assert isinstance(result, tuple), repr(result)
            return list(result)
        elif isinstance(argument, str):
            if argument not in self._named_children:
                raise ValueError(f"can not find component named {argument!r}.")
            elif 1 < len(self._named_children.__getitem__(argument)):
                raise ValueError(f"multiple components named {argument!r}.")
            return self._named_children.__getitem__(argument)[0]
        raise ValueError(f"can not get container at {argument!r}.")

    def __getnewargs__(self) -> tuple:
        """
        Gets new container arguments.
        """
        return ([],)

    def __iter__(self) -> typing.Iterator:
        """
        Iterates container.

        ..  container:: example

            Abjad containers are iterables:

            >>> import collections
            >>> container = abjad.Container()
            >>> isinstance(container, collections.abc.Iterable)
            True

        ..  container:: example

            Abjad containers are not sequences:

            >>> import collections
            >>> container = abjad.Container()
            >>> isinstance(container, collections.abc.Sequence)
            False

        Yields container elements.
        """
        return iter(self.components())

    def __len__(self) -> int:
        """
        Gets number of components in container.
        """
        return len(self.components())

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        string = self._get_contents_summary()
        if string:
            return f"{type(self).__name__}({string!r})"
        else:
            return f"{type(self).__name__}()"

    def __setitem__(self, i, argument) -> None:
        """
        Sets container ``i`` equal to ``argument``.
        """
        if isinstance(argument, str):
            argument = self._parse_string(argument)
            if isinstance(i, int):
                assert len(argument) == 1, repr(argument)
                argument = argument[0]
        wrappers = []
        for component in self._get_components(argument):
            wrappers_ = component._get_wrappers()
            wrappers.extend(wrappers_)
        if isinstance(i, int):
            argument = [argument]
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
        new_argument = []
        for item in argument:
            if hasattr(item, "_items"):
                new_argument.extend(item)
            else:
                new_argument.append(item)
        argument = new_argument
        assert all(isinstance(_, Component) for _ in argument), repr(argument)
        if any(hasattr(_, "_main_leaf") for _ in argument):
            raise Exception("must attach grace container to note or chord.")
        if self._check_for_cycles(argument):
            raise _exceptions.ParentageError("attempted to induce cycles.")
        if (
            i.start == i.stop
            and i.start is not None
            and i.stop is not None
            and i.start <= -len(self)
        ):
            start, stop = 0, 0
        else:
            start, stop, stride = i.indices(len(self))
        del self[start:stop]
        self._components.__setitem__(slice(start, start), argument)
        for component in argument:
            component._set_parent(self)
        for wrapper in wrappers:
            wrapper._update_effective_context()

    ### PRIVATE METHODS ###

    def _copy_with_children(self):
        new_container = self.__copy__()
        for component in self:
            if isinstance(component, Container):
                new_component = component._copy_with_children()
            else:
                new_component = component.__copy__()
            new_container.append(new_component)
        return new_container

    def _format_after_site(self, contributions):
        result = []
        strings = contributions.alphabetize(contributions.after.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        return result

    def _format_before_site(self, contributions):
        result = []
        strings = contributions.alphabetize(contributions.before.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        return result

    def _format_close_brackets(self):
        result = []
        strings = []
        if self.simultaneous():
            if self.identifier():
                string = f">>  {self.identifier()}"
            else:
                string = ">>"
        else:
            if self.identifier():
                string = f"}}   {self.identifier()}"
            else:
                string = "}"
        strings.append(string)
        if self.tag() is not None:
            strings = _tag.double_tag(strings, self.tag())
        result.extend(strings)
        return result

    def _format_closing_site(self, contributions):
        result = []
        strings = contributions.grob_reverts
        if strings:
            result.append(f"% {_contributions.Types.GROB_REVERTS.name}:")
            result.extend(strings)
        strings = contributions.alphabetize(contributions.closing.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        result = _indent_strings(result)
        return result

    def _format_content_pieces(self):
        strings = []
        for component in self.components():
            string = component._get_lilypond_format()
            for string in string.split("\n"):
                if string.isspace():
                    string = ""
                else:
                    string = _indentlib.INDENT + string
                strings.append(string)
        return strings

    def _format_contents(self):
        result = []
        strings = self._format_content_pieces()
        result.extend(strings)
        return result

    def _format_open_brackets_site(self, contributions):
        result = []
        strings = []
        if self.simultaneous():
            if self.identifier():
                string = f"<<  {self.identifier()}"
            else:
                string = "<<"
        else:
            if self.identifier():
                string = f"{{   {self.identifier()}"
            else:
                string = "{"
        strings.append(string)
        if self.tag() is not None:
            strings = _tag.double_tag(strings, self.tag())
        result.extend(strings)
        return result

    def _format_opening_site(self, contributions):
        result = []
        strings = contributions.alphabetize(contributions.opening.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        strings = contributions.grob_overrides
        if strings:
            result.append(f"% {_contributions.Types.GROB_OVERRIDES.name}:")
            result.extend(strings)
        strings = contributions.context_settings
        if strings:
            result.append(f"% {_contributions.Types.CONTEXT_SETTINGS.name}:")
            result.extend(strings)
        result = _indent_strings(result)
        return result

    def _get_abbreviated_string_format(self):
        if 0 < len(self):
            summary = str(len(self))
        else:
            summary = ""
        if self.simultaneous():
            open_bracket_string, close_bracket_string = "<<", ">>"
        else:
            open_bracket_string, close_bracket_string = "{", "}"
        name = self.name()
        if name is not None:
            name = f'-"{name}"'
        else:
            name = ""
        if hasattr(self, "_lilypond_type"):
            result = "<{}{}{}{}{}>"
            result = result.format(
                self.lilypond_type(),
                name,
                open_bracket_string,
                summary,
                close_bracket_string,
            )
        else:
            result = "<{}{}{}{}>"
            result = result.format(
                name, open_bracket_string, summary, close_bracket_string
            )
        return result

    def _get_compact_representation(self):
        if not self:
            return "{ }"
        return f"{{ {self._get_contents_summary()} }}"

    def _get_contents_duration(self):
        if self.simultaneous():
            return max(
                [_duration.Duration(0)] + [_._get_preprolated_duration() for _ in self]
            )
        else:
            duration = _duration.Duration(0)
            for component in self:
                duration += component._get_preprolated_duration()
            return duration

    def _get_contents_summary(self):
        if 0 < len(self):
            result = []
            for component in self.components():
                if hasattr(component, "_get_compact_representation"):
                    result.append(component._get_compact_representation())
                else:
                    result.append(str(component))
            return " ".join(result)
        else:
            return ""

    def _get_descendants_starting_with(self):
        result = []
        result.append(self)
        if self.simultaneous():
            for item in self:
                result.extend(item._get_descendants_starting_with())
        elif self:
            result.extend(self[0]._get_descendants_starting_with())
        return result

    def _get_descendants_stopping_with(self):
        result = []
        result.append(self)
        if self.simultaneous():
            for item in self:
                result.extend(item._get_descendants_stopping_with())
        elif self:
            result.extend(self[-1]._get_descendants_stopping_with())
        return result

    def _get_preprolated_duration(self):
        return self._get_contents_duration()

    def _get_subtree(self):
        result = [self]
        for component in self:
            result.extend(component._get_subtree())
        return result

    def _initialize_components(self, components, *, language: str = "english"):
        if isinstance(components, collections.abc.Iterable) and not isinstance(
            components, str
        ):
            components_ = []
            for item in components:
                if isinstance(item, str):
                    parsed = self._parse_string(item, language=language)
                    components_.append(parsed)
                else:
                    assert isinstance(item, Component)
                    components_.append(item)
            components = components_
            assert all(isinstance(_, Component) for _ in components), repr(components)
        if isinstance(components, str):
            parsed = self._parse_string(components, language=language)
            self._components = []
            self.set_simultaneous(parsed.simultaneous())
            self[:] = parsed[:]
        else:
            for component in components:
                if component._parent is not None:
                    raise Exception(f"must not have parent: {component!r}.")
            self._components = list(components)
            for component in self:
                component._set_parent(self)

    def _is_one_of_my_first_leaves(self, leaf):
        return leaf in self._get_descendants_starting_with()

    def _is_one_of_my_last_leaves(self, leaf):
        return leaf in self._get_descendants_stopping_with()

    def _parse_string(self, string, *, language="english"):
        user_input = string.strip()
        if not user_input.startswith("<<") or not user_input.endswith(">>"):
            user_input = f"{{ {user_input} }}"
        parsed = self._parse_lilypond_string(user_input, language=language)
        assert isinstance(parsed, Container)
        return parsed

    def _scale(self, multiplier):
        assert isinstance(multiplier, fractions.Fraction), repr(multiplier)
        for item in list(self):
            item._scale(multiplier)

    ### PUBLIC PROPERTIES ###

    def components(self) -> tuple:
        """
        Gets components in container.
        """
        return tuple(self._components)

    def identifier(self) -> str | None:
        r"""
        Gets bracket comment.

        ..  container:: example

            >>> container = abjad.Container(
            ...     "c'4 d'4 e'4 f'4",
            ...     identifier='%*% AB',
            ...     )
            >>> abjad.show(container) # doctest: +SKIP

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {   %*% AB
                c'4
                d'4
                e'4
                f'4
            }   %*% AB

        """
        return self._identifier

    def set_identifier(self, argument):
        """
        Sets bracket comment.
        """
        assert isinstance(argument, str | type(None)), repr(argument)
        self._identifier = argument

    def name(self) -> str | None:
        r"""
        Gets name of container.

        ..  container:: example

            Gets container name:

            >>> container = abjad.Container("c'4 d'4 e'4 f'4")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> container.name() is None
            True


        """
        return self._name

    def set_name(self, argument):
        """
        Sets name of container.

        ..  container:: example

            >>> container = abjad.Container("c'4 d'4 e'4 f'4", name='Special')
            >>> abjad.show(container) # doctest: +SKIP

            >>> container.name()
            'Special'

            Container name does not appear in LilyPond output:

            >>> string = abjad.lilypond(container)
            >>> print(string)
            {
                c'4
                d'4
                e'4
                f'4
            }

        """
        assert isinstance(argument, str | type(None))
        old_name = self._name
        parent = self._parent
        while parent is not None:
            named_children = parent._named_children
            if old_name is not None:
                named_children[old_name].remove(self)
                if not named_children[old_name]:
                    del named_children[old_name]
            if argument is not None:
                if argument not in named_children:
                    named_children[argument] = [self]
                else:
                    named_children[argument].append(self)
            parent = parent._parent
        self._name = argument

    def simultaneous(self) -> bool | None:
        r"""
        Gets container ``simultaneous`` flag.

        ..  container:: example

            Gets simultaneity status of container:

            >>> container = abjad.Container()
            >>> container.append(abjad.Voice("c'8 d'8 e'8"))
            >>> container.append(abjad.Voice('g4.'))
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                    }
                    \new Voice
                    {
                        g4.
                    }
                }

            >>> container.simultaneous()
            False

        ..  container:: example

            Sets simultaneity status of container:

            >>> container = abjad.Container()
            >>> container.append(abjad.Voice("c'8 d'8 e'8"))
            >>> container.append(abjad.Voice('g4.'))
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                    }
                    \new Voice
                    {
                        g4.
                    }
                }

            >>> container.set_simultaneous(True)
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                <<
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                    }
                    \new Voice
                    {
                        g4.
                    }
                >>

        """
        return self._is_simultaneous

    def set_simultaneous(self, argument):
        """
        Sets container ``simultaneous`` flag.
        """
        if argument is None:
            return
        assert isinstance(argument, bool), repr(argument)
        if argument and not all(isinstance(_, Container) for _ in self):
            message = "simultaneous containers must contain"
            message += " only other containers."
            raise ValueError(message)
        self._is_simultaneous = argument
        self._update_later(offsets=True)

    ### PUBLIC METHODS ###

    def append(self, component: Component, *, language: str = "english") -> None:
        r"""
        Appends ``component`` to container.

        ..  container:: example

            Appends note to container:

            >>> container = abjad.Container("c'4 ( d'4 f'4 )")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> container.append(abjad.Note("e'4"))
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'4
                }

        """
        if isinstance(component, str):
            components = self._parse_string(component, language=language)
            assert len(components) == 1
            component = components[0]
        assert isinstance(component, Component), repr(component)
        self.__setitem__(slice(len(self), len(self)), [component])

    def extend(self, argument, *, language: str = "english") -> None:
        r"""
        Extends container with ``argument``.

        ..  container:: example

            Extends container with three notes:

            >>> container = abjad.Container("c'4 ( d'4 f'4 )")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> notes = [abjad.Note("e'32"), abjad.Note("d'32"), abjad.Note("e'16")]
            >>> container.extend(notes)
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'32
                    d'32
                    e'16
                }

        """
        if isinstance(argument, str):
            argument = self._parse_string(argument, language=language)
        self.__setitem__(
            slice(len(self), len(self)),
            argument.__getitem__(slice(0, len(argument))),
        )

    def index(self, component) -> int:
        r"""
        Returns index of ``component`` in container.

        ..  container:: example

            Gets index of last element in container:

            >>> container = abjad.Container("c'4 d'4 f'4 e'4")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    c'4
                    d'4
                    f'4
                    e'4
                }

            >>> note = container[-1]
            >>> note
            Note("e'4")

            >>> container.index(note)
            3

        """
        for i, element in enumerate(self.components()):
            if element is component:
                return i
        else:
            raise ValueError(f"component {component!r} not in container {self!r}.")

    def insert(
        self, i: int, component: str | Component, *, language: str = "english"
    ) -> None:
        r"""
        Inserts ``component`` at index ``i`` in container.

        ..  container:: example

            Inserts note:

            >>> container = abjad.Container([])
            >>> container.extend("fs16 cs' e' a'")
            >>> container.extend("cs''16 e'' cs'' a'")
            >>> container.extend("fs'16 e' cs' fs")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    fs16
                    cs'16
                    e'16
                    a'16
                    cs''16
                    e''16
                    cs''16
                    a'16
                    fs'16
                    e'16
                    cs'16
                    fs16
                }

            >>> container.insert(-4, abjad.Note("e'4"))
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    fs16
                    cs'16
                    e'16
                    a'16
                    cs''16
                    e''16
                    cs''16
                    a'16
                    e'4
                    fs'16
                    e'16
                    cs'16
                    fs16
                }

        """
        assert isinstance(i, int)
        if isinstance(component, str):
            components = self._parse_string(component, language=language)
            assert len(components) == 1, repr(components)
            component = components[0]
        assert isinstance(component, Component), repr(component)
        self.__setitem__(slice(i, i), [component])
        return

    def pop(self, i: int = -1) -> Component:
        r"""
        Pops component from container at index ``i``.

        ..  container:: example

            Pops last element from container:

            >>> container = abjad.Container("c'4 ( d'4 f'4 ) e'4")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'4
                }

            >>> container.pop()
            Note("e'4")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

        """
        assert isinstance(i, int), repr(i)
        component = self[i]
        del self[i]
        return component

    def remove(self, component: Component) -> None:
        r"""
        Removes ``component`` from container.

        ..  container:: example

            Removes note from container:

            >>> container = abjad.Container("c'4 d'4 f'4 e'4")
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    c'4
                    d'4
                    f'4
                    e'4
                }

            >>> note = container[2]
            >>> note
            Note("f'4")

            >>> container.remove(note)
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(container)
                >>> print(string)
                {
                    c'4
                    d'4
                    e'4
                }

        """
        assert isinstance(component, Component), repr(component)
        i = self.index(component)
        del self[i]


class AfterGraceContainer(Container):
    r"""
    After grace container.

    After grace notes are played in the last moments of duration of the note
    they follow.

    Fill after grace containers with notes, rests or chords.

    Attach after grace containers to notes, rests or chords.

    ..  container:: example

        LilyPond positions after grace notes at a point 3/4 of the way after
        the note they follow. The resulting spacing is usually too loose.
        Customize ``fraction`` as shown here:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> notes = [abjad.Note("c'16"), abjad.Note("d'16")]
        >>> after_grace_container = abjad.AfterGraceContainer(notes, fraction=(15, 16))
        >>> abjad.attach(after_grace_container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \afterGrace 15/16
                d'4
                {
                    c'16
                    d'16
                }
                e'4
                f'4
            }

    ..  container:: example

        REGRESSION. After grace containers format correctly with main note
        articulations and markup:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.AfterGraceContainer("c'16 d'16", fraction=(15, 16))
        >>> abjad.attach(container, voice[1])
        >>> leaves = abjad.select.leaves(voice, grace=None)
        >>> markup = abjad.Markup(r'\markup Allegro')
        >>> abjad.attach(markup, leaves[1], direction=abjad.UP)
        >>> abjad.attach(abjad.Articulation("."), leaves[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \afterGrace 15/16
                d'4
                - \staccato
                ^ \markup Allegro
                {
                    c'16
                    d'16
                }
                e'4
                f'4
            }

    ..  container:: example

        REGRESSION #1074. After grace containers format correctly with chords
        and overrides. It is important here that the ``\afterGrace`` command
        appear lexically after the ``\override`` command:

        >>> voice = abjad.Voice("c'4 <d' f'>4 e'4 f'4")
        >>> container = abjad.AfterGraceContainer("c'16 d'16", fraction=(15, 16))
        >>> abjad.attach(container, voice[1])
        >>> abjad.override(voice[1]).NoteHead.color = "#red"
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \once \override NoteHead.color = #red
                \afterGrace 15/16
                <d' f'>4
                {
                    c'16
                    d'16
                }
                e'4
                f'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_fraction", "_main_leaf")

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        *,
        fraction: tuple[int, int] | None = None,
        language: str = "english",
        tag: _tag.Tag | None = None,
    ) -> None:
        # NOTE: _main_leaf must be initialized before container initialization
        self._main_leaf = None
        Container.__init__(self, components, language=language, tag=tag)
        self.set_fraction(fraction)

    ### SPECIAL METHODS ###

    def __getnewargs__(self) -> tuple[tuple[int, int] | None]:
        """
        Gets new after grace container arguments.

        ..  container:: example

            >>> abjad.AfterGraceContainer("d'8", fraction=(15, 16)).__getnewargs__()
            ((15, 16),)

        """
        return (self.fraction(),)

    ### PRIVATE METHODS ###

    def _attach(self, leaf):
        if not hasattr(leaf, "written_duration"):
            raise TypeError(f"must attach to leaf (not {leaf!r}).")
        leaf._after_grace_container = self
        self._main_leaf = leaf

    def _detach(self):
        if self._main_leaf is not None:
            main_leaf = self._main_leaf
            main_leaf._after_grace_container = None
            self._main_leaf = None
        return self

    def _format_open_brackets_site(self, contributions):
        result = []
        result.extend(["{"])
        return result

    def fraction(self) -> tuple[int, int] | None:
        r"""
        Gets LilyPond `\afterGraceFraction`.
        """
        return self._fraction

    def set_fraction(self, fraction: tuple[int, int] | None):
        r"""
        Sets LilyPond `\afterGraceFraction`.
        """
        if fraction is not None:
            assert isinstance(fraction, tuple), repr(fraction)
            assert len(fraction) == 2, repr(fraction)
            assert isinstance(fraction[0], int), repr(fraction)
            assert isinstance(fraction[0], int), repr(fraction)
            assert isinstance(fraction[1], int), repr(fraction)
        self._fraction = fraction


class BeforeGraceContainer(Container):
    r"""
    Grace container.

    LilyPond provides four types of left-positioned grace music: acciaccaturas,
    appoggiaturas, grace notes and slashed grace notes; see
    ``abjad.BeforeGraceContainer.command`` to choose between these. LilyPond's
    left-positioned grace music contrasts with "right-positioned" after-grace
    music; see ``abjad.AfterGraceContainer``.

    Note that neither LilyPond nor Abjad attempts to model the ways that
    different categories of grace music have been performed historically.
    Typographic differences in slurring and slashing are provided. But
    distinctions between (for example) on-the-beat versus before-the-beat
    performance are left implicit.

    .. container:: example

        Grace container models LilyPond's different types of "left-positioned"
        grace music:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.BeforeGraceContainer("cs'16 ds'")
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
                    ds'16
                }
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Fill grace containers with notes, rests or chords:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.BeforeGraceContainer("<cs' ds'>16 e'")
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \grace {
                    <cs' ds'>16
                    e'16
                }
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Detach grace containers like this:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.BeforeGraceContainer("<cs' ds'>16 e'")
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \grace {
                    <cs' ds'>16
                    e'16
                }
                d'4
                e'4
                f'4
            }

        >>> abjad.detach(abjad.BeforeGraceContainer, voice[1])
        (BeforeGraceContainer("<cs' ds'>16 e'16"),)

        >>> abjad.detach(abjad.BeforeGraceContainer, voice[1])
        ()

        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Move grace containers like this:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.BeforeGraceContainer("<cs' ds'>16 e'")
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \grace {
                    <cs' ds'>16
                    e'16
                }
                d'4
                e'4
                f'4
            }

        >>> result = abjad.detach(abjad.BeforeGraceContainer, voice[1])
        >>> container = result[0]
        >>> abjad.attach(container, voice[3])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                d'4
                e'4
                \grace {
                    <cs' ds'>16
                    e'16
                }
                f'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_command", "_main_leaf")

    _commands = (
        r"\acciaccatura",
        r"\appoggiatura",
        r"\grace",
        r"\slashedGrace",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        *,
        command: str = r"\grace",
        language: str = "english",
        tag: _tag.Tag | None = None,
    ) -> None:
        if command not in self._commands:
            message = f"unknown command: {repr(command)}.\n"
            message += "  must be in {self._commands}"
            raise Exception(message)
        self._command = command
        self._main_leaf = None
        Container.__init__(self, components, language=language, tag=tag)

    ### SPECIAL METHODS ###

    def __getnewargs__(self) -> tuple:
        """
        Gets new grace container arguments.

        Returns tuple of single empty list.
        """
        return ([],)

    ### PRIVATE METHODS ###

    def _attach(self, leaf):
        if not hasattr(leaf, "written_duration"):
            raise TypeError(f"must attach to leaf {leaf!r}.")
        leaf._before_grace_container = self
        self._main_leaf = leaf

    def _detach(self):
        if self._main_leaf is not None:
            main_leaf = self._main_leaf
            main_leaf._before_grace_container = None
            self._main_leaf = None
        return self

    def _format_open_brackets_site(self, contributions):
        result = []
        string = f"{self.command()} {{"
        result.extend([string])
        return result

    ### PUBLIC PROPERTIES ###

    def command(self) -> str:
        r"""
        Gets command. Chooses between LilyPond's four types of left-positioned
        grace music.

        .. container:: example

            **(Vanilla) grace notes.** LilyPond formats single grace notes with
            neither a slash nor a slur:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
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

            LilyPond likewise formats runs of grace notes with neither a slash
            nor a slur:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.BeforeGraceContainer("cs'16 ds'")
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
                        ds'16
                    }
                    d'4
                    e'4
                    f'4
                }

        .. container:: example

            **Acciaccaturas.** LilyPond formats single acciaccaturas with both
            a slash and a slur:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.BeforeGraceContainer(
            ...     "cs'16", command=r"\acciaccatura"
            ... )
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'4
                    \acciaccatura {
                        cs'16
                    }
                    d'4
                    e'4
                    f'4
                }

            ..  container:: example exception

                But LilyPond fails to slash runs of acciaccaturas. This
                behavior is a longstanding LilyPond bug:

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
                >>> container = abjad.BeforeGraceContainer(
                ...     "cs'16 ds'", command=r"\acciaccatura"
                ... )
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        c'4
                        \acciaccatura {
                            cs'16
                            ds'16
                        }
                        d'4
                        e'4
                        f'4
                    }

                ..  note:: LilyPond fails to slash runs of acciaccaturas.

        .. container:: example

            **Appoggiaturas.** LilyPond formats single appoggiaturas with only
            a slur; no slash is included:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.BeforeGraceContainer(
            ...     "cs'16", command=r"\appoggiatura"
            ... )
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'4
                    \appoggiatura {
                        cs'16
                    }
                    d'4
                    e'4
                    f'4
                }

            LilyPond likewise formats runs of appoggiaturas with only a slur:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.BeforeGraceContainer(
            ...     "cs'16 ds'", command=r"\appoggiatura"
            ... )
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'4
                    \appoggiatura {
                        cs'16
                        ds'16
                    }
                    d'4
                    e'4
                    f'4
                }

        .. container:: example

            **Slashed grace notes.** LilyPond formats single slashed grace
            notes with only a slash; no slur is included:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.BeforeGraceContainer(
            ...     "cs'16", command=r"\slashedGrace"
            ... )
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    c'4
                    \slashedGrace {
                        cs'16
                    }
                    d'4
                    e'4
                    f'4
                }

            ..  container:: example exception

                But LilyPond fails to slash runs of "slashed" grace notes. This
                is a longstanding LilyPond bug:

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
                >>> container = abjad.BeforeGraceContainer(
                ...     "cs'16 ds'", command=r"\slashedGrace"
                ... )
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        c'4
                        \slashedGrace {
                            cs'16
                            ds'16
                        }
                        d'4
                        e'4
                        f'4
                    }

                ..  note:: LilyPond fails to slash runs of "slashed" grace notes.

        ..  container:: example

            LilyPond ``\acciaccatura``, ``\appoggiatura`` are syntactic sugar.

            .. container:: example

                **Grace notes with slur may be used instead of appoggiatura:**

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
                >>> container = abjad.BeforeGraceContainer("cs'16")
                >>> abjad.attach(container, voice[1])
                >>> leaves = abjad.select.leaves(voice)[1:3]
                >>> abjad.slur(leaves)
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        c'4
                        \grace {
                            cs'16
                            (
                        }
                        d'4
                        )
                        e'4
                        f'4
                    }

            .. container:: example

                **Slashed grace notes with slur may be used instead of
                acciaccatura:**

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
                >>> container = abjad.BeforeGraceContainer(
                ...     "cs'16", command=r"\slashedGrace"
                ... )
                >>> abjad.attach(container, voice[1])
                >>> leaves = abjad.select.leaves(voice)[1:3]
                >>> abjad.slur(leaves)
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(voice)
                    >>> print(string)
                    \new Voice
                    {
                        c'4
                        \slashedGrace {
                            cs'16
                            (
                        }
                        d'4
                        )
                        e'4
                        f'4
                    }

        """
        return self._command


class Chord(Leaf):
    """
    Chord.

    ..  container:: example

        >>> chord = abjad.Chord("<e' cs'' f''>4")
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <e' cs'' f''>4

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_note_heads",)

    ### INITIALIZER ###

    def __init__(
        self,
        *arguments,
        language: str = "english",
        multiplier: tuple[int, int] | None = None,
        tag: _tag.Tag | None = None,
    ) -> None:
        assert len(arguments) in (0, 1, 2)
        self._note_heads = NoteHeadList()
        if len(arguments) == 1 and isinstance(arguments[0], str):
            string = f"{{ {arguments[0]} }}"
            parsed = self._parse_lilypond_string(string, language=language)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            arguments = tuple([parsed[0]])
        are_cautionary: list[bool | None] = []
        are_forced: list[bool | None] = []
        are_parenthesized: list[bool | None] = []
        if len(arguments) == 1 and isinstance(arguments[0], Leaf):
            leaf = arguments[0]
            written_pitches = []
            written_duration = leaf.written_duration()
            if multiplier is None:
                multiplier = leaf.multiplier()
            # TODO: move to dedicated from_note() constructor:
            if isinstance(leaf, Note) and leaf.note_head() is not None:
                written_pitches.append(leaf.note_head().written_pitch())
                are_cautionary = [leaf.note_head().is_cautionary()]
                are_forced = [leaf.note_head().is_forced()]
                are_parenthesized = [leaf.note_head().is_parenthesized()]
            elif isinstance(leaf, Chord):
                written_pitches.extend(_.written_pitch() for _ in leaf.note_heads())
                are_cautionary = [_.is_cautionary() for _ in leaf.note_heads()]
                are_forced = [_.is_forced() for _ in leaf.note_heads()]
                are_parenthesized = [_.is_parenthesized() for _ in leaf.note_heads()]
        # TODO: move to dedicated constructor:
        elif len(arguments) == 2:
            written_pitches, written_duration = arguments
            if isinstance(written_pitches, str):
                written_pitches = [_ for _ in written_pitches.split() if _]
            elif isinstance(written_pitches, type(self)):
                written_pitches = list(written_pitches.written_pitches())
        elif len(arguments) == 0:
            written_pitches = [_pitch.NamedPitch(_) for _ in [0, 4, 7]]
            written_duration = _duration.Duration(1, 4)
        else:
            raise ValueError(f"can not initialize chord from {arguments!r}.")
        Leaf.__init__(self, written_duration, multiplier=multiplier, tag=tag)
        if not are_cautionary:
            are_cautionary = [None] * len(written_pitches)
        if not are_forced:
            are_forced = [None] * len(written_pitches)
        if not are_parenthesized:
            are_parenthesized = [None] * len(written_pitches)
        for written_pitch, is_cautionary, is_forced, is_parenthesized in zip(
            written_pitches, are_cautionary, are_forced, are_parenthesized
        ):
            if not is_cautionary:
                is_cautionary = False
            if not is_forced:
                is_forced = False
            if not is_parenthesized:
                is_parenthesized = False
            if written_pitch not in _lyconst.drums:
                note_head = NoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                )
            else:
                assert isinstance(written_pitch, str), repr(written_pitch)
                note_head = DrumNoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                )
            if isinstance(written_pitch, NoteHead):
                note_head.tweaks = copy.deepcopy(written_pitch.tweaks)
            self._note_heads.append(note_head)
        if len(arguments) == 1 and isinstance(arguments[0], Leaf):
            self._copy_override_and_set_from_leaf(arguments[0])

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments) -> "Chord":
        """
        Copies chord.
        """
        new_chord = Leaf.__copy__(self, *arguments)
        new_chord.note_heads()[:] = []
        for note_head in self.note_heads():
            note_head = copy.copy(note_head)
            new_chord.note_heads().append(note_head)
        return new_chord

    def __getnewargs__(
        self,
    ) -> tuple[tuple[_pitch.NamedPitch, ...], _duration.Duration]:
        """
        Gets new chord arguments.

        ..  container:: example

            >>> abjad.Chord("<c' d'>4").__getnewargs__()
            ((NamedPitch("c'"), NamedPitch("d'")), Duration(1, 4))

        """
        return self.written_pitches(), self.written_duration()

    ### PRIVATE METHODS ###

    def _format_before_site(self, contributions):
        result = []
        if self._before_grace_container is not None:
            string = self._before_grace_container._get_lilypond_format()
            result.append(string)
        strings = contributions.alphabetize(contributions.before.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        strings = contributions.grob_overrides
        if strings:
            result.append(f"% {_contributions.Types.GROB_OVERRIDES.name}:")
            result.extend(strings)
        strings = contributions.context_settings
        if strings:
            result.append(f"% {_contributions.Types.CONTEXT_SETTINGS.name}:")
            result.extend(strings)
        return result

    def _format_leaf_nucleus(self):
        result = []
        note_heads = self.note_heads()
        if any("\n" in _._get_lilypond_format() for _ in note_heads):
            for note_head in note_heads:
                current_format = note_head._get_lilypond_format()
                format_list = current_format.split("\n")
                format_list = [_indentlib.INDENT + _ for _ in format_list]
                result.extend(format_list)
            result.insert(0, "<")
            result.append(">")
            result = "\n".join(result)
            result += str(self._get_formatted_duration())
        else:
            result.extend([_._get_lilypond_format() for _ in note_heads])
            pitches = " ".join(result)
            duration = self._get_formatted_duration()
            result = f"<{pitches}>{duration}"
        # single string, but wrapped in list bc contribution
        return [result]

    def _get_compact_representation(self):
        summary = self._get_summary()
        duration = self._get_formatted_duration()
        return f"<{summary}>{duration}"

    def _get_summary(self):
        return " ".join([_._get_chord_string() for _ in self.note_heads()])

    ### PUBLIC PROPERTIES ###

    def note_heads(self) -> "NoteHeadList":
        r"""
        Gets note-heads in chord.

        ..  container:: example

            Gets note-heads in chord:

            >>> chord = abjad.Chord("<g' c'' e''>4")
            >>> abjad.show(chord) # doctest: +SKIP
            >>> for _ in chord.note_heads(): _
            NoteHead("g'")
            NoteHead("c''")
            NoteHead("e''")

        ..  container:: example

            Sets note-heads with pitch names:

            >>> chord = abjad.Chord("<g' c'' e''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.set_note_heads("c' d' fs'")
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <c' d' fs'>4

        ..  container:: example

            Sets note-heads with pitch numbers:

                >>> chord = abjad.Chord("<g' c'' e''>4")
                >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.set_note_heads([16, 17, 19])
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <e'' f'' g''>4

        """
        return self._note_heads

    def set_note_heads(self, note_heads):
        """
        Sets note-heads in chord.
        """
        self._note_heads[:] = []
        if isinstance(note_heads, str):
            note_heads = note_heads.split()
        self.note_heads().extend(note_heads)

    def written_duration(self) -> _duration.Duration:
        """
        Gets and sets written duration of chord.

        ..  container:: example

            Get written duration:

            >>> chord = abjad.Chord("<e' cs'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.written_duration()
            Duration(1, 4)

        ..  container:: example

            Set written duration:

            >>> chord = abjad.Chord("<e' cs'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.set_written_duration(abjad.Duration(1, 16))
            >>> abjad.show(chord) # doctest: +SKIP

        """
        return super().written_duration()

    def set_written_duration(self, argument):
        Leaf.set_written_duration(self, argument)

    def written_pitches(self) -> tuple[_pitch.NamedPitch, ...]:
        """
        Written pitches in chord.

        ..  container:: example

            Get written pitches:

            >>> chord = abjad.Chord("<g' c'' e''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.written_pitches()
            (NamedPitch("g'"), NamedPitch("c''"), NamedPitch("e''"))

        ..  container:: example

            Set written pitches with pitch names:

            >>> chord = abjad.Chord("<e' g' c''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.set_written_pitches("f' b' d''")
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <f' b' d''>4

            >>> chord.written_pitches()
            (NamedPitch("f'"), NamedPitch("b'"), NamedPitch("d''"))

        """
        return tuple(_.written_pitch() for _ in self.note_heads())

    def set_written_pitches(self, pitches):
        self.set_note_heads(pitches)


class Cluster(Container):
    r"""
    Cluster.

    ..  container:: example

        >>> cluster = abjad.Cluster("c'8 <d' g'>8 b'8")
        >>> abjad.show(cluster) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(cluster)
            >>> print(string)
            \makeClusters {
                c'8
                <d' g'>8
                b'8
            }

        >>> cluster
        Cluster("c'8 <d' g'>8 b'8")

    """

    __slots__ = ()

    def _format_open_brackets_site(self, contributions):
        result = []
        if self.simultaneous():
            brackets_open = ["<<"]
        else:
            brackets_open = ["{"]
        string = rf"\makeClusters {brackets_open[0]}"
        result.append(string)
        return result


class Context(Container):
    r"""
    LilyPond context.

    ..  container:: example

        >>> context = abjad.Context(lilypond_type='GlobalContext', name='Meter_Voice')
        >>> context
        Context(lilypond_type='GlobalContext', name='Meter_Voice')

        ..  docs::

            >>> string = abjad.lilypond(context)
            >>> print(string)
            \context GlobalContext = "Meter_Voice"
            {
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_lilypond_type",
        "_consists_commands",
        "_dependent_wrappers",
        "_remove_commands",
    )

    _default_lilypond_type = "Voice"

    lilypond_types = (
        "Score",
        "StaffGroup",
        "ChoirStaff",
        "GrandStaff",
        "PianoStaff",
        "Staff",
        "RhythmicStaff",
        "TabStaff",
        "DrumStaff",
        "VaticanaStaff",
        "MensuralStaff",
        "Voice",
        "VaticanaVoice",
        "MensuralVoice",
        "Lyrics",
        "DrumVoice",
        "FiguredBass",
        "TabVoice",
        "CueVoice",
        "ChordNames",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        *,
        language: str = "english",
        lilypond_type: str = "Context",
        name: str | None = None,
        simultaneous: bool = False,
        tag: _tag.Tag | None = None,
    ) -> None:
        self._consists_commands: list[str] = []
        self._dependent_wrappers: list = []
        self._remove_commands: list[str] = []
        self.set_lilypond_type(lilypond_type)
        Container.__init__(
            self,
            simultaneous=simultaneous,
            components=components,
            language=language,
            name=name,
            tag=tag,
        )

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies context.

        Copies indicators.

        Does not copy children.

        Returns new component.
        """
        new_context = Container.__copy__(self)
        new_context._consists_commands = copy.copy(self.consists_commands())
        new_context._remove_commands = copy.copy(self.remove_commands())
        return new_context

    def __getnewargs__(self):
        """
        Gets new context arguments.

        Returns tuple.
        """
        return ([],)

    def __repr__(self) -> str:
        """
        Gets interpreter representation of context.

        ..  container:: example

            >>> context = abjad.Context(
            ...     lilypond_type='GlobalContext',
            ...     name='Meter_Voice',
            ... )
            >>> repr(context)
            "Context(lilypond_type='GlobalContext', name='Meter_Voice')"

        """
        parameters = []
        if self.components():
            string = repr(self._get_contents_summary())
            parameters.append(string)
        if self.lilypond_type() != type(self).__name__:
            parameters.append(f"lilypond_type={self.lilypond_type()!r}")
        if self.name():
            parameters.append(f"name={self.name()!r}")
        if self.simultaneous() is True:
            parameters.append(f"simultaneous={self.simultaneous()!r}")
        string = ", ".join(parameters)
        return f"{type(self).__name__}({string})"

    ### PRIVATE METHODS ###

    def _format_closing_site(self, contributions):
        result = []
        strings = contributions.alphabetize(contributions.closing.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        result = _indent_strings(result)
        return result

    def _format_consists_commands(self):
        result = []
        for engraver in self.consists_commands():
            string = rf"\consists {engraver}"
            result.append(string)
        return result

    def _format_invocation(self):
        if self.name() is not None:
            string = rf'\context {self.lilypond_type()} = "{self.name()}"'
        else:
            string = rf"\new {self.lilypond_type()}"
        return string

    def _format_open_brackets_site(self, contributions):
        result = []
        if self.simultaneous():
            if self.identifier():
                open_bracket = f"<<  {self.identifier()}"
            else:
                open_bracket = "<<"
        else:
            if self.identifier():
                open_bracket = f"{{   {self.identifier()}"
            else:
                open_bracket = "{"
        brackets_open = [open_bracket]
        remove_commands = self._format_remove_commands()
        consists_commands = self._format_consists_commands()
        overrides = contributions.grob_overrides
        settings = contributions.context_settings
        if remove_commands or consists_commands or overrides or settings:
            contributions = [self._format_invocation(), r"\with", "{"]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
            contributions = [_indentlib.INDENT + _ for _ in remove_commands]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
            contributions = [_indentlib.INDENT + _ for _ in consists_commands]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
            contributions = [_indentlib.INDENT + _ for _ in overrides]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
            contributions = [_indentlib.INDENT + _ for _ in settings]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
            contributions = [f"}} {brackets_open[0]}"]
            contributions = ["}", open_bracket]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
        else:
            contribution = self._format_invocation()
            contribution += f" {brackets_open[0]}"
            contributions = [contribution]
            contributions = [self._format_invocation(), open_bracket]
            contributions = self._tag_strings(contributions)
            result.extend(contributions)
        return result

    def _format_opening_site(self, contributions):
        result = []
        strings = contributions.alphabetize(contributions.opening.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        result = _indent_strings(result)
        return result

    def _format_remove_commands(self):
        result = []
        for engraver in self.remove_commands():
            string = rf"\remove {engraver}"
            result.append(string)
        return result

    ### PUBLIC PROPERTIES ###

    def consists_commands(self):
        r"""
        Unordered set of LilyPond engravers to include in context definition.

        ..  container:: example

            Manage with add, update, other standard set commands:

            >>> staff = abjad.Staff([])
            >>> staff.consists_commands().append("Horizontal_bracket_engraver")
            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \consists Horizontal_bracket_engraver
            }
            {
            }

        """
        return self._consists_commands

    def lilypond_context(self):
        """
        Gets ``LilyPondContext`` associated with context.

        Returns LilyPond context instance.
        """
        try:
            lilypond_context = _lyproxy.LilyPondContext(name=self.lilypond_type())
        except AssertionError:
            lilypond_context = _lyproxy.LilyPondContext(
                name=self._default_lilypond_type
            )
        return lilypond_context

    def lilypond_type(self) -> str:
        """
        Gets LilyPond type of context.

        ..  container:: example

            >>> context = abjad.Context(
            ...     lilypond_type="ViolinStaff",
            ...     name="MyViolinStaff",
            ... )
            >>> context.lilypond_type()
            'ViolinStaff'

        """
        return self._lilypond_type

    def set_lilypond_type(self, argument):
        """
        Sets LilyPond type of context.
        """
        if argument is None:
            argument = type(self).__name__
        else:
            argument = str(argument)
        self._lilypond_type = argument

    def remove_commands(self):
        r"""
        Unordered set of LilyPond engravers to remove from context.

        ..  container:: example

            Manage with add, update, other standard set commands:

            >>> staff = abjad.Staff([])
            >>> staff.remove_commands().append("Time_signature_engraver")
            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \remove Time_signature_engraver
            }
            {
            }

        """
        return self._remove_commands


class IndependentAfterGraceContainer(Container):
    r"""
    Independent after grace container.

    ..  container:: example

        LilyPond positions after grace notes at a point 3/4 of the way after
        the note they follow. The resulting spacing is usually too loose.
        Customize ``fraction`` as shown:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> notes = [abjad.Note("c'16"), abjad.Note("d'16")]
        >>> container = abjad.IndependentAfterGraceContainer(notes, fraction=(15, 16))
        >>> voice.insert(2, container)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'4
                \afterGrace 15/16
                d'4
                {
                    c'16
                    d'16
                }
                e'4
                f'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_fraction",)

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        *,
        fraction: tuple[int, int] | None = None,
        language: str = "english",
        tag: _tag.Tag | None = None,
    ) -> None:
        Container.__init__(self, components, language=language, tag=tag)
        self.set_fraction(fraction)

    def __getnewargs__(self):
        """
        Gets new after grace container arguments.

        Returns tuple of single empty list.
        """
        return ([],)

    def _format_open_brackets_site(self, contributions):
        result = []
        result.extend(["{"])
        return result

    def _get_preprolated_duration(self):
        return _duration.Duration(0)

    def fraction(self) -> tuple[int, int] | None:
        r"""
        Gets LilyPond `\afterGraceFraction`.
        """
        return self._fraction

    def set_fraction(self, fraction: tuple[int, int] | None):
        r"""
        Sets LilyPond `\afterGraceFraction`.
        """
        if fraction is not None:
            assert isinstance(fraction, tuple), repr(fraction)
            assert len(fraction) == 2, repr(fraction)
            assert isinstance(fraction[0], int), repr(fraction)
            assert isinstance(fraction[0], int), repr(fraction)
            assert isinstance(fraction[1], int), repr(fraction)
        self._fraction = fraction


class MultimeasureRest(Leaf):
    r"""
    Multimeasure rest.

    ..  container:: example

        >>> rest = abjad.MultimeasureRest("R1")
        >>> abjad.show(rest) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(rest)
            >>> print(string)
            R1

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *arguments,
        language: str = "english",
        multiplier: tuple[int, int] | None = None,
        tag: _tag.Tag | None = None,
    ) -> None:
        if len(arguments) == 0:
            arguments = ((1, 4),)
        rest = Rest(*arguments, language=language)
        Leaf.__init__(self, rest.written_duration(), multiplier=multiplier, tag=tag)

    ### PRIVATE METHODS ###

    def _get_body(self) -> list[str]:
        """
        Gets body of multimeasure rest as list of strings.
        Picked up as contribution at format-time.
        """
        result = "R" + str(self._get_formatted_duration())
        return [result]

    def _get_compact_representation(self):
        return f"R{self._get_formatted_duration()}"


@functools.total_ordering
class NoteHead:
    r"""
    Note-head.

    ..  container:: example

        >>> note = abjad.Note("cs''")
        >>> abjad.show(note) # doctest: +SKIP

        >>> note.note_head()
        NoteHead("cs''")

    ..  container:: example

        >>> note_head = abjad.NoteHead("cs''")
        >>> abjad.tweak(note_head, r"\tweak color #red")
        >>> note_head.tweaks
        (Tweak(string='\\tweak color #red', i=None, tag=None),)

        >>> string = abjad.lilypond(note_head)
        >>> print(string)
        \tweak color #red
        cs''

    ..  container:: example

        >>> chord = abjad.Chord([0, 2, 10], (1, 4))

        >>> abjad.tweak(chord.note_heads()[0], r"\tweak color #red")
        >>> abjad.tweak(chord.note_heads()[0], r"\tweak thickness 2")
        >>> abjad.tweak(chord.note_heads()[1], r"\tweak color #red")
        >>> abjad.tweak(chord.note_heads()[1], r"\tweak thickness 2")
        >>> abjad.tweak(chord.note_heads()[2], r"\tweak color #blue")
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <
                \tweak color #red
                \tweak thickness 2
                c'
                \tweak color #red
                \tweak thickness 2
                d'
                \tweak color #blue
                bf'
            >4

    """

    __slots__ = (
        "_alternative",
        "_is_cautionary",
        "_is_forced",
        "_is_parenthesized",
        "_written_pitch",
        "tweaks",
    )

    def __init__(
        self,
        written_pitch=None,
        *,
        is_cautionary=None,
        is_forced=None,
        is_parenthesized=None,
        tweaks=None,
    ):
        self._alternative = None
        tweaks_ = ()
        if isinstance(written_pitch, NoteHead):
            note_head = written_pitch
            tweaks_ = copy.deepcopy(note_head.tweaks)
            written_pitch = note_head.written_pitch()
            is_cautionary = note_head.is_cautionary()
            is_forced = note_head.is_forced()
        elif written_pitch is None:
            written_pitch = 0
        self.set_written_pitch(written_pitch)
        self.set_is_cautionary(is_cautionary)
        self.set_is_forced(is_forced)
        self.set_is_parenthesized(is_parenthesized)
        self.tweaks = None
        if tweaks is not None:
            assert all(isinstance(_, _tweaks.Tweak) for _ in tweaks)
            tweaks_ = tweaks_ + tuple(tweaks)
        self.tweaks = tweaks_

    def __copy__(self, *arguments) -> "NoteHead":
        """
        Copies note-head.

        ..  container:: example

            >>> import copy
            >>> note_head = abjad.NoteHead(13)
            >>> copy.copy(note_head)
            NoteHead("cs''")

        """
        result = type(self)(
            self.written_pitch(),
            is_cautionary=self.is_cautionary(),
            is_forced=self.is_forced(),
            is_parenthesized=self.is_parenthesized(),
        )
        tweaks = copy.deepcopy(self.tweaks)
        result.tweaks = tweaks
        return result

    def __eq__(self, argument) -> bool:
        """
        Is true when ```argument`` is a note-head with written pitch equal to that of
        this note-head.
        """
        if isinstance(argument, type(self)):
            return self.written_pitch() == argument.written_pitch()
        return self.written_pitch() == argument

    def __hash__(self) -> int:
        """
        Hashes note-head.
        """
        return super().__hash__()

    def __lt__(self, argument) -> bool:
        """
        Is true when ``argument`` is a note-head with written pitch greater than that of
        this note-head.
        """
        if isinstance(argument, type(self)):
            return self.written_pitch() < argument.written_pitch()
        try:
            argument = type(self)(argument)
        except (ValueError, TypeError):
            return False
        return self.written_pitch() < argument.written_pitch()

    def __repr__(self) -> str:
        """
        Gets interpreter representation of note-head.

        ..  container:: example

            >>> note_head = abjad.NoteHead(13)
            >>> note_head
            NoteHead("cs''")

        """
        strings = []
        if isinstance(self.written_pitch(), _pitch.NamedPitch):
            string = self.written_pitch().name()
            strings.append(repr(string))
        # drum note head:
        elif isinstance(self.written_pitch(), str):
            string = repr(self.written_pitch())
            strings.append(string)
        if self.is_cautionary():
            string = f"is_cautionary={self.is_cautionary()!r}"
            strings.append(string)
        if self.is_forced():
            string = f"is_forced={self.is_forced()!r}"
            strings.append(string)
        if self.is_parenthesized():
            string = f"is_parenthesized={self.is_parenthesized()!r}"
            strings.append(string)
        if self.tweaks:
            string = f"tweaks={self.tweaks!r}"
            strings.append(string)
        string = ", ".join(strings)
        return f"{type(self).__name__}({string})"

    def _get_chord_string(self) -> str:
        result = ""
        if self.written_pitch():
            result = self.written_pitch().name()
            if self.is_forced():
                result += "!"
            if self.is_cautionary():
                result += "?"
        return result

    def _get_note_head_strings(self):
        assert self.written_pitch()
        result = []
        if self.is_parenthesized():
            result.append(r"\parenthesize")
        for tweak in sorted(self.tweaks):
            strings = tweak._list_contributions()
            result.extend(strings)
        written_pitch = self.written_pitch()
        if isinstance(written_pitch, _pitch.NamedPitch):
            written_pitch = written_pitch.simplify()
            kernel = written_pitch.name()
        # drum note head:
        else:
            assert isinstance(written_pitch, str)
            kernel = written_pitch
        if self.is_forced():
            kernel += "!"
        if self.is_cautionary():
            kernel += "?"
        result.append(kernel)
        return result

    def _get_lilypond_format(self, duration=None):
        pieces = self._get_note_head_strings()
        if duration is not None:
            pieces[-1] = pieces[-1] + duration
        if self.alternative():
            pieces = _tag.double_tag(pieces, self.alternative()[2])
            pieces_ = self.alternative()[0]._get_note_head_strings()
            if duration is not None:
                pieces_[-1] = pieces_[-1] + duration
            pieces_ = _tag.double_tag(pieces_, self.alternative()[1], deactivate=True)
            pieces.extend(pieces_)
        result = "\n".join(pieces)
        return result

    def alternative(self) -> tuple["NoteHead", _tag.Tag, _tag.Tag]:
        """
        Gets note-head alternative.

        >>> import copy

        ..  container:: example

            >>> note = abjad.Note("c''4")
            >>> alternative = copy.copy(note.note_head())
            >>> alternative.set_is_forced(True)
            >>> triple = (alternative, abjad.Tag("-PARTS"), abjad.Tag("+PARTS"))
            >>> note.note_head().set_alternative(triple)
            >>> abjad.show(note) # doctest: +SKIP

            >>> string = abjad.lilypond(note, tags=True)
            >>> print(string)
            %! +PARTS
            c''4
            %! -PARTS
            %@% c''!4

            Survives pitch reassignment:

            >>> note.set_written_pitch("D5")
            >>> abjad.show(note) # doctest: +SKIP

            >>> string = abjad.lilypond(note, tags=True)
            >>> print(string)
            %! +PARTS
            d''4
            %! -PARTS
            %@% d''!4

            Clear with none:

            >>> note.note_head().set_alternative(None)
            >>> abjad.show(note) # doctest: +SKIP

            >>> string = abjad.lilypond(note, tags=True)
            >>> print(string)
            d''4

        ..  container:: example

            >>> chord = abjad.Chord("<c' d' bf''>4")
            >>> alternative = copy.copy(chord.note_heads()[0])
            >>> alternative.set_is_forced(True)
            >>> triple = (alternative, abjad.Tag("-PARTS"), abjad.Tag("+PARTS"))
            >>> chord.note_heads()[0].set_alternative(triple)
            >>> abjad.show(chord) # doctest: +SKIP

            >>> string = abjad.lilypond(chord, tags=True)
            >>> print(string)
            <
                %! +PARTS
                c'
                %! -PARTS
                %@% c'!
                d'
                bf''
            >4

            Suvives pitch reassignment:

            >>> chord.note_heads()[0].set_written_pitch("B3")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> string = abjad.lilypond(chord, tags=True)
            >>> print(string)
            <
                %! +PARTS
                b
                %! -PARTS
                %@% b!
                d'
                bf''
            >4

            Clear with none:

            >>> chord.note_heads()[0].set_alternative(None)
            >>> string = abjad.lilypond(chord, tags=True)
            >>> print(string)
            <b d' bf''>4

        """
        return self._alternative

    def set_alternative(self, argument):
        """
        Sets note-head alternative.
        """
        if argument is not None:
            assert isinstance(argument, tuple), repr(argument)
            assert len(argument) == 3, repr(argument)
            assert isinstance(argument[0], NoteHead), repr(argument)
            assert argument[0].alternative() is None, repr(argument)
            assert isinstance(argument[1], _tag.Tag), repr(argument)
            assert isinstance(argument[2], _tag.Tag), repr(argument)
        self._alternative = argument

    def is_cautionary(self) -> bool:
        """
        Gets cautionary accidental flag.

        ..  container:: example

            >>> note = abjad.Note("c''")
            >>> note.note_head().set_is_cautionary(True)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c''?4

            >>> note = abjad.Note("cs''")
            >>> note.note_head().set_is_cautionary(True)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''?4

        """
        return self._is_cautionary

    def set_is_cautionary(self, argument):
        """
        Sets cautionary accidental flag.
        """
        self._is_cautionary = bool(argument)

    def is_forced(self) -> bool:
        """
        Gets forced accidental flag.

        ..  container:: example

            >>> note = abjad.Note("c''")
            >>> note.note_head().set_is_forced(True)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c''!4

            >>> note = abjad.Note("cs''")
            >>> note.note_head().set_is_forced(True)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''!4

        """
        return self._is_forced

    def set_is_forced(self, argument):
        """
        Sets forced accidental flag.
        """
        if argument is not None:
            argument = bool(argument)
        self._is_forced = argument

    def is_parenthesized(self) -> bool:
        r"""
        Gets parenthesized accidental flag.

        ..  container:: example

            >>> note = abjad.Note("c''")
            >>> note.note_head().set_is_parenthesized(True)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                \parenthesize
                c''4

            >>> note = abjad.Note("cs''")
            >>> note.note_head().set_is_parenthesized(True)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                \parenthesize
                cs''4

        """
        return self._is_parenthesized

    def set_is_parenthesized(self, argument):
        """
        Sets parenthesized accidental flag.
        """
        if argument is not None:
            argument = bool(argument)
        self._is_parenthesized = argument

    def written_pitch(self) -> _pitch.NamedPitch:
        """
        Gets and sets written pitch of note-head.

        ..  container:: example

            >>> note_head = abjad.NoteHead("cs''")
            >>> note_head.written_pitch()
            NamedPitch("cs''")

            >>> note_head = abjad.NoteHead("cs''")
            >>> note_head.set_written_pitch("d''")
            >>> note_head.written_pitch()
            NamedPitch("d''")

        """
        return self._written_pitch

    def set_written_pitch(self, argument):
        """
        Sets written pitch.
        """
        written_pitch = _pitch.NamedPitch(argument)
        self._written_pitch = written_pitch
        if self.alternative() is not None:
            self.alternative()[0].set_written_pitch(written_pitch)


class DrumNoteHead(NoteHead):
    """
    Drum note-head.

    ..  container:: example

        >>> note_head = abjad.DrumNoteHead("snare")
        >>> note_head
        DrumNoteHead('snare')

    """

    __slots__ = ()

    def __init__(
        self,
        written_pitch: str = "snare",
        *,
        is_cautionary: bool = False,
        is_forced: bool = False,
        is_parenthesized: bool = False,
        tweaks: _tweaks.Tweak | None = None,
    ) -> None:
        NoteHead.__init__(
            self,
            written_pitch=None,
            is_cautionary=is_cautionary,
            is_forced=is_forced,
            is_parenthesized=is_parenthesized,
            tweaks=tweaks,
        )
        assert str(written_pitch) in _lyconst.drums
        drum_pitch = _lyconst.drums[str(written_pitch)]
        self._written_pitch = drum_pitch


class NoteHeadList(list):
    """
    Note-head list.

    ..  container:: example

        >>> for _ in abjad.NoteHeadList([11, 10, 9]): _
        NoteHead("a'")
        NoteHead("bf'")
        NoteHead("b'")

    """

    def __init__(self, argument=()):
        note_heads = [NoteHead(_) for _ in argument]
        list.__init__(self, note_heads)
        self.sort()

    def __setitem__(self, i, argument):
        """
        Coerces ``argument`` and sets at ``i``.
        """
        if isinstance(i, int):
            new_item = NoteHead(argument)
            list.__setitem__(self, i, new_item)
        elif isinstance(i, slice):
            new_items = [NoteHead(_) for _ in argument]
            list.__setitem__(self, i, new_items)
        self.sort()

    def append(self, item):
        """
        Coerces ``item`` and appends note-head.
        """
        if isinstance(item, NoteHead):
            note_head = item
        else:
            note_head = NoteHead(item)
        list.append(self, note_head)
        self.sort()

    def extend(self, items) -> None:
        r"""
        Extends note-heads.

        ..  container:: example

            >>> chord = abjad.Chord("<ef'>")
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <ef'>4

            >>> note_heads = []
            >>> note_head = abjad.NoteHead("cs''")
            >>> abjad.tweak(note_head, r"\tweak color #blue")
            >>> note_heads.append(note_head)
            >>> note_head = abjad.NoteHead("f''")
            >>> abjad.tweak(note_head, r"\tweak color #green")
            >>> note_heads.append(note_head)
            >>> chord.note_heads().extend(note_heads)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <
                    ef'
                    \tweak color #blue
                    cs''
                    \tweak color #green
                    f''
                >4

        """
        note_heads = [_ if isinstance(_, NoteHead) else NoteHead(_) for _ in items]
        list.extend(self, note_heads)
        self.sort()

    def get(self, pitch) -> NoteHead:
        r"""
        Gets note-head by ``pitch``.

        Raises missing note-head error when chord contains no note-head with
        ``pitch``.

        Raises extra note-head error when chord contains more than one
        note-head with ``pitch``.

        ..  container:: example

            Gets note-head by pitch name:

            >>> chord = abjad.Chord("<e' cs'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> note_head = chord.note_heads().get("e'")
            >>> abjad.tweak(note_head, r"\tweak color #red")
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <
                    \tweak color #red
                    e'
                    cs''
                    f''
                >4

        ..  container:: example

            Gets note-head by pitch number:

            >>> chord = abjad.Chord("<e' cs'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> note_head = chord.note_heads().get(4)
            >>> abjad.tweak(note_head, r"\tweak color #red")
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <
                    \tweak color #red
                    e'
                    cs''
                    f''
                >4

        """
        result = []
        pitch = _pitch.NamedPitch(pitch)
        for note_head in self:
            assert isinstance(note_head, NoteHead), repr(note_head)
            if note_head.written_pitch() == pitch:
                result.append(note_head)
        count = len(result)
        if count == 0:
            raise ValueError("missing note-head.")
        elif count == 1:
            note_head = result[0]
            return note_head
        else:
            raise ValueError("extra note-head.")

    def pop(self, i=-1) -> NoteHead:
        r"""
        Pops note-head ``i``.

        ..  container:: example

            >>> chord = abjad.Chord("<ef' c'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <ef' c'' f''>4

            >>> chord.note_heads().pop(1)
            NoteHead("c''")

            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <ef' f''>4

        """
        return list.pop(self, i)

    def remove(self, item):
        r"""
        Removes ``item``.

        ..  container:: example

            >>> chord = abjad.Chord("<ef' c'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <ef' c'' f''>4

            >>> note_head = chord.note_heads()[1]
            >>> chord.note_heads().remove(note_head)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <ef' f''>4

        """
        if isinstance(item, NoteHead):
            note_head = item
        else:
            note_head = NoteHead(item)
        list.remove(self, note_head)


class Note(Leaf):
    """
    Note.

    ..  container:: example

        >>> note = abjad.Note("cs''8.")
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            cs''8.

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_note_head",)

    ### INITIALIZER ###

    def __init__(
        self,
        *arguments,
        language: str = "english",
        multiplier: tuple[int, int] | None = None,
        tag: _tag.Tag | None = None,
    ) -> None:
        assert len(arguments) in (0, 1, 2)
        if len(arguments) == 1 and isinstance(arguments[0], str):
            string = f"{{ {arguments[0]} }}"
            parsed = self._parse_lilypond_string(string, language=language)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            arguments = tuple([parsed[0]])
        written_pitch = None
        is_cautionary = False
        is_forced = False
        is_parenthesized = False
        if len(arguments) == 1 and isinstance(arguments[0], Leaf):
            leaf = arguments[0]
            written_pitch = None
            written_duration = leaf.written_duration()
            if multiplier is None:
                multiplier = leaf.multiplier()
            if isinstance(leaf, Note) and leaf.note_head() is not None:
                written_pitch = leaf.note_head().written_pitch()
                is_cautionary = leaf.note_head().is_cautionary()
                is_forced = leaf.note_head().is_forced()
                is_parenthesized = leaf.note_head().is_parenthesized()
            # TODO: move into separate from_chord() constructor:
            elif isinstance(leaf, Chord):
                written_pitches = [_.written_pitch() for _ in leaf.note_heads()]
                if written_pitches:
                    written_pitch = written_pitches[0]
                    is_cautionary = leaf.note_heads()[0].is_cautionary()
                    is_forced = leaf.note_heads()[0].is_forced()
                    is_parenthesized = leaf.note_heads()[0].is_parenthesized()
        elif len(arguments) == 2:
            written_pitch, written_duration = arguments
        elif len(arguments) == 0:
            written_pitch = _pitch.NamedPitch("C4")
            written_duration = _duration.Duration(1, 4)
        else:
            raise ValueError(f"can not initialize note from {arguments!r}.")
        Leaf.__init__(self, written_duration, multiplier=multiplier, tag=tag)
        if written_pitch is not None:
            if written_pitch not in _lyconst.drums:
                note_head = NoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                )
                self.set_note_head(note_head)
            else:
                assert isinstance(written_pitch, str), repr(written_pitch)
                note_head = DrumNoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                )
                self.set_note_head(note_head)
            if isinstance(written_pitch, NoteHead):
                self.note_head().tweaks = copy.deepcopy(written_pitch.tweaks)
        else:
            raise Exception("must have note-head")
        if len(arguments) == 1 and isinstance(arguments[0], Leaf):
            self._copy_override_and_set_from_leaf(arguments[0])

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments) -> "Note":
        """
        Copies note.
        """
        new_note = Leaf.__copy__(self, *arguments)
        note_head = copy.copy(self.note_head())
        new_note.set_note_head(note_head)
        return new_note

    def __getnewargs__(self) -> tuple:
        """
        Gets new arguments.
        """
        return (self.written_pitch(), self.written_duration())

    ### PRIVATE METHODS ###

    def _get_body(self) -> list[str]:
        duration = self._get_formatted_duration()
        if self.note_head() is not None:
            string = self.note_head()._get_lilypond_format(duration=duration)
        else:
            string = duration
        return [string]

    def _get_compact_representation(self) -> str:
        return self._get_body()[0]

    ### PUBLIC PROPERTIES ###

    def note_head(self) -> NoteHead:
        """
        Gets note-head.

        .. container:: example

            >>> note = abjad.Note("cs''8.")
            >>> note.note_head()
            NoteHead("cs''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''8.

            >>> note.set_note_head("D5")
            >>> note.note_head()
            NoteHead("d''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                d''8.

        """
        return self._note_head

    def set_note_head(self, argument):
        """
        Sets note-head.
        """
        if isinstance(argument, type(None)):
            self._note_head = None
        elif isinstance(argument, NoteHead):
            self._note_head = argument
        else:
            note_head = NoteHead(written_pitch=argument)
            self._note_head = note_head

    def written_duration(self) -> _duration.Duration:
        """
        Gets and sets written duration.

        ..  container:: example

            >>> note = abjad.Note("cs''8.")
            >>> note.written_duration()
            Duration(3, 16)

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''8.

            >>> note.set_written_duration((1, 16))
            >>> note.written_duration()
            Duration(1, 16)

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''16

        """
        return super().written_duration()

    def set_written_duration(self, argument):
        return Leaf.set_written_duration(self, argument)

    # TODO: change Note always to have a note head
    def written_pitch(self) -> _pitch.NamedPitch | None:
        """
        Gets and sets written pitch.

        ..  container:: example

            >>> note = abjad.Note("cs''8.")
            >>> note.written_pitch()
            NamedPitch("cs''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''8.

            >>> note.set_written_pitch("D5")
            >>> note.written_pitch()
            NamedPitch("d''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                d''8.

        """
        if self.note_head() is not None:
            return self.note_head().written_pitch()
        else:
            return None

    def set_written_pitch(self, argument):
        if argument is None:
            if self.note_head() is not None:
                self.note_head().set_written_pitch(None)
        else:
            if self.note_head() is None:
                note_head = NoteHead(self, written_pitch=None)
                self.set_note_head(note_head)
            else:
                pitch = _pitch.NamedPitch(argument)
                self.note_head().set_written_pitch(pitch)

    ### PUBLIC METHODS ###

    @staticmethod
    def from_pitch_and_duration(pitch, duration) -> "Note":
        """
        Makes note from ``pitch`` and ``duration``.

        ..  container:: example

            >>> note = abjad.Note.from_pitch_and_duration("C#5", (3, 16))
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''8.

        """
        note = Note(pitch, duration)
        return note


class Rest(Leaf):
    r"""
    Rest.

    ..  container:: example

        >>> rest = abjad.Rest("r8.")
        >>> staff = abjad.Staff([rest])
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.attach(abjad.TimeSignature((3, 16)), rest)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 3/16
                r8.
            }

    """

    __slots__ = ()

    def __init__(
        self,
        written_duration=None,
        *,
        language: str = "english",
        multiplier: tuple[int, int] | None = None,
        tag: _tag.Tag | None = None,
    ) -> None:
        original_input = written_duration
        if isinstance(written_duration, Leaf):
            multiplier = written_duration.multiplier()
        if isinstance(written_duration, str):
            string = f"{{ {written_duration} }}"
            parsed = self._parse_lilypond_string(string, language=language)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            written_duration = parsed[0]
        if isinstance(written_duration, Leaf):
            written_duration = written_duration.written_duration()
        elif written_duration is None:
            written_duration = _duration.Duration(1, 4)
        else:
            written_duration = _duration.Duration(written_duration)
        Leaf.__init__(self, written_duration, multiplier=multiplier, tag=tag)
        if isinstance(original_input, Leaf):
            self._copy_override_and_set_from_leaf(original_input)

    def _get_body(self) -> list[str]:
        return [self._get_compact_representation()]

    def _get_compact_representation(self) -> str:
        return f"r{self._get_formatted_duration()}"


class Score(Context):
    r"""
    Score.

    ..  container:: example

        >>> staff_1 = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> staff_2 = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score = abjad.Score([staff_1, staff_2])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _default_lilypond_type = "Score"

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        *,
        language: str = "english",
        lilypond_type: str = "Score",
        name: str | None = None,
        simultaneous: bool = True,
        tag: _tag.Tag | None = None,
    ) -> None:
        Context.__init__(
            self,
            components=components,
            language=language,
            lilypond_type=lilypond_type,
            simultaneous=simultaneous,
            name=name,
            tag=tag,
        )


class Skip(Leaf):
    """
    LilyPond skip.

    ..  container:: example

        >>> skip = abjad.Skip("s1")
        >>> skip
        Skip('s1')

        ..  docs::

            >>> string = abjad.lilypond(skip)
            >>> print(string)
            s1

        >>> skip = abjad.Skip("s1", multiplier=(5, 4))
        >>> skip
        Skip('s1 * 5/4')

        ..  docs::

            >>> string = abjad.lilypond(skip)
            >>> print(string)
            s1 * 5/4

        >>> note = abjad.Note("c'4", multiplier=(5, 4))
        >>> skip = abjad.Skip(note)
        >>> skip
        Skip('s4 * 5/4')

        ..  docs::

            >>> string = abjad.lilypond(skip)
            >>> print(string)
            s4 * 5/4

    """

    __slots__ = ("_measure_initial_grace_note",)

    def __init__(
        self,
        *arguments,
        language: str = "english",
        multiplier: tuple[int, int] | None = None,
        tag: _tag.Tag | None = None,
    ) -> None:
        input_leaf = None
        if len(arguments) == 1 and isinstance(arguments[0], str):
            string = f"{{ {arguments[0]} }}"
            parsed = self._parse_lilypond_string(string, language=language)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            input_leaf = parsed[0]
            written_duration = input_leaf.written_duration()
        elif len(arguments) == 1 and isinstance(arguments[0], Leaf):
            input_leaf = arguments[0]
            written_duration = input_leaf.written_duration()
            multiplier = input_leaf.multiplier()
        elif len(arguments) == 1 and not isinstance(arguments[0], str):
            written_duration = arguments[0]
        elif len(arguments) == 0:
            written_duration = _duration.Duration(1, 4)
        else:
            raise ValueError(f"can not initialize skip from {arguments!r}.")
        Leaf.__init__(self, written_duration, multiplier=multiplier, tag=tag)
        if input_leaf is not None:
            self._copy_override_and_set_from_leaf(input_leaf)
        self._measure_initial_grace_note = None

    def _get_body(self) -> list[str]:
        result = []
        if getattr(self, "_measure_initial_grace_note", None) is not None:
            grace_strings = self._measure_initial_grace_note
            assert isinstance(grace_strings, list), repr(grace_strings)
            assert "grace" in repr(grace_strings), repr(grace_strings)
            result.extend(grace_strings)
        result.append(f"s{self._get_formatted_duration()}")
        return result

    def _get_compact_representation(self) -> str:
        return f"s{self._get_formatted_duration()}"


class Staff(Context):
    r"""
    Staff.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }

    """

    __slots__ = ()

    _default_lilypond_type = "Staff"

    def __init__(
        self,
        components=None,
        *,
        language: str = "english",
        lilypond_type: str = "Staff",
        name: str | None = None,
        simultaneous: bool = False,
        tag: _tag.Tag | None = None,
    ) -> None:
        Context.__init__(
            self,
            components=components,
            language=language,
            lilypond_type=lilypond_type,
            simultaneous=simultaneous,
            name=name,
            tag=tag,
        )


class StaffGroup(Context):
    r"""
    Staff group.

    ..  container:: example

        >>> staff_1 = abjad.Staff("c'4 d'4 e'4 f'4 g'1")
        >>> staff_2 = abjad.Staff("g2 f2 e1")
        >>> staff_group = abjad.StaffGroup([staff_1, staff_2])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new StaffGroup
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                    g'1
                }
                \new Staff
                {
                    g2
                    f2
                    e1
                }
            >>

    """

    __slots__ = ()

    _default_lilypond_type = "StaffGroup"

    def __init__(
        self,
        components=None,
        *,
        language: str = "english",
        lilypond_type: str = "StaffGroup",
        name: str | None = None,
        simultaneous: bool = True,
        tag: _tag.Tag | None = None,
    ) -> None:
        Context.__init__(
            self,
            components=components,
            language=language,
            lilypond_type=lilypond_type,
            simultaneous=simultaneous,
            name=name,
            tag=tag,
        )


class TremoloContainer(Container):
    r"""
    Tremolo container.

    ..  container:: example

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \repeat tremolo 2
                {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2
                {
                    d'16
                    f'16
                }
                ds'4
            }

        Duration of container equal to contents duration multiplied by count:

        >>> abjad.get.duration(staff[0])
        Duration(1, 4)

        Duration of each leaf equal to written duration multiplied by count:

        >>> abjad.get.duration(staff[0][0])
        Duration(1, 8)

    """

    __slots__ = ("_count",)

    def __init__(
        self,
        count: int = 2,
        components=None,
        *,
        language: str = "english",
        tag: _tag.Tag | None = None,
    ) -> None:
        assert _math.is_assignable_integer(count), repr(count)
        self._count = count
        Container.__init__(self, components, language=language, tag=tag)
        if len(self) != 2:
            raise Exception(f"must contain 2 leaves (not {len(self)}")

    def __getnewargs__(self) -> tuple:
        """
        Gets new arguments of tremolo container.
        """
        return (self.count(),)

    def _format_open_brackets_site(self, contributions) -> list[str]:
        result = []
        result.append(rf"\repeat tremolo {self.count()}")
        result.append("{")
        return result

    def _get_preprolated_duration(self) -> _duration.Duration:
        return self._get_prolation() * self._get_contents_duration()

    def _get_prolation(self) -> fractions.Fraction:
        return fractions.Fraction(self.count())

    def count(self) -> int:
        """
        Gets count.

        ..  container:: example

            >>> tremolo_container = abjad.TremoloContainer(2, "<c' d'>16 e'16")
            >>> tremolo_container.count()
            2

        """
        return self._count


class Tuplet(Container):
    r"""
    Tuplet.

    ..  container:: example

        A tuplet:

        >>> tuplet = abjad.Tuplet("6:4", "c'8 d'8 e'8")
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tuplet 6/4
            {
                c'8
                d'8
                e'8
            }

    ..  container:: example

        Tweak tuplets like this:

        >>> tuplet_1 = abjad.Tuplet("3:2", "c'4 ( d'4 e'4 )")
        >>> abjad.tweak(tuplet_1, r"\tweak color #red")
        >>> abjad.tweak(tuplet_1, r"\tweak staff-padding 2")

        >>> tuplet_2 = abjad.Tuplet("3:2", "c'4 ( d'4 e'4 )")
        >>> abjad.tweak(tuplet_2, r"\tweak color #green")
        >>> abjad.tweak(tuplet_2, r"\tweak staff-padding 2")

        >>> tuplet_3 = abjad.Tuplet("4:5", [tuplet_1, tuplet_2])
        >>> abjad.tweak(tuplet_3, r"\tweak text #tuplet-number::calc-fraction-text")
        >>> abjad.tweak(tuplet_3, r"\tweak color #blue")
        >>> abjad.tweak(tuplet_3, r"\tweak staff-padding 4")

        >>> staff = abjad.Staff(r"\time 6/4 r4")
        >>> staff.append(tuplet_3)
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 6/4
                r4
                \tweak color #blue
                \tweak staff-padding 4
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 4/5
                {
                    \tweak color #red
                    \tweak staff-padding 2
                    \tuplet 3/2
                    {
                        c'4
                        (
                        d'4
                        e'4
                        )
                    }
                    \tweak color #green
                    \tweak staff-padding 2
                    \tuplet 3/2
                    {
                        c'4
                        (
                        d'4
                        e'4
                        )
                    }
                }
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_ratio",
        "tweaks",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        ratio: tuple[int, int] | str | _duration.Ratio = "3:2",
        components=None,
        *,
        language: str = "english",
        tag: _tag.Tag | None = None,
        tweaks: _tweaks.Tweak | None = None,
    ) -> None:
        Container.__init__(self, components, language=language, tag=tag)
        self.tweaks: tuple[_tweaks.Tweak, ...] = ()
        if isinstance(ratio, _duration.Ratio):
            ratio_ = ratio
        elif isinstance(ratio, str):
            assert ":" in ratio, repr(ratio)
            strings = ratio.split(":")
            assert len(strings) == 2, repr(ratio)
            numbers = [int(_) for _ in strings]
            ratio_ = _duration.Ratio(*numbers)
        else:
            message = f"tuplet ratio must be ratio or string (not {ratio!r})."
            raise ValueError(message)
        self.set_ratio(ratio_)

    ### SPECIAL METHODS ###

    def __getnewargs__(self) -> tuple:
        """
        Gets new arguments of tuplet.
        """
        string = str(self.ratio())
        return (string,)

    def __repr__(self) -> str:
        """
        Gets interpreter representation of tuplet.
        """
        string = self._get_contents_summary()
        return f"{type(self).__name__}({str(self.ratio())!r}, {string!r})"

    ### PRIVATE METHODS ###

    def _format_after_site(self, contributions) -> list[str]:
        result = []
        strings = contributions.grob_reverts
        if strings:
            result.append(f"% {_contributions.Types.GROB_REVERTS.name}:")
            result.extend(strings)
        strings = contributions.alphabetize(contributions.after.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        return result

    def _format_before_site(self, contributions) -> list[str]:
        result = []
        strings = contributions.alphabetize(contributions.before.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        strings = contributions.grob_overrides
        if strings:
            result.append(f"% {_contributions.Types.GROB_OVERRIDES.name}:")
            result.extend(strings)
        strings = contributions.context_settings
        if strings:
            result.append(f"% {_contributions.Types.CONTEXT_SETTINGS.name}:")
            result.extend(strings)
        return result

    def _format_close_brackets(self) -> list[str]:
        result = ["}"]
        self_tag = self.tag()
        if self_tag is not None:
            result = _tag.double_tag(result, self_tag)
        return result

    def _format_closing_site(self, contributions) -> list[str]:
        result = []
        strings = contributions.alphabetize(contributions.closing.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        result = _indent_strings(result)
        return result

    def _format_open_brackets_site(self, contributions) -> list[str]:
        contributions = []
        for tweak in sorted(self.tweaks):
            strings = tweak._list_contributions()
            contributions.extend(strings)
        tuplet_command_string = self._get_tuplet_command_string()
        contributions.append(tuplet_command_string)
        contributions.append("{")
        self_tag = self.tag()
        if self_tag is not None:
            contributions = _tag.double_tag(contributions, self_tag)
        return contributions

    def _format_opening_site(self, contributions) -> list[str]:
        result = []
        strings = contributions.alphabetize(contributions.opening.commands)
        if strings:
            result.append(f"% {_contributions.Types.COMMANDS.name}:")
            result.extend(strings)
        result = _indent_strings(result)
        return result

    def _get_compact_representation(self) -> str:
        if not self:
            return f"{{ {str(self.ratio())} }}"
        return f"{{ {str(self.ratio())} {self._get_contents_summary()} }}"

    def _get_preprolated_duration(self) -> _duration.Duration:
        return self.multiplier() * self._get_contents_duration()

    def _get_prolation(self) -> fractions.Fraction:
        return self.multiplier()

    def _get_summary(self) -> str:
        if 0 < len(self):
            string = ", ".join([str(_) for _ in self.components()])
        else:
            string = ""
        return string

    def _get_tuplet_command_string(self) -> str:
        string = rf"\tuplet {self.ratio().numerator}/{self.ratio().denominator}"
        return string

    def _scale(self, multiplier) -> None:
        assert isinstance(multiplier, fractions.Fraction), repr(multiplier)
        for component in self[:]:
            if isinstance(component, Leaf):
                component._scale(multiplier)
        self.normalize_ratio()

    ### PUBLIC PROPERTIES ###

    def ratio(self) -> _duration.Ratio:
        r"""
        Gets and sets tuplet ratio.

        ..  container:: example

            >>> tuplet = abjad.Tuplet("3:2", "c'8 d'8 e'8")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 3/2
                {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.ratio()
            Ratio(numerator=3, denominator=2)

            >>> tuplet.set_ratio(abjad.Ratio(6, 4))
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 6/4
                {
                    c'8
                    d'8
                    e'8
                }

        """
        return self._ratio

    def set_ratio(self, ratio):
        """
        Sets tuplet ratio.
        """
        assert isinstance(ratio, _duration.Ratio), repr(ratio)
        assert ratio.denominator != 0, repr(ratio)
        self._ratio = ratio

    ### PUBLIC METHODS ###

    def append(
        self,
        component: Component,
        *,
        language: str = "english",
        preserve_duration: bool = False,
    ) -> None:
        r"""
        Appends ``component`` to tuplet.

        ..  container:: example

            Appends note to tuplet:

            >>> tuplet = abjad.Tuplet("3:2", "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tuplet 3/2
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> tuplet.append(abjad.Note("e'4"))
            >>> abjad.makers.tweak_tuplet_bracket_edge_height(tuplet)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'4
                }

        ..  container:: example

            Appends note to tuplet and changes tuplet ratio to preserve tuplet
            duration:

            >>> tuplet = abjad.Tuplet("3:2", "c'4 ( d'4 f'4 )")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> voice = abjad.Voice([tuplet])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 3/2
                    {
                        c'4
                        (
                        d'4
                        f'4
                        )
                    }
                }

            >>> tuplet.append(abjad.Note("e'4"), preserve_duration=True)
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 2/1
                    {
                        c'4
                        (
                        d'4
                        f'4
                        )
                        e'4
                    }
                }

        """
        if preserve_duration is True:
            old_duration = self._get_duration()
        Container.append(self, component, language=language)
        if preserve_duration is True:
            new_duration = self._get_contents_duration()
            multiplier = old_duration / new_duration
            ratio = _duration.Ratio(multiplier.denominator, multiplier.numerator)
            self.set_ratio(ratio)
            assert self._get_duration() == old_duration

    def extend(
        self, argument, *, language: str = "english", preserve_duration: bool = False
    ) -> None:
        r"""
        Extends tuplet with ``argument``.

        ..  container:: example

            Extends tuplet with three notes:

            >>> tuplet = abjad.Tuplet("3:2", "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tuplet 3/2
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> notes = [abjad.Note("e'32"), abjad.Note("d'32"), abjad.Note("e'16")]
            >>> tuplet.extend(notes)
            >>> abjad.makers.tweak_tuplet_bracket_edge_height(tuplet)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak edge-height #'(0.7 . 0)
                \tuplet 3/2
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'32
                    d'32
                    e'16
                }

        ..  container:: example

            Extends tuplet with three notes and preserves tuplet duration:

            >>> tuplet = abjad.Tuplet("3:2", "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tuplet 3/2
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> notes = [abjad.Note("e'32"), abjad.Note("d'32"), abjad.Note("e'16")]
            >>> tuplet.extend(notes, preserve_duration=True)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tuplet 7/4
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'32
                    d'32
                    e'16
                }

        """
        if preserve_duration is True:
            old_duration = self._get_duration()
        Container.extend(self, argument, language=language)
        if preserve_duration is True:
            new_duration = self._get_contents_duration()
            multiplier = old_duration / new_duration
            ratio = _duration.Ratio(multiplier.denominator, multiplier.numerator)
            self.set_ratio(ratio)
            assert self._get_duration() == old_duration

    def is_rest_filled(self) -> bool:
        r"""
        Is true when tuplet is rest-filled.

        ..  container:: example

            >>> tuplet = abjad.Tuplet("3:2", "r2 r2 r2")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tuplet 3/2
                {
                    r2
                    r2
                    r2
                }

            >>> tuplet.is_rest_filled()
            True

        """
        return all(isinstance(_, Rest) for _ in self)

    def is_trivial(self) -> bool:
        r"""
        Is true when tuplet ratio reduces to 1:1.

        ..  container:: example

            >>> tuplet = abjad.Tuplet("1:1", "c'8 d'8 e'8")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.is_trivial()
            True

        ..  container:: example

            Is false when duration multiplier attaches to leaf in tuplet:

            >>> tuplet = abjad.Tuplet("1:1", "c'8 d'8 e'8")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> tuplet[0].set_multiplier((2, 1))
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'8 * 2/1
                    d'8
                    e'8
                }

            >>> tuplet.is_trivial()
            False

        """
        if not self.ratio().is_trivial():
            return False
        for component in self:
            if isinstance(component, Tuplet):
                continue
            elif hasattr(component, "written_duration"):
                if component.multiplier() is not None:
                    return False
        return True

    def is_trivializable(self) -> bool:
        r"""
        Is true when tuplet can be rewritten with a ratio of 1:1.

        ..  container:: example

            >>> tuplet = abjad.Tuplet("4:3", "c'4 c'4 c'4 c'4")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> staff = abjad.Staff([tuplet])
            >>> score = abjad.Score([staff], name="Score")
            >>> abjad.attach(abjad.TimeSignature((3, 4)), tuplet[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 4/3
                {
                    \time 3/4
                    c'4
                    c'4
                    c'4
                    c'4
                }

            >>> tuplet.is_trivializable()
            True

            >>> tuplet.trivialize()
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    \time 3/4
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                }

        ..  container:: example

            >>> tuplet = abjad.Tuplet("5:3", "c'4 c'4 c'4 c'4 c'4")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> staff = abjad.Staff([tuplet])
            >>> score = abjad.Score([staff], name="Score")
            >>> abjad.attach(abjad.TimeSignature((3, 4)), tuplet[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 5/3
                    {
                        \time 3/4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                }

            >>> tuplet.is_trivializable()
            False

        """
        for component in self:
            if isinstance(component, Tuplet):
                continue
            assert isinstance(component, Leaf), repr(component)
            duration = self.multiplier() * component.written_duration()
            if not duration.is_assignable():
                return False
        return True

    def multiplier(self) -> fractions.Fraction:
        """
        Gets tuplet multiplier.

        ..  container:: example

            >>> abjad.Tuplet("6:4", "c'4 d'4 e'4").multiplier()
            Fraction(2, 3)

        """
        return self.ratio().reciprocal().as_fraction()

    def normalize_ratio(self) -> None:
        r"""
        Normalizes tuplet ratio.

        ..  container:: example

            >>> tuplet = abjad.Tuplet("3:1", "c'4 d' e'")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tuplet 3/1
                {
                    c'4
                    d'4
                    e'4
                }

            >>> tuplet.ratio().is_normalized()
            False

            >>> tuplet.normalize_ratio()
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

            >>> tuplet.ratio().is_normalized()
            True

        ..  container:: example

            >>> tuplet = abjad.Tuplet("3:8", "c'32 d'32 e'32")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 3/8
                {
                    c'32
                    d'32
                    e'32
                }

            >>> tuplet.ratio().is_normalized()
            False

            >>> tuplet.normalize_ratio()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 3/4
                {
                    c'16
                    d'16
                    e'16
                }

            >>> tuplet.ratio().is_normalized()
            True

        ..  container:: example

            >>> tuplet = abjad.Tuplet("12:5", "c'4 d'4 e'4")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 12/5
                {
                    c'4
                    d'4
                    e'4
                }

            >>> tuplet.ratio().is_normalized()
            False

            >>> tuplet.normalize_ratio()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 6/5
                {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.ratio().is_normalized()
            True

        """
        multiplier_ = _math.greatest_power_of_two_less_equal(self.multiplier())
        multiplier = fractions.Fraction(multiplier_)
        for component in self:
            if isinstance(component, Leaf):
                component._scale(multiplier)
        multiplier = self.multiplier() / multiplier
        ratio = _duration.Ratio(multiplier.denominator, multiplier.numerator)
        self.set_ratio(ratio)
        assert self.ratio().is_normalized()

    def rewrite_dots(self) -> None:
        r"""
        Rewrites dots of leaves in tuplet.

        Not implemented for multiply nested tuplets.

        ..  container:: example

            Rewrites single dots as 3:2 prolation:

            >>> tuplet = abjad.Tuplet("1:1", "c'8. c'8.")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'8.
                    c'8.
                }

            >>> tuplet.rewrite_dots()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 2/3
                {
                    c'8
                    c'8
                }

        ..  container:: example

            Rewrites double dots as 7:4 prolation:

            >>> tuplet = abjad.Tuplet("1:1", "c'8.. c'8..")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'8..
                    c'8..
                }

            >>> tuplet.rewrite_dots()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 4/7
                {
                    c'8
                    c'8
                }

        ..  container:: example

            Does nothing when dot counts differ:

            >>> tuplet = abjad.Tuplet("1:1", "c'8. d'8. e'8")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'8.
                    d'8.
                    e'8
                }

            >>> tuplet.rewrite_dots()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'8.
                    d'8.
                    e'8
                }

        ..  container:: example

            Does nothing when leaves carry no dots:

            >>> tuplet = abjad.Tuplet("2:3", "c'8 d' e'")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 2/3
                {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.rewrite_dots()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 2/3
                {
                    c'8
                    d'8
                    e'8
                }

        """
        dot_counts = set()
        for component in self:
            if isinstance(component, Tuplet):
                return
            dot_count = component.written_duration().dot_count()
            dot_counts.add(dot_count)
        if 1 < len(dot_counts):
            return
        assert len(dot_counts) == 1
        global_dot_count = dot_counts.pop()
        if global_dot_count == 0:
            return
        dot_multiplier = _duration.fraction_from_dot_count(global_dot_count)
        multiplier = dot_multiplier * self.multiplier()
        ratio = _duration.Ratio(multiplier.denominator, multiplier.numerator)
        self.set_ratio(ratio)
        dot_multiplier_duration = _duration.Duration(dot_multiplier)
        dot_multiplier_reciprocal_duration = dot_multiplier_duration.reciprocal()
        for component in self:
            component_written_duration = component.written_duration()
            component_written_duration *= dot_multiplier_reciprocal_duration
            component.set_written_duration(component_written_duration)

    def toggle_prolation(self) -> None:
        r"""
        Toggles tuplet prolation.

        Not implemented for nested tuplets.

        ..  container:: example

            Changes augmented tuplet to diminished; that is, multiplies the
            written duration of the leaves in tuplet by the least power of
            ``2`` necessary to diminshed tuplet:

            >>> tuplet = abjad.Tuplet("3:4", "c'8 d'8 e'8")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 3/4
                {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.toggle_prolation()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 3/2
                {
                    c'4
                    d'4
                    e'4
                }

        ..  container:: example

            Changes diminished tuplet to augmented; that is, divides the
            written duration of the leaves in tuplet by the least power of
            ``2`` necessary to diminshed tuplet.

            >>> tuplet = abjad.Tuplet("3:2", "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tuplet 3/2
                {
                    c'4
                    d'4
                    e'4
                }

            >>> tuplet.toggle_prolation()
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 3/4
                {
                    c'8
                    d'8
                    e'8
                }

        ..  container:: example

            Leaves trivial tuplets unchanged:

            >>> tuplet = abjad.Tuplet("1:1", "c'4 d'4 e'4")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'4
                    d'4
                    e'4
                }

            >>> tuplet.toggle_prolation()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'4
                    d'4
                    e'4
                }

        """
        if self.ratio().is_diminished():
            while self.ratio().is_diminished():
                multiplier = 2 * self.multiplier()
                ratio = _duration.Ratio(multiplier.denominator, multiplier.numerator)
                self.set_ratio(ratio)
                for component in self._get_subtree():
                    if isinstance(component, Leaf):
                        component_written_duration = component.written_duration()
                        component_written_duration /= 2
                        component.set_written_duration(component_written_duration)
        elif self.ratio().is_augmented():
            while not self.ratio().is_diminished():
                multiplier = self.multiplier() / 2
                ratio = _duration.Ratio(multiplier.denominator, multiplier.numerator)
                self.set_ratio(ratio)
                for component in self._get_subtree():
                    if isinstance(component, Leaf):
                        component_written_duration = component.written_duration()
                        component_written_duration *= 2
                        component.set_written_duration(component_written_duration)

    def trivialize(self) -> None:
        r"""
        Rewrites tuplet with ratio of 1:1.

        ..  container:: example

            >>> tuplet = abjad.Tuplet("4:3", "c'4 c'4 c'4 c'4")
            >>> abjad.tweak(tuplet, r"\tweak text #tuplet-number::calc-fraction-text")
            >>> staff = abjad.Staff([tuplet])
            >>> score = abjad.Score([staff], name="Score")
            >>> abjad.attach(abjad.TimeSignature((3, 4)), tuplet[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 4/3
                {
                    \time 3/4
                    c'4
                    c'4
                    c'4
                    c'4
                }

            >>> tuplet.is_trivializable()
            True

            >>> tuplet.trivialize()
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    \time 3/4
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                }

        """
        if not self.is_trivializable():
            return
        for component in self:
            if isinstance(component, Tuplet):
                multiplier = self.multiplier() * component.multiplier()
                ratio = _duration.Ratio(multiplier.denominator, multiplier.numerator)
                component.set_ratio(ratio)
            elif isinstance(component, Leaf):
                component_written_duration = component.written_duration()
                component_written_duration *= self.multiplier()
                component.set_written_duration(component_written_duration)
            else:
                raise TypeError(component)
        self.set_ratio(_duration.Ratio(1, 1))


class Voice(Context):
    r"""
    Voice.

    Voice-contexted indicators like dynamics work with nested voices.

    ..  container:: example

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8")
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'8
                d'8
                e'8
                f'8
            }

    ..  container:: example

        Forte affects all red notes:

        >>> outer_red_voice = abjad.Voice("e''8 d''", name='Red_Voice')
        >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name='Red_Voice')
        >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name='Blue_Voice')
        >>> container = abjad.Container(
        ...     [inner_red_voice, inner_blue_voice],
        ...     simultaneous=True,
        ...     )
        >>> outer_red_voice.append(container)
        >>> outer_red_voice.extend("d''8")
        >>> abjad.override(outer_red_voice).NoteHead.color = "#red"
        >>> command = abjad.VoiceNumber(1)
        >>> abjad.attach(command, outer_red_voice[0])
        >>> abjad.override(inner_blue_voice).NoteHead.color = "#blue"
        >>> command = abjad.VoiceNumber(2)
        >>> abjad.attach(command, inner_blue_voice[0])
        >>> dynamic = abjad.Dynamic('f')
        >>> abjad.attach(dynamic, outer_red_voice[0])
        >>> abjad.show(outer_red_voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(outer_red_voice)
            >>> print(string)
            \context Voice = "Red_Voice"
            \with
            {
                \override NoteHead.color = #red
            }
            {
                \voiceOne
                e''8
                \f
                d''8
                <<
                    \context Voice = "Red_Voice"
                    {
                        c''4
                        b'4
                        c''8
                    }
                    \context Voice = "Blue_Voice"
                    \with
                    {
                        \override NoteHead.color = #blue
                    }
                    {
                        \voiceTwo
                        e'4
                        f'4
                        e'8
                    }
                >>
                d''8
            }

        >>> for leaf in abjad.iterate.leaves(outer_red_voice):
        ...     dynamic = abjad.get.effective_indicator(leaf, abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        Note("e''8") Dynamic(name='f', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("d''8") Dynamic(name='f', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("c''4") Dynamic(name='f', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("b'4") Dynamic(name='f', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("c''8") Dynamic(name='f', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("e'4") None
        Note("f'4") None
        Note("e'8") None
        Note("d''8") Dynamic(name='f', command=None, leak=False, name_is_textual=False, ordinal=None)

    ..  container:: example

        Piano affects all blue notes:

        >>> outer_red_voice = abjad.Voice("e''8 d''", name='Red_Voice')
        >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name='Red_Voice')
        >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name='Blue_Voice')
        >>> container = abjad.Container(
        ...     [inner_red_voice, inner_blue_voice],
        ...     simultaneous=True,
        ...     )
        >>> outer_red_voice.append(container)
        >>> outer_red_voice.extend("d''8")
        >>> abjad.override(outer_red_voice).NoteHead.color = "#red"
        >>> command = abjad.VoiceNumber(1)
        >>> abjad.attach(command, outer_red_voice[0])
        >>> abjad.override(inner_blue_voice).NoteHead.color = "#blue"
        >>> command = abjad.VoiceNumber(2)
        >>> abjad.attach(command, inner_blue_voice[0])
        >>> dynamic = abjad.Dynamic('p')
        >>> abjad.attach(dynamic, inner_blue_voice[0])
        >>> abjad.show(outer_red_voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(outer_red_voice)
            >>> print(string)
            \context Voice = "Red_Voice"
            \with
            {
                \override NoteHead.color = #red
            }
            {
                \voiceOne
                e''8
                d''8
                <<
                    \context Voice = "Red_Voice"
                    {
                        c''4
                        b'4
                        c''8
                    }
                    \context Voice = "Blue_Voice"
                    \with
                    {
                        \override NoteHead.color = #blue
                    }
                    {
                        \voiceTwo
                        e'4
                        \p
                        f'4
                        e'8
                    }
                >>
                d''8
            }

        >>> for leaf in abjad.iterate.leaves(outer_red_voice):
        ...     dynamic = abjad.get.effective_indicator(leaf, abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        Note("e''8") None
        Note("d''8") None
        Note("c''4") None
        Note("b'4") None
        Note("c''8") None
        Note("e'4") Dynamic(name='p', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("f'4") Dynamic(name='p', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("e'8") Dynamic(name='p', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("d''8") None

    ..  container:: example

        Mezzoforte affects red notes from C4 forward:

        >>> outer_red_voice = abjad.Voice("e''8 d''", name='Red_Voice')
        >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name='Red_Voice')
        >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name='Blue_Voice')
        >>> container = abjad.Container(
        ...     [inner_red_voice, inner_blue_voice],
        ...     simultaneous=True,
        ...     )
        >>> outer_red_voice.append(container)
        >>> outer_red_voice.extend("d''8")
        >>> abjad.override(outer_red_voice).NoteHead.color = "#red"
        >>> command = abjad.VoiceNumber(1)
        >>> abjad.attach(command, outer_red_voice[0])
        >>> abjad.override(inner_blue_voice).NoteHead.color = "#blue"
        >>> command = abjad.VoiceNumber(2)
        >>> abjad.attach(command, inner_blue_voice[0])
        >>> dynamic = abjad.Dynamic('mf')
        >>> abjad.attach(dynamic, inner_red_voice[0])
        >>> abjad.show(outer_red_voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(outer_red_voice)
            >>> print(string)
            \context Voice = "Red_Voice"
            \with
            {
                \override NoteHead.color = #red
            }
            {
                \voiceOne
                e''8
                d''8
                <<
                    \context Voice = "Red_Voice"
                    {
                        c''4
                        \mf
                        b'4
                        c''8
                    }
                    \context Voice = "Blue_Voice"
                    \with
                    {
                        \override NoteHead.color = #blue
                    }
                    {
                        \voiceTwo
                        e'4
                        f'4
                        e'8
                    }
                >>
                d''8
            }

        >>> for leaf in abjad.iterate.leaves(outer_red_voice):
        ...     dynamic = abjad.get.effective_indicator(leaf, abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        Note("e''8") None
        Note("d''8") None
        Note("c''4") Dynamic(name='mf', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("b'4") Dynamic(name='mf', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("c''8") Dynamic(name='mf', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("e'4") None
        Note("f'4") None
        Note("e'8") None
        Note("d''8") Dynamic(name='mf', command=None, leak=False, name_is_textual=False, ordinal=None)

    ..  container:: example

        Mezzoforte and piano set at the same time:

        >>> outer_red_voice = abjad.Voice("e''8 d''", name='Red_Voice')
        >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name='Red_Voice')
        >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name='Blue_Voice')
        >>> container = abjad.Container(
        ...     [inner_red_voice, inner_blue_voice],
        ...     simultaneous=True,
        ...     )
        >>> outer_red_voice.append(container)
        >>> outer_red_voice.extend("d''8")
        >>> abjad.override(outer_red_voice).NoteHead.color = "#red"
        >>> command = abjad.VoiceNumber(1)
        >>> abjad.attach(command, outer_red_voice[0])
        >>> abjad.override(inner_blue_voice).NoteHead.color = "#blue"
        >>> command = abjad.VoiceNumber(2)
        >>> abjad.attach(command, inner_blue_voice[0])
        >>> dynamic = abjad.Dynamic('mf')
        >>> abjad.attach(dynamic, inner_red_voice[0])
        >>> dynamic = abjad.Dynamic('p')
        >>> abjad.attach(dynamic, inner_blue_voice[0])
        >>> abjad.show(outer_red_voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(outer_red_voice)
            >>> print(string)
            \context Voice = "Red_Voice"
            \with
            {
                \override NoteHead.color = #red
            }
            {
                \voiceOne
                e''8
                d''8
                <<
                    \context Voice = "Red_Voice"
                    {
                        c''4
                        \mf
                        b'4
                        c''8
                    }
                    \context Voice = "Blue_Voice"
                    \with
                    {
                        \override NoteHead.color = #blue
                    }
                    {
                        \voiceTwo
                        e'4
                        \p
                        f'4
                        e'8
                    }
                >>
                d''8
            }

        >>> for leaf in abjad.iterate.leaves(outer_red_voice):
        ...     dynamic = abjad.get.effective_indicator(leaf, abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        Note("e''8") None
        Note("d''8") None
        Note("c''4") Dynamic(name='mf', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("b'4") Dynamic(name='mf', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("c''8") Dynamic(name='mf', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("e'4") Dynamic(name='p', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("f'4") Dynamic(name='p', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("e'8") Dynamic(name='p', command=None, leak=False, name_is_textual=False, ordinal=None)
        Note("d''8") Dynamic(name='mf', command=None, leak=False, name_is_textual=False, ordinal=None)

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _default_lilypond_type = "Voice"

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        *,
        language: str = "english",
        lilypond_type: str = "Voice",
        name: str | None = None,
        simultaneous: bool = False,
        tag: _tag.Tag | None = None,
    ) -> None:
        Context.__init__(
            self,
            components=components,
            language=language,
            lilypond_type=lilypond_type,
            simultaneous=simultaneous,
            name=name,
            tag=tag,
        )
