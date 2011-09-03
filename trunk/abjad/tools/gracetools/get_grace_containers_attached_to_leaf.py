def get_grace_containers_attached_to_leaf(leaf):
    r'''.. versionadded:: 2.0

    Get grace containers attached to leaf::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> gracetools.Grace([Note("cs'16")], kind = 'grace')(staff[1])
        Note("d'8")
        abjad> gracetools.Grace([Note("ds'16")], kind = 'after')(staff[1])
        Note("d'8")

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            \grace {
                cs'16
            }
            \afterGrace
            d'8
            {
                ds'16
            }
            e'8
            f'8
        }

    ::

        abjad> gracetools.get_grace_containers_attached_to_leaf(staff[1])
        (Grace(cs'16), Grace(ds'16))

    Return tuple.
    '''

    result = []
    if hasattr(leaf, '_grace'):
        result.append(leaf._grace)
    if hasattr(leaf, '_after_grace'):
        result.append(leaf._after_grace)
    return tuple(result)
