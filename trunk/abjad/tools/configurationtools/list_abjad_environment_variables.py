from abjad.cfg import cfg
import types


def list_abjad_environment_variables():
    '''.. versionadded:: 1.1

    List Abjad environment variables.

    Return tuple of zero or more environment variable / setting pairs.

    Abjad environment variables are defined in ``abjad/cfg/cfg.py``.

    .. versionchanged:: 2.0
        renamed ``configurationtools.list_settings()`` to
        ``configurationtools.list_abjad_environment_variables()``.
    '''

    result = []
    for key, value in sorted(vars(cfg).items()):
        if not isinstance(value, types.ModuleType):
            if not key.startswith('_'):
                if not key == 'abjad_version_string':
                    result.append((key, value))
    return tuple(result)
