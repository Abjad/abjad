def attach(
    attachable,
    target,
    context=None,
    deactivate=None,
    left_open=None,
    right_open=None,
    site=None,
    synthetic_offset=None,
    tag=None,
    ):
    r'''Attaches `attachable` to `target`.
    
    First form attaches indicator `attachable` to single leaf `target`.
    
    Second form attaches spanner `attachable` to leaf selection `target`.

    Third for attaches grace container `attachable` to leaf `target`.

    Fourth form attaches time signature `attachable` to measure `target`.

    Fifth form attaches wrapper `attachable` to unknown (?) `target`.

    ..  container:: example

        Attaches clef to first note in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Clef('alto'), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
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
            \new Staff {
                c'4
                d'4
                e'4
                f'4 -\accent
            }

    ..  container:: example

        Works with context names:

        >>> voice = abjad.Voice("c'4 d' e' f'", name='MusicVoice')
        >>> staff = abjad.Staff([voice], name='MusicStaff')
        >>> abjad.attach(abjad.Clef('alto'), voice[0], context='MusicStaff')
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \context Staff = "MusicStaff" {
                \context Voice = "MusicVoice" {
                    \clef "alto"
                    c'4
                    d'4
                    e'4
                    f'4
                }
            }

        >>> for leaf in abjad.select(staff).leaves():
        ...     leaf, abjad.inspect(leaf).get_effective(abjad.Clef)
        ...
        (Note("c'4"), Clef('alto'))
        (Note("d'4"), Clef('alto'))
        (Note("e'4"), Clef('alto'))
        (Note("f'4"), Clef('alto'))

    Derives context from default `attachable` context when `context` is none.

    Returns none.
    '''
    import abjad

    nonindicator_prototype = (
        abjad.AfterGraceContainer,
        abjad.GraceContainer,
        abjad.Spanner,
        )

    if context is not None and isinstance(attachable, nonindicator_prototype):
        message = 'set context only for indicators, not {!r}.'
        message = message.format(attachable)
        raise Exception(message)

    if left_open is not None and not isinstance(attachable, abjad.Spanner):
        message = 'set left_open only for spanners, not {!r}.'
        message = message.format(attachable)
        raise Exception(message)

    if right_open is not None and not isinstance(attachable, abjad.Spanner):
        message = 'set right_open only for spanners, not {!r}.'
        message = message.format(attachable)
        raise Exception(message)
            
    if hasattr(attachable, '_before_attach'):
        attachable._before_attach(target)

    if hasattr(attachable, '_attachment_test_all'):
        if not attachable._attachment_test_all(target):
            message = '{!r} attachment test fails for ...'.format(attachable)
            message += '\n\n'
            message += '{!r}'.format(target)
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
            left_open=left_open,
            right_open=right_open,
            site=site,
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
        if left_open is None:
            left_open = attachable.left_open
        if right_open is None:
            right_open = attachable.right_open
        site = site or attachable.site
        synthetic_offset = synthetic_offset or attachable.synthetic_offset
        tag = tag or attachable.tag
        attachable._detach()
        attachable = attachable.indicator

    if hasattr(attachable, 'context'):
        context = context or attachable.context

    wrapper = abjad.Wrapper(
        annotation=annotation,
        component=component,
        context=context,
        deactivate=deactivate,
        indicator=attachable,
        left_open=left_open,
        right_open=right_open,
        site=site,
        synthetic_offset=synthetic_offset,
        tag=tag,
        )
    wrapper._bind_to_component(component)
