from abjad.tools.resttools.Rest import Rest


def set_vertical_positioning_pitch_on_rest(rest, pitch):
    r'''.. versionadded:: 2.0

    Set vertical positioning `pitch` on `rest`::

        abjad> rest = Rest((1, 4))

    ::

        abjad> resttools.set_vertical_positioning_pitch_on_rest(rest, "d''")
        Rest('r4')

    ::

        abjad> f(rest)
        d''4 \rest

    Raise type error when `rest` is not a rest.

    Return `rest`.
    '''
    from abjad.tools import pitchtools

    if not isinstance(rest, Rest):
        raise TypeError('\n\tMust be rest: "%s".' % rest)

    if pitch is not None:
        pitch = pitchtools.NamedChromaticPitch(pitch)

    rest._vertical_positioning_pitch = pitch

    return rest
