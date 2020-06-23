import types
import typing

from . import enums
from .formatting import StorageFormatManager

_lilypond_parsers_by_language: typing.Dict = {}


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
    import abjad

    if isinstance(attachable, abjad.Tag):
        message = "use the tag=None keyword instead of attach():\n"
        message += f"   {repr(attachable)}"
        raise Exception(message)

    if tag is not None and not isinstance(tag, abjad.Tag):
        raise Exception(f"must be be tag: {repr(tag)}")

    if isinstance(attachable, abjad.Multiplier):
        message = "use the Leaf.multiplier property to multiply leaf duration."
        raise Exception(message)

    assert attachable is not None, repr(attachable)
    assert target is not None, repr(target)

    grace_prototype = (abjad.AfterGraceContainer, abjad.BeforeGraceContainer)

    if context is not None and isinstance(attachable, grace_prototype):
        message = f"set context only for indicators, not {attachable!r}."
        raise Exception(message)

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

    if isinstance(attachable, grace_prototype):
        if not isinstance(target, abjad.Leaf):
            raise Exception("grace containers attach to single leaf only.")
        attachable._attach(target)
        return

    assert isinstance(target, abjad.Component), repr(target)

    if isinstance(target, abjad.Container):
        acceptable = False
        if isinstance(attachable, (dict, str, abjad.Tag, abjad.Wrapper)):
            acceptable = True
        if getattr(attachable, "_can_attach_to_containers", False):
            acceptable = True
        if not acceptable:
            message = "can not attach {!r} to containers: {!r}"
            message = message.format(attachable, target)
            raise Exception(message)
    elif not isinstance(target, abjad.Leaf):
        message = "indicator {!r} must attach to leaf instead, not {!r}."
        message = message.format(attachable, target)
        raise Exception(message)

    component = target
    assert isinstance(component, abjad.Component)

    annotation = None
    if isinstance(attachable, abjad.Wrapper):
        annotation = attachable.annotation
        context = context or attachable.context
        deactivate = deactivate or attachable.deactivate
        synthetic_offset = synthetic_offset or attachable.synthetic_offset
        tag = tag or attachable.tag
        attachable._detach()
        attachable = attachable.indicator

    if hasattr(attachable, "context"):
        context = context or attachable.context

    wrapper_ = abjad.Wrapper(
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
    import abjad

    assert target is not None
    after_grace_container = None
    before_grace_container = None
    inspector = abjad.inspect(target)
    if isinstance(argument, type):
        if argument == abjad.AfterGraceContainer:
            after_grace_container = inspector.after_grace_container()
        elif argument == abjad.BeforeGraceContainer:
            before_grace_container = inspector.before_grace_container()
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
        if isinstance(argument, abjad.AfterGraceContainer):
            after_grace_container = inspector.after_grace_container()
        elif isinstance(argument, abjad.BeforeGraceContainer):
            before_grace_container = inspector.before_grace_container()
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


def f(argument, strict=None):
    r"""
    Formats ``argument`` and prints result.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup('Allegro', direction=abjad.Up)
        >>> markup = markup.with_color('blue')
        >>> abjad.attach(markup, staff[0])
        >>> for leaf in staff:
        ...     abjad.attach(abjad.Articulation('.'), leaf)
        ...
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            - \staccato
            ^ \markup {
                \with-color
                    #blue
                    Allegro
                }
            d'4
            - \staccato
            e'4
            - \staccato
            f'4
            - \staccato
        }

        >>> abjad.show(staff) # doctest: +SKIP

    """
    import abjad

    if strict is not None:
        assert isinstance(strict, int), repr(strict)
    if hasattr(argument, "_publish_storage_format"):
        string = StorageFormatManager(argument).get_storage_format()
    else:
        string = format(argument, "lilypond")
    realign = None
    if isinstance(strict, int):
        string = abjad.LilyPondFormatManager.align_tags(string, strict)
        realign = strict
    string = abjad.LilyPondFormatManager.left_shift_tags(string, realign=realign)
    print(string)


def graph(argument, format_="pdf", layout="dot",) -> None:
    r"""
    Graphs ``argument``.

    ..  container:: example

        Graphs staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.graph(staff) # doctest: +SKIP

        ..  docs::

            >>> print(format(staff.__graph__(), 'graphviz'))
            digraph G {
                graph [style=rounded];
                node [fontname=Arial,
                    shape=none];
                Staff_0 [label=<
                    <TABLE BORDER="2" CELLPADDING="5">
                        <TR>
                            <TD BORDER="0">Staff</TD>
                        </TR>
                    </TABLE>>,
                    margin=0.05,
                    style=rounded];
                subgraph Staff {
                    graph [color=grey75,
                        penwidth=2];
                    Note_0 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">c'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_1 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">d'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_2 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">e'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_3 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">f'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                }
                Staff_0 -> Note_0;
                Staff_0 -> Note_1;
                Staff_0 -> Note_2;
                Staff_0 -> Note_3;
            }

    ..  container:: example

        Graphs rhythm tree:

        >>> rtm_syntax = '(3 ((2 (2 1)) 2))'
        >>> parser = abjad.rhythmtrees.RhythmTreeParser()
        >>> rhythm_tree = parser(rtm_syntax)[0]
        >>> abjad.graph(rhythm_tree) # doctest: +SKIP

        ..  docs::

            >>> print(format(rhythm_tree.__graph__(), 'graphviz'))
            digraph G {
                graph [bgcolor=transparent,
                    truecolor=true];
                node_0 [label="3",
                    shape=triangle];
                node_1 [label="2",
                    shape=triangle];
                node_2 [label="2",
                    shape=box];
                node_3 [label="1",
                    shape=box];
                node_4 [label="2",
                    shape=box];
                node_0 -> node_1;
                node_0 -> node_4;
                node_1 -> node_2;
                node_1 -> node_3;
            }

    Opens image in default image viewer.
    """
    import abjad.iox

    return abjad.iox.graph(argument, format_=format_, layout=layout,)


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
    import abjad

    return abjad.Inspection(client=client)


def iterate(client=None):
    r"""
    Makes iteration agent.

    ..  container:: example

        Iterates leaves:

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

        >>> for leaf in abjad.iterate(staff).leaves():
        ...     leaf
        ...
        Note("c'4")
        Note("e'4")
        Note("d'4")
        Note("f'4")

    """
    import abjad

    if client is not None:
        return abjad.Iteration(client=client)
    expression = abjad.Expression()
    expression = expression.iterate()
    return expression


def label(client=None, deactivate=None, tag=None):
    r"""
    Makes label agent or label expression.

    ..  container:: example

        Labels logical ties with start offsets:

        >>> staff = abjad.Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
        >>> abjad.label(staff).with_start_offsets(direction=abjad.Up)
        Duration(1, 1)

        >>> abjad.override(staff).text_script.staff_padding = 4
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextScript.staff-padding = #4
                \override TupletBracket.staff-padding = #0
            }
            {
                \times 2/3 {
                    c'4
                    ^ \markup { 0 }
                    d'4
                    ^ \markup { 1/6 }
                    e'4
                    ^ \markup { 1/3 }
                    ~
                }
                e'4
                ef'4
                ^ \markup { 3/4 }
            }

        See the ``Label`` API entry for many more examples.

    ..  container:: example expression

        Initializes positionally:

        >>> expression = abjad.label()
        >>> expression(staff)
        Label(client=<Staff{3}>)

        Initializes from keyword:

        >>> expression = abjad.label()
        >>> expression(client=staff)
        Label(client=<Staff{3}>)

        Makes label expression:

            >>> expression = abjad.label()
            >>> expression = expression.with_start_offsets()

        >>> staff = abjad.Staff(r"\times 2/3 { c'4 d'4 e'4 ~ } e'4 ef'4")
        >>> expression(staff)
        Duration(1, 1)

        >>> abjad.override(staff).text_script.staff_padding = 4
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 0
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextScript.staff-padding = #4
                \override TupletBracket.staff-padding = #0
            }
            {
                \times 2/3 {
                    c'4
                    ^ \markup { 0 }
                    d'4
                    ^ \markup { 1/6 }
                    e'4
                    ^ \markup { 1/3 }
                    ~
                }
                e'4
                ef'4
                ^ \markup { 3/4 }
            }

        See the ``Label`` API entry for many more examples.

    Returns label agent when ``client`` is not none.

    Returns label expression when ``client`` is none.
    """
    import abjad

    if client is not None:
        return abjad.Label(client=client, deactivate=deactivate, tag=tag)
    expression = abjad.Expression()
    expression = expression.label(tag=tag)
    return expression


def mutate(client):
    r"""
    Makes mutation agent.

    ..  container:: example

        Scales duration of last note notes in staff:

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

        >>> abjad.mutate(staff[-2:]).scale(abjad.Multiplier(3, 2))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                e'4
                d'4.
                f'4.
            }

    ..  container:: example

        Returns mutation agent:

        >>> abjad.mutate(staff[-2:])
        Mutation(client=Selection([Note("d'4."), Note("f'4.")]))

    """
    import abjad

    return abjad.Mutation(client=client)


def new(argument, *arguments, **keywords):
    r"""
    Makes new ``argument`` with positional ``arguments`` and ``keywords``.

    ..  container:: example

        Makes markup with new direction:

        >>> markup = abjad.Markup('Andante assai', direction=abjad.Up).italic()
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                ^ \markup {
                    \italic
                        "Andante assai"
                    }
                d'4
                e'4
                f'4
            }

        >>> markup = abjad.new(markup, direction=abjad.Down)
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                _ \markup {
                    \italic
                        "Andante assai"
                    }
                d'4
                e'4
                f'4
            }


    ..  container:: example

        REGRESSION. Can be used to set existing properties to none:

        >>> markup = abjad.Markup('Andante assai', direction=abjad.Up).italic()
        >>> abjad.f(markup)
        ^ \markup {
            \italic
                "Andante assai"
            }

        >>> markup = abjad.new(markup, direction=None)
        >>> abjad.f(markup)
        \markup {
            \italic
                "Andante assai"
            }

    Returns new object with type equal to that of ``argument``.
    """
    if argument is None:
        return argument
    manager = StorageFormatManager(argument)
    template_dict = manager.get_template_dict()
    if not (template_dict):
        message = "low-level class not equipped for new():\n"
        message += f"   {repr(argument)}"
        raise Exception(message)
    recursive_arguments = {}
    for key, value in keywords.items():
        if "__" in key:
            key, divider, subkey = key.partition("__")
            if key not in recursive_arguments:
                recursive_arguments[key] = []
            pair = (subkey, value)
            recursive_arguments[key].append(pair)
            continue
        if key in template_dict or manager.signature_accepts_kwargs:
            template_dict[key] = value
        elif isinstance(getattr(argument, key, None), types.MethodType):
            method = getattr(argument, key)
            result = method(value)
            if isinstance(result, type(argument)):
                argument = result
                manager_ = StorageFormatManager(argument)
                template_dict.update(manager_.get_template_dict())
        else:
            message = f"{type(argument)} has no key {key!r}."
            raise KeyError(message)
    for key, pairs in recursive_arguments.items():
        recursed_object = getattr(argument, key)
        if recursed_object is None:
            continue
        recursive_template_dict = dict(pairs)
        recursed_object = new(recursed_object, **recursive_template_dict)
        if key in template_dict:
            template_dict[key] = recursed_object
    positional_values = []
    for name in manager.signature_positional_names:
        if name in template_dict:
            positional_values.append(template_dict.pop(name))
    # _positional_arguments_name used, for example, in rhythm-makers
    positional_name = getattr(argument, "_positional_arguments_name", None)
    if positional_name is not None:
        assert isinstance(positional_name, str), repr(positional_name)
        positional_values_ = getattr(argument, positional_name)
        positional_values.extend(positional_values_)
    if arguments == (None,):
        positional_values = []
    elif arguments != ():
        positional_values = list(arguments)
    result = type(argument)(*positional_values, **template_dict)
    for name in getattr(argument, "_private_attributes_to_copy", []):
        value = getattr(argument, name, None)
        setattr(result, name, value)
    return result


def override(argument):
    r"""
    Makes LilyPond grob name manager.

    ..  container:: example

        Overrides staff symbol color:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.override(staff).staff_symbol.color = 'red'
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override StaffSymbol.color = #red
            }
            {
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Specify grob context like this:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.override(staff[0]).staff.staff_symbol.color = 'blue'
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override Staff.StaffSymbol.color = #blue
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Returns LilyPond grob name manager:

        >>> staff = abjad.Staff("c'4 e' d' f'")
        >>> abjad.override(staff)
        LilyPondGrobNameManager()

    """
    import abjad

    if getattr(argument, "_overrides", None) is None:
        manager = abjad.lilypondnames.LilyPondGrobNameManager()
        argument._overrides = manager
    return argument._overrides


def parse(string, language="english"):
    r"""
    Parses LilyPond ``string``.

    ..  container:: example

        Parses LilyPond string with English note names:

        >>> container = abjad.parse("{c'4 d'4 e'4 f'4}")
        >>> abjad.show(container) # doctest: +SKIP

    ..  container:: example

        Parses LilyPond string with Dutch note names:

        >>> container = abjad.parse(
        ...     "{c'8 des' e' fis'}",
        ...     language='nederlands',
        ...     )
        >>> abjad.show(container) # doctest: +SKIP

    Returns Abjad component.
    """
    from .parsers.parser import LilyPondParser
    from .parsers.reduced import parse_reduced_ly_syntax
    import abjad.rhythmtrees

    if string.startswith("abj:"):
        return parse_reduced_ly_syntax(string[4:])
    elif string.startswith("rtm:"):
        return abjad.rhythmtrees.parse_rtm_syntax(string[4:])
    if language not in _lilypond_parsers_by_language:
        parser = LilyPondParser(default_language=language)
        _lilypond_parsers_by_language[language] = parser
    return _lilypond_parsers_by_language[language](string)


def persist(client):
    r"""
    Makes persistence manager.

    ..  container:: example

        Persists staff as LilyPond file:

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

        >>> abjad.persist(staff).as_ly() # doctest: +SKIP

    ..  container:: example

        Returns persistence agent:

        >>> abjad.persist(staff)
        PersistenceManager(client=Staff("c'4 e'4 d'4 f'4"))

    """
    import abjad

    return abjad.PersistenceManager(client)


def play(argument) -> None:
    """
    Plays ``argument``.

    ..  container:: example

        >>> note = abjad.Note("c'4")
        >>> abjad.play(note) # doctest: +SKIP

    Makes MIDI file.

    Appends ``.mid`` filename extension under Windows.

    Appends ``.midi`` filename extension under other operating systems.

    Opens MIDI file.
    """
    import abjad.iox

    return abjad.iox.play(argument)


def select(items=None, previous=None):
    r"""
    Selects ``items`` or makes select expression.

    ..  container:: example

        Selects first two notes in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> selection = abjad.select(staff[:2]).leaves(pitched=True)
        >>> for note in selection:
        ...     abjad.override(note).note_head.color = 'red'

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override NoteHead.color = #red
                c'4
                \once \override NoteHead.color = #red
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Returns selection agent:

        >>> abjad.select(staff)
        Selection([Staff("c'4 d'4 e'4 f'4")])

        >>> abjad.select()
        abjad.select()

    """
    import abjad

    if items is None:
        return abjad.Expression().select(previous=previous)
    return abjad.Selection(items=items, previous=previous)


def sequence(items=None, **keywords):
    r"""
    Makes sequence or sequence expression.

    ..  container:: example

        ..  container:: example

            Makes sequence:

            >>> abjad.sequence([1, 2, [3, [4]], 5])
            Sequence([1, 2, [3, [4]], 5])

        ..  container:: example expression

            Makes sequence expression:

            >>> expression = abjad.sequence()
            >>> expression([1, 2, [3, [4]], 5])
            Sequence([1, 2, [3, [4]], 5])

    ..  container:: example

        Flattens, reverses and slices sequence:

        ..  container:: example

            >>> sequence_ = abjad.sequence([1, 2, [3, [4]], 5])
            >>> sequence_
            Sequence([1, 2, [3, [4]], 5])

            >>> sequence_ = sequence_.flatten(depth=-1)
            >>> sequence_
            Sequence([1, 2, 3, 4, 5])

            >>> sequence_ = sequence_.reverse()
            >>> sequence_
            Sequence([5, 4, 3, 2, 1])

            >>> sequence_ = sequence_[-3:]
            >>> sequence_
            Sequence([3, 2, 1])

        ..  container:: example expression

            >>> expression = abjad.sequence()
            >>> expression = expression.flatten(depth=-1)
            >>> expression = expression.reverse()
            >>> expression = expression[-3:]
            >>> expression([1, 2, [3, [4]], 5])
            Sequence([3, 2, 1])

    Returns sequence when ``items`` is not none.

    Returns sequence expression when ``items`` is none.
    """
    import abjad

    if items is not None:
        return abjad.Sequence(items=items, **keywords)
    else:
        expression = abjad.Expression()
        expression = expression.sequence(**keywords)
        return expression


def setting(argument):
    r"""
    Makes LilyPond setting name manager.

    ..  container:: example

        Sets instrument name:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.setting(staff).instrument_name = abjad.Markup('Vn. I')
        >>> abjad.show(staff) # doctest: +SKIP


        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                instrumentName = \markup { "Vn. I" }
            }
            {
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Returns LilyPond setting name manager:

        >>> abjad.setting(staff)
        LilyPondSettingNameManager(('instrument_name', Markup(contents=['Vn. I'])))

    """
    import abjad

    if getattr(argument, "_lilypond_setting_name_manager", None) is None:
        manager = abjad.lilypondnames.LilyPondSettingNameManager()
        argument._lilypond_setting_name_manager = manager
    return argument._lilypond_setting_name_manager


def show(argument, return_timing=False, **keywords):
    r"""
    Shows ``argument``.

    ..  container:: example

        Shows note:

        >>> note = abjad.Note("c'4")
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4

    ..  container:: example

        Shows staff:

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

    Makes LilyPond input files and output PDF.

    Writes LilyPond input file and output PDF to Abjad output directory.

    Opens output PDF.

    Returns none when ``return_timing`` is false.

    Returns pair of ``abjad_formatting_time`` and ``lilypond_rendering_time``
    when ``return_timing`` is true.
    """
    import abjad.iox

    return abjad.iox.show(argument, return_timing=return_timing, **keywords)


def tweak(argument, *, deactivate=None, expression=None, literal=None, tag=None):
    r"""
    Makes LilyPond tweak manager.

    ..  container:: example

        Tweaks markup:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup('Allegro assai', direction=abjad.Up)
        >>> abjad.tweak(markup).color = 'red'
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup { "Allegro assai" }
                d'4
                e'4
                f'4
            }

        Survives copy:

        >>> import copy
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup('Allegro assai', direction=abjad.Up)
        >>> abjad.tweak(markup_1).color = 'red'
        >>> markup_2 = copy.copy(markup_1)
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup { "Allegro assai" }
                d'4
                e'4
                f'4
            }

        Survives dot-chaining:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup('Allegro assai', direction=abjad.Up)
        >>> abjad.tweak(markup).color = 'red'
        >>> markup = markup.italic()
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup {
                    \italic
                        "Allegro assai"
                    }
                d'4
                e'4
                f'4
            }

        Works for opposite-directed coincident markup:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup('Allegro assai ...', direction=abjad.Up)
        >>> abjad.tweak(markup_1).color = 'red'
        >>> abjad.attach(markup_1, staff[0])
        >>> markup_2 = abjad.Markup('... ma non troppo', direction=abjad.Down)
        >>> abjad.tweak(markup_2).color = 'blue'
        >>> abjad.tweak(markup_2).staff_padding = 4
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup { "Allegro assai ..." }
                - \tweak color #blue
                - \tweak staff-padding #4
                _ \markup { "... ma non troppo" }
                d'4
                e'4
                f'4
            }

        Ignored for same-directed coincident markup:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup('Allegro assai ...', direction=abjad.Up)
        >>> abjad.tweak(markup_1).color = 'red'
        >>> abjad.attach(markup_1, staff[0])
        >>> markup_2 = abjad.Markup('... ma non troppo', direction=abjad.Up)
        >>> abjad.tweak(markup_2).color = 'blue'
        >>> abjad.tweak(markup_2).staff_padding = 4
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #red
                ^ \markup { "Allegro assai ..." }
                - \tweak color #blue
                - \tweak staff-padding #4
                ^ \markup { "... ma non troppo" }
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Tweaks note-head:

        >>> staff = abjad.Staff("c'4 cs' d' ds'")
        >>> abjad.tweak(staff[1].note_head).color = 'red'
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \tweak color #red
                cs'4
                d'4
                ds'4
            }

        Tweaks grob aggregated to note-head:

        >>> staff = abjad.Staff("c'4 cs' d' ds'")
        >>> abjad.tweak(staff[1].note_head).accidental.color = 'red'
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \tweak Accidental.color #red
                cs'4
                d'4
                ds'4
            }

    ..  container:: example

        Tweaks can be tagged:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> dynamic = abjad.Dynamic("f")
        >>> abjad.tweak(dynamic, tag=abjad.Tag("RED")).color = "red"
        >>> abjad.attach(dynamic, staff[0])

        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            - \tweak color #red %! RED
            \f
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

        REGRESSION. Tweaked tags can be set multiple times:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> dynamic = abjad.Dynamic('f')
        >>> abjad.tweak(dynamic, tag=abjad.Tag("RED")).color = "red"
        >>> abjad.tweak(dynamic, tag=abjad.Tag("BLUE")).color = "blue"
        >>> abjad.attach(dynamic, staff[0])

        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            - \tweak color #blue %! BLUE
            \f
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

    ..  container:: example

        Returns LilyPond tweak manager:

        >>> abjad.tweak(markup_1)
        LilyPondTweakManager(('_literal', None), ('color', 'red'))

    ..  container:: example

        Tweak expressions work like this:

        >>> abjad.tweak('red').color
        LilyPondTweakManager(('_literal', None), ('color', 'red'))

        >>> abjad.tweak(6).Y_offset
        LilyPondTweakManager(('Y_offset', 6), ('_literal', None))

        >>> abjad.tweak(False).bound_details__left_broken__text
        LilyPondTweakManager(('_literal', None), ('bound_details__left_broken__text', False))

    """
    import abjad

    if tag is not None and not isinstance(tag, abjad.Tag):
        raise Exception(f"must be be tag: {repr(tag)}")

    constants = (enums.Down, enums.Left, enums.Right, enums.Up)
    prototype = (bool, int, float, str, tuple, abjad.Scheme)
    if expression is True or argument in constants or isinstance(argument, prototype):
        manager = abjad.LilyPondTweakManager(
            deactivate=deactivate, literal=literal, tag=tag
        )
        manager._pending_value = argument
        return manager
    if not hasattr(argument, "_tweaks"):
        name = type(argument).__name__
        raise NotImplementedError(f"{name} does not allow tweaks (yet).")
    if argument._tweaks is None:
        manager = abjad.LilyPondTweakManager(
            deactivate=deactivate, literal=literal, tag=tag
        )
        argument._tweaks = manager
    else:
        manager = argument._tweaks
        manager.__init__(deactivate=deactivate, literal=literal, tag=tag)
    return manager
