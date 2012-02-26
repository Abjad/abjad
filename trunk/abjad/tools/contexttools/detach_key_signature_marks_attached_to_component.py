from abjad.tools.contexttools.get_key_signature_marks_attached_to_component import get_key_signature_marks_attached_to_component


def detach_key_signature_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Detach key signature marks attached to `component`::

        abjad> staff = Staff("c'4 d'4 e'4 f'4")
        abjad> key_signature_mark = contexttools.KeySignatureMark('c', 'major')
        abjad> key_signature_mark.attach(staff)
        KeySignatureMark(NamedChromaticPitchClass('c'), Mode('major'))(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \key c \major
            c'4
            d'4
            e'4
            f'4
        }

    ::

        abjad> contexttools.detach_key_signature_marks_attached_to_component(staff)
        (KeySignatureMark(NamedChromaticPitchClass('c'), Mode('major')),)

    ::

        abjad> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more key signature marks.
    '''

    marks = []
    for mark in get_key_signature_marks_attached_to_component(component):
        mark.detach()
        marks.append(mark)
    return tuple(marks)
