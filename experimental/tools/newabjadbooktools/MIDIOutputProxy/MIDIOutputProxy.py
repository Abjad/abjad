import copy
import os
from abjad.tools import configurationtools
from abjad.tools import lilypondfiletools
from abjad.tools.iotools._insert_expr_into_lilypond_file import _insert_expr_into_lilypond_file
from experimental.tools.newabjadbooktools.AssetOutputProxy import AssetOutputProxy


class MIDIOutputProxy(AssetOutputProxy):

    ### INITIALIZER ###

    def __init__(self, payload):
        if isinstance(payload, str):
            self._payload = payload
        else:
            payload = copy.deepcopy(payload)
            lilypond_file = _insert_expr_into_lilypond_file(payload)
            lilypond_file.file_initial_system_comments[:] = []
            lilypond_version_token = lilypondfiletools.LilyPondVersionToken(
                configurationtools.get_lilypond_minimum_version_string(),
                )
            lilypond_file.file_initial_system_includes[0] = lilypond_version_token
            lilypond_file.score_block.append(lilypondfiletools.MIDIBlock())
            lilypond_format = lilypond_file.lilypond_format
            self._payload = lilypond_format
             
    ### PUBLIC METHODS ###


    def get_absolute_asset_output_path(self, document_handler):
        return os.path.join(
            document_handler.asset_output_directory_name,
            '{}.{}'.format(self.file_name_without_extension, 'mid'),
            )

    def get_relative_asset_output_path(self, document_handler):
        return os.path.join(
            document_handler.asset_output_directory_name,
            '{}.{}'.format(self.file_name_without_extension, 'mid'),
            )

