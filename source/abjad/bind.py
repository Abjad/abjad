"""
Functions to bind indicators to score components.
"""

import enum
import typing

from . import duration as _duration
from . import enums as _enums
from . import exceptions as _exceptions
from . import score as _score
from . import tag as _tag
from . import tweaks as _tweaks
from . import wrapper as _wrapper


def _before_attach(
    indicator: typing.Any,
    context: str | None,
    deactivate: bool,
    hide: bool,
    synthetic_offset: _duration.Offset | None,
    component: _score.Component,
) -> None:
    if getattr(indicator, "temporarily_do_not_check", False) is True:
        return
    if hasattr(indicator, "allowable_sites"):
        if indicator.site not in component._allowable_sites:
            message = f"\n  {indicator!r}"
            message += f"\n  Can not attach to {component.__class__.__name__}."
            message += f"\n  {component.__class__.__name__} allows only "
            message += ", ".join(component._allowable_sites)
            message += " sites."
            raise Exception(message)
    if not hasattr(indicator, "context"):
        return
    if getattr(indicator, "find_context_on_attach", False) is True:
        the_context = context or indicator.context
        if the_context is not None:
            context_ = _wrapper.Wrapper._find_correct_effective_context(
                component, the_context
            )
            if context_ is None:
                message = f"\n    {indicator} requires {the_context} context;"
                message += f"\n    can not find {the_context}"
                message += f" in parentage of {component!r}."
                raise _exceptions.MissingContextError(message)
    if getattr(indicator, "nestable_spanner", False) is True:
        return
    if deactivate is True:
        return
    if synthetic_offset is not None:
        return
    for wrapper in component._get_wrappers():
        if not isinstance(wrapper.unbundle_indicator(), type(indicator)):
            continue
        if getattr(indicator, "leak", None) != getattr(
            wrapper.unbundle_indicator(), "leak", None
        ):
            continue
        if indicator != wrapper.unbundle_indicator():
            if (
                getattr(indicator, "allow_multiple_with_different_values", False)
                is True
            ):
                continue
            if hide != wrapper.get_hide():
                continue
            if getattr(indicator, "site", None) != getattr(
                wrapper.unbundle_indicator(), "site", None
            ):
                continue
        classname = type(component).__name__
        message = f"attempting to attach conflicting indicator to {classname}:"
        message += "\n  Already attached:"
        message += f"\n    {wrapper.unbundle_indicator()!r}"
        message += "\n  Attempting to attach:"
        message += f"\n    {indicator!r}"
        raise _exceptions.PersistentIndicatorError(message)


def _unsafe_attach(
    indicator: typing.Any,
    component,
    *,
    check_duplicate_indicator: bool = False,
    context: str | None = None,
    deactivate: bool = False,
    direction: _enums.Vertical | None = None,
    do_not_test: bool = False,
    hide: bool = False,
    synthetic_offset: _duration.Offset | None = None,
    tag: _tag.Tag | None = None,
) -> None:
    if isinstance(indicator, _tweaks.Bundle):
        nonbundle_indicator = indicator.indicator
    else:
        nonbundle_indicator = indicator
    assert not isinstance(nonbundle_indicator, _tweaks.Bundle)
    if isinstance(nonbundle_indicator, _tag.Tag):
        message = "use the tag=None keyword instead of attach():\n"
        message += f"   {repr(indicator)}"
        raise Exception(message)
    assert isinstance(component, _score.Component), repr(component)
    if tag is not None and not isinstance(tag, _tag.Tag):
        raise Exception(f"must be be tag: {repr(tag)}")
    assert nonbundle_indicator is not None, repr(nonbundle_indicator)
    assert isinstance(component, _score.Component), repr(component)
    grace_prototype = (_score.AfterGraceContainer, _score.BeforeGraceContainer)
    if context is not None and isinstance(nonbundle_indicator, grace_prototype):
        raise Exception(f"set context only for indicators, not {indicator!r}.")
    if deactivate is True and tag is None:
        raise Exception("tag must exist when deactivate is true.")
    if hasattr(nonbundle_indicator, "_attachment_test_all") and not do_not_test:
        result = nonbundle_indicator._attachment_test_all(component)
        if result is not True:
            assert isinstance(result, list), repr(result)
            result = ["  " + _ for _ in result]
            message = f"{nonbundle_indicator!r}._attachment_test_all():"
            result.insert(0, message)
            message = "\n".join(result)
            raise Exception(message)
    if isinstance(nonbundle_indicator, grace_prototype):
        if not isinstance(component, _score.Leaf):
            raise Exception("grace containers attach to single leaf only.")
        nonbundle_indicator._attach(component)
        return None
    if isinstance(component, _score.Container):
        acceptable = False
        if isinstance(
            nonbundle_indicator, dict | str | enum.Enum | _tag.Tag | _wrapper.Wrapper
        ):
            acceptable = True
        if getattr(nonbundle_indicator, "can_attach_to_containers", False):
            acceptable = True
        if not acceptable:
            message = f"can not attach {indicator!r} to containers: {component!r}"
            raise Exception(message)
    elif not isinstance(component, _score.Leaf):
        message = f"indicator {indicator!r} must attach to leaf, not {component!r}."
        raise Exception(message)
    annotation = None
    if isinstance(indicator, _wrapper.Wrapper):
        annotation = indicator.get_annotation()
        context = context or indicator.get_context_name()
        deactivate = deactivate or indicator.get_deactivate()
        hide = hide or indicator.get_hide()
        synthetic_offset = synthetic_offset or indicator.get_synthetic_offset()
        tag = tag or indicator.get_tag()
        indicator._detach()
        indicator = indicator.get_indicator()
    if hasattr(nonbundle_indicator, "context"):
        context = context or nonbundle_indicator.context
    if tag is None:
        tag = _tag.Tag()
    _wrapper.Wrapper(
        annotation=annotation,
        check_duplicate_indicator=check_duplicate_indicator,
        component=component,
        context_name=context,
        deactivate=deactivate,
        direction=direction,
        hide=hide,
        indicator=indicator,
        synthetic_offset=synthetic_offset,
        tag=tag,
    )


# TODO: remove abjad.Wrapper.annotation;
#       store annotations in abjad.Component._annotations dictionary instead;
#       annotations do not need context_name, hide, synthetic_offset, etc.
def annotate(component: _score.Component, key: str, value: object) -> None:
    r"""
    Annotates ``component`` with ``key`` equal to ``value``.

    ..  container:: example

        Annotations do not affect LilyPond output.

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.annotate(staff[0], "motive_number", 6)
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

        >>> abjad.get.annotation(staff[0], "motive_number")
        6

    """
    assert isinstance(component, _score.Component), repr(component)
    assert isinstance(key, str), repr(key)
    _wrapper.Wrapper(annotation=key, component=component, indicator=value)


def attach(
    indicator: typing.Any,
    component: _score.Component,
    *,
    check_duplicate_indicator: bool = False,
    # TODO: change `context` to `context_name`
    context: str | None = None,
    deactivate: bool = False,
    # TODO: remove _enums.Vertical and consolidate direction in some other way
    direction: _enums.Vertical | None = None,
    do_not_test: bool = False,
    hide: bool = False,
    synthetic_offset: _duration.Offset | None = None,
    tag: _tag.Tag | None = None,
) -> None:
    r"""
    Attaches ``indicator`` to ``component``.

    ..  container:: example

        The class of ``component`` is almost always a leaf. (A small number of
        indicators can attach to both leaves and containers.) Acceptable types
        of ``indicator``:

        ::

            * indicator
            * abjad.Wrapper
            * abjad.BeforeGraceContainer (DEPRECATED)
            * abjad.AfterGraceContainer  (DEPRECATED)

    ..  container:: example

        Attaches articulation to last note in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> articulation = abjad.Articulation(">")
        >>> abjad.attach(articulation, staff[-1])
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

        The ``check_duplicate_indicator=False`` keyword. Consider the case of a
        score with two staves. In the usual case, it is necessary to attach a
        metronome mark to the first note of only one of the two staves:

        >>> staff_1 = abjad.Staff("c''4 d''4 e''4 f''4")
        >>> staff_2 = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> score = abjad.Score([staff_1, staff_2])
        >>> metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 52)
        >>> abjad.attach(metronome_mark, staff_1[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo 4=52
                    c''4
                    d''4
                    e''4
                    f''4
                }
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>

        But what should happen when a conflicting metronome mark is attached at
        the same moment in a different context? Abjad allows this behavior, but
        it is not clear what it should mean to have two metronome marks in
        effect at the same time. Set ``check_duplicate_indicators=True`` to
        raise an exception instead.

    ..  container:: example

        The ``context=None`` keyword. Indicators that affect many notes, rests
        or chords in a row define the context at which they take effect. Clefs
        effect all notes on a staff, for example, which is why attaching a clef
        to the first note in a staff effects all the others:

        >>> clef = abjad.Clef("alto")
        >>> clef.context
        'Staff'

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(clef, staff[0])
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

        >>> for leaf in abjad.select.leaves(staff):
        ...     leaf, abjad.get.effective_indicator(leaf, abjad.Clef)
        ...
        (Note("c'4"), Clef(name='alto'))
        (Note("d'4"), Clef(name='alto'))
        (Note("e'4"), Clef(name='alto'))
        (Note("f'4"), Clef(name='alto'))

        This example sets ``context="MusicStaff"`` to show that the alto clef
        governs all notes in a custom staff context (rather than the default
        staff context):

        >>> voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
        >>> staff = abjad.Staff([voice], name="MusicStaff")
        >>> clef = abjad.Clef("alto")
        >>> abjad.attach(clef, voice[0], context="MusicStaff")
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
        ...     leaf, abjad.get.effective_indicator(leaf, abjad.Clef)
        ...
        (Note("c'4"), Clef(name='alto'))
        (Note("d'4"), Clef(name='alto'))
        (Note("e'4"), Clef(name='alto'))
        (Note("f'4"), Clef(name='alto'))

    ..  container:: example

        If multiple contexted indicators are attached at the same offset then
        ``abjad.attach()`` raises ``abjad.PersistentIndicatorError`` if all
        indicators are active. But simultaneous contexted indicators are
        allowed if only one is active (and all others are inactive):

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

        Active indicator is always effective when competing inactive indicators
        are present:

        >>> for note in staff:
        ...     clef = abjad.get.effective_indicator(staff[0], abjad.Clef)
        ...     note, clef
        ...
        (Note("c'4"), Clef(name='treble'))
        (Note("d'4"), Clef(name='treble'))
        (Note("e'4"), Clef(name='treble'))
        (Note("f'4"), Clef(name='treble'))

        But a lone inactivate indicator is effective when no active indicator
        is present. Note that ``tag`` must be an ``abjad.Tag`` when
        ``deactivate=True``:


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
        ...     clef = abjad.get.effective_indicator(staff[0], abjad.Clef)
        ...     note, clef
        ...
        (Note("c'4"), Clef(name='alto'))
        (Note("d'4"), Clef(name='alto'))
        (Note("e'4"), Clef(name='alto'))
        (Note("f'4"), Clef(name='alto'))

    """
    if isinstance(indicator, _tweaks.Bundle):
        nonbundle_indicator = indicator.indicator
    else:
        nonbundle_indicator = indicator
    assert not isinstance(nonbundle_indicator, _tweaks.Bundle)
    assert nonbundle_indicator is not None, repr(nonbundle_indicator)
    assert isinstance(component, _score.Component), repr(component)
    assert isinstance(hide, bool), repr(hide)
    _before_attach(
        nonbundle_indicator,
        context,
        deactivate,
        hide,
        synthetic_offset,
        component,
    )
    _unsafe_attach(
        indicator,
        component,
        check_duplicate_indicator=check_duplicate_indicator,
        context=context,
        deactivate=deactivate,
        direction=direction,
        do_not_test=do_not_test,
        hide=hide,
        synthetic_offset=synthetic_offset,
        tag=tag,
    )


def detach(indicator, component: _score.Component, *, by_id: bool = False) -> tuple:
    r"""
    Detaches indicators equals to ``indicator`` from ``component``. Returns
    tuple of zero or more detached items.

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

        Set ``by_id`` to true to detach exact ``indicator`` from ``component``
        (rather than detaching all indicatorslequal to ``indicator``). The use
        of ``by_id`` is motivated by the following.

        Consider the three document-specifier markups below:

        >>> markup_1 = abjad.Markup(r"\markup tutti")
        >>> markup_2 = abjad.Markup(r"\markup { with the others }")
        >>> markup_3 = abjad.Markup(r"\markup { with the others }")

        Markups two and three compare equal:

        >>> markup_2 == markup_3
        True

        But document-tagging like this makes sense for score and two diferent parts:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> tag = abjad.Tag(string="+SCORE")
        >>> abjad.attach(markup_1, staff[0], direction=abjad.UP, tag=tag)
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

        The question is then how to detach just one of the two markups that
        compare equal to each other?

        Passing in one of the markup objects directory doesn't work. This is
        because detach tests for equality to input argument:

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
        >>> tag = abjad.Tag(string="+SCORE")
        >>> abjad.attach(markup_1, staff[0], direction=abjad.UP, tag=tag)
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

        This time we set ``by_id`` to true. Now detach checks the exact id of
        its input argument (rather than just testing for equality). This gives
        us what we want:

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

        REGRESSION. Attach-detach-attach pattern works correctly when detaching
        wrappers:

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
        >>> wrappers = abjad.detach(wrapper, wrapper.get_component())
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

    """
    assert isinstance(component, _score.Component), repr(component)
    assert isinstance(by_id, bool), repr(by_id)
    after_grace_container = None
    before_grace_container = None
    if isinstance(indicator, type):
        if "AfterGraceContainer" in indicator.__name__:
            assert isinstance(component, _score.Leaf)
            after_grace_container = component._after_grace_container
        elif "BeforeGraceContainer" in indicator.__name__:
            assert isinstance(component, _score.Leaf)
            before_grace_container = component._before_grace_container
        else:
            assert hasattr(component, "_wrappers")
            result = []
            for wrapper in component._wrappers[:]:
                if isinstance(wrapper, indicator):
                    component._wrappers.remove(wrapper)
                    result.append(wrapper)
                elif isinstance(wrapper.unbundle_indicator(), indicator):
                    wrapper._detach()
                    result.append(wrapper.get_indicator())
            return tuple(result)
    else:
        if "AfterGraceContainer" in indicator.__class__.__name__:
            assert isinstance(component, _score.Leaf)
            after_grace_container = component._after_grace_container
        elif "BeforeGraceContainer" in indicator.__class__.__name__:
            assert isinstance(component, _score.Leaf)
            before_grace_container = component._before_grace_container
        else:
            assert hasattr(component, "_wrappers")
            result = []
            for wrapper in component._wrappers[:]:
                if wrapper is indicator:
                    wrapper._detach()
                    result.append(wrapper)
                elif wrapper.unbundle_indicator() == indicator:
                    if by_id is True and id(indicator) != id(
                        wrapper.unbundle_indicator()
                    ):
                        pass
                    else:
                        wrapper._detach()
                        result.append(wrapper.get_indicator())
            return tuple(result)
    items: list[typing.Any] = []
    if after_grace_container is not None:
        items.append(after_grace_container)
    if before_grace_container is not None:
        items.append(before_grace_container)
    if by_id is True:
        items = [_ for _ in items if id(_) == id(indicator)]
    for item in items:
        item._detach()
    return tuple(items)
