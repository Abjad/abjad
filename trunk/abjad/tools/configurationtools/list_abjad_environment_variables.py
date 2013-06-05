import types


def list_abjad_environment_variables():
    '''.. versionadded:: 1.1

    List Abjad environment variables.

    Return tuple of zero or more environment variable / setting pairs.

    Abjad environment variables are defined in
    ``abjad/tools/configurationtools/AbjadConfiguration/AbjadConfiguration.py``.
    '''

    from abjad import abjad_configuration

    result = []
    for key in dir(abjad_configuration):
        if key.isupper() and not key.startswith('_'):
            result.append((key, getattr(abjad_configuration, key)))
    return tuple(result)
