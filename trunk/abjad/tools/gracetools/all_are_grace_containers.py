from abjad.tools.componenttools.all_are_components import all_are_components
from abjad.tools.gracetools.Grace import Grace


def all_are_grace_containers(expr):
    r'''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad grace containers::

        abjad> graces = [gracetools.Grace("<c' e' g'>4"), gracetools.Grace("<c' f' a'>4")]
        abjad> voice = Voice("c'8 d'8 e'8 f'8")
        abjad> grace_notes = [Note("c'16"), Note("d'16")]
        abjad> grace_container = gracetools.Grace(grace_notes, kind = 'grace')
        abjad> grace_container(voice[1])
        Note("d'8")

    ::

        abjad> f(voice)
        \new Voice {
            c'8
            \grace {
                c'16
                d'16
            }
            d'8
            e'8
            f'8
        }

    ::

        abjad> gracetools.all_are_grace_containers([grace_container])
        True

    True when `expr` is an empty sequence::

        abjad> gracetools.all_are_grace_containers([])
        True

    Otherwise false::

        abjad> gracetools.all_are_grace_containers('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''

    return all_are_components(expr, klasses=(Grace,))
