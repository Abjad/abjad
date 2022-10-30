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
        >>> abjad.attach(abjad.Clef("alto"), voice_2[0])
        >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
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
        check_duplicate_indicator=False,
        component=None,
        context: str = None,
        deactivate: bool = False,
        direction: _enums.Vertical = None,
        indicator: typing.Any = None,
        synthetic_offset: int = None,
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

        ..  container:: example

            Preserves annotation flag:

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
        # if getattr(self.indicator, "context", None) is not None:
        if getattr(indicator, "context", None) is not None:
            if check_duplicate_indicator is True:
                self._warn_duplicate_indicator(component)
            self._unbind_component()
            self._component = component
            self._update_effective_context()
            # if getattr(self.indicator, "_mutates_offsets_in_seconds", False):
            if getattr(indicator, "_mutates_offsets_in_seconds", False):
                self._component._update_later(offsets_in_seconds=True)
        component._wrappers.append(self)

    def _bind_effective_context(self, correct_effective_context):
        self._unbind_effective_context()
        if correct_effective_context is not None:
            correct_effective_context._dependent_wrappers.append(self)
        self._effective_context = correct_effective_context
        self._update_effective_context()
        if isinstance(self.indicator, _tweaks.Bundle):
            indicator = self.indicator.indicator
        else:
            indicator = self.indicator
        # if getattr(self.indicator, "_mutates_offsets_in_seconds", False):
        if getattr(indicator, "_mutates_offsets_in_seconds", False):
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
            _updatelib._update_now(self.component, indicators=True)
        return self._effective_context

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
        if self._effective_context is not correct_effective_context:
            self._bind_effective_context(correct_effective_context)

    def _warn_duplicate_indicator(self, component):
        if self.deactivate is True:
            return
        if isinstance(self.indicator, _tweaks.Bundle):
            indicator = self.indicator.indicator
        else:
            indicator = self.indicator
        prototype = type(indicator)
        command = getattr(indicator, "command", None)
        wrapper = _getlib._get_effective(
            component,
            prototype,
            attributes={"command": command},
            unwrap=False,
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
    def component(self):
        """
        Gets start component.

        Returns component or none.
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
        self._deactivate: bool | None = argument

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

        Returns offset.
        """
        if self._synthetic_offset is not None:
            return self._synthetic_offset
        if isinstance(self.indicator, _tweaks.Bundle):
            indicator = self.indicator.indicator
        else:
            indicator = self.indicator
        if not getattr(indicator, "leak", False):
            return self._component._get_timespan().start_offset
        else:
            return self._component._get_timespan().stop_offset

    @property
    def start_offset(self) -> _duration.Offset:
        """
        Gets start offset.

        This is either the wrapper's synthetic offset or the start offset of the
        wrapper's component.
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
        Gets unbundled indicator.
        """
        if isinstance(self.indicator, _tweaks.Bundle):
            return self.indicator.indicator
        return self.indicator


def annotate(component, annotation, indicator) -> None:
    r"""
    Annotates ``component`` with ``indicator``.

    ..  container:: example

        Annotates first note in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.annotate(staff[0], "bow_direction", abjad.DOWN)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }

        >>> abjad.get.annotation(staff[0], "bow_direction")
        <Vertical.DOWN: -1>

        >>> abjad.get.annotation(staff[0], "bow_fraction") is None
        True

        >>> abjad.get.annotation(staff[0], "bow_fraction", 99)
        99

    """
    if isinstance(annotation, _tag.Tag):
        message = "use the tag=None keyword instead of annotate():\n"
        message += f"   {repr(annotation)}"
        raise Exception(message)
    assert isinstance(annotation, str | enum.Enum), repr(annotation)
    Wrapper(annotation=annotation, component=component, indicator=indicator)


def attach(  # noqa: 302
    attachable,
    target,
    check_duplicate_indicator=False,
    context=None,
    deactivate=False,
    direction: _enums.Vertical = None,
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
        >>> abjad.attach(abjad.Clef("alto"), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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
        >>> abjad.attach(abjad.Articulation(">"), staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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

        >>> voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> staff = abjad.Staff([voice], name="MusicStaff")
        >>> abjad.attach(abjad.Clef("alto"), voice[0], context="MusicStaff")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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

        >>> for leaf in abjad.select.leaves(staff):
        ...     leaf, abjad.get.effective(leaf, abjad.Clef)
        ...
        (Note("c'4"), Clef(name='alto', hide=False))
        (Note("d'4"), Clef(name='alto', hide=False))
        (Note("e'4"), Clef(name='alto', hide=False))
        (Note("f'4"), Clef(name='alto', hide=False))

        Derives context from default ``attachable`` context when ``context`` is none.

    ..  container:: example

        Two contexted indicators can not be attached at the same offset if both
        indicators are active:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Clef("treble"), staff[0])
        >>> abjad.attach(abjad.Clef("alto"), staff[0], check_duplicate_indicator=True)
        Traceback (most recent call last):
            ...
        abjad...PersistentIndicatorError: Can not attach ...

        But simultaneous contexted indicators are allowed if only one is active (and all
        others are inactive):

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Clef("treble"), staff[0])
        >>> abjad.attach(
        ...     abjad.Clef("alto"),
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("+PARTS"),
        ... )
        >>> abjad.attach(
        ...     abjad.Clef("tenor"),
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("+PARTS"),
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff, tags=True)
            >>> print(string)
            \new Staff
            {
                %! +PARTS
                %@% \clef "alto"
                %! +PARTS
                %@% \clef "tenor"
                \clef "treble"
                c'4
                d'4
                e'4
                f'4
            }

        Active indicator is always effective when competing inactive indicators are
        present:

        >>> for note in staff:
        ...     clef = abjad.get.effective(staff[0], abjad.Clef)
        ...     note, clef
        ...
        (Note("c'4"), Clef(name='treble', hide=False))
        (Note("d'4"), Clef(name='treble', hide=False))
        (Note("e'4"), Clef(name='treble', hide=False))
        (Note("f'4"), Clef(name='treble', hide=False))

        But a lone inactivate indicator is effective when no active indicator is present:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(
        ...     abjad.Clef("alto"),
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("+PARTS"),
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff, tags=True)
            >>> print(string)
            \new Staff
            {
                %! +PARTS
                %@% \clef "alto"
                c'4
                d'4
                e'4
                f'4
            }

        >>> for note in staff:
        ...     clef = abjad.get.effective(staff[0], abjad.Clef)
        ...     note, clef
        ...
        (Note("c'4"), Clef(name='alto', hide=False))
        (Note("d'4"), Clef(name='alto', hide=False))
        (Note("e'4"), Clef(name='alto', hide=False))
        (Note("f'4"), Clef(name='alto', hide=False))

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
        >>> abjad.attach(abjad.Clef('alto'), staff[0], wrapper=True)
        Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string=''))

    Otherwise returns none.
    """
    if isinstance(attachable, _tweaks.Bundle):
        nonbundle_attachable = attachable.indicator
    else:
        nonbundle_attachable = attachable
    assert not isinstance(nonbundle_attachable, _tweaks.Bundle)

    if isinstance(nonbundle_attachable, _tag.Tag):
        message = "use the tag=None keyword instead of attach():\n"
        message += f"   {repr(attachable)}"
        raise Exception(message)

    if tag is not None and not isinstance(tag, _tag.Tag):
        raise Exception(f"must be be tag: {repr(tag)}")

    if isinstance(nonbundle_attachable, _duration.Multiplier):
        message = "use the Leaf.multiplier property to multiply leaf duration."
        raise Exception(message)

    assert nonbundle_attachable is not None, repr(nonbundle_attachable)
    assert target is not None, repr(target)

    if context is not None and hasattr(nonbundle_attachable, "_main_leaf"):
        raise Exception(f"set context only for indicators, not {attachable!r}.")

    if deactivate is True and tag is None:
        raise Exception("tag must exist when deactivate is true.")

    if hasattr(nonbundle_attachable, "_before_attach"):
        nonbundle_attachable._before_attach(target)

    if hasattr(nonbundle_attachable, "_attachment_test_all") and not do_not_test:
        result = nonbundle_attachable._attachment_test_all(target)
        if result is not True:
            assert isinstance(result, list), repr(result)
            result = ["  " + _ for _ in result]
            message = f"{nonbundle_attachable!r}._attachment_test_all():"
            result.insert(0, message)
            message = "\n".join(result)
            raise Exception(message)

    prototype = (_score.AfterGraceContainer, _score.BeforeGraceContainer)
    if isinstance(nonbundle_attachable, prototype):
        if not hasattr(target, "written_duration"):
            raise Exception("grace containers attach to single leaf only.")
        nonbundle_attachable._attach(target)
        return

    assert isinstance(target, _score.Component), repr(target)

    if isinstance(target, _score.Container):
        acceptable = False
        if isinstance(
            nonbundle_attachable, dict | str | enum.Enum | _tag.Tag | Wrapper
        ):
            acceptable = True
        if getattr(nonbundle_attachable, "_can_attach_to_containers", False):
            acceptable = True
        if not acceptable:
            message = f"can not attach {attachable!r} to containers: {target!r}"
            raise Exception(message)
    elif not isinstance(target, _score.Leaf):
        message = f"indicator {attachable!r} must attach to leaf, not {target!r}."
        raise Exception(message)

    component = target
    assert isinstance(component, _score.Component), repr(component)

    annotation = None
    if isinstance(attachable, Wrapper):
        annotation = attachable.annotation
        context = context or attachable.context
        deactivate = deactivate or attachable.deactivate
        synthetic_offset = synthetic_offset or attachable.synthetic_offset
        tag = tag or attachable.tag
        attachable._detach()
        attachable = attachable.indicator

    if hasattr(nonbundle_attachable, "context"):
        context = context or nonbundle_attachable.context

    if tag is None:
        tag = _tag.Tag()

    wrapper_ = Wrapper(
        annotation=annotation,
        check_duplicate_indicator=check_duplicate_indicator,
        component=component,
        context=context,
        deactivate=deactivate,
        direction=direction,
        indicator=attachable,
        synthetic_offset=synthetic_offset,
        tag=tag,
    )

    if wrapper is True:
        return wrapper_


def detach(argument, target=None, by_id=False):
    r"""
    Detaches indicators-equal-to-``argument`` from ``target``.

    Set ``by_id`` to true to detach exact ``argument`` from ``target`` (rather than
    detaching all indicators-equal-to-``argument``).

    ..  container:: example

        Detaches articulations from first note in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Articulation(">"), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \accent
                d'4
                e'4
                f'4
            }

        >>> abjad.detach(abjad.Articulation, staff[0])
        (Articulation(name='>'),)

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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

        >>> markup_1 = abjad.Markup(r"\markup tutti")
        >>> markup_2 = abjad.Markup(r"\markup { with the others }")
        >>> markup_3 = abjad.Markup(r"\markup { with the others }")

        Markups two and three compare equal:

        >>> markup_2 == markup_3
        True

        But document-tagging like this makes sense for score and two diferent parts:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(markup_1, staff[0], direction=abjad.UP, tag=abjad.Tag(string="+SCORE"))
        >>> abjad.attach(
        ...     markup_2,
        ...     staff[0],
        ...     deactivate=True,
        ...     direction=abjad.UP,
        ...     tag=abjad.Tag("+PARTS_VIOLIN_1"),
        ... )
        >>> abjad.attach(
        ...     markup_3,
        ...     staff[0],
        ...     deactivate=True,
        ...     direction=abjad.UP,
        ...     tag=abjad.Tag("+PARTS_VIOLIN_2"),
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'4
            %! +SCORE
            ^ \markup tutti
            %! +PARTS_VIOLIN_1
            %@% ^ \markup { with the others }
            %! +PARTS_VIOLIN_2
            %@% ^ \markup { with the others }
            d'4
            e'4
            f'4
        }

        The question is then how to detach just one of the two markups that compare equal
        to each other?

        Passing in one of the markup objects directory doesn't work. This is because
        detach tests for equality to input argument:

        >>> markups = abjad.detach(markup_2, staff[0])
        >>> for markup in markups:
        ...     markup
        Markup(string='\\markup { with the others }')
        Markup(string='\\markup { with the others }')

        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'4
            %! +SCORE
            ^ \markup tutti
            d'4
            e'4
            f'4
        }

        We start again:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(markup_1, staff[0], direction=abjad.UP, tag=abjad.Tag(string="+SCORE"))
        >>> abjad.attach(
        ...     markup_2,
        ...     staff[0],
        ...     deactivate=True,
        ...     direction=abjad.UP,
        ...     tag=abjad.Tag("+PARTS_VIOLIN_1"),
        ... )
        >>> abjad.attach(
        ...     markup_3,
        ...     staff[0],
        ...     deactivate=True,
        ...     direction=abjad.UP,
        ...     tag=abjad.Tag("+PARTS_VIOLIN_2"),
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'4
            %! +SCORE
            ^ \markup tutti
            %! +PARTS_VIOLIN_1
            %@% ^ \markup { with the others }
            %! +PARTS_VIOLIN_2
            %@% ^ \markup { with the others }
            d'4
            e'4
            f'4
        }

        This time we set ``by_id`` to true. Now detach checks the exact id of its input
        argument (rather than just testing for equality). This gives us what we want:

        >>> markups = abjad.detach(markup_2, staff[0], by_id=True)
        >>> for markup in markups:
        ...     markup
        Markup(string='\\markup { with the others }')

        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'4
            %! +SCORE
            ^ \markup tutti
            %! +PARTS_VIOLIN_2
            %@% ^ \markup { with the others }
            d'4
            e'4
            f'4
        }

    ..  container:: example

        REGRESSION. Attach-detach-attach pattern works correctly when detaching wrappers:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Clef("alto"), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "alto"
                c'4
                d'4
                e'4
                f'4
            }

        >>> wrapper = abjad.get.wrappers(staff[0])[0]
        >>> abjad.detach(wrapper, wrapper.component)
        (Wrapper(annotation=None, context='Staff', deactivate=False, direction=None, indicator=Clef(name='alto', hide=False), synthetic_offset=None, tag=Tag(string='')),)

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }

        >>> abjad.attach(abjad.Clef("tenor"), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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
                # elif isinstance(wrapper.indicator, argument):
                elif isinstance(wrapper.unbundle_indicator(), argument):
                    wrapper._detach()
                    # result.append(wrapper.indicator)
                    result.append(wrapper.get_item())
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
                # elif wrapper.indicator == argument:
                elif wrapper.unbundle_indicator() == argument:
                    # if by_id is True and id(argument) != id(wrapper.indicator):
                    if by_id is True and id(argument) != id(
                        wrapper.unbundle_indicator()
                    ):
                        pass
                    else:
                        wrapper._detach()
                        # result.append(wrapper.indicator)
                        result.append(wrapper.get_item())
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
