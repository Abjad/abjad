# -*- encoding: utf-8 -*-
import os
import re
import shutil
import tempfile
from abjad.tools import abctools


class PersistenceAgent(abctools.AbjadObject):
    r'''A wrapper around the Abjad persistence methods.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> persist(staff)
            PersistenceAgent(client=Staff("c'4 e'4 d'4 f'4"))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    _png_page_pattern = re.compile(r'.+page(\d+)\.png')

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

    def as_ly(
        self, 
        ly_file_path=None, 
        candidacy=False,
        illustrate_function=None, 
        **kwargs
        ):
        r'''Persists client as LilyPond file.

        Autogenerates file path when `ly_file_path` is none.

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> for x in persist(staff).as_ly('~/example.ly'): # doctest: +SKIP
            ...     x
            ...
            '/Users/josiah/Desktop/test.ly'
            0.04491996765136719

        When `candidacy` is true, writes LilyPond output only when LilyPond 
        output would differ from any existing output file.

        When `candidacy` is false, writes LilyPond output even if LilyPond
        output would not differ from any existing output file.

        Returns output path and elapsed formatting time when LilyPond output is
        written.

        Returns false when when LilyPond output is not written due to 
        `candidacy` being set.
        '''
        from abjad import abjad_configuration
        from abjad.tools import systemtools
        if illustrate_function is None:
            assert '__illustrate__' in dir(self._client)
            illustrate_function = self._client.__illustrate__
        illustration = illustrate_function(**kwargs)
        if ly_file_path is None:
            ly_file_name = systemtools.IOManager.get_next_output_file_name()
            ly_file_path = os.path.join(
                abjad_configuration.abjad_output_directory,
                ly_file_name,
                )
        else:
            ly_file_path = os.path.expanduser(ly_file_path)
        assert ly_file_path.endswith('.ly'), ly_file_path
        timer = systemtools.Timer()
        with timer:
            lilypond_format = format(illustration, 'lilypond')
        abjad_formatting_time = timer.elapsed_time
        directory = os.path.dirname(ly_file_path)
        systemtools.IOManager._ensure_directory_existence(directory)
        if not os.path.exists(ly_file_path) or not candidacy:
            with open(ly_file_path, 'w') as file_pointer:
                file_pointer.write(lilypond_format)
            return ly_file_path, abjad_formatting_time
        base, extension = os.path.splitext(ly_file_path)
        candidate_path = base + '.candidate' + extension
        with systemtools.FilesystemState(remove=[candidate_path]):
            with open(candidate_path, 'w') as file_pointer:
                file_pointer.write(lilypond_format)
            if systemtools.TestManager.compare_files(
                ly_file_path, 
                candidate_path,
                ):
                return False
            else:
                shutil.move(candidate_path, ly_file_path)
                return ly_file_path, abjad_formatting_time
        
    def as_midi(self, midi_file_path=None, remove_ly=False, **kwargs):
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
        illustration = self._client.__illustrate__(**kwargs)
        assert hasattr(illustration, 'score_block')
        block = lilypondfiletools.Block(name='midi')
        illustration.score_block.items.append(block)
        if midi_file_path is not None:
            midi_file_path = os.path.expanduser(midi_file_path)
            without_extension = os.path.splitext(midi_file_path)[0]
            ly_file_path = '{}.ly'.format(without_extension)
        else:
            ly_file_path = None
        result = type(self)(illustration).as_ly(ly_file_path, **kwargs)
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
        manager = systemtools.StorageFormatManager
        result = ['# -*- encoding: utf-8 -*-']
        import_statements = manager.get_import_statements(self._client)
        result.extend(import_statements)
        result.extend(('', ''))
        if '_storage_format_specification' in dir(self._client):
            storage_pieces = format(self._client, 'storage')
        else:
            try:
                storage_pieces = manager.format_one_value(self._client)
                storage_pieces = ''.join(storage_pieces)
            except ValueError:
                storage_pieces = repr(self._client)
        storage_pieces = storage_pieces.splitlines()
        line = '{} = {}'.format(object_name, storage_pieces[0])
        result.append(line)
        result.extend(storage_pieces[1:])
        result = '\n'.join(result)
        module_file_path = os.path.expanduser(module_file_path)
        directory = os.path.dirname(module_file_path)
        systemtools.IOManager._ensure_directory_existence(directory)
        with open(module_file_path, 'w') as f:
            f.write(result)

    def as_pdf(
        self,
        pdf_file_path=None,
        candidacy=False,
        illustrate_function=None,
        remove_ly=False,
        **kwargs
        ):
        r'''Persists client as PDF.

        Autogenerates file path when `pdf_file_path` is none.

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> for x in persist(staff).as_pdf(): # doctest: +SKIP
            ...     x
            ...
            '/Users/josiah/.abjad/output/1416.pdf'
            0.047142982482910156
            0.7839350700378418

        When `candidacy` is true, writes PDF output only when PDF 
        output would differ from any existing output file.

        When `candidacy` is false, writes PDF output even if PDF
        output would not differ from any existing output file.

        Returns output path, elapsed formatting time and elapsed rendering
        time when PDF output is written.

        Returns false when when PDF output is not written due to 
        `candidacy` being set.
        '''
        from abjad.tools import systemtools
        if illustrate_function is None:
            assert '__illustrate__' in dir(self._client)
        if pdf_file_path is not None:
            pdf_file_path = os.path.expanduser(pdf_file_path)
            without_extension = os.path.splitext(pdf_file_path)[0]
            ly_file_path = '{}.ly'.format(without_extension)
        else:
            ly_file_path = None
        result = self.as_ly(
            ly_file_path,
            candidacy=candidacy,
            illustrate_function=illustrate_function,
            **kwargs
            )
        if candidacy and result == False:
            return False
        ly_file_path, abjad_formatting_time = result
        without_extension = os.path.splitext(ly_file_path)[0]
        pdf_file_path = '{}.pdf'.format(without_extension)
        timer = systemtools.Timer()
        with timer:
            success = systemtools.IOManager.run_lilypond(
                ly_file_path,
                candidacy=candidacy,
                )
        lilypond_rendering_time = timer.elapsed_time
        if remove_ly:
            os.remove(ly_file_path)
        if candidacy and not success:
            return False
        else:
            return (
                pdf_file_path,
                abjad_formatting_time,
                lilypond_rendering_time,
                success,
                )

    def as_png(
        self,
        png_file_path=None,
        remove_ly=False,
        illustrate_function=None,
        **kwargs
        ):
        r'''Persists client as PNG.

        ::

            >>> staff = Staff()
            >>> measure = Measure((4, 4), "c'4 d'4 e'4 f'4")
            >>> command = indicatortools.LilyPondCommand('break', 'after')
            >>> attach(command, measure[-1])
            >>> staff.extend(measure * 200)

        ::

            >>> result = persist(staff).as_png() # doctest: +SKIP
            >>> for x in result[0]: # doctest: +SKIP
            ...     x
            ...
            '/Users/josiah/Desktop/test-page1.png'
            '/Users/josiah/Desktop/test-page2.png'
            '/Users/josiah/Desktop/test-page3.png'
            '/Users/josiah/Desktop/test-page4.png'
            '/Users/josiah/Desktop/test-page5.png'
            '/Users/josiah/Desktop/test-page6.png'
            '/Users/josiah/Desktop/test-page7.png'
            '/Users/josiah/Desktop/test-page8.png'
            '/Users/josiah/Desktop/test-page9.png'
            '/Users/josiah/Desktop/test-page10.png'
            '/Users/josiah/Desktop/test-page11.png'
            '/Users/josiah/Desktop/test-page12.png'
            '/Users/josiah/Desktop/test-page13.png'
            '/Users/josiah/Desktop/test-page14.png'
            '/Users/josiah/Desktop/test-page15.png'

        Autogenerates file path when `png_file_path` is none.

        Returns output path(s), elapsed formatting time and elapsed rendering
        time.
        '''
        from abjad.tools import systemtools
        if illustrate_function is None:
            assert '__illustrate__' in dir(self._client)
        if png_file_path is not None:
            png_file_path = os.path.expanduser(png_file_path)
            without_extension = os.path.splitext(png_file_path)[0]
            ly_file_path = '{}.ly'.format(without_extension)
        else:
            ly_file_path = None
        result = self.as_ly(
            ly_file_path,
            illustrate_function=illustrate_function,
            **kwargs
            )

        ly_file_path, abjad_formatting_time = result

        original_directory = os.path.split(ly_file_path)[0]
        original_ly_file_path = ly_file_path
        temporary_directory = tempfile.mkdtemp()
        temporary_ly_file_path = os.path.join(
            temporary_directory,
            os.path.split(ly_file_path)[1],
            )
        shutil.copy(original_ly_file_path, temporary_ly_file_path)

        timer = systemtools.Timer()
        with timer:
            success = systemtools.IOManager.run_lilypond(
                temporary_ly_file_path,
                flags='--png',
                )
        lilypond_rendering_time = timer.elapsed_time

        png_file_paths = []
        for file_name in os.listdir(temporary_directory):
            if not file_name.endswith('.png'):
                continue
            source_png_file_path = os.path.join(
                temporary_directory,
                file_name,
                )
            target_png_file_path = os.path.join(
                original_directory,
                file_name,
                )
            shutil.move(source_png_file_path, target_png_file_path)
            png_file_paths.append(target_png_file_path)
        shutil.rmtree(temporary_directory)

        if remove_ly:
            os.remove(ly_file_path)

        if 1 < len(png_file_paths):
            png_file_paths.sort(
                key=lambda x: int(self._png_page_pattern.match(x).groups()[0]),
                )

        return (
            tuple(png_file_paths),
            abjad_formatting_time,
            lilypond_rendering_time,
            success,
            )