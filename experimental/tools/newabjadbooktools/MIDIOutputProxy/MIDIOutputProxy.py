import copy
import os
from abjad.tools import iotools
from abjad.tools import lilypondfiletools
from experimental.tools.newabjadbooktools.AssetOutputProxy \
    import AssetOutputProxy


class MIDIOutputProxy(AssetOutputProxy):
    r'''Output proxy for LilyPond MIDI files"

    ::

        >>> payload = Staff("c'4 d'4 e'4 f'4")
        >>> output_proxy = newabjadbooktools.MIDIOutputProxy(payload)
        >>> print output_proxy
        MIDIOutputProxy()

    Return output_proxy.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        from abjad import abjad_configuration
        if isinstance(payload, str):
            self._payload = payload
        else:
            payload = copy.deepcopy(payload)
            lilypond_file = iotools.insert_expr_into_lilypond_file(payload)
            lilypond_file.file_initial_system_comments[:] = []
            lilypond_version_token = lilypondfiletools.LilyPondVersionToken(
                abjad_configuration.get_lilypond_minimum_version_string(),
                )
            lilypond_file.file_initial_system_includes[0] = \
                lilypond_version_token
            lilypond_file.score_block.append(lilypondfiletools.MIDIBlock())
            lilypond_format = lilypond_file.lilypond_format
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
            '\t<source src="assets/midi-841714d6c9f05853df8b09fdff45f27c.mid">'
            '</audio>'

        Return list.
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

        Return list.
        '''
        result = []
        return result

    def handle_rest_document_environment(self, document_handler):
        r'''Handle an ReST document environment:

        ::

            >>> document_handler = newabjadbooktools.ReSTDocumentHandler([])
            >>> output_proxy.handle_rest_document_environment(document_handler)
            [':download:`MIDI <assets/midi-841714d6c9f05853df8b09fdff45f27c.mid>`']

        Return list.
        '''
        asset_path = self.get_asset_output_relative_file_path(document_handler)
        result = [
            ':download:`MIDI <{}>`'.format(asset_path),
            ]
        return result

    def write_asset_to_disk(self, document_handler):
        pass
