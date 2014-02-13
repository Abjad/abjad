# -*- encoding: utf-8 -*-
import copy
import os
from abjad.tools import systemtools
from abjad.tools import lilypondfiletools
from experimental.tools.newabjadbooktools.AssetOutputProxy \
    import AssetOutputProxy


class MIDIOutputProxy(AssetOutputProxy):
    r'''Output proxy for LilyPond MIDI files.

    ::

        >>> payload = Staff("c'4 d'4 e'4 f'4")
        >>> output_proxy = newabjadbooktools.MIDIOutputProxy(payload)
        >>> print output_proxy
        MIDIOutputProxy('\\version "2.19.0"\n\\language "english"\n\n\\header {}\n\n\\layout {}\n\n\\paper {}\n\n\\score {\n\t\\new Staff {\n\t\tc\'4\n\t\td\'4\n\t\te\'4\n\t\tf\'4\n\t}\n\t\\midi {}\n}')

    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        from abjad import abjad_configuration
        if isinstance(payload, str):
            self._payload = payload
        else:
            payload = copy.deepcopy(payload)
            manager = systemtools.IOManager
            lilypond_file = manager._insert_expr_into_lilypond_file(payload)
            lilypond_file.file_initial_system_comments[:] = []
            token = lilypondfiletools.LilyPondVersionToken(
                abjad_configuration.get_lilypond_minimum_version_string(),
                )
            lilypond_file.file_initial_system_includes[0] = token
            midi_block = lilypondfiletools.Block(name='midi')
            lilypond_file.score_block.items.append(midi_block)
            lilypond_format = format(lilypond_file)
            self._payload = lilypond_format
             
    ### PUBLIC METHODS ###

    def get_asset_output_absolute_file_path(self, document_handler):
        return os.path.join(
            document_handler.asset_output_directory_name,
            '{}.{}'.format(self.file_name_without_extension, 'mid'),
            )

    def get_asset_output_relative_file_path(self, document_handler):
        return os.path.join(
            document_handler.asset_output_directory_name,
            '{}.{}'.format(self.file_name_without_extension, 'mid'),
            )

    def handle_html_document_environment(self, document_handler):
        r'''Handle an HTML document environment:

        ::

            >>> document_handler = newabjadbooktools.HTMLDocumentHandler([])
            >>> result = output_proxy.handle_html_document_environment(
            ...     document_handler)
            >>> for x in result:
            ...     x
            ...
            '<audio controls="controls">'
            '\tYour browser does not support the <code>audio</code> element.'
            '\t<source src="assets/midi-....mid">'
            '</audio>'

        Returns list.
        '''
        asset_path = self.get_asset_output_relative_file_path(document_handler)
        result = [
            '<audio controls="controls">',
            '\tYour browser does not support the <code>audio</code> element.',
            '\t<source src="{}">'.format(asset_path),
            '</audio>',
            ]
        return result

    def handle_latex_document_environment(self, document_handler):
        r'''Handle a LaTeX document environment:

        ::

            >>> document_handler = newabjadbooktools.LaTeXDocumentHandler([])
            >>> result = output_proxy.handle_latex_document_environment(
            ...     document_handler)
            >>> print result
            []

        Returns list.
        '''
        result = []
        return result

    def handle_rest_document_environment(self, document_handler):
        r'''Handle an ReST document environment:

        ::

            >>> document_handler = newabjadbooktools.ReSTDocumentHandler([])
            >>> output_proxy.handle_rest_document_environment(document_handler)
            [':download:`MIDI <assets/midi-....mid>`']

        Returns list.
        '''
        asset_path = self.get_asset_output_relative_file_path(document_handler)
        result = [
            ':download:`MIDI <{}>`'.format(asset_path),
            ]
        return result

    def write_asset(self, document_handler):
        pass
