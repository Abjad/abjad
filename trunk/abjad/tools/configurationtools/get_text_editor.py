import os


def get_text_editor():
    '''.. versionadded:: 2.2

    Get OS-appropriate text editor.
    '''
    from abjad import abjad_configuration
    from abjad.tools import configurationtools

    text_editor = abjad_configuration['text_editor']

    if text_editor is not None:
        return text_editor
    elif os.name == 'posix':
        return 'vim'
    else:
        return 'edit'
