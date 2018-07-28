def attach(
    attachable,
    target,
    context=None,
    deactivate=None,
    synthetic_offset=None,
    tag=None,
    wrapper=None,
    ):
    r"""
    Attaches ``attachable`` to ``target``.
    
    First form attaches indicator ``attachable`` to single leaf ``target``.
    
    Second form attaches spanner ``attachable`` to leaf selection ``target``.

    Third for attaches grace container ``attachable`` to leaf ``target``.

    Fourth form attaches time signature ``attachable`` to measure ``target``.

    Fifth form attaches wrapper ``attachable`` to unknown (?) ``target``.

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
                -\accent
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
        ...     tag='+PARTS_1',
        ...     )
        >>> abjad.attach(
        ...     abjad.Clef('tenor'),
        ...     staff[0],
        ...     deactivate=True,
        ...     tag='+PARTS_2',
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \clef "treble"
            %@% \clef "alto" %! +PARTS_1
            %@% \clef "tenor" %! +PARTS_2
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
        ...     tag='+PARTS',
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

    assert attachable is not None, repr(attachable)
    assert target is not None, repr(target)

    nonindicator_prototype = (
        abjad.AfterGraceContainer,
        abjad.GraceContainer,
        abjad.Spanner,
        )

    if context is not None and isinstance(attachable, nonindicator_prototype):
        message = 'set context only for indicators, not {!r}.'
        message = message.format(attachable)
        raise Exception(message)

    if deactivate is True and tag is None:
        raise Exception(f'tag must exist when deactivate is true.')

    if hasattr(attachable, '_before_attach'):
        attachable._before_attach(target)

    if hasattr(attachable, '_attachment_test_all'):
        result = attachable._attachment_test_all(target)
        if result is not True:
            assert isinstance(result, list), repr(result)
            result = ['  ' + _ for _ in result]
            message = f'{attachable!r}._attachment_test_all():'
            result.insert(0, message)
            message = '\n'.join(result)
            raise Exception(message)

    grace_container = (abjad.AfterGraceContainer, abjad.GraceContainer)
    if isinstance(attachable, abjad.Spanner):
        if not isinstance(target, abjad.Selection):
            raise Exception('spanners attach to leaf selections only.')
        if not target.are_leaves():
            raise Exception('spanners attach to leaf selections only.')
        attachable._attach(
            target,
            deactivate=deactivate,
            tag=tag,
            )
        return
    elif isinstance(attachable, grace_container):
        if not isinstance(target, abjad.Leaf):
            raise Exception('grace containers attach to single leaf only.')
        attachable._attach(target)
        return

    assert isinstance(target, abjad.Component), repr(target)

    if isinstance(target, abjad.Container):
        acceptable = False
        if isinstance(attachable, (dict, str, abjad.Wrapper)):
            acceptable = True
        if (isinstance(attachable, abjad.TimeSignature) and
            isinstance(target, abjad.Measure)):
            acceptable = True
        if getattr(attachable, '_can_attach_to_containers', False):
            acceptable = True
        if not acceptable:
            message = 'can not attach {!r} to containers: {!r}'
            message = message.format(attachable, target)
            raise Exception(message)
    elif not isinstance(target, abjad.Leaf):
        message = 'indicator {!r} must attach to leaf instead, not {!r}.'
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

    if hasattr(attachable, 'context'):
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
    wrapper_._bind_to_component(component)

    if wrapper is True:
        return wrapper_
