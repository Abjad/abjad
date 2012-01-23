from abjad.tools.componenttools.all_are_components import all_are_components
from abjad.tools.voicetools.Voice import Voice


def all_are_voices(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad voices::

        abjad> voice = Voice("c'4 d'4 e'4 f'4")

    ::

        abjad> voicetools.all_are_voices([voice])
        True

    True when `expr` is an empty sequence::

        abjad> voicetools.all_are_voices([])
        True

    Otherwise false::

        abjad> voicetools.all_are_voices('foo')
        False

    Return boolean.

    Function wraps ``componenttools.all_are_components()``.
    '''

    return all_are_components(expr, klasses=(Voice,))
