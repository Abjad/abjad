from abjad.tools.configurationtools.read_abjad_user_config_file import read_abjad_user_config_file
import sys


def _change_abjad_prompt():
    if read_abjad_user_config_file().get('use_abjad_prompt'):
        sys.ps1 = 'abjad> '
