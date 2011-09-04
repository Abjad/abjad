from abjad.tools.marktools.get_stem_tremolo_attached_to_component import get_stem_tremolo_attached_to_component


def detach_stem_tremolos_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Detach stem tremolos attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> marktools.StemTremolo(16)(staff[0])
        StemTremolo(16)(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 :16
            d'8
            e'8
            f'8
        }

    ::

        abjad> marktools.get_stem_tremolos_attached_to_component(staff[0])
        (StemTremolo(16)(c'8),)

    ::

        abjad> marktools.detach_stem_tremolos_attached_to_component(staff[0])
        (StemTremolo(16),)

    ::

        abjad> marktools.get_stem_tremolos_attached_to_component(staff[0])
        ()

    Return tuple or zero or more stem tremolos detached.
    '''

    stem_tremolos = []
#    for stem_tremolo in get_stem_tremolo_attached_to_component(component):
#        stem_tremolo.detach()
#        stem_tremolos.append(stem_tremolo)
    try:
        stem_tremolo = get_stem_tremolo_attached_to_component(component)
        stem_tremolo.detach()
        stem_tremolos.append(stem_tremolo)
    except (MissingMarkError):
        pass

    return tuple(stem_tremolos)
