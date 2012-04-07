import sys
from abjad.cfg._read_config_file import _read_config_file


def _change_abjad_prompt():
    if _read_config_file( ).get('use_abjad_prompt'):
        sys.ps1 = 'abjad> '
