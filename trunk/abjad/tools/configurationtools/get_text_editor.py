import os


def _get_text_editor():
    '''.. versionadded:: 2.2

    Get OS-appropriate text editor.
    '''
    from abjad.tools import configuraitontools

    text_editor = configurationtools.read_abjad_config_file('text_editor')

    if text_editor is not None:
        return text_editor
    elif os.name == 'posix':
        return 'vim'
    else:
        return 'edit'
