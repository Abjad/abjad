"""
Wrapper.
"""

import copy
import enum
import importlib
import typing

from . import _getlib, _updatelib
from . import duration as _duration
from . import enums as _enums
from . import exceptions as _exceptions
from . import score as _score
from . import tag as _tag
from . import tweaks as _tweaks


class Wrapper:
    r"""
    Wrapper.

    ..  container:: example

        >>> component = abjad.Note("c'4")
        >>> articulation = abjad.Articulation("accent")
        >>> abjad.attach(articulation, component, direction=abjad.UP)
        >>> abjad.get.wrapper(component)
        Wrapper(annotation=None, context=None, deactivate=False, direction=<Vertical.UP: 1>, indicator=Articulation(name='accent'), synthetic_offset=None, tag=Tag(string=''))

    ..  container:: example

        Duplicate indicator warnings take two forms.

        >>> voice_1 = abjad.Voice("c''4 d'' e'' f''", name="VoiceI")
        >>> voice_2 = abjad.Voice("c'4 d' e' f'", name="VoiceII")
        >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
        >>> abjad.attach(abjad.Clef("alto"), voice_2[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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

        First form when attempting to attach a contexted indicator to a leaf that already
        carries a contexted indicator of the same type:

        >>> # abjad.attach(abjad.Clef("treble"), voice_2[0])

        Second form when attempting to attach a contexted indicator to a leaf governed by
        some other component carrying a contexted indicator of the same type.

        >>> # abjad.attach(abjad.Clef("treble"), voice_1[0])

    """

    __documentation_section__ = "Internals"

    __slots__ = (
        "_annotation",
        "_component",
        "_context",
        "_deactivate",
        "_direction",
        "_effective_context",
        "_indicator",
        "_synthetic_offset",
        "_tag",
    )

    def __init__(
        self,
        annotation: str | enum.Enum | None = None,
        # TODO: move check_duplicate_indicator to _unsafe_attach()
        check_duplicate_indicator: bool = False,
        component: _score.Component | None = None,
        context: str | None = None,
        deactivate: bool = False,
        direction: _enums.Vertical | None = None,
        indicator: typing.Any = None,
        synthetic_offset: _duration.Offset | None = None,
        tag: _tag.Tag = _tag.Tag(),
    ) -> None:
        assert not isinstance(indicator, type(self)), repr(indicator)
        if annotation is not None:
            assert isinstance(annotation, str | enum.Enum), repr(annotation)
        self._annotation = annotation
        if component is not None:
            assert isinstance(component, _score.Component), repr(component)
        self._component = component
        deactivate = bool(deactivate)
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if deactivate is not None:
            deactivate = bool(deactivate)
        self._deactivate = deactivate
        self._direction = direction
        self._effective_context = None
        self._indicator = indicator
        self._synthetic_offset: _duration.Offset | None
        if synthetic_offset is not None:
            assert isinstance(synthetic_offset, _duration.Offset), repr(
                synthetic_offset
            )
            self._synthetic_offset = _duration.Offset(synthetic_offset)
        else:
            self._synthetic_offset = synthetic_offset
        if tag is not None:
            assert isinstance(tag, str | _tag.Tag)
        assert isinstance(tag, _tag.Tag), repr(tag)
        self._tag = tag
        if component is not None:
            self._bind_component(
                component, check_duplicate_indicator=check_duplicate_indicator
            )

    def __copy__(self, *arguments) -> "Wrapper":
        r"""
        Copies wrapper.

        Preserves annotation flag:

        ..  container:: example

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.annotate(old_staff[0], "bow_direction", abjad.DOWN)
            >>> string = abjad.lilypond(old_staff)
            >>> print(string)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = old_staff[0]
            >>> abjad.get.annotation(leaf, "bow_direction")
            <Vertical.DOWN: -1>

            >>> new_staff = abjad.mutate.copy(old_staff)
            >>> string = abjad.lilypond(new_staff)
            >>> print(string)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = new_staff[0]
            >>> abjad.get.annotation(leaf, "bow_direction")
            <Vertical.DOWN: -1>

        ..  container:: example

            Preserves tag:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> clef = abjad.Clef("alto")
            >>> abjad.attach(clef, old_staff[0], tag=abjad.Tag("RED:M1"))
            >>> string = abjad.lilypond(old_staff, tags=True)
            >>> print(string)
            \new Staff
            {
                %! M1
                %! RED
                \clef "alto"
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = old_staff[0]
            >>> abjad.get.wrapper(leaf)
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string='RED:M1'))

            >>> new_staff = abjad.mutate.copy(old_staff)
            >>> string = abjad.lilypond(new_staff, tags=True)
            >>> print(string)
            \new Staff
            {
                %! M1
                %! RED
                \clef "alto"
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = new_staff[0]
            >>> abjad.get.wrapper(leaf)
            Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string='RED:M1'))

        ..  container:: example

            Preserves deactivate flag:

            >>> old_staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.attach(
            ...     abjad.Clef("alto"),
            ...     old_staff[0],
            ...     deactivate=True,
            ...     tag=abjad.Tag("RED:M1"),
            ... )
            >>> string = abjad.lilypond(old_staff, tags=True)
            >>> print(string)
            \new Staff
            {
                %! M1
                %! RED
                %@% \clef "alto"
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = old_staff[0]
            >>> abjad.get.wrapper(leaf)
            Wrapper(annotation=None, context='Staff', deactivate=True, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string='RED:M1'))

            >>> new_staff = abjad.mutate.copy(old_staff)
            >>> string = abjad.lilypond(new_staff, tags=True)
            >>> print(string)
            \new Staff
            {
                %! M1
                %! RED
                %@% \clef "alto"
                c'4
                d'4
                e'4
                f'4
            }

            >>> leaf = new_staff[0]
            >>> abjad.get.wrapper(leaf)
            Wrapper(annotation=None, context='Staff', deactivate=True, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string='RED:M1'))

        Copies all properties except component.

        Copy operations must supply component after wrapper copy.
        """
        new = type(self)(
            annotation=self.annotation,
            component=None,
            context=self.context,
            deactivate=self.deactivate,
            direction=self.direction,
            indicator=copy.copy(self.indicator),
            synthetic_offset=self.synthetic_offset,
            tag=self.tag,
        )
        return new

    def __eq__(self, argument) -> bool:
        """
        Is true when self equals ``argument``.
        """
        if not isinstance(argument, Wrapper):
            return False
        if self.annotation != argument.annotation:
            return False
        if self.component != argument.component:
            return False
        if self.context != argument.context:
            return False
        if self.deactivate != argument.deactivate:
            return False
        if self.indicator != argument.indicator:
            return False
        if self.synthetic_offset != argument.synthetic_offset:
            return False
        if self.tag != argument.tag:
            return False
        return True

    def __hash__(self) -> int:
        """
        Hashes wrapper.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        parameters = f"""
            annotation={self.annotation!r},
            context={self.context!r},
            deactivate={self.deactivate!r},
            direction={self.direction!r},
            indicator={self.indicator!r},
            synthetic_offset={self.synthetic_offset!r},
            tag={self.tag!r}
        """
        parameters = " ".join(parameters.split())
        return f"{type(self).__name__}({parameters})"

    def _bind_component(self, component, check_duplicate_indicator=False):
        if isinstance(self.indicator, _tweaks.Bundle):
            indicator = self.indicator.indicator
        else:
            indicator = self.indicator
        if getattr(indicator, "context", None) is not None:
            if check_duplicate_indicator is True:
                self._check_duplicate_indicator(component)
            self._unbind_component()
            self._component = component
            self._update_effective_context()
            if getattr(indicator, "mutates_offsets_in_seconds", False):
                self._component._update_later(offsets_in_seconds=True)
        component._wrappers.append(self)

    def _bind_effective_context(self, correct_effective_context):
        self._unbind_effective_context()
        if correct_effective_context is not None:
            if self not in correct_effective_context._dependent_wrappers:
                correct_effective_context._dependent_wrappers.append(self)
        self._effective_context = correct_effective_context
        self._update_effective_context()
        if isinstance(self.indicator, _tweaks.Bundle):
            indicator = self.indicator.indicator
        else:
            indicator = self.indicator
        if correct_effective_context is not None:
            if getattr(indicator, "mutates_offsets_in_seconds", False):
                correct_effective_context._update_later(offsets_in_seconds=True)

    def _check_duplicate_indicator(self, component):
        if self.deactivate is True:
            return
        if isinstance(self.indicator, _tweaks.Bundle):
            indicator = self.indicator.indicator
        else:
            indicator = self.indicator
        prototype = type(indicator)
        command = getattr(indicator, "command", None)
        wrapper = _getlib._get_effective_wrapper(
            component,
            prototype,
            attributes={"command": command},
        )
        wrapper_site = None
        if wrapper is not None:
            wrapper_site = getattr(wrapper.unbundle_indicator(), "site", None)
        my_site = getattr(indicator, "site", None)
        if (
            wrapper is None
            or wrapper.context is None
            or wrapper.deactivate is True
            or wrapper.start_offset != self.start_offset
            or wrapper_site != my_site
        ):
            return
        my_leak = getattr(indicator, "leak", None)
        if getattr(wrapper.unbundle_indicator(), "leak", None) != my_leak:
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
        if wrapper.unbundle_indicator() == indicator and context is not wrapper_context:
            return
        message = f"\n\nCan not attach ...\n\n{repr(self)}\n\n..."
        message += f" to {repr(component)}"
        message += f" in {getattr(context, 'name', None)} because ..."
        message += f"\n\n{repr(wrapper)}\n\n"
        message += "... is already attached"
        if component is wrapper.component:
            message += " to the same leaf."
        else:
            message += f" to {repr(wrapper.component)}"
            message += f" in {wrapper_context.name}."
        message += "\n"
        raise _exceptions.PersistentIndicatorError(message)

    def _detach(self):
        self._unbind_component()
        self._unbind_effective_context()
        return self

    @staticmethod
    def _find_correct_effective_context(component, context):
        if context is None:
            return None
        abjad = importlib.import_module("abjad")
        context = getattr(abjad, context, context)
        candidate = None
        parentage = component._get_parentage()
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
            _updatelib._update_now(self.component, indicators=True)
        return self._effective_context

    def _unbind_component(self):
        if self._component is not None and id(self) in [
            id(_) for _ in self._component._wrappers
        ]:
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
        correct_effective_context = self._find_correct_effective_context(
            self.component, self.context
        )
        if self._effective_context is not correct_effective_context:
            self._bind_effective_context(correct_effective_context)
        if correct_effective_context is not None:
            if self not in correct_effective_context._dependent_wrappers:
                correct_effective_context._dependent_wrappers.append(self)

    @property
    def annotation(self) -> str | enum.Enum | None:
        """
        Gets wrapper annotation.

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation("accent")
            >>> abjad.attach(articulation, note, direction=abjad.UP)
            >>> wrapper = abjad.get.wrapper(note)
            >>> wrapper.annotation is None
            True

            >>> note = abjad.Note("c'4")
            >>> articulation = abjad.Articulation("accent")
            >>> abjad.annotate(note, "foo", articulation)
            >>> abjad.get.annotation(note, "foo")
            Articulation(name='accent')

        """
        return self._annotation

    @property
    def component(self) -> _score.Component | None:
        """
        Gets start component.
        """
        return self._component

    @property
    def context(self) -> str | None:
        """
        Gets context (name).
        """
        return self._context

    @property
    def deactivate(self) -> bool:
        """
        Is true when wrapper deactivates tag.
        """
        assert self._deactivate in (True, False, None)
        return self._deactivate

    @deactivate.setter
    def deactivate(self, argument):
        assert argument in (True, False, None)
        self._deactivate = argument

    @property
    def direction(self):
        """
        Gets direction of indicator.
        """
        return self._direction

    @property
    def indicator(self) -> typing.Any:
        """
        Gets indicator.
        """
        return self._indicator

    @property
    def leaked_start_offset(self) -> _duration.Offset:
        r"""
        Gets start offset and checks to see whether indicator leaks to the right.

        This is either the wrapper's synthetic offset (if set); or the START offset of
        the wrapper's component (if indicator DOES NOT leak); or else the STOP offset of
        the wrapper's component (if indicator DOES leak).

        ..  container:: example

            Start- and stop-text-spans attach to the same leaf. But stop-text-span leaks
            to the right:

            >>> voice = abjad.Voice("c'2 d'2")
            >>> start_text_span = abjad.StartTextSpan()
            >>> abjad.attach(start_text_span, voice[0])
            >>> stop_text_span = abjad.StopTextSpan(leak=True)
            >>> abjad.attach(stop_text_span, voice[0])
            >>> abjad.show(voice) # doctest: +SKIP

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                c'2
                \startTextSpan
                <> \stopTextSpan
                d'2
            }

            Start offset and leaked start offset are the same for start-text-span:

            >>> wrapper = abjad.get.wrapper(voice[0], abjad.StartTextSpan)
            >>> wrapper.start_offset, wrapper.leaked_start_offset
            (Offset((0, 1)), Offset((0, 1)))

            Start offset and leaked start offset differ for stop-text-span:

            >>> wrapper = abjad.get.wrapper(voice[0], abjad.StopTextSpan)
            >>> wrapper.start_offset, wrapper.leaked_start_offset
            (Offset((0, 1)), Offset((1, 2)))

        """
        if self._synthetic_offset is not None:
            return self._synthetic_offset
        if isinstance(self.indicator, _tweaks.Bundle):
            indicator = self.indicator.indicator
        else:
            indicator = self.indicator
        assert isinstance(self.component, _score.Component)
        if not getattr(indicator, "leak", False):
            return self.component._get_timespan().start_offset
        else:
            return self.component._get_timespan().stop_offset

    @property
    def site_adjusted_start_offset(self) -> _duration.Offset:
        r"""
        Gets site-adjusted start offset.

        ..  container:: example

            Indicators with site equal to ``absolute_after``, ``after`` or
            ``closing`` give a site-adjusted start offset equal to the stop
            offset of the wrapper's component.

            Indicators with any other site give a site-adjusted start offset
            equal to the start offset of the wrapper's component. This is the
            usual case, and means that site-adjusted start offset equals
            vanilla start offset.

            But if ``synthetic_offset`` is set then ``synthetic_offset`` is
            returned directly without examining the format site at all.

            >>> staff = abjad.Staff("c'4")
            >>> abjad.attach(abjad.Ottava(-1, site="before"), staff[0])
            >>> abjad.attach(abjad.Ottava(0, site="after"), staff[0])
            >>> for wrapper in abjad.get.wrappers(staff[0], abjad.Ottava):
            ...     wrapper.indicator, wrapper.site_adjusted_start_offset
            (Ottava(n=-1, site='before'), Offset((0, 1)))
            (Ottava(n=0, site='after'), Offset((1, 4)))

        """
        if self.synthetic_offset is not None:
            return self.synthetic_offset
        site = getattr(self.unbundle_indicator(), "site", "before")
        assert self.component is not None
        if site in ("absolute_after", "after", "closing"):
            return self.component._get_timespan().stop_offset
        else:
            return self.component._get_timespan().start_offset

    @property
    def start_offset(self) -> _duration.Offset:
        """
        Gets start offset.

        This is either the wrapper's synthetic offset or the start offset of the
        wrapper's component.
        """
        if self.synthetic_offset is not None:
            return self.synthetic_offset
        assert isinstance(self.component, _score.Component)
        return self.component._get_timespan().start_offset

    @property
    def synthetic_offset(self) -> _duration.Offset | None:
        """
        Gets synthetic offset.
        """
        return self._synthetic_offset

    @property
    def tag(self) -> _tag.Tag:
        """
        Gets and sets tag.
        """
        assert isinstance(self._tag, _tag.Tag), repr(self._tag)
        return self._tag

    @tag.setter
    def tag(self, argument):
        if not isinstance(argument, _tag.Tag):
            raise Exception(f"must be tag: {argument!r}.")
        self._tag = argument

    def bundled(self):
        """
        Is true when indicator is bundled.
        """
        return isinstance(self._indicator, _tweaks.Bundle)

    def get_item(self):
        """
        Gets indicator or bundled indicator.
        """
        return self._indicator

    def unbundle_indicator(self):
        """
        Unbundles indicator.
        """
        if isinstance(self.indicator, _tweaks.Bundle):
            return self.indicator.indicator
        return self.indicator
