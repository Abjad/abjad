"""
Wrapper.
"""

import copy
import importlib
import typing

from . import _getlib, _updatelib
from . import duration as _duration
from . import enums as _enums
from . import exceptions as _exceptions
from . import parentage as _parentage
from . import score as _score
from . import tag as _tag
from . import tweaks as _tweaks


class Wrapper:
    r"""
    Wrapper.

    ..  container:: example

        Use ``abjad.get.attach()`` to attach an indicator to a component.

        Use ``abjad.get.wrapper()`` to inspect the wrapper that is created.

        >>> component = abjad.Note("c'4")
        >>> articulation = abjad.Articulation("accent")
        >>> abjad.attach(articulation, component, direction=abjad.UP)
        >>> wrapper = abjad.get.wrapper(component)
        >>> type(wrapper)
        <class 'abjad.wrapper.Wrapper'>

    """

    __slots__ = (
        "_annotation",
        "_component",
        "_context_name",
        "_deactivate",
        "_direction",
        "_effective_context",
        "_hide",
        "_indicator",
        "_synthetic_offset",
        "_tag",
    )

    def __init__(
        self,
        *,
        annotation: str | None = None,
        check_duplicate_indicator: bool = False,
        component: _score.Component | None = None,
        context_name: str | None = None,
        deactivate: bool = False,
        direction: _enums.Vertical | str | None = None,
        hide: bool = False,
        indicator: typing.Any = None,
        synthetic_offset: _duration.Offset | None = None,
        tag: _tag.Tag = _tag.Tag(),
    ) -> None:
        if annotation is not None:
            assert isinstance(annotation, str), repr(annotation)
        if component is not None:
            assert isinstance(component, _score.Component), repr(component)
        if context_name is not None:
            assert isinstance(context_name, str), repr(context_name)
        assert isinstance(deactivate, bool), repr(deactivate)
        if direction is not None:
            assert isinstance(direction, _enums.Vertical | str), repr(direction)
        assert isinstance(hide, bool), repr(hide)
        assert not isinstance(indicator, type(self)), repr(indicator)
        if synthetic_offset is not None:
            prototype = _duration.Offset
            assert isinstance(synthetic_offset, prototype), repr(synthetic_offset)
        assert isinstance(tag, _tag.Tag), repr(tag)
        self._annotation = annotation
        self._component = component
        self._context_name = context_name
        self._deactivate = deactivate
        self._direction = direction
        self._effective_context: _score.Context | None = None
        self._hide = hide
        self._indicator = indicator
        self._synthetic_offset = synthetic_offset
        self._tag = tag
        if component is not None:
            self._bind_component(
                component,
                check_duplicate_indicator=check_duplicate_indicator,
            )

    def __copy__(self, *arguments) -> "Wrapper":
        """
        Copies all properties except component; calling code must supply
        component after copy.
        """
        new = type(self)(
            annotation=self.get_annotation(),
            component=None,
            context_name=self.get_context_name(),
            deactivate=self.get_deactivate(),
            direction=self.get_direction(),
            hide=self.get_hide(),
            indicator=copy.copy(self.get_indicator()),
            synthetic_offset=self.get_synthetic_offset(),
            tag=self.get_tag(),
        )
        return new

    def __eq__(self, argument) -> bool:
        if not isinstance(argument, Wrapper):
            return False
        if self.get_annotation() != argument.get_annotation():
            return False
        if self.get_component() != argument.get_component():
            return False
        if self.get_context_name() != argument.get_context_name():
            return False
        if self.get_deactivate() != argument.get_deactivate():
            return False
        if self.get_hide() != argument.get_hide():
            return False
        if self.get_indicator() != argument.get_indicator():
            return False
        if self.get_synthetic_offset() != argument.get_synthetic_offset():
            return False
        if self.get_tag() != argument.get_tag():
            return False
        return True

    def __hash__(self) -> int:
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        parameters = f"""
            annotation={self.get_annotation()!r},
            context_name={self.get_context_name()!r},
            deactivate={self.get_deactivate()!r},
            direction={self.get_direction()!r},
            hide={self.get_hide()!r},
            indicator={self.get_indicator()!r},
            synthetic_offset={self.get_synthetic_offset()!r},
            tag={self.get_tag()!r}
        """
        parameters = " ".join(parameters.split())
        return f"{type(self).__name__}({parameters})"

    def _bind_component(
        self,
        component: _score.Component,
        *,
        check_duplicate_indicator: bool = False,
    ) -> None:
        indicator = self.unbundle_indicator()
        if getattr(indicator, "context", None) is not None:
            if check_duplicate_indicator is True:
                self._check_duplicate_indicator(component)
            self._unbind_component()
            self._component = component
            self._update_effective_context()
            if getattr(indicator, "mutates_offsets_in_seconds", False):
                self._component._update_later(offsets_in_seconds=True)
        component._wrappers.append(self)

    def _bind_effective_context(
        self,
        correct_effective_context: _score.Context | None,
    ) -> None:
        if correct_effective_context is not None:
            assert isinstance(correct_effective_context, _score.Context)
        self._unbind_effective_context()
        if correct_effective_context is not None:
            if self not in correct_effective_context._dependent_wrappers:
                correct_effective_context._dependent_wrappers.append(self)
        self._effective_context = correct_effective_context
        self._update_effective_context()
        indicator = self.unbundle_indicator()
        if correct_effective_context is not None:
            if getattr(indicator, "mutates_offsets_in_seconds", False):
                correct_effective_context._update_later(offsets_in_seconds=True)

    def _check_duplicate_indicator(self, component: _score.Component) -> None:
        if self.get_deactivate() is True:
            return
        indicator = self.unbundle_indicator()
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
            or wrapper.get_context_name() is None
            or wrapper.get_deactivate() is True
            or wrapper.start_offset() != self.start_offset()
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
        for parent in wrapper.get_component()._get_parentage():
            if hasattr(parent, "_lilypond_type"):
                wrapper_context = parent
                break
        if wrapper.unbundle_indicator() == indicator and context is not wrapper_context:
            return
        assert isinstance(wrapper_context, _score.Context)
        message = f"\n\nCan not attach ...\n\n{repr(self)}\n\n..."
        message += f" to {repr(component)}"
        # message += f" in {getattr(context, 'name', None)} because ..."
        assert context is not None
        message += f" in {context.get_name()} because ..."
        message += f"\n\n{repr(wrapper)}\n\n"
        message += "... is already attached"
        if component is wrapper.get_component():
            message += " to the same leaf."
        else:
            message += f" to {repr(wrapper.get_component())}"
            message += f" in {wrapper_context.get_name()}."
        message += "\n"
        raise _exceptions.PersistentIndicatorError(message)

    def _detach(self) -> "Wrapper":
        self._unbind_component()
        self._unbind_effective_context()
        return self

    @staticmethod
    def _find_correct_effective_context(
        component: _score.Component | None,
        context_name: str,
    ) -> _score.Context | None:
        assert isinstance(component, _score.Component), repr(component)
        assert isinstance(context_name, str), repr(context_name)
        abjad = importlib.import_module("abjad")
        context = getattr(abjad, context_name, None)
        candidate = None
        parentage = _parentage.Parentage(component)
        if context is not None:
            assert issubclass(context, _score.Context), repr(context)
            candidate = parentage.get(context)
        else:
            for component in parentage:
                assert component is not None
                # if getattr(component, "name", None) == context_name:
                if (
                    hasattr(component, "get_name")
                    and component.get_name() == context_name
                ):
                    candidate = component
                    break
                # if getattr(component, "lilypond_type", None) == context_name:
                if hasattr(component, "get_lilypond_type") and (
                    component.get_lilypond_type() == context_name
                ):
                    candidate = component
                    break
        if candidate.__class__.__name__ == "Voice":
            for component in reversed(parentage):
                if not component.__class__.__name__ == "Voice":
                    continue
                assert isinstance(component, _score.Voice)
                assert isinstance(candidate, _score.Voice)
                if component.get_name() == candidate.get_name():
                    candidate = component
                    break
        assert isinstance(candidate, _score.Context | None), repr(candidate)
        return candidate

    def _get_effective_context(self) -> _score.Context | None:
        if self.get_component() is not None:
            _updatelib._update_now(self.get_component(), indicators=True)
        return self._effective_context

    def _unbind_component(self) -> None:
        component = self.get_component()
        if component is not None and id(self) in [id(_) for _ in component._wrappers]:
            component._wrappers.remove(self)
        self._component = None

    def _unbind_effective_context(self) -> None:
        if (
            self._effective_context is not None
            and self in self._effective_context._dependent_wrappers
        ):
            self._effective_context._dependent_wrappers.remove(self)
        self._effective_context = None

    def _update_effective_context(self) -> None:
        context_name = self.get_context_name()
        if context_name is not None:
            correct_effective_context = self._find_correct_effective_context(
                self.get_component(),
                context_name,
            )
        else:
            correct_effective_context = None
        if self._effective_context is not correct_effective_context:
            self._bind_effective_context(correct_effective_context)
        if correct_effective_context is not None:
            if self not in correct_effective_context._dependent_wrappers:
                correct_effective_context._dependent_wrappers.append(self)

    def get_annotation(self) -> str | None:
        """
        Gets annotation with which indicator is attached to component.
        """
        return self._annotation

    def get_component(self) -> _score.Component | None:
        """
        Gets component to which indicator is attached.
        """
        return self._component

    def get_context_name(self) -> str | None:
        """
        Gets name of context at which indicator is attached to component.
        """
        return self._context_name

    def get_deactivate(self) -> bool:
        """
        Is true when indicator is deactivated in LilyPond output.
        """
        return self._deactivate

    def set_deactivate(self, argument: bool) -> None:
        """
        Sets wrapper ``deactivate`` flag.
        """
        assert isinstance(argument, bool), repr(argument)
        self._deactivate = argument

    # TODO: typehint
    def get_direction(self):
        """
        Gets direction of indicator.
        """
        return self._direction

    def get_hide(self) -> bool:
        """
        Is true when indcator does not appear in LilyPond output.
        """
        return self._hide

    def get_indicator(self) -> typing.Any:
        """
        Gets indicator.
        """
        return self._indicator

    def is_bundled(self) -> bool:
        """
        Is true when indicator is bundled.
        """
        return isinstance(self.get_indicator(), _tweaks.Bundle)

    def leaked_start_offset(self) -> _duration.Offset:
        r"""
        Gets start offset and checks to see whether indicator leaks to the
        right. This is either the wrapper's synthetic offset (if set); or the
        START offset of the wrapper's component (if indicator DOES NOT leak);
        or else the STOP offset of the wrapper's component (if indicator DOES
        leak).

        ..  container:: example

            Start- and stop-text-spans attach to the same leaf. But
            stop-text-span leaks to the right:

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

            Start offset and leaked start offset are the same for
            start-text-span:

            >>> wrapper = abjad.get.wrapper(voice[0], abjad.StartTextSpan)
            >>> wrapper.start_offset(), wrapper.leaked_start_offset()
            (Offset((0, 1)), Offset((0, 1)))

            Start offset and leaked start offset differ for stop-text-span:

            >>> wrapper = abjad.get.wrapper(voice[0], abjad.StopTextSpan)
            >>> wrapper.start_offset(), wrapper.leaked_start_offset()
            (Offset((0, 1)), Offset((1, 2)))

        """
        synthetic_offset = self.get_synthetic_offset()
        if synthetic_offset is not None:
            return synthetic_offset
        indicator = self.unbundle_indicator()
        component = self.get_component()
        assert isinstance(component, _score.Component)
        if not getattr(indicator, "leak", False):
            return component._get_timespan().start_offset
        else:
            return component._get_timespan().stop_offset

    def site_adjusted_start_offset(self) -> _duration.Offset:
        r"""
        Gets site-adjusted start offset. Indicators with site equal to
        ``absolute_after``, ``after`` or ``closing`` give a site-adjusted start
        offset equal to the stop offset of the wrapper's component. Indicators
        with any other site give a site-adjusted start offset equal to the
        start offset of the wrapper's component. This is the usual case, and
        means that site-adjusted start offset equals vanilla start offset. But
        if ``synthetic_offset`` is set then ``synthetic_offset`` is returned
        directly without examining the format site at all.

        ..  container:: example

            >>> staff = abjad.Staff("c'4")
            >>> abjad.attach(abjad.Ottava(-1, site="before"), staff[0])
            >>> abjad.attach(abjad.Ottava(0, site="after"), staff[0])
            >>> for wrapper in abjad.get.wrappers(staff[0], abjad.Ottava):
            ...     wrapper.get_indicator(), wrapper.site_adjusted_start_offset()
            (Ottava(n=-1, site='before'), Offset((0, 1)))
            (Ottava(n=0, site='after'), Offset((1, 4)))

        """
        synthetic_offset = self.get_synthetic_offset()
        if synthetic_offset is not None:
            return synthetic_offset
        site = getattr(self.unbundle_indicator(), "site", "before")
        component = self.get_component()
        assert component is not None
        if site in ("absolute_after", "after", "closing"):
            return component._get_timespan().stop_offset
        else:
            return component._get_timespan().start_offset

    def start_offset(self) -> _duration.Offset:
        """
        Gets start offset. This is either the wrapper's synthetic offset or the
        start offset of the wrapper's component.
        """
        synthetic_offset = self.get_synthetic_offset()
        if synthetic_offset is not None:
            return synthetic_offset
        component = self.get_component()
        assert isinstance(component, _score.Component)
        return component._get_timespan().start_offset

    def get_synthetic_offset(self) -> _duration.Offset | None:
        """
        Gets synthetic offset.
        """
        return self._synthetic_offset

    def get_tag(self) -> _tag.Tag:
        """
        Gets wrapper tag.
        """
        return self._tag

    def set_tag(self, argument: _tag.Tag) -> None:
        """
        Sets wrapper tag.
        """
        assert isinstance(argument, _tag.Tag), repr(argument)
        self._tag = argument

    def unbundle_indicator(self) -> typing.Any:
        """
        Unbundles indicator.
        """
        if self.is_bundled():
            indicator = self.get_indicator().indicator
        else:
            indicator = self.get_indicator()
        return indicator
