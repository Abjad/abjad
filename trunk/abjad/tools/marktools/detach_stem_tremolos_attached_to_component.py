def detach_stem_tremolos_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Detach stem tremolos attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> marktools.StemTremolo(16)(staff[0])
        StemTremolo(16)(c'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 :16
            d'8
            e'8
            f'8
        }

    ::

        >>> marktools.get_stem_tremolos_attached_to_component(staff[0])
        (StemTremolo(16)(c'8),)

    ::

        >>> marktools.detach_stem_tremolos_attached_to_component(staff[0])
        (StemTremolo(16),)

    ::

        >>> marktools.get_stem_tremolos_attached_to_component(staff[0])
        ()

    Return tuple or zero or more stem tremolos detached.
    '''
    from abjad.tools import marktools

    stem_tremolos = []
    try:
        stem_tremolo = marktools.get_stem_tremolo_attached_to_component(component)
        stem_tremolo.detach()
        stem_tremolos.append(stem_tremolo)
    except (MissingMarkError):
        pass

    return tuple(stem_tremolos)
