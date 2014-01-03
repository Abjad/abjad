# -*- encoding: utf-8 -*-
import os
import re
from abjad.tools import abctools


class PersistenceAgent(abctools.AbjadObject):
    r'''A wrapper around the Abjad persistence methods.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> persist(staff)
            PersistenceAgent(client={c'4, e'4, d'4, f'4})

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        self._client = client

    ### PRIVATE PROPERTIES ###

    @property
    def client(self):
        r'''Client of persistence agent.

        Returns selection or component.
        '''
        return self._client

    ### PUBLIC METHODS ###

    def as_ly(self, ly_file_path=None):
        r'''Persists client as LilyPond file.

        Autogenerates file path when `ly_file_path` is none.

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> for x in persist(staff).as_ly('~/example.ly'): # doctest: +SKIP
            ...     x
            ...
            '/Users/josiah/Desktop/test.ly'
            0.04491996765136719

        Returns output path and elapsed formatting time.
        '''
        from abjad import abjad_configuration
        from abjad.tools import systemtools
        # get the illustration
        assert '__illustrate__' in dir(self._client)
        illustration = self._client.__illustrate__()
        # validate the output path
        if ly_file_path is None:
            ly_file_name = systemtools.IOManager.get_next_output_file_name()
            ly_file_path = os.path.join(
                abjad_configuration.abjad_output_directory_path,
                ly_file_name,
                )
        else:
            ly_file_path = os.path.expanduser(ly_file_path)
        assert ly_file_path.endswith('.ly'), ly_file_path
        # format the illustration
        timer = systemtools.Timer()
        with timer:
            lilypond_format = format(illustration, 'lilypond')
        abjad_formatting_time = timer.elapsed_time
        # write the formatted illustration to disk
        directory_path = os.path.dirname(ly_file_path)
        systemtools.IOManager.ensure_directory_existence(directory_path)
        with open(ly_file_path, 'w') as file_handle:
            file_handle.write(lilypond_format)
        return ly_file_path, abjad_formatting_time

    def as_midi(self, midi_file_path=None, remove_ly=False):
        r'''Persists client as MIDI file.

        Autogenerates file path when `midi_file_path` is none.

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> for x in persist(staff).as_midi(): # doctest: +SKIP
            ...     x
            ...
            '/Users/josiah/.abjad/output/1415.midi'
            0.07831692695617676
            1.0882699489593506

        Returns output path, elapsed formatting time and elapsed rendering
        time.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import systemtools
        assert '__illustrate__' in dir(self._client)
        illustration = self._client.__illustrate__()
        assert hasattr(illustration, 'score_block')
        illustration.score_block.append(lilypondfiletools.MIDIBlock())
        if midi_file_path is not None:
            midi_file_path = os.path.expanduser(midi_file_path)
            without_extension = os.path.splitext(midi_file_path)[0]
            ly_file_path = '{}.ly'.format(without_extension)
        else:
            ly_file_path = None
        result = type(self)(illustration).as_ly(ly_file_path)
        ly_file_path, abjad_formatting_time = result
        timer = systemtools.Timer()
        with timer:
            systemtools.IOManager.run_lilypond(ly_file_path)
        lilypond_rendering_time = timer.elapsed_time
        if os.name == 'nt':
            extension = 'mid'
        else:
            extension = 'midi'
        midi_file_path = '{}.{}'.format(
            os.path.splitext(ly_file_path)[0],
            extension,
            )
        if remove_ly:
            os.remove(ly_file_path)
        return midi_file_path, abjad_formatting_time, lilypond_rendering_time

    def as_module(self, module_file_path, object_name):
        r'''Persists client as Python module.

        ::

            >>> inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 1),
            ...     timespantools.Timespan(2, 4),
            ...     timespantools.Timespan(6, 8),
            ...     ])
            >>> persist(inventory).as_module( # doctest: +SKIP
            ...     '~/example.py', 
            ...     'inventory',
            ...     )

        Returns none.
        '''
        from abjad.tools import systemtools
        assert '_storage_format_specification' in dir(self._client)
        result = ['# -*- encoding: utf-8 -*-']
        storage_pieces = format(self._client, 'storage').splitlines()
        pattern = re.compile(r'\b[a-z]+tools\b')
        tools_package_names = set()
        for line in storage_pieces:
            match = pattern.search(line)
            while match is not None:
                group = match.group()
                tools_package_names.add(group)
                end = match.end()
                match = pattern.search(line, pos=end)
        for name in sorted(tools_package_names):
            line = 'from abjad.tools import {}'.format(name)
            result.append(line)
        result.append('')
        result.append('')
        line = '{} = {}'.format(object_name, storage_pieces[0])
        result.append(line)
        result.extend(storage_pieces[1:])
        result = '\n'.join(result)
        module_file_path = os.path.expanduser(module_file_path)
        directory_path = os.path.dirname(module_file_path)
        systemtools.IOManager.ensure_directory_existence(directory_path)
        with open(module_file_path, 'w') as f:
            f.write(result)

    def as_pdf(self, pdf_file_path=None, remove_ly=False):
        r'''Persists client as PDF.

        Autogenerates file path when `pdf_file_path` is none.

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> for x in persist(staff).as_pdf(): # doctest: +SKIP
            '/Users/josiah/.abjad/output/1416.pdf'
            0.047142982482910156
            0.7839350700378418

        Returns output path, elapsed formatting time and elapsed rendering
        time.
        '''
        from abjad.tools import systemtools
        assert '__illustrate__' in dir(self._client)
        # validate the output path
        if pdf_file_path is not None:
            pdf_file_path = os.path.expanduser(pdf_file_path)
            without_extension = os.path.splitext(pdf_file_path)[0]
            ly_file_path = '{}.ly'.format(without_extension)
        else:
            ly_file_path = None
        # format and write the lilypond file
        ly_file_path, abjad_formatting_time = self.as_ly(ly_file_path)
        without_extension = os.path.splitext(ly_file_path)[0]
        pdf_file_path = '{}.pdf'.format(without_extension)
        # render the pdf
        timer = systemtools.Timer()
        with timer:
            systemtools.IOManager.run_lilypond(ly_file_path)
        lilypond_rendering_time = timer.elapsed_time
        if remove_ly:
            os.remove(ly_file_path)
        return pdf_file_path, abjad_formatting_time, lilypond_rendering_time
