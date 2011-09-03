from abjad.tools.componenttools._Component import _Component
from abjad.tools.componenttools.iterate_components_depth_first import iterate_components_depth_first
from abjad.tools.threadtools.component_to_thread_signature import component_to_thread_signature


def iterate_thread_backward_from_component(component, klass = None):
    r'''.. versionadded:: 2.0

    Yield right-to-left components in the thread of `component`
    starting from `component`.

    When ``klass = None`` return all components in the thread of `component`.

    When `klass` is set to some other Abjad class,
    yield only `klass` instances in the thread of `component`::

        abjad> from abjad.tools import threadtools

    ::

        abjad> container = Container(Voice(notetools.make_repeated_notes(2)) * 2)
        abjad> container.is_parallel = True
        abjad> container[0].name = 'voice 1'
        abjad> container[1].name = 'voice 2'
        abjad> staff = Staff(container * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> print staff.format
        \new Staff {
            <<
                \context Voice = "voice 1" {
                    c'8
                    d'8
                }
                \context Voice = "voice 2" {
                    e'8
                    f'8
                }
            >>
            <<
                \context Voice = "voice 1" {
                    g'8
                    a'8
                }
                \context Voice = "voice 2" {
                    b'8
                    c''8
                }
            >>
        }

    Starting from the last leaf in score. ::

        abjad> for x in threadtools.iterate_thread_backward_from_component(staff.leaves[-1], Note):
        ...     x
        Note("c''8")
        Note("b'8")
        Note("f'8")
        Note("e'8")

    Yield all components in thread::

        abjad> for x in threadtools.iterate_thread_backward_from_component(staff.leaves[-1]):
        ...     x
        Note("c''8")
        Voice-"voice 2"{2}
        Note("b'8")
        Voice-"voice 2"{2}
        Note("f'8")
        Note("e'8")

    Note that this function is a special type of depth-first search.

    Compare with :func:`threadtools.iterate_thread_backward_in_expr()
    <abjad.tools.threadtools.iterate_thread_backward_in_expr>`.

    .. versionchanged:: 2.0
        renamed ``iterate.thread_backward_from()`` to
        ``threadtools.iterate_thread_backward_from_component()``.

    .. versionchanged:: 2.0
        renamed ``iterate.thread_backward_from_component()`` to
        ``threadtools.iterate_thread_backward_from_component()``.
    '''

    # set default class
    if klass is None:
        klass = _Component

    # save thread signature of input component
    component_thread_signature = component_to_thread_signature(component)

    # iterate component depth-first allowing to crawl UP into score
    for x in iterate_components_depth_first(component, capped = False, direction = 'right'):
        if isinstance(x, klass):
            if component_to_thread_signature(x) == component_thread_signature:
                yield x
