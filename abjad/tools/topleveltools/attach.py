def attach(
    indicator,
    argument,
    alternate=None,
    annotation=None,
    context=None,
    deactivate=None,
    name=None,
    site=None,
    synthetic_offset=None,
    tag=None,
    ):
    r'''Attaches `indicator` to component, selection or spanner `argument`.

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

    Derives context from default `indicator` context when `context` is none.

    Returns none.
    '''
    import abjad
    prototype = (abjad.Component, abjad.Selection, abjad.Spanner)
    if not isinstance(argument, prototype):
        message = 'must be component, selection or spanner: {!r}.'
        message = message.format(argument)
        raise TypeError(message)

    if tag is not None:
        tag = getattr(tag, 'name', tag)
        assert ':' not in tag, repr(tag)

    def _is_acceptable(argument):
        if isinstance(argument, abjad.Leaf):
            return True
        if not isinstance(argument, (list, abjad.Selection, abjad.Spanner)):
            return False
        for item in argument:
            if not isinstance(item, abjad.Leaf):
                return False
        return True

    prototype = (str, dict, abjad.IndicatorWrapper)
    if (isinstance(indicator, prototype) or
        getattr(indicator, '_can_attach_to_containers', False)):
        pass
    elif (isinstance(indicator, abjad.TimeSignature) and
        isinstance(argument, abjad.Measure)):
        pass
    elif not _is_acceptable(argument):
        message = 'attach {!r} to a leaf (or selection of leaves) not to {!r}.'
        message = message.format(indicator, argument)
        raise Exception(message)

    if hasattr(indicator, '_before_attach'):
        indicator._before_attach(argument)

    if hasattr(indicator, '_attachment_test_all'):
        if not indicator._attachment_test_all(argument):
            message = '{!r} attachment test fails for {!r}.'
            message = message.format(indicator, argument)
            raise Exception(message)

    if hasattr(indicator, '_attach'):
        prototype = (
            abjad.AfterGraceContainer,
            abjad.GraceContainer,
            abjad.Spanner,
            )
        assert isinstance(indicator, prototype), repr(indicator)
        assert context is None

    prototype = (abjad.AfterGraceContainer, abjad.GraceContainer)
    if isinstance(indicator, prototype):
        assert context is None, repr(context)
        indicator._attach(argument)
        return

    if isinstance(indicator, abjad.Spanner):
        leaves = []
        try:
            for item in argument:
                if isinstance(item, abjad.Leaf):
                    leaves.append(item)
                else:
                    leaves.extend(abjad.iterate(item).leaves())
        except TypeError:
            leaves.append(argument)
        indicator._attach(leaves, deactivate=deactivate, site=site, tag=tag)
        return

    component = argument
    prototype = (abjad.Component, abjad.Spanner)
    if not isinstance(component, prototype):
        message = 'must be component or spanner: {!r}.'
        message = message.format(component)
        raise Exception(message)

    if isinstance(indicator, abjad.IndicatorWrapper):
        alternate = alternate or indicator.alternate
        annotation = annotation or indicator.annotation
        context = context or indicator.context
        deactivate = deactivate or indicator.deactivate
        name = name or indicator.name
        site = site or indicator.site
        synthetic_offset = synthetic_offset or indicator.synthetic_offset
        tag = tag or indicator.tag
        indicator._detach()
        indicator = indicator.indicator

    if hasattr(indicator, 'context'):
        context = context or indicator.context

    wrapper = abjad.IndicatorWrapper(
        alternate=alternate,
        annotation=annotation,
        component=component,
        context=context,
        deactivate=deactivate,
        indicator=indicator,
        name=name,
        site=site,
        synthetic_offset=synthetic_offset,
        tag=tag,
        )
    wrapper._bind_to_component(component)
