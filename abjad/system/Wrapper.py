import copy
import typing

from .FormatSpecification import FormatSpecification
from .LilyPondFormatManager import LilyPondFormatManager
from .StorageFormatManager import StorageFormatManager
from .Tag import Tag


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
        from abjad.core.Component import Component
        from abjad.utilities.Offset import Offset

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
        import abjad

        if self.context is None:
            return None
        context = getattr(abjad, self.context, self.context)
        candidate = None
        parentage = abjad.inspect(self.component).parentage()
        if isinstance(context, type):
            for component in parentage:
                if not isinstance(component, abjad.Context):
                    continue
                if isinstance(component, context):
                    candidate = component
                    break
        elif isinstance(context, str):
            for component in parentage:
                if not isinstance(component, abjad.Context):
                    continue
                if component.name == context or component.lilypond_type == context:
                    candidate = component
                    break
        else:
            raise TypeError("must be context or string: {context!r}.")
        if isinstance(candidate, abjad.Voice):
            for component in reversed(parentage):
                if not isinstance(component, abjad.Voice):
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
        import abjad

        if self.deactivate is True:
            return
        prototype = type(self.indicator)
        command = getattr(self.indicator, "command", None)
        wrapper = abjad.inspect(component).effective_wrapper(
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
        context = abjad.inspect(component).parentage().get(abjad.Context)
        parentage = abjad.inspect(wrapper.component).parentage()
        wrapper_context = parentage.get(abjad.Context)
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
        raise abjad.PersistentIndicatorError(message)

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
        from abjad.top.inspect import inspect

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
        from abjad.top.inspect import inspect

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
