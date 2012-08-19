import types


def list_abjad_environment_variables():
    '''.. versionadded:: 1.1

    List Abjad environment variables.

    Return tuple of zero or more environment variable / setting pairs.

    Abjad environment variables are defined in 
    ``abjad/tools/configurationtools/AbjadConfig/AbjadConfig.py``.

    .. versionchanged:: 2.0
        renamed ``configurationtools.list_settings()`` to
        ``configurationtools.list_abjad_environment_variables()``.
    '''

    from abjad import ABJCFG

    result = []
    for key in dir(ABJCFG):
        if key.isupper() and not key.startswith('_'):
            result.append((key, getattr(ABJCFG, key)))
    return tuple(result)
