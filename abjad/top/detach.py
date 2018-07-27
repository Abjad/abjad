def detach(argument, target=None, by_id=False):
    r"""
    Detaches indicators-equal-to-``argument`` from ``target``.
        
    When ``target`` is none ``argument`` must be a spanner; spanner will then
    detach from all leaves to which spanner attaches.

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
                -\accent
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
        >>> abjad.attach(markup_1, staff[0], tag='+SCORE')
        >>> abjad.attach(
        ...     markup_2,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag='+PARTS_VIOLIN_1',
        ...     )
        >>> abjad.attach(
        ...     markup_3,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag='+PARTS_VIOLIN_2',
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
        >>> abjad.attach(markup_1, staff[0], tag='+SCORE')
        >>> abjad.attach(
        ...     markup_2,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag='+PARTS_VIOLIN_1',
        ...     )
        >>> abjad.attach(
        ...     markup_3,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag='+PARTS_VIOLIN_2',
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
    if isinstance(argument, abjad.Spanner):
        if by_id is True:
            raise Exception('ignoring by_id with spanner argument.')
        argument._detach()
        return
    assert target is not None
    after_grace_container = None
    grace_container = None
    spanners = []
    inspector = abjad.inspect(target)
    if isinstance(argument, type):
        if issubclass(argument, abjad.Spanner):
            spanners = inspector.spanners(argument)
        elif issubclass(argument, abjad.AfterGraceContainer):
            after_grace_container = inspector.after_grace_container()
        elif issubclass(argument, abjad.GraceContainer):
            grace_container = inspector.grace_container()
        else:
            assert hasattr(target, '_wrappers')
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
        if isinstance(argument, abjad.Spanner):
            spanners = inspector.spanners(argument)
        elif isinstance(argument, abjad.AfterGraceContainer):
            after_grace_container = inspector.after_grace_container()
        elif isinstance(argument, abjad.GraceContainer):
            grace_container = inspector.grace_container()
        else:
            assert hasattr(target, '_wrappers')
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
    items.extend(spanners)
    if after_grace_container is not None:
        items.append(after_grace_container)
    if grace_container is not None:
        items.append(grace_container)
    if by_id is True:
        items = [_ for _ in items if id(item) == id(argument)]
    for item in items:
        item._detach()
    items = tuple(items)
    return items
