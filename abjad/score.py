import collections
import copy
import fractions
import functools
import math
import typing

from . import _indentlib, _updatelib
from . import contributions as _contributions
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
from . import typings as _typings


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
        component = type(self)(*self.__getnewargs__(), tag=self.tag)
        if hasattr(self, "identifier"):
            component.identifier = self.identifier
        if hasattr(self, "lilypond_type"):
            component.lilypond_type = self.lilypond_type
        if hasattr(self, "name"):
            component.name = self.name
        if hasattr(self, "simultaneous"):
            component.simultaneous = self.simultaneous
        if getattr(self, "_overrides", None) is not None:
            component._overrides = copy.copy(_overrides.override(self))
        if getattr(self, "_lilypond_setting_name_manager", None) is not None:
            component._lilypond_setting_name_manager = copy.copy(
                _overrides.setting(self)
            )
        for wrapper in self._wrappers:
            if not wrapper.annotation:
                continue
            wrapper_ = copy.copy(wrapper)
            wrapper_._component = component
            wrapper_._bind_component(component)
        for wrapper in list(self._get_indicators(unwrap=False)):
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
            multiplier = getattr(parent, "implied_prolation", fractions.Fraction(1))
            duration *= multiplier
        return duration

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
            elif isinstance(wrapper.unbundle_indicator(), prototype_classes):
                result.append(wrapper)
            elif any(wrapper.unbundle_indicator() == _ for _ in prototype_objects):
                result.append(wrapper)
        if attributes is not None:
            result_ = []
            for wrapper in result:
                for name, value in attributes.items():
                    if getattr(wrapper.unbundle_indicator(), name, None) != value:
                        break
                else:
                    result_.append(wrapper)
            result = result_
        if unwrap:
            indicators = []
            for wrapper in result:
                indicators.append(wrapper.unbundle_indicator())
            result = indicators
        result = result
        return result

    def _get_lilypond_format(self):
        _updatelib._update_now(self, indicators=True)
        string = _format.format_component(self)
        return string

    def _get_markup(self, direction=None):
        wrappers = self._get_indicators(_indicators.Markup, unwrap=False)
        if direction is _enums.UP:
            return tuple(_.get_item() for _ in wrappers if _.direction is _enums.UP)
        elif direction is _enums.DOWN:
            return tuple(_.get_item() for _ in wrappers if _.direction is _enums.DOWN)
        indicators = [_.get_item() for _ in wrappers]
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
        if self._parent.simultaneous:
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
            sibling = parent._get_sibling(_math.sign(n))
            if sibling is not None:
                return sibling

    def _tag_strings(self, strings):
        if self.tag is not None:
            strings = _tag.double_tag(strings, self.tag)
        return strings

    def _update_later(self, offsets=False, offsets_in_seconds=False):
        assert offsets or offsets_in_seconds
        for component in self._get_parentage():
            if offsets:
                component._offsets_are_current = False
            elif offsets_in_seconds:
                component._offsets_in_seconds_are_current = False

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self) -> _tag.Tag | None:
        """
        Gets component tag.
        """
        if self._tag is not None:
            assert isinstance(self._tag, _tag.Tag), repr(self._tag)
        return self._tag

    @tag.setter
    def tag(self, argument):
        if argument is not None:
            assert isinstance(argument, _tag.Tag), repr(argument)
        self._tag = argument


class Leaf(Component):
    """
    Leaf baseclass.

    Leaves include notes, rests, chords and skips.
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
        self, written_duration, *, multiplier=None, tag: _tag.Tag | None = None
    ) -> None:
        Component.__init__(self, tag=tag)
        self._after_grace_container = None
        self._before_grace_container = None
        self.multiplier = multiplier
        self.written_duration = written_duration

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies leaf.
        """
        leaf = Component.__copy__(self, *arguments)
        leaf.multiplier = self.multiplier
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
        return (self.written_duration,)

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
        if self.tag is not None and self.tag.string:
            strings = _tag.double_tag(strings, self.tag)
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
            if self._after_grace_container.fraction is not None:
                n, d = self._after_grace_container.fraction
                string = f"{string} {n}/{d}"
            result.append(string)
        if self._is_followed_by_after_grace_container():
            assert self._after_grace_container is None, repr(
                self._after_grace_container
            )
            string = r"\afterGrace"
            container = self._get_following_after_grace_container()
            if container.fraction is not None:
                n, d = container.fraction
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
        strings = []
        strings.append(self.written_duration.lilypond_duration_string)
        if self.multiplier is not None:
            strings.append(f"{self.multiplier[0]}/{self.multiplier[1]}")
        if hasattr(self._parent, "_leaf_multiplier"):
            multiplier = self._parent._leaf_multiplier()
            if multiplier is not None:
                strings.append(str(multiplier))
        result = " * ".join(strings)
        return result

    def _get_multiplied_duration(self):
        if self.written_duration:
            if self.multiplier is not None:
                duration = _duration.Duration(self.multiplier) * self.written_duration
                return _duration.Duration(duration)
            return _duration.Duration(self.written_duration)

    def _get_preprolated_duration(self):
        return self._get_multiplied_duration()

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
        self.written_duration *= multiplier

    ### PUBLIC PROPERTIES ###

    @property
    def multiplier(self) -> tuple[int, int] | None:
        """
        Gets multiplier.
        """
        return self._multiplier

    @multiplier.setter
    def multiplier(self, argument):
        if argument is None:
            self._multiplier = None
        else:
            assert isinstance(argument, tuple), repr(argument)
            assert len(argument) == 2, repr(argument)
            self._multiplier = argument

    @property
    def written_duration(self) -> _duration.Duration:
        """
        Gets written duration.
        """
        return self._written_duration

    @written_duration.setter
    def written_duration(self, argument):
        duration = _duration.Duration(argument)
        if not duration.is_assignable:
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

    __documentation_section__ = "Containers"

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
        self.identifier = identifier
        self.simultaneous = bool(simultaneous)
        # sets name permanently after _initalize_components:
        self.name = name

    ### SPECIAL METHODS ###

    def __contains__(self, argument) -> bool:
        """
        Is true when ``argument`` appears in container.
        """
        if isinstance(argument, str):
            return argument in self._named_children
        else:
            for component in self.components:
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
            >>> voice.append(abjad.Tuplet((4, 6), "c'4 d'4 e'4"))
            >>> voice.append(abjad.Tuplet((2, 3), "e'4 d'4 c'4"))
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

            >>> abjad.wf.wellformed(voice)
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

            >>> abjad.wf.wellformed(tuplet_1)
            True

        """
        result = self[i]
        wrappers = []
        for component in self._get_components(result):
            wrappers_ = component._get_indicators(unwrap=False)
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
            return self.components.__getitem__(argument)
        elif isinstance(argument, slice):
            result = self.components.__getitem__(argument)
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

    def __iter__(self):
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

        Returns generator.
        """
        return iter(self.components)

    def __len__(self) -> int:
        """
        Gets number of components in container.
        """
        return len(self.components)

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
            wrappers_ = component._get_indicators(unwrap=False)
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
        if self.simultaneous:
            if self.identifier:
                string = f">>  {self.identifier}"
            else:
                string = ">>"
        else:
            if self.identifier:
                string = f"}}   {self.identifier}"
            else:
                string = "}"
        strings.append(string)
        if self.tag is not None:
            strings = _tag.double_tag(strings, self.tag)
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
        for component in self.components:
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
        if self.simultaneous:
            if self.identifier:
                string = f"<<  {self.identifier}"
            else:
                string = "<<"
        else:
            if self.identifier:
                string = f"{{   {self.identifier}"
            else:
                string = "{"
        strings.append(string)
        if self.tag is not None:
            strings = _tag.double_tag(strings, self.tag)
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
        if self.simultaneous:
            open_bracket_string, close_bracket_string = "<<", ">>"
        else:
            open_bracket_string, close_bracket_string = "{", "}"
        name = self.name
        if name is not None:
            name = f'-"{name}"'
        else:
            name = ""
        if hasattr(self, "_lilypond_type"):
            result = "<{}{}{}{}{}>"
            result = result.format(
                self.lilypond_type,
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
        if self.simultaneous:
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
            for component in self.components:
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
        if self.simultaneous:
            for item in self:
                result.extend(item._get_descendants_starting_with())
        elif self:
            result.extend(self[0]._get_descendants_starting_with())
        return result

    def _get_descendants_stopping_with(self):
        result = []
        result.append(self)
        if self.simultaneous:
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
            self.simultaneous = parsed.simultaneous
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
        for item in list(self):
            item._scale(multiplier)

    ### PUBLIC PROPERTIES ###

    @property
    def components(self) -> tuple:
        """
        Gets components in container.
        """
        return tuple(self._components)

    @property
    def identifier(self) -> str | None:
        r"""
        Gets and sets bracket comment.

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

    @identifier.setter
    def identifier(self, argument):
        assert isinstance(argument, str | type(None)), repr(argument)
        self._identifier = argument

    @property
    def name(self) -> str | None:
        r"""
        Gets and sets name of container.

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

            >>> container.name is None
            True

        ..  container:: example

            Sets container name:

            >>> container = abjad.Container(
            ...     "c'4 d'4 e'4 f'4",
            ...     name='Special',
            ...     )
            >>> abjad.show(container) # doctest: +SKIP

            >>> container.name
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
        return self._name

    @name.setter
    def name(self, argument):
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

    @property
    def simultaneous(self) -> bool | None:
        r"""
        Is true when container is simultaneous.

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

            >>> container.simultaneous
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

            >>> container.simultaneous = True
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

    @simultaneous.setter
    def simultaneous(self, argument):
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
            selection = self._parse_string(component, language=language)
            assert len(selection) == 1
            component = selection[0]
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
        for i, element in enumerate(self.components):
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
            selection = self._parse_string(component, language=language)
            assert len(selection) == 1, repr(selection)
            component = selection[0]
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

    ..  container:: example

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

        LilyPond positions after grace notes at a point 3/4 of the way after
        the note they follow. The resulting spacing is usually too loose.
        Customize ``fraction`` as shown here.

    After grace notes are played in the last moments of duration of the note
    they follow.

    Fill after grace containers with notes, rests or chords.

    Attach after grace containers to notes, rests or chords.

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

    __documentation_section__ = "Containers"

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
        self.fraction = fraction

    ### SPECIAL METHODS ###

    def __getnewargs__(self) -> tuple[tuple[int, int] | None]:
        """
        Gets new after grace container arguments.

        ..  container:: example

            >>> abjad.AfterGraceContainer("d'8", fraction=(15, 16)).__getnewargs__()
            ((15, 16),)

        """
        return (self.fraction,)

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

    @property
    def fraction(self) -> tuple[int, int] | None:
        r"""
        Gets LilyPond `\afterGraceFraction`.
        """
        return self._fraction

    @fraction.setter
    def fraction(self, fraction: tuple[int, int] | None):
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

        LilyPond engraves grace music at a reduced size.

        LilyPond positions grace music immediately before a "main note" which
        follows.

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

    LilyPond provides four types of left-positioned grace music: acciaccaturas,
    appoggiaturas, grace notes and slashed grace notes; see
    ``abjad.BeforeGraceContainer.command`` to choose between these. LilyPond's
    left-positioned grace music contrasts with "right-positioned" after-grace music; see
    ``abjad.AfterGraceContainer``.

    Note that neither LilyPond nor Abjad attempts to model the ways that different
    categories of grace music have been performed historically. Typographic differences
    in slurring and slashing are provided. But distinctions between (for example)
    on-the-beat versus before-the-beat performance are left implicit.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Containers"

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
        string = f"{self.command} {{"
        result.extend([string])
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def command(self) -> str:
        r"""
        Gets command. Chooses between LilyPond's four types of left-positioned grace
        music.

        .. container:: example

            **(Vanilla) grace notes.** LilyPond formats single grace notes with neither a
            slash nor a slur:

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

            LilyPond likewise formats runs of grace notes with neither a slash nor a
            slur:

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

            **Acciaccaturas.** LilyPond formats single acciaccaturas with both a slash
            and a slur:

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

                But LilyPond fails to slash runs of acciaccaturas. This behavior is a
                longstanding LilyPond bug:

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

            **Appoggiaturas.** LilyPond formats single appoggiaturas with only a slur; no
            slash is included:

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

            **Slashed grace notes.** LilyPond formats single slashed grace notes with
            only a slash; no slur is included:

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

                But LilyPond fails to slash runs of "slashed" grace notes. This is a
                longstanding LilyPond bug:

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

                **Slashed grace notes with slur may be used instead of acciaccatura:**

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

    ..  container:: example

        REGRESSION. Initializes from other chord:

        >>> chord = abjad.Chord("<e' cs'' f''>4", multiplier=(1, 2))
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <e' cs'' f''>4 * 1/2

        >>> new_chord = abjad.Chord(chord)
        >>> abjad.show(new_chord) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(new_chord)
            >>> print(string)
            <e' cs'' f''>4 * 1/2

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Leaves"

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
            written_duration = leaf.written_duration
            if multiplier is None:
                multiplier = leaf.multiplier
            # TODO: move to dedicated from_note() constructor:
            if isinstance(leaf, Note) and leaf.note_head is not None:
                written_pitches.append(leaf.note_head.written_pitch)
                are_cautionary = [leaf.note_head.is_cautionary]
                are_forced = [leaf.note_head.is_forced]
                are_parenthesized = [leaf.note_head.is_parenthesized]
            elif isinstance(leaf, Chord):
                written_pitches.extend(_.written_pitch for _ in leaf.note_heads)
                are_cautionary = [_.is_cautionary for _ in leaf.note_heads]
                are_forced = [_.is_forced for _ in leaf.note_heads]
                are_parenthesized = [_.is_parenthesized for _ in leaf.note_heads]
        # TODO: move to dedicated constructor:
        elif len(arguments) == 2:
            written_pitches, written_duration = arguments
            if isinstance(written_pitches, str):
                written_pitches = [_ for _ in written_pitches.split() if _]
            elif isinstance(written_pitches, type(self)):
                written_pitches = list(written_pitches.written_pitches)
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
        new_chord.note_heads[:] = []
        for note_head in self.note_heads:
            note_head = copy.copy(note_head)
            new_chord.note_heads.append(note_head)
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
        return self.written_pitches, self.written_duration

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
        note_heads = self.note_heads
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
        return " ".join([_._get_chord_string() for _ in self.note_heads])

    ### PUBLIC PROPERTIES ###

    @property
    def note_heads(self) -> "NoteHeadList":
        r"""
        Gets note-heads in chord.

        ..  container:: example

            Gets note-heads in chord:

            >>> chord = abjad.Chord("<g' c'' e''>4")
            >>> abjad.show(chord) # doctest: +SKIP
            >>> for _ in chord.note_heads: _
            NoteHead("g'")
            NoteHead("c''")
            NoteHead("e''")

        ..  container:: example

            Sets note-heads with pitch names:

            >>> chord = abjad.Chord("<g' c'' e''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.note_heads = "c' d' fs'"
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <c' d' fs'>4

        ..  container:: example

            Sets note-heads with pitch numbers:

                >>> chord = abjad.Chord("<g' c'' e''>4")
                >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.note_heads = [16, 17, 19]
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <e'' f'' g''>4

        Set note-heads with any iterable.
        """
        return self._note_heads

    @note_heads.setter
    def note_heads(self, note_heads):
        self._note_heads[:] = []
        if isinstance(note_heads, str):
            note_heads = note_heads.split()
        self.note_heads.extend(note_heads)

    @property
    def written_duration(self) -> _duration.Duration:
        """
        Gets and sets written duration of chord.

        ..  container:: example

            Get written duration:

            >>> chord = abjad.Chord("<e' cs'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.written_duration
            Duration(1, 4)

        ..  container:: example

            Set written duration:

            >>> chord = abjad.Chord("<e' cs'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.written_duration = abjad.Duration(1, 16)
            >>> abjad.show(chord) # doctest: +SKIP

        """
        return super().written_duration

    @written_duration.setter
    def written_duration(self, argument):
        Leaf.written_duration.fset(self, argument)

    @property
    def written_pitches(self) -> tuple[_pitch.NamedPitch, ...]:
        """
        Written pitches in chord.

        ..  container:: example

            Get written pitches:

            >>> chord = abjad.Chord("<g' c'' e''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.written_pitches
            (NamedPitch("g'"), NamedPitch("c''"), NamedPitch("e''"))

        ..  container:: example

            Set written pitches with pitch names:

            >>> chord = abjad.Chord("<e' g' c''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.written_pitches = "f' b' d''"
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(chord)
                >>> print(string)
                <f' b' d''>4

            >>> chord.written_pitches
            (NamedPitch("f'"), NamedPitch("b'"), NamedPitch("d''"))

        Set written pitches with any iterable.
        """
        return tuple(_.written_pitch for _ in self.note_heads)

    @written_pitches.setter
    def written_pitches(self, pitches):
        self.note_heads = pitches


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

    __documentation_section__ = "Containers"

    __slots__ = ()

    def _format_open_brackets_site(self, contributions):
        result = []
        if self.simultaneous:
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

    __documentation_section__ = "Contexts"

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
        self.lilypond_type = lilypond_type
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
        new_context._consists_commands = copy.copy(self.consists_commands)
        new_context._remove_commands = copy.copy(self.remove_commands)
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
        if self.components:
            string = repr(self._get_contents_summary())
            parameters.append(string)
        if self.lilypond_type != type(self).__name__:
            parameters.append(f"lilypond_type={self.lilypond_type!r}")
        if self.name:
            parameters.append(f"name={self.name!r}")
        if self.simultaneous is True:
            parameters.append(f"simultaneous={self.simultaneous!r}")
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
        for engraver in self.consists_commands:
            string = rf"\consists {engraver}"
            result.append(string)
        return result

    def _format_invocation(self):
        if self.name is not None:
            string = rf'\context {self.lilypond_type} = "{self.name}"'
        else:
            string = rf"\new {self.lilypond_type}"
        return string

    def _format_open_brackets_site(self, contributions):
        result = []
        if self.simultaneous:
            if self.identifier:
                open_bracket = f"<<  {self.identifier}"
            else:
                open_bracket = "<<"
        else:
            if self.identifier:
                open_bracket = f"{{   {self.identifier}"
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
        for engraver in self.remove_commands:
            string = rf"\remove {engraver}"
            result.append(string)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def consists_commands(self):
        r"""
        Unordered set of LilyPond engravers to include in context definition.

        ..  container:: example

            Manage with add, update, other standard set commands:

            >>> staff = abjad.Staff([])
            >>> staff.consists_commands.append("Horizontal_bracket_engraver")
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

    @property
    def lilypond_context(self):
        """
        Gets ``LilyPondContext`` associated with context.

        Returns LilyPond context instance.
        """
        try:
            lilypond_context = _lyproxy.LilyPondContext(name=self.lilypond_type)
        except AssertionError:
            lilypond_context = _lyproxy.LilyPondContext(
                name=self._default_lilypond_type
            )
        return lilypond_context

    @property
    def lilypond_type(self) -> str:
        """
        Gets lilypond type.

        ..  container:: example

            >>> context = abjad.Context(
            ...     lilypond_type="ViolinStaff",
            ...     name="MyViolinStaff",
            ... )
            >>> context.lilypond_type
            'ViolinStaff'

        Gets and sets lilypond type of context.
        """
        return self._lilypond_type

    @lilypond_type.setter
    def lilypond_type(self, argument):
        if argument is None:
            argument = type(self).__name__
        else:
            argument = str(argument)
        self._lilypond_type = argument

    @property
    def remove_commands(self):
        r"""
        Unordered set of LilyPond engravers to remove from context.

        ..  container:: example

            Manage with add, update, other standard set commands:

            >>> staff = abjad.Staff([])
            >>> staff.remove_commands.append("Time_signature_engraver")
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

    @property
    def tag(self) -> _tag.Tag | None:
        r"""
        Gets tag.

        ..  container:: example

            >>> context = abjad.Context(
            ...     "c'4 d' e' f'",
            ...     lilypond_type="CustomContext",
            ...     tag=abjad.Tag("RED"),
            ...     )
            >>> abjad.show(context) # doctest: +SKIP

            >>> string = abjad.lilypond(context, tags=True)
            >>> print(string)
            %! RED
            \new CustomContext
            %! RED
            {
                c'4
                d'4
                e'4
                f'4
            %! RED
            }

        """
        return super().tag

    @tag.setter
    def tag(self, argument) -> None:
        self._tag = argument


class IndependentAfterGraceContainer(Container):
    r"""
    Independent after grace container.

    ..  container:: example

        After grace notes:

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

        LilyPond positions after grace notes at a point 3/4 of the way
        after the note they follow. The resulting spacing is usually too
        loose. Customize ``fraction`` as shown above.

    After grace notes are played in the last moments of the duration of the
    note they follow.

    Fill grace containers with notes, rests or chords.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Containers"

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
        self.fraction = fraction

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

    @property
    def fraction(self) -> tuple[int, int] | None:
        r"""
        Gets LilyPond `\afterGraceFraction`.
        """
        return self._fraction

    @fraction.setter
    def fraction(self, fraction: tuple[int, int] | None):
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

        >>> rest = abjad.MultimeasureRest((1, 4))
        >>> abjad.show(rest) # doctest: +SKIP

    ..  container:: example

        Multimeasure rests may be tagged:

        >>> rest = abjad.MultimeasureRest(
        ...     "R1", tag=abjad.Tag("GLOBAL_MULTIMEASURE_REST")
        ... )
        >>> string = abjad.lilypond(rest, tags=True)
        >>> print(string)
        %! GLOBAL_MULTIMEASURE_REST
        R1

    ..  container:: example

        REGRESSION #1049. Parser reads multimeasure rest multipliers:

        >>> staff = abjad.Staff(r"\time 3/8 R1 * 3/8")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 3/8
                R1 * 3/8
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Leaves"

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
        Leaf.__init__(self, rest.written_duration, multiplier=multiplier, tag=tag)

    ### PRIVATE METHODS ###

    def _get_body(self):
        """
        Gets list of string representation of body of rest.
        Picked up as contribution at format-time.
        """
        result = "R" + str(self._get_formatted_duration())
        return [result]

    def _get_compact_representation(self):
        return f"R{self._get_formatted_duration()}"

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self) -> _tag.Tag | None:
        r"""
        Gets tag.

        ..  container:: example

            >>> rest = abjad.MultimeasureRest(
            ...     1, tag=abjad.Tag('MULTIMEASURE_REST')
            ... )
            >>> rest.multiplier = (3, 8)

            >>> string = abjad.lilypond(rest, tags=True)
            >>> print(string)
            %! MULTIMEASURE_REST
            R1 * 3/8

        """
        return super().tag

    @tag.setter
    def tag(self, argument) -> None:
        self._tag = argument


@functools.total_ordering
class NoteHead:
    r"""
    Note-head.

    ..  container:: example

        >>> note = abjad.Note("cs''")
        >>> abjad.show(note) # doctest: +SKIP

        >>> note.note_head
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

        >>> abjad.tweak(chord.note_heads[0], r"\tweak color #red")
        >>> abjad.tweak(chord.note_heads[0], r"\tweak thickness 2")
        >>> abjad.tweak(chord.note_heads[1], r"\tweak color #red")
        >>> abjad.tweak(chord.note_heads[1], r"\tweak thickness 2")
        >>> abjad.tweak(chord.note_heads[2], r"\tweak color #blue")
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

    __documentation_section__ = "Note-heads"

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
            written_pitch = note_head.written_pitch
            is_cautionary = note_head.is_cautionary
            is_forced = note_head.is_forced
        elif written_pitch is None:
            written_pitch = 0
        self.written_pitch = written_pitch
        self.is_cautionary = is_cautionary
        self.is_forced = is_forced
        self.is_parenthesized = is_parenthesized
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
            self.written_pitch,
            is_cautionary=self.is_cautionary,
            is_forced=self.is_forced,
            is_parenthesized=self.is_parenthesized,
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
            return self.written_pitch == argument.written_pitch
        return self.written_pitch == argument

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
            return self.written_pitch < argument.written_pitch
        try:
            argument = type(self)(argument)
        except (ValueError, TypeError):
            return False
        return self.written_pitch < argument.written_pitch

    def __repr__(self) -> str:
        """
        Gets interpreter representation of note-head.

        ..  container:: example

            >>> note_head = abjad.NoteHead(13)
            >>> note_head
            NoteHead("cs''")

        """
        strings = []
        if isinstance(self.written_pitch, _pitch.NamedPitch):
            string = self.written_pitch.name
            strings.append(repr(string))
        # drum note head:
        elif isinstance(self.written_pitch, str):
            string = self.written_pitch
            strings.append(repr(string))
        if self.is_cautionary:
            string = f"is_cautionary={self.is_cautionary!r}"
            strings.append(string)
        if self.is_forced:
            string = f"is_forced={self.is_forced!r}"
            strings.append(string)
        if self.is_parenthesized:
            string = f"is_parenthesized={self.is_parenthesized!r}"
            strings.append(string)
        if self.tweaks:
            string = f"tweaks={self.tweaks!r}"
            strings.append(string)
        string = ", ".join(strings)
        return f"{type(self).__name__}({string})"

    def _get_chord_string(self) -> str:
        result = ""
        if self.written_pitch:
            result = self.written_pitch.name
            if self.is_forced:
                result += "!"
            if self.is_cautionary:
                result += "?"
        return result

    def _get_note_head_strings(self):
        assert self.written_pitch
        result = []
        if self.is_parenthesized:
            result.append(r"\parenthesize")
        for tweak in sorted(self.tweaks):
            strings = tweak._list_contributions()
            result.extend(strings)
        written_pitch = self.written_pitch
        if isinstance(written_pitch, _pitch.NamedPitch):
            written_pitch = written_pitch.simplify()
            kernel = written_pitch.name
        # drum note head:
        else:
            assert isinstance(written_pitch, str)
            kernel = written_pitch
        if self.is_forced:
            kernel += "!"
        if self.is_cautionary:
            kernel += "?"
        result.append(kernel)
        return result

    def _get_lilypond_format(self, duration=None):
        pieces = self._get_note_head_strings()
        if duration is not None:
            pieces[-1] = pieces[-1] + duration
        if self.alternative:
            pieces = _tag.double_tag(pieces, self.alternative[2])
            pieces_ = self.alternative[0]._get_note_head_strings()
            if duration is not None:
                pieces_[-1] = pieces_[-1] + duration
            pieces_ = _tag.double_tag(pieces_, self.alternative[1], deactivate=True)
            pieces.extend(pieces_)
        result = "\n".join(pieces)
        return result

    @property
    def alternative(self) -> tuple["NoteHead", _tag.Tag, _tag.Tag]:
        """
        Gets and sets note-head alternative.

        >>> import copy

        ..  container:: example

            >>> note = abjad.Note("c''4")
            >>> alternative = copy.copy(note.note_head)
            >>> alternative.is_forced = True
            >>> triple = (alternative, abjad.Tag("-PARTS"), abjad.Tag("+PARTS"))
            >>> note.note_head.alternative = triple
            >>> abjad.show(note) # doctest: +SKIP

            >>> string = abjad.lilypond(note, tags=True)
            >>> print(string)
            %! +PARTS
            c''4
            %! -PARTS
            %@% c''!4

            Survives pitch reassignment:

            >>> note.written_pitch = "D5"
            >>> abjad.show(note) # doctest: +SKIP

            >>> string = abjad.lilypond(note, tags=True)
            >>> print(string)
            %! +PARTS
            d''4
            %! -PARTS
            %@% d''!4

            Clear with none:

            >>> note.note_head.alternative = None
            >>> abjad.show(note) # doctest: +SKIP

            >>> string = abjad.lilypond(note, tags=True)
            >>> print(string)
            d''4

        ..  container:: example

            >>> chord = abjad.Chord("<c' d' bf''>4")
            >>> alternative = copy.copy(chord.note_heads[0])
            >>> alternative.is_forced = True
            >>> triple = (alternative, abjad.Tag("-PARTS"), abjad.Tag("+PARTS"))
            >>> chord.note_heads[0].alternative = triple
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

            >>> chord.note_heads[0].written_pitch = "B3"
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

            >>> chord.note_heads[0].alternative = None
            >>> string = abjad.lilypond(chord, tags=True)
            >>> print(string)
            <b d' bf''>4

        """
        return self._alternative

    @alternative.setter
    def alternative(self, argument):
        if argument is not None:
            assert isinstance(argument, tuple), repr(argument)
            assert len(argument) == 3, repr(argument)
            assert isinstance(argument[0], NoteHead), repr(argument)
            assert argument[0].alternative is None, repr(argument)
            assert isinstance(argument[1], _tag.Tag), repr(argument)
            assert isinstance(argument[2], _tag.Tag), repr(argument)
        self._alternative = argument

    @property
    def is_cautionary(self) -> bool:
        """
        Gets and sets cautionary accidental flag.

        ..  container:: example

            >>> note = abjad.Note("c''")
            >>> note.note_head.is_cautionary = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c''?4

            >>> note = abjad.Note("cs''")
            >>> note.note_head.is_cautionary = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''?4

        """
        return self._is_cautionary

    @is_cautionary.setter
    def is_cautionary(self, argument):
        self._is_cautionary = bool(argument)

    @property
    def is_forced(self) -> bool:
        """
        Gets and sets forced accidental flag.

        ..  container:: example

            >>> note = abjad.Note("c''")
            >>> note.note_head.is_forced = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c''!4

            >>> note = abjad.Note("cs''")
            >>> note.note_head.is_forced = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''!4

        """
        return self._is_forced

    @is_forced.setter
    def is_forced(self, argument):
        if argument is not None:
            argument = bool(argument)
        self._is_forced = argument

    @property
    def is_parenthesized(self) -> bool:
        r"""
        Gets and sets forced accidental flag.

        ..  container:: example

            >>> note = abjad.Note("c''")
            >>> note.note_head.is_parenthesized = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                \parenthesize
                c''4

            >>> note = abjad.Note("cs''")
            >>> note.note_head.is_parenthesized = True
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                \parenthesize
                cs''4

        """
        return self._is_parenthesized

    @is_parenthesized.setter
    def is_parenthesized(self, argument):
        if argument is not None:
            argument = bool(argument)
        self._is_parenthesized = argument

    @property
    def named_pitch(self) -> _pitch.NamedPitch:
        """
        Gets named pitch.

        ..  container:: example

            >>> note_head = abjad.NoteHead("cs''")
            >>> note_head.named_pitch
            NamedPitch("cs''")

        """
        return self.written_pitch

    @property
    def written_pitch(self) -> _pitch.NamedPitch:
        """
        Gets and sets written pitch of note-head.

        ..  container:: example

            >>> note_head = abjad.NoteHead("cs''")
            >>> note_head.written_pitch
            NamedPitch("cs''")

            >>> note_head = abjad.NoteHead("cs''")
            >>> note_head.written_pitch = "d''"
            >>> note_head.written_pitch
            NamedPitch("d''")

        """
        return self._written_pitch

    @written_pitch.setter
    def written_pitch(self, argument):
        written_pitch = _pitch.NamedPitch(argument)
        self._written_pitch = written_pitch
        if self.alternative is not None:
            self.alternative[0].written_pitch = written_pitch


class DrumNoteHead(NoteHead):
    """
    Drum note-head.

    ..  container:: example

        >>> note_head = abjad.DrumNoteHead("snare")
        >>> note_head
        DrumNoteHead('snare')

    """

    __documentation_section__ = "Note-heads"

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

    __documentation_section__ = "Note-heads"

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
            >>> chord.note_heads.extend(note_heads)
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

        ..  container:: example

            Gets note-head by pitch name:

            >>> chord = abjad.Chord("<e' cs'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> note_head = chord.note_heads.get("e'")
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

            >>> note_head = chord.note_heads.get(4)
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

        Raises missing note-head error when chord contains no note-head with ``pitch``.

        Raises extra note-head error when chord contains more than one note-head with
        ``pitch``.
        """
        result = []
        pitch = _pitch.NamedPitch(pitch)
        for note_head in self:
            assert isinstance(note_head, NoteHead), repr(note_head)
            if note_head.written_pitch == pitch:
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

            >>> chord.note_heads.pop(1)
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

            >>> note_head = chord.note_heads[1]
            >>> chord.note_heads.remove(note_head)
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

    ..  container:: example

        REGRESSION. Initializes from other note:

        >>> note = abjad.Note("cs''4", multiplier=(1, 1))
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            cs''4 * 1/1

        >>> new_note = abjad.Note(note)
        >>> abjad.show(new_note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(new_note)
            >>> print(string)
            cs''4 * 1/1

    ..  container:: example

        Selects language:

        >>> abjad.Note("dod''8.", language="français")
        Note("cs''8.")

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Leaves"

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
            written_duration = leaf.written_duration
            if multiplier is None:
                multiplier = leaf.multiplier
            if isinstance(leaf, Note) and leaf.note_head is not None:
                written_pitch = leaf.note_head.written_pitch
                is_cautionary = leaf.note_head.is_cautionary
                is_forced = leaf.note_head.is_forced
                is_parenthesized = leaf.note_head.is_parenthesized
            # TODO: move into separate from_chord() constructor:
            elif isinstance(leaf, Chord):
                written_pitches = [_.written_pitch for _ in leaf.note_heads]
                if written_pitches:
                    written_pitch = written_pitches[0]
                    is_cautionary = leaf.note_heads[0].is_cautionary
                    is_forced = leaf.note_heads[0].is_forced
                    is_parenthesized = leaf.note_heads[0].is_parenthesized
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
                self.note_head = NoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                )
            else:
                assert isinstance(written_pitch, str), repr(written_pitch)
                self.note_head = DrumNoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                )
            if isinstance(written_pitch, NoteHead):
                self.note_head.tweaks = copy.deepcopy(written_pitch.tweaks)
        else:
            self._note_head = None
        if len(arguments) == 1 and isinstance(arguments[0], Leaf):
            self._copy_override_and_set_from_leaf(arguments[0])

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments) -> "Note":
        """
        Copies note.
        """
        new_note = Leaf.__copy__(self, *arguments)
        new_note.note_head = copy.copy(self.note_head)
        return new_note

    def __getnewargs__(self) -> tuple:
        """
        Gets new arguments.
        """
        return (self.written_pitch, self.written_duration)

    ### PRIVATE METHODS ###

    def _get_body(self):
        duration = self._get_formatted_duration()
        if self.note_head is not None:
            string = self.note_head._get_lilypond_format(duration=duration)
        else:
            string = duration
        return [string]

    def _get_compact_representation(self):
        return self._get_body()[0]

    ### PUBLIC PROPERTIES ###

    @property
    def note_head(self) -> NoteHead | None:
        """
        Gets and sets note-head.

        .. container:: example

            >>> note = abjad.Note("cs''8.")
            >>> note.note_head
            NoteHead("cs''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''8.

            >>> note.note_head = 'D5'
            >>> note.note_head
            NoteHead("d''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                d''8.

        """
        return self._note_head

    @note_head.setter
    def note_head(self, argument):
        if isinstance(argument, type(None)):
            self._note_head = None
        elif isinstance(argument, NoteHead):
            self._note_head = argument
        else:
            note_head = NoteHead(written_pitch=argument)
            self._note_head = note_head

    @property
    def written_duration(self) -> _duration.Duration:
        """
        Gets and sets written duration.

        ..  container:: example

            >>> note = abjad.Note("cs''8.")
            >>> note.written_duration
            Duration(3, 16)

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''8.

            >>> note.written_duration = (1, 16)
            >>> note.written_duration
            Duration(1, 16)

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''16

        """
        return super().written_duration

    @written_duration.setter
    def written_duration(self, argument):
        return Leaf.written_duration.fset(self, argument)

    # TODO: change Note always to have a note head
    @property
    def written_pitch(self) -> _pitch.NamedPitch | None:
        """
        Gets and sets written pitch.

        ..  container:: example

            >>> note = abjad.Note("cs''8.")
            >>> note.written_pitch
            NamedPitch("cs''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                cs''8.

            >>> note.written_pitch = 'D5'
            >>> note.written_pitch
            NamedPitch("d''")

            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                d''8.

        """
        if self.note_head is not None:
            return self.note_head.written_pitch
        else:
            return None

    @written_pitch.setter
    def written_pitch(self, argument):
        if argument is None:
            if self.note_head is not None:
                self.note_head.written_pitch = None
        else:
            if self.note_head is None:
                self.note_head = NoteHead(self, written_pitch=None)
            else:
                pitch = _pitch.NamedPitch(argument)
                self.note_head.written_pitch = pitch

    ### PUBLIC METHODS ###

    @staticmethod
    def from_pitch_and_duration(pitch, duration) -> "Note":
        """
        Makes note from ``pitch`` and ``duration``.

        ..  container:: example

            >>> note = abjad.Note.from_pitch_and_duration('C#5', (3, 16))
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

    __documentation_section__ = "Leaves"

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
            multiplier = written_duration.multiplier
        if isinstance(written_duration, str):
            string = f"{{ {written_duration} }}"
            parsed = self._parse_lilypond_string(string, language=language)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            written_duration = parsed[0]
        if isinstance(written_duration, Leaf):
            written_duration = written_duration.written_duration
        elif written_duration is None:
            written_duration = _duration.Duration(1, 4)
        else:
            written_duration = _duration.Duration(written_duration)
        Leaf.__init__(self, written_duration, multiplier=multiplier, tag=tag)
        if isinstance(original_input, Leaf):
            self._copy_override_and_set_from_leaf(original_input)

    def _get_body(self):
        return [self._get_compact_representation()]

    def _get_compact_representation(self):
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

    __documentation_section__ = "Contexts"

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

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self) -> _tag.Tag | None:
        r"""
        Gets tag.

        ..  container:: example

            >>> voice = abjad.Voice("c'4 d' e' f'", tag=abjad.Tag("RED"))
            >>> staff = abjad.Staff([voice], tag=abjad.Tag("BLUE"))
            >>> score = abjad.Score([staff], tag=abjad.Tag("GREEN"))
            >>> abjad.show(score) # doctest: +SKIP

            >>> string = abjad.lilypond(score, tags=True)
            >>> print(string)
            %! GREEN
            \new Score
            %! GREEN
            <<
                %! BLUE
                \new Staff
                %! BLUE
                {
                    %! RED
                    \new Voice
                    %! RED
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                    %! RED
                    }
                %! BLUE
                }
            %! GREEN
            >>

        """
        return super().tag

    @tag.setter
    def tag(self, argument) -> None:
        self._tag = argument


class Skip(Leaf):
    """
    LilyPond skip.

    ..  container:: example

        >>> skip = abjad.Skip((1, 1))
        >>> skip
        Skip('s1')

        ..  docs::

            >>> string = abjad.lilypond(skip)
            >>> print(string)
            s1

        >>> skip = abjad.Skip((1, 1), multiplier=(5, 4))
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

    ..  container:: example

        Skips can be tagged:

        >>> skip = abjad.Skip("s8.", tag=abjad.Tag("GLOBAL_SKIP"))
        >>> string = abjad.lilypond(skip, tags=True)
        >>> print(string)
        %! GLOBAL_SKIP
        s8.

    """

    __documentation_section__ = "Leaves"

    __slots__ = ("_hide_body", "_measure_initial_grace_note")

    def __init__(
        self,
        *arguments,
        language: str = "english",
        multiplier: tuple[int, int] | None = None,
        tag: _tag.Tag | None = None,
    ) -> None:
        input_leaf = None
        written_duration = None
        if len(arguments) == 1 and isinstance(arguments[0], str):
            string = f"{{ {arguments[0]} }}"
            parsed = self._parse_lilypond_string(string, language=language)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            input_leaf = parsed[0]
            written_duration = input_leaf.written_duration
        elif len(arguments) == 1 and isinstance(arguments[0], Leaf):
            input_leaf = arguments[0]
            written_duration = input_leaf.written_duration
            multiplier = input_leaf.multiplier
        elif len(arguments) == 1 and not isinstance(arguments[0], str):
            written_duration = arguments[0]
        elif len(arguments) == 0:
            written_duration = _duration.Duration(1, 4)
        else:
            raise ValueError(f"can not initialize skip from {arguments!r}.")
        Leaf.__init__(self, written_duration, multiplier=multiplier, tag=tag)
        if input_leaf is not None:
            self._copy_override_and_set_from_leaf(input_leaf)

    def _get_body(self):
        result = []
        if getattr(self, "_hide_body", False) is not True:
            if getattr(self, "_measure_initial_grace_note", None) is not None:
                grace_strings = self._measure_initial_grace_note
                assert isinstance(grace_strings, list), repr(grace_strings)
                assert "grace" in repr(grace_strings), repr(grace_strings)
                result.extend(grace_strings)
            result.append(f"s{self._get_formatted_duration()}")
        return result

    def _get_compact_representation(self):
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

    ..  container:: example

        Can initialize from collection of strings:

        >>> staff = abjad.Staff([
        ...     r"\times 9/10 { r8 c'16 c'16 bf'4~ bf'16 r16 }",
        ...     r"\times 9/10 { bf'16 e''16 e''4 ~ e''16 r16 fs''16 af''16 }",
        ...     r"\times 4/5 { a'16 r4 }",
        ... ])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 10/9
                    {
                        r8
                        c'16
                        c'16
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 10/9
                    {
                        bf'16
                        e''16
                        e''4
                        ~
                        e''16
                        r16
                        fs''16
                        af''16
                    }
                }
                {
                    \tuplet 5/4
                    {
                        a'16
                        r4
                    }
                }
            }

    """

    __documentation_section__ = "Contexts"

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

    __documentation_section__ = "Contexts"

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

    __documentation_section__ = "Containers"

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
        return (self.count,)

    def _format_open_brackets_site(self, contributions):
        result = []
        result.append(rf"\repeat tremolo {self.count}")
        result.append("{")
        return result

    def _get_preprolated_duration(self):
        return self.implied_prolation * self._get_contents_duration()

    @property
    def count(self) -> int:
        """
        Gets count.

        ..  container:: example

            >>> tremolo_container = abjad.TremoloContainer(2, "<c' d'>16 e'16")
            >>> tremolo_container.count
            2

        """
        return self._count

    @property
    def implied_prolation(self) -> fractions.Fraction:
        r"""
        Gets implied prolation of tremolo container.

        ..  container:: example

            Defined equal to count.

            >>> tremolo_container = abjad.TremoloContainer(2, "<c' d'>16 e'16")
            >>> abjad.show(tremolo_container) # doctest: +SKIP

            >>> tremolo_container.implied_prolation
            Fraction(2, 1)

        """
        fraction = fractions.Fraction(self.count)
        return fraction


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

        A nested tuplet:

        >>> second_tuplet = abjad.Tuplet("7:4", "g'4. ( a'16 )")
        >>> tuplet.insert(1, second_tuplet)
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak edge-height #'(0.7 . 0)
            \tuplet 6/4
            {
                c'8
                \tuplet 7/4
                {
                    g'4.
                    (
                    a'16
                    )
                }
                d'8
                e'8
            }


    ..  container:: example

        A doubly nested tuplet:

            >>> third_tuplet = abjad.Tuplet("5:4", [])
            >>> third_tuplet.extend("e''32 [ ef''32 d''32 cs''32 cqs''32 ]")
            >>> second_tuplet.insert(1, third_tuplet)
            >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(tuplet)
            >>> print(string)
            \tweak edge-height #'(0.7 . 0)
            \tuplet 6/4
            {
                c'8
                \tweak edge-height #'(0.7 . 0)
                \tuplet 7/4
                {
                    g'4.
                    (
                    \tuplet 5/4
                    {
                        e''32
                        [
                        ef''32
                        d''32
                        cs''32
                        cqs''32
                        ]
                    }
                    a'16
                    )
                }
                d'8
                e'8
            }

    ..  container:: example

        Selects language:

        >>> abjad.Tuplet("6:4", "do'2 dod' re'", language="français")
        Tuplet('6:4', "c'2 cs'2 d'2")

    ..  container:: example

        Tuplets can be entered as LilyPond input:

        >>> voice = abjad.Voice(r"\tuplet 6/4 { c'4 d' e' }")
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \tuplet 6/4
                {
                    c'4
                    d'4
                    e'4
                }
            }

        >>> voice = abjad.Voice(r"\times 4/6 { c'4 d' e' }")
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                \tuplet 6/4
                {
                    c'4
                    d'4
                    e'4
                }
            }

    ..  container:: example

        Tweak tuplets like this:

        >>> tuplet_1 = abjad.Tuplet((2, 3), "c'4 ( d'4 e'4 )")
        >>> abjad.tweak(tuplet_1, r"\tweak color #red")
        >>> abjad.tweak(tuplet_1, r"\tweak staff-padding 2")

        >>> tuplet_2 = abjad.Tuplet((2, 3), "c'4 ( d'4 e'4 )")
        >>> abjad.tweak(tuplet_2, r"\tweak color #green")
        >>> abjad.tweak(tuplet_2, r"\tweak staff-padding 2")

        >>> tuplet_3 = abjad.Tuplet((5, 4), [tuplet_1, tuplet_2])
        >>> abjad.tweak(tuplet_3, r"\tweak color #blue")
        >>> abjad.tweak(tuplet_3, r"\tweak staff-padding 4")

        >>> staff = abjad.Staff([tuplet_3])
        >>> score = abjad.Score([staff], name="Score")
        >>> leaves = abjad.select.leaves(staff)
        >>> abjad.attach(abjad.TimeSignature((5, 4)), leaves[0])
        >>> literal = abjad.LilyPondLiteral(
        ...     r"\set tupletFullLength = ##t", site="opening"
        ... )
        >>> abjad.attach(literal, staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \set tupletFullLength = ##t
                \tweak text #tuplet-number::calc-fraction-text
                \tweak color #blue
                \tweak staff-padding 4
                \tuplet 4/5
                {
                    \tweak color #red
                    \tweak staff-padding 2
                    \tuplet 3/2
                    {
                        \time 5/4
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

        ..  todo:: Report LilyPond bug that results from removing tupletFullLength
            in the example above: blue tuplet bracket shrinks to encompass only the
            second underlying tuplet.

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Containers"

    __slots__ = (
        "_denominator",
        "_force_fraction",
        "_hide",
        "_multiplier",
        "tweaks",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        multiplier="3:2",
        components=None,
        *,
        denominator: int | None = None,
        force_fraction: bool = False,
        hide: bool = False,
        language: str = "english",
        tag: _tag.Tag | None = None,
        tweaks: _tweaks.Tweak | None = None,
    ) -> None:
        Container.__init__(self, components, language=language, tag=tag)
        self.tweaks = ()
        if isinstance(multiplier, str) and ":" in multiplier:
            strings = multiplier.split(":")
            numbers = [int(_) for _ in strings]
            pair = numbers[1], numbers[0]
        elif isinstance(multiplier, tuple):
            pair = multiplier[0], multiplier[1]
        else:
            message = f"tuplet multiplier must be pair or string (not {multiplier!r})."
            raise ValueError(message)
        self.multiplier = pair
        self.denominator = denominator
        self.force_fraction = force_fraction
        self.hide = hide

    ### SPECIAL METHODS ###

    def __getnewargs__(self) -> tuple:
        """
        Gets new arguments of tuplet.
        """
        return (self.multiplier,)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        string = self._get_contents_summary()
        return f"{type(self).__name__}({self.colon_string!r}, {string!r})"

    ### PRIVATE METHODS ###

    def _format_after_site(self, contributions):
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

    def _format_before_site(self, contributions):
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

    def _format_close_brackets(self):
        result = []
        if self.multiplier:
            strings = ["}"]
            if self.tag is not None:
                strings = _tag.double_tag(strings, self.tag)
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

    def _format_lilypond_fraction_command_string(self):
        if self.hide:
            return ""
        if "text" in vars(_overrides.override(self).TupletNumber):
            return ""
        if (
            self.augmentation()
            or not self._is_dyadic_rational()
            or self.multiplier[1] == 1
            or self.force_fraction
        ):
            return r"\tweak text #tuplet-number::calc-fraction-text"
        return ""

    def _format_open_brackets_site(self, contributions):
        result = []
        if self.multiplier:
            if self.hide:
                string = self._get_scale_durations_command_string()
                contributions = [string, "{"]
            else:
                contributions = []
                fraction_command_string = (
                    self._format_lilypond_fraction_command_string()
                )
                if fraction_command_string:
                    contributions.append(fraction_command_string)
                edge_height_tweak_string = self._get_edge_height_tweak_string()
                if edge_height_tweak_string:
                    contributions.append(edge_height_tweak_string)
                for tweak in sorted(self.tweaks):
                    strings = tweak._list_contributions()
                    contributions.extend(strings)
                tuplet_command_string = self._get_tuplet_command_string()
                contributions.append(tuplet_command_string)
                contributions.append("{")
            if self.tag is not None:
                contributions = _tag.double_tag(contributions, self.tag)
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

    def _get_compact_representation(self):
        n, d = self.multiplier
        if not self:
            return f"{{ {d}:{n} }}"
        return f"{{ {d}:{n} {self._get_contents_summary()} }}"

    def _get_edge_height_tweak_string(self):
        duration = self._get_preprolated_duration()
        denominator = duration.denominator
        if not _math.is_nonnegative_integer_power_of_two(denominator):
            return r"\tweak edge-height #'(0.7 . 0)"

    def _get_multiplier_fraction_string(self):
        numerator, denominator = self.multiplier
        if self.denominator is not None:
            inverse_multiplier = fractions.Fraction(denominator, numerator)
            pair = _duration.with_denominator(inverse_multiplier, self.denominator)
            denominator, numerator = pair
        return f"{numerator}/{denominator}"

    def _is_dyadic_rational(self):
        if self.multiplier:
            numerator = self.multiplier[0]
            return _math.is_nonnegative_integer_power_of_two(numerator)
        else:
            return True

    def _get_preprolated_duration(self):
        return self.multiplied_duration

    def _get_ratio_string(self):
        if self.multiplier is not None:
            numerator, denominator = self.multiplier
            ratio_string = f"{denominator}:{numerator}"
            return ratio_string
        else:
            return None

    def _get_scale_durations_command_string(self):
        numerator, denominator = self.multiplier
        string = rf"\scaleDurations #'({numerator} . {denominator})"
        return string

    def _get_summary(self):
        if 0 < len(self):
            return ", ".join([str(_) for _ in self.components])
        else:
            return ""

    def _get_times_command_string(self):
        string = rf"\times {self._get_multiplier_fraction_string()}"
        return string

    def _get_tuplet_command_string(self):
        numerator, denominator = self.multiplier
        if self.denominator is not None:
            inverse_multiplier = fractions.Fraction(denominator, numerator)
            pair = _duration.with_denominator(inverse_multiplier, self.denominator)
            denominator, numerator = pair
        string = rf"\tuplet {denominator}/{numerator}"
        return string

    def _scale(self, multiplier):
        multiplier = fractions.Fraction(multiplier)
        for component in self[:]:
            if isinstance(component, Leaf):
                component._scale(multiplier)
        self.normalize_multiplier()

    ### PUBLIC PROPERTIES ###

    @property
    def colon_string(self) -> str:
        r"""
        Gets colon string.

        ..  container example

            >>> tuplet = abjad.Tuplet("3:2", "c'4 d' e'")
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

            >>> tuplet.colon_string
            '3:2'

        """
        numerator, denominator = self.multiplier
        return f"{denominator}:{numerator}"

    @property
    def denominator(self) -> int | None:
        r"""
        Gets and sets preferred denominator of tuplet.

        ..  container:: example

            Gets preferred denominator of tuplet:

            >>> tuplet = abjad.Tuplet("3:2", "c'8 d'8 e'8")
            >>> tuplet.denominator is None
            True
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

        ..  container:: example

            Sets preferred denominator of tuplet:

            >>> tuplet = abjad.Tuplet("3:2", "c'8 d'8 e'8")
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

            >>> tuplet.denominator = 4
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

        """
        return self._denominator

    @denominator.setter
    def denominator(self, argument):
        if isinstance(argument, int):
            if not 0 < argument:
                raise ValueError(argument)
        elif not isinstance(argument, type(None)):
            raise TypeError(argument)
        self._denominator = argument

    @property
    def force_fraction(self) -> bool | None:
        r"""
        Gets and sets force fraction flag.

        ..  container:: example

            To illustrate the effect of Abjad's force fraction property, we can
            temporarily restore LilyPond's default tuplet number formatting
            like this:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> string = '#tuplet-number::calc-denominator-text'
            >>> abjad.override(staff).TupletNumber.text = string
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletNumber.text = #tuplet-number::calc-denominator-text
                }
                {
                    \tuplet 3/2
                    {
                        c'4
                        d'4
                        e'4
                    }
                    \tuplet 3/2
                    {
                        c'4
                        d'4
                        e'4
                    }
                    \tuplet 3/2
                    {
                        c'4
                        d'4
                        e'4
                    }
                }

            Which makes it possible to see the effect of setting force fraction
            to true on a single tuplet:

            >>> tuplet = staff[1]
            >>> tuplet.force_fraction = True
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletNumber.text = #tuplet-number::calc-denominator-text
                }
                {
                    \tuplet 3/2
                    {
                        c'4
                        d'4
                        e'4
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 3/2
                    {
                        c'4
                        d'4
                        e'4
                    }
                    \tuplet 3/2
                    {
                        c'4
                        d'4
                        e'4
                    }
                }

        ..  container:: example

            Ignored when tuplet number text is overridden explicitly:

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> duration = abjad.get.duration(tuplet)
            >>> note = abjad.Note.from_pitch_and_duration(0, duration)
            >>> string = abjad.illustrators.components_to_score_markup_string([note])
            >>> string = rf"\markup {{ {string} }}"
            >>> abjad.override(tuplet).TupletNumber.text = string
            >>> staff = abjad.Staff([tuplet])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \override TupletNumber.text = \markup { \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        } }
                    \tuplet 3/2
                    {
                        c'8
                        d'8
                        e'8
                    }
                    \revert TupletNumber.text
                }

        """
        return self._force_fraction

    @force_fraction.setter
    def force_fraction(self, argument):
        if isinstance(argument, bool):
            self._force_fraction = argument
        else:
            raise TypeError(f"force fraction must be boolean (not {argument!r}).")

    @property
    def hide(self) -> bool | None:
        r"""
        Is true when tuplet bracket hides.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
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

            >>> tuplet.hide
            False

        ..  container:: example

            >>> tuplet_1 = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> tuplet_2 = abjad.Tuplet((2, 3), "d'4 e'4 f'4")
            >>> staff = abjad.Staff([tuplet_1, tuplet_2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \tuplet 3/2
                    {
                        c'4
                        d'4
                        e'4
                    }
                    \tuplet 3/2
                    {
                        d'4
                        e'4
                        f'4
                    }
                }

            >>> staff[0].hide = True
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \scaleDurations #'(2 . 3)
                    {
                        c'4
                        d'4
                        e'4
                    }
                    \tuplet 3/2
                    {
                        d'4
                        e'4
                        f'4
                    }
                }

        Hides tuplet bracket and tuplet number when true.
        """
        return self._hide

    @hide.setter
    def hide(self, argument):
        assert isinstance(argument, bool), repr(argument)
        self._hide = argument

    @property
    def implied_prolation(self) -> fractions.Fraction:
        r"""
        Gets implied prolation of tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.implied_prolation
            Fraction(2, 3)

        """
        return fractions.Fraction(*self.multiplier)

    @property
    def multiplied_duration(self) -> _duration.Duration:
        r"""
        Gets multiplied duration of tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")

            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.multiplied_duration
            Duration(1, 4)

        """
        multiplier = fractions.Fraction(*self.multiplier)
        contents_duration = self._get_contents_duration()
        return _duration.Duration(multiplier * contents_duration)

    @property
    def multiplier(self) -> tuple[int, int]:
        r"""
        Gets and sets multiplier of tuplet.

        ..  container:: example

            Gets tuplet multiplier:

                >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
                >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.multiplier
            (2, 3)

        ..  container:: example

            Sets tuplet multiplier:

                >>> tuplet.multiplier = (4, 3)
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

        """
        return self._multiplier

    @multiplier.setter
    def multiplier(self, argument):
        if isinstance(argument, tuple):
            assert len(argument) == 2, repr(argument)
        else:
            raise ValueError(f"tuplet multiplier must be pair, not {argument!r}.")
        if fractions.Fraction(*argument) <= 0:
            raise ValueError(f"tuplet multiplier must be positive, not {argument!r}.")
        self._multiplier = argument

    @property
    def tag(self) -> _tag.Tag | None:
        r"""
        Gets tag.

        ..  container:: example

            >>> tuplet = abjad.Tuplet(
            ...     (2, 3), "c'4 d' e'", tag=abjad.Tag('RED')
            ... )
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> string = abjad.lilypond(tuplet, tags=True)
            >>> print(string)
              %! RED
            \tuplet 3/2
              %! RED
            {
                c'4
                d'4
                e'4
              %! RED
            }

        """
        return super().tag

    @tag.setter
    def tag(self, argument) -> None:
        self._tag = argument

    ### PUBLIC METHODS ###

    def append(
        self,
        component: Component,
        *,
        language: str = "english",
        preserve_duration=False,
    ) -> None:
        r"""
        Appends ``component`` to tuplet.

        ..  container:: example

            Appends note to tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
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

            Appends note to tuplet and preserves tuplet duration:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
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

            >>> tuplet.append(abjad.Note("e'4"), preserve_duration=True)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tuplet 2/1
                {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'4
                }

        """
        if preserve_duration:
            old_duration = self._get_duration()
        Container.append(self, component, language=language)
        if preserve_duration:
            new_duration = self._get_contents_duration()
            multiplier = old_duration / new_duration
            self.multiplier = _duration.pair(multiplier)
            assert self._get_duration() == old_duration

    def augmentation(self) -> bool:
        r"""
        Is true when tuplet multiplier is greater than ``1``.

        ..  container:: example

            Augmented tuplet:

            >>> tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.augmentation()
            True

        ..  container:: example

            Diminished tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.augmentation()
            False

        ..  container:: example

            Trivial tuplet:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8. d'8. e'8.")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.augmentation()
            False

        """
        if self.multiplier:
            return 1 < fractions.Fraction(*self.multiplier)
        else:
            return False

    def diminution(self) -> bool:
        r"""
        Is true when tuplet multiplier is less than ``1``.

        ..  container:: example

            Augmented tuplet:

            >>> tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.diminution()
            False

        ..  container:: example

            Diminished tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.diminution()
            True

        ..  container:: example

            Trivial tuplet:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8. d'8. e'8.")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.diminution()
            False

        """
        if self.multiplier:
            return fractions.Fraction(*self.multiplier) < 1
        else:
            return False

    def extend(
        self, argument, *, language: str = "english", preserve_duration=False
    ) -> None:
        r"""
        Extends tuplet with ``argument``.

        ..  container:: example

            Extends tuplet with three notes:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
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

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
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
        if preserve_duration:
            old_duration = self._get_duration()
        Container.extend(self, argument, language=language)
        if preserve_duration:
            new_duration = self._get_contents_duration()
            multiplier = old_duration / new_duration
            self.multiplier = _duration.pair(multiplier)
            assert self._get_duration() == old_duration

    @staticmethod
    def from_duration(
        duration: _typings.Duration, components, *, tag: _tag.Tag | None = None
    ) -> "Tuplet":
        r"""
        Makes tuplet from ``duration`` and ``components``.

        ..  container:: example

            Makes diminution:

            >>> tuplet = abjad.Tuplet.from_duration((2, 8), "c'8 d' e'")
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

        """
        if not len(components):
            raise Exception(f"components must be nonempty: {components!r}.")
        target_duration = _duration.Duration(duration)
        tuplet = Tuplet((1, 1), components, tag=tag)
        contents_duration = tuplet._get_duration()
        multiplier = target_duration / contents_duration
        tuplet.multiplier = _duration.pair(multiplier)
        return tuplet

    def normalize_multiplier(self) -> None:
        r"""
        Normalizes tuplet multiplier.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((1, 3), "c'4 d' e'")
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

            >>> abjad.Duration(tuplet.multiplier).normalized()
            False

            >>> tuplet.normalize_multiplier()
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

            >>> abjad.Duration(tuplet.multiplier).normalized()
            True

        ..  container:: example

            >>> tuplet = abjad.Tuplet((8, 3), "c'32 d'32 e'32")
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

            >>> abjad.Duration(tuplet.multiplier).normalized()
            False

            >>> tuplet.normalize_multiplier()
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

            >>> abjad.Duration(tuplet.multiplier).normalized()
            True

        ..  container:: example

            >>> tuplet = abjad.Tuplet((5, 12), "c'4 d'4 e'4")
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

            >>> abjad.Duration(tuplet.multiplier).normalized()
            False

            >>> tuplet.normalize_multiplier()
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

            >>> abjad.Duration(tuplet.multiplier).normalized()
            True

        """
        # find tuplet multiplier
        multiplier = fractions.Fraction(*self.multiplier)
        integer_exponent = int(math.log(multiplier, 2))
        leaf_multiplier = fractions.Fraction(2) ** integer_exponent
        # scale leaves in tuplet by power of two
        for component in self:
            if isinstance(component, Leaf):
                old_written_duration = component.written_duration
                new_written_duration = leaf_multiplier * old_written_duration
                multiplier = new_written_duration / old_written_duration
                component._scale(multiplier)
        numerator, denominator = _duration.pair(leaf_multiplier)
        multiplier = fractions.Fraction(denominator, numerator)
        multiplier *= fractions.Fraction(*self.multiplier)
        pair = multiplier.numerator, multiplier.denominator
        self.multiplier = pair

    def rest_filled(self) -> bool:
        r"""
        Is true when tuplet is rest-filled.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((3, 2), "r4 r r")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  container:: example

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 2/3
                {
                    r4
                    r4
                    r4
                }

            >>> tuplet.rest_filled()
            True

        """
        return all(isinstance(_, Rest) for _ in self)

    def rewrite_dots(self) -> None:
        r"""
        Rewrites dots.

        ..  container:: example

            Rewrites single dots as 3:2 prolation:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8. c'8.")
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

            >>> tuplet = abjad.Tuplet((1, 1), "c'8.. c'8..")
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

            >>> tuplet = abjad.Tuplet((1, 1), "c'8. d'8. e'8")
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

            >>> tuplet = abjad.Tuplet((3, 2), "c'8 d' e'")
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

        Not yet implemented for multiply nested tuplets.
        """
        dot_counts = set()
        for component in self:
            if isinstance(component, Tuplet):
                return
            dot_count = component.written_duration.dot_count
            dot_counts.add(dot_count)
        if 1 < len(dot_counts):
            return
        assert len(dot_counts) == 1
        global_dot_count = dot_counts.pop()
        if global_dot_count == 0:
            return
        dot_multiplier = _duration.Duration.from_dot_count(global_dot_count)
        multiplier = fractions.Fraction(*self.multiplier) * dot_multiplier
        self.multiplier = multiplier.pair
        dot_multiplier_reciprocal = dot_multiplier.reciprocal
        for component in self:
            component.written_duration *= dot_multiplier_reciprocal

    def set_minimum_denominator(self, denominator) -> None:
        r"""
        Sets preferred denominator of tuplet to at least ``denominator``.

        ..  container:: example

            Sets preferred denominator of tuplet to ``8`` at least:

            >>> tuplet = abjad.Tuplet((3, 5), "c'4 d'8 e'8 f'4 g'2")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 5/3
                {
                    c'4
                    d'8
                    e'8
                    f'4
                    g'2
                }

            >>> tuplet.set_minimum_denominator(8)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 10/6
                {
                    c'4
                    d'8
                    e'8
                    f'4
                    g'2
                }

        """
        assert _math.is_nonnegative_integer_power_of_two(denominator)
        self.force_fraction = True
        durations = [
            self._get_contents_duration(),
            self._get_preprolated_duration(),
            _duration.Duration(1, denominator),
        ]
        pairs = _duration.Duration.durations_to_nonreduced_fractions(durations)
        self.denominator = pairs[1][0]

    def toggle_prolation(self) -> None:
        r"""
        Changes augmented tuplets to diminished; changes diminished tuplets to augmented.

        ..  container:: example

            Changes augmented tuplet to diminished:

            >>> tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")
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
                \tuplet 3/2
                {
                    c'4
                    d'4
                    e'4
                }

            Multiplies the written duration of the leaves in tuplet
            by the least power of ``2`` necessary to diminshed tuplet.

        ..  container:: example

            Changes diminished tuplet to augmented:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
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

            Divides the written duration of the leaves in tuplet
            by the least power of ``2`` necessary to diminshed tuplet.

        ..  container:: example

            REGRESSION. Leaves trivial tuplets unchanged:

            >>> tuplet = abjad.Tuplet((1, 1), "c'4 d'4 e'4")
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

        Does not yet work with nested tuplets.
        """
        if self.diminution():
            while self.diminution():
                multiplier = 2 * fractions.Fraction(*self.multiplier)
                pair = multiplier.numerator, multiplier.denominator
                self.multiplier = pair
                for component in self._get_subtree():
                    if isinstance(component, Leaf):
                        component.written_duration /= 2
        elif self.augmentation():
            while not self.diminution():
                multiplier = fractions.Fraction(*self.multiplier) / 2
                pair = multiplier.numerator, multiplier.denominator
                self.multiplier = pair
                for component in self._get_subtree():
                    if isinstance(component, Leaf):
                        component.written_duration *= 2

    def trivial(self) -> bool:
        r"""
        Is true when tuplet multiplier is equal to ``1`` and no multipliers
        attach to any leaves in tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((1, 1), "c'8 d'8 e'8")
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

            >>> tuplet.trivial()
            True

        ..  container:: example

            Tuplet is not trivial when multipliers attach to tuplet leaves:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8 d'8 e'8")
            >>> tuplet[0].multiplier = (3, 2)
            >>> tuplet[-1].multiplier = (1, 2)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'8 * 3/2
                    d'8
                    e'8 * 1/2
                }

            >>> tuplet.trivial()
            False

        """
        if self.multiplier != (1, 1):
            return False
        for component in self:
            if isinstance(component, Tuplet):
                continue
            elif hasattr(component, "written_duration"):
                if component.multiplier is not None:
                    return False
        return True

    def trivializable(self) -> bool:
        r"""
        Is true when tuplet is trivializable (can be rewritten with a ratio of 1:1).

        Redudant tuplet:

        ..  container:: example

            >>> tuplet = abjad.Tuplet((3, 4), "c'4 c'4")
            >>> staff = abjad.Staff([tuplet])
            >>> score = abjad.Score([staff], name="Score")
            >>> abjad.attach(abjad.TimeSignature((3, 8)), tuplet[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 4/3
                {
                    \time 3/8
                    c'4
                    c'4
                }

            >>> tuplet.trivializable()
            True

            Can be rewritten without a tuplet bracket:

            >>> staff = abjad.Staff("c'8. c'8.")
            >>> score = abjad.Score([staff], name="Score")
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \time 3/8
                    c'8.
                    c'8.
                }

        ..  container:: example

            Nontrivializable tuplet:

            >>> tuplet = abjad.Tuplet((3, 5), "c'4 c'4 c'4 c'4 c'4")
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

            >>> tuplet.trivializable()
            False

            Can not be rewritten without a tuplet bracket.

        ..  container:: example

            REGRESSION. Nontrivializable tuplet:

            >>> tuplet = abjad.Tuplet((3, 4), "c'2. c4")
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
                    \tuplet 4/3
                    {
                        \time 3/4
                        c'2.
                        c4
                    }
                }

            >>> tuplet.trivializable()
            False

        """
        for component in self:
            if isinstance(component, Tuplet):
                continue
            assert isinstance(component, Leaf), repr(component)
            fraction = fractions.Fraction(*self.multiplier) * component.written_duration
            duration = _duration.Duration(fraction)
            if not duration.is_assignable:
                return False
        return True

    def trivialize(self) -> None:
        r"""
        Trivializes tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((3, 4), "c'2")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 4/3
                {
                    c'2
                }

            >>> tuplet.trivializable()
            True

            >>> tuplet.trivialize()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(tuplet)
                >>> print(string)
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'4.
                }

        """
        if not self.trivializable():
            return
        for component in self:
            if isinstance(component, Tuplet):
                multiplier = fractions.Fraction(*component.multiplier)
                multiplier *= fractions.Fraction(*self.multiplier)
                pair = multiplier.numerator, multiplier.denominator
                component.multiplier = pair
            elif isinstance(component, Leaf):
                component.written_duration *= fractions.Fraction(*self.multiplier)
            else:
                raise TypeError(component)
        self.multiplier = (1, 1)


class Voice(Context):
    r"""
    Voice.

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

    Voice-contexted indicators like dynamics work with nested voices.

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
        ...     dynamic = abjad.get.effective(leaf, abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        Note("e''8") Dynamic(name='f', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("d''8") Dynamic(name='f', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("c''4") Dynamic(name='f', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("b'4") Dynamic(name='f', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("c''8") Dynamic(name='f', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("e'4") None
        Note("f'4") None
        Note("e'8") None
        Note("d''8") Dynamic(name='f', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)

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
        ...     dynamic = abjad.get.effective(leaf, abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        Note("e''8") None
        Note("d''8") None
        Note("c''4") None
        Note("b'4") None
        Note("c''8") None
        Note("e'4") Dynamic(name='p', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("f'4") Dynamic(name='p', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("e'8") Dynamic(name='p', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
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
        ...     dynamic = abjad.get.effective(leaf, abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        Note("e''8") None
        Note("d''8") None
        Note("c''4") Dynamic(name='mf', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("b'4") Dynamic(name='mf', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("c''8") Dynamic(name='mf', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("e'4") None
        Note("f'4") None
        Note("e'8") None
        Note("d''8") Dynamic(name='mf', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)

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
        ...     dynamic = abjad.get.effective(leaf, abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        Note("e''8") None
        Note("d''8") None
        Note("c''4") Dynamic(name='mf', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("b'4") Dynamic(name='mf', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("c''8") Dynamic(name='mf', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("e'4") Dynamic(name='p', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("f'4") Dynamic(name='p', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("e'8") Dynamic(name='p', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)
        Note("d''8") Dynamic(name='mf', command=None, hide=False, leak=False, name_is_textual=False, ordinal=None)

    ..  container:: example

        Selects language:

        >>> abjad.Voice("do'8 re' mi' fa'", language="français")
        Voice("c'8 d'8 e'8 f'8")

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Contexts"

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

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self) -> _tag.Tag | None:
        r"""
        Gets tag.

        ..  container:: example

            >>> voice = abjad.Voice("c'4 d' e' f'", tag=abjad.Tag('RED'))
            >>> abjad.show(voice) # doctest: +SKIP

            >>> string = abjad.lilypond(voice, tags=True)
            >>> print(string)
            %! RED
            \new Voice
            %! RED
            {
                c'4
                d'4
                e'4
                f'4
            %! RED
            }

        """
        return super().tag

    @tag.setter
    def tag(self, argument) -> None:
        self._tag = argument
