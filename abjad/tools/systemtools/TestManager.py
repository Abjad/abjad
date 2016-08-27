# -*- coding: utf-8 -*-
import difflib
import inspect
import os
from abjad.tools.abctools import AbjadObject


class TestManager(AbjadObject):
    r'''Manages test logic.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Managers'

    ### PRIVATE METHODS ###

    @staticmethod
    def _compare_backup(path):
        if isinstance(path, str):
            paths = [path]
        elif (isinstance(path, (tuple, list))):
            paths = path
        else:
            raise TypeError(path)
        for path in paths:
            backup_path = path + '.backup'
            if not TestManager.compare_files(path, backup_path):
                return False
        return True

    @staticmethod
    def _compare_lys(path_1, path_2):
        r'''Compares LilyPond file `path_1` to LilyPond file `path_2`.

        Performs line-by-line comparison.

        Discards blank lines.

        Discards any LilyPond version statements.

        Discards any lines beginning with ``%``.

        Returns true or false.
        '''
        file_1_lines = TestManager._normalize_ly(path_1)
        file_2_lines = TestManager._normalize_ly(path_2)
        return file_1_lines == file_2_lines

    @staticmethod
    def _compare_pdfs(path_1, path_2):
        r'''Compares PDF `path_1` to PDF `path_2`.

        Performs line-by-line comparison.

        Discards blank lines.

        Discards lines that contain any of the following strings:

        * ``/ID``
        * ``/CreationDate``
        * ``/ModDate``
        * ``xmp:CreateDate``
        * ``xmp:ModifyDate``
        * ``xapMM:DocumentID``
        * ``rdf:about``

        Discards first (binary) stream object in PDF;
        possibly first stream contains binary-encoded creator
        or timestamp information that can vary from one creation
        of a PDF to another.

        Returns true or false.
        '''
        file_1_lines = TestManager._normalize_pdf(path_1)
        file_2_lines = TestManager._normalize_pdf(path_2)
        return file_1_lines == file_2_lines

    @staticmethod
    def _compare_text_files(path_1, path_2):
        r'''Compares text file `path_1` to text file `path_2`.

        Performs line-by-line comparison.

        Discards blank lines.

        Trims whitespace from the end of each line.

        Returns true or false.
        '''
        file_1_lines, file_2_lines = [], []
        with open(path_1, 'r') as file_pointer:
            for line in file_pointer.readlines():
                line = line.strip()
                if line == '':
                    continue
                file_1_lines.append(line)
        with open(path_2, 'r') as file_pointer:
            for line in file_pointer.readlines():
                line = line.strip()
                if line == '':
                    continue
                file_2_lines.append(line)
        return file_1_lines == file_2_lines

    @staticmethod
    def _get_first_differing_pdf_lines(path_1, path_2):
        file_1_lines = TestManager._normalize_pdf(path_1)
        file_2_lines = TestManager._normalize_pdf(path_2)
        for file_1_line, file_2_line in zip(file_1_lines, file_2_lines):
            if not file_1_line == file_2_line:
                return file_1_line, file_2_line

    @staticmethod
    def _normalize_ly(path):
        lines = []
        with open(path, 'r') as file_pointer:
            for line in file_pointer.readlines():
                line = line.strip()
                if line == '':
                    continue
                if line.startswith(r'\version'):
                    continue
                elif line.startswith('%'):
                    continue
                lines.append(line)
        return lines

    @staticmethod
    def _normalize_pdf(path):
        lines = []
        with open(path, 'rb') as file_pointer:
            contents = file_pointer.read()
            for line in contents.splitlines():
                line = line.strip()
                if line == b'':
                    continue
                elif line.startswith(b'%'):
                    continue
                elif b'/ID' in line:
                    continue
                elif b'/Creator' in line:
                    continue
                elif b'/CreationDate' in line:
                    continue
                elif b'/ModDate' in line:
                    continue
                elif b'xmp:CreateDate' in line:
                    continue
                elif b'xmp:CreatorTool' in line:
                    continue
                elif b'xmp:ModifyDate' in line:
                    continue
                elif b'xapMM:DocumentID' in line:
                    continue
                elif b'rdf:about' in line:
                    continue
                lines.append(line)
        # discard first stream in document: can contain differences;
        # no idea why; possibly first stream includes binary-encoded
        # creator information or binary-encoded timestamp information
        new_lines = []
        found_first_stream = False
        in_first_stream = False
        for line in lines:
            if line == b'stream' and not found_first_stream:
                found_first_stream = True
                in_first_stream = True
            elif line.endswith(b'endstream') and in_first_stream:
                in_first_stream = False
                continue
            if in_first_stream:
                continue
            else:
                new_lines.append(line)
        return new_lines

    ### PUBLIC METHODS ###

    @staticmethod
    def apply_additional_layout(lilypond_file):
        r'''Configures multiple-voice rhythmic staves in `lilypond_file`.

        Operates in place.

        Returns none.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import scoretools
        from abjad.tools import topleveltools
        # configure multiple-voice rhythmic staves
        for staff in topleveltools.iterate(lilypond_file.score_block.items[0]
            ).by_class(scoretools.Staff):
            if staff.is_simultaneous:
                assert len(staff) == 2
                voice_1 = staff[0]
                topleveltools.override(voice_1).note_head.Y_offset = 0.5
                topleveltools.override(voice_1).stem.direction = Up
                voice_2 = staff[1]
                topleveltools.override(voice_2).note_head.Y_offset = -0.5
                topleveltools.override(voice_2).stem.direction = Down
                spacing_vector = schemetools.make_spacing_vector(0, 0, 6, 0)
                manager = topleveltools.override(staff)
                manager.vertical_axis_group.staff_staff_spacing = spacing_vector
        # provide more space between staves with pitched notes
        for staff in topleveltools.iterate(
            lilypond_file.score_block.items[0]).by_class(scoretools.Staff):
            if not (isinstance(staff, scoretools.Staff) and
                staff.context_name == 'RhythmicStaff'):
                for item in lilypond_file.layout_block.items:
                    if isinstance(item, lilypondfiletools.ContextBlock):
                        if item.source_context_name == 'StaffGroup':
                            break
                else:
                    message = 'no staff group context block found.'
                    raise Exception(message)
                spacing_vector = schemetools.make_spacing_vector(0, 0, 6, 0)
                manager = topleveltools.override(item)
                manager.vertical_axis_group.staff_staff_spacing = spacing_vector
            break

    @staticmethod
    def clean_string(string):
        r'''Cleans string.
        '''
        from abjad.tools import stringtools
        return stringtools.normalize(string)

    @staticmethod
    def compare(string_1, string_2):
        r'''Compares `string_1` to `string_2`.

        Massage newlines.

        Returns true or false.
        '''
        if not isinstance(string_1, str):
            string_1 = format(string_1)
        split_lines = string_2.split('\n')
        if not split_lines[0] or split_lines[0].isspace():
            split_lines.pop(0)
        if not split_lines[-1] or split_lines[-1].isspace():
            split_lines.pop(-1)
        indent_width = 0
        if split_lines:
            for indent_width, character in enumerate(split_lines[0]):
                if character != ' ':
                    break
        massaged_lines = []
        for split_line in split_lines:
            massaged_line = split_line[indent_width:]
            massaged_lines.append(massaged_line)
        massaged_string = '\n'.join(massaged_lines)
        return string_1.replace('\t', '    ') == massaged_string

    @staticmethod
    def compare_files(path_1, path_2):
        r'''Compares file `path_1` to file `path_2`.

        For all file types::

        * Performs line-by-line comparison
        * Discards blank lines

        For LilyPond files, additionally::

        * Discards any LilyPond version statements
        * Discards any lines beginning with ``%``

        For PDFs, additionally discards lines that contain any of the
        following strings:

        * ``/ID``
        * ``/CreationDate``
        * ``/ModDate``
        * ``xmp:CreateDate``
        * ``xmp:ModifyDate``
        * ``xapMM:DocumentID``
        * ``rdf:about``

        Discards first (binary) stream object in PDF;
        possibly first stream contains binary-encoded creator
        or timestamp information that can vary from one creation
        of a PDF to another.

        Returns true when files compare the same and false when files compare
        differently.
        '''
        if os.path.exists(path_1) and not os.path.exists(path_2):
            return False
        elif not os.path.exists(path_1) and os.path.exists(path_2):
            return False
        elif not os.path.exists(path_1) and not os.path.exists(path_2):
            return True
        if path_1.endswith('.backup'):
            path_1 = path_1.strip('.backup')
        if path_2.endswith('.backup'):
            path_2 = path_2.strip('.backup')
        base_1, extension_1 = os.path.splitext(path_1)
        base_2, extension_2 = os.path.splitext(path_2)
        assert extension_1 == extension_2
        if extension_1 == '.ly':
            return TestManager._compare_lys(path_1, path_2)
        elif extension_1 == '.pdf':
            return TestManager._compare_pdfs(path_1, path_2)
        else:
            return TestManager._compare_text_files(path_1, path_2)

    @staticmethod
    def compare_objects(object_one, object_two):
        r'''Compares `object_one` to `object_two`.

        Returns true or false.
        '''
        from abjad.tools import systemtools
        agent_one = systemtools.StorageFormatAgent(object_one)
        if agent_one.format_specification.coerce_for_equality:
            try:
                object_two = type(object_one)(object_two)
            except (
                TypeError,
                ValueError,
                ):
                return False
        elif not isinstance(object_two, type(object_one)):
            return False
        agent_two = systemtools.StorageFormatAgent(object_two)
        return agent_one.get_template_dict() == agent_two.get_template_dict()

    @staticmethod
    def diff(object_a, object_b, title=None):
        r'''Gets diff of `object_a` and `object_b` formats.

        ::

            >>> one = rhythmmakertools.TaleaRhythmMaker(
            ...     talea=rhythmmakertools.Talea(
            ...         counts=[1, 2, 3],
            ...         denominator=8,
            ...         )
            ...     )

        ::

            >>> two = rhythmmakertools.TaleaRhythmMaker(
            ...     talea=rhythmmakertools.Talea(
            ...         counts=[1, 5, 3],
            ...         denominator=4,
            ...         )
            ...     )

        ::

            >>> diff = systemtools.TestManager.diff(one, two, 'Diff:')
            >>> print(diff)
            Diff:
              rhythmmakertools.TaleaRhythmMaker(
                  talea=rhythmmakertools.Talea(
            -         counts=(1, 2, 3),
            ?                    ^
            +         counts=(1, 5, 3),
            ?                    ^
            -         denominator=8,
            ?                     ^
            +         denominator=4,
            ?                     ^
                      ),
                  )

        Returns string.
        '''
        try:
            a_format = format(object_a, 'storage')
        except ValueError:
            a_format = format(object_a)
        try:
            b_format = format(object_b, 'storage')
        except ValueError:
            b_format = format(object_b)
        a_format = a_format.splitlines(True)
        b_format = b_format.splitlines(True)
        diff = ''.join(difflib.ndiff(a_format, b_format))
        if title is not None:
            diff = title + '\n' + diff
        return diff

    @staticmethod
    def get_current_function_name():
        r'''Gets current function name.

        ::

            >>> def foo():
            ...        function_name = systemtools.TestManager.get_current_function_name()
            ...        print('Function name is {!r}.'.format(function_name))

        ::

            >>> foo()
            Function name is 'foo'.

        Call this function within the implementation of any ofther function.

        Returns enclosing function name as a string or else none.
        '''
        stack = inspect.stack()
        # per the inspect module doc page ...
        try:
            parent_frame_record = stack[1]
            parent_frame = parent_frame_record[0]
            parent_frame_info = inspect.getframeinfo(parent_frame)
            parent_frame_function_name = parent_frame_info.function
            return parent_frame_function_name
        # ... destroy frame to avoid reference cycle
        finally:
            del stack

    @staticmethod
    def read_test_output(full_file_name, current_function_name):
        r'''Reads test output.

        Returns list.
        '''
        segment_ly_file_name = '{}.ly'.format(current_function_name)
        directory_name = os.path.dirname(full_file_name)
        segment_ly_path_name = os.path.join(
            directory_name,
            segment_ly_file_name,
            )
        with open(segment_ly_path_name, 'r') as f:
            string = f.read()
        return string

    @staticmethod
    def test_function_name_to_title_lines(test_function_name):
        r'''Changes `test_function_name` to title lines.

        Returns list.
        '''
        from abjad.tools import sequencetools
        title_lines = []
        test_function_name = test_function_name[5:]
        if '__' in test_function_name:
            left_half, right_half = test_function_name.split('__')
            left_half = left_half.replace('_', ' ')
            title_lines.append(left_half)
            parts = right_half.split('_')
        else:
            parts = test_function_name.split('_')
        test_number = int(parts[-1])
        parts.pop(-1)
        if parts[0][0].isupper() and 1 < len(parts[0]):
            title_lines.append(parts.pop(0))
        lengths = [len(part) for part in parts]
        if 35 < sum(lengths):
            halves = sequencetools.partition_sequence_by_ratio_of_weights(
                lengths,
                [1, 1],
                )
            left_count = len(halves[0])
            right_count = len(halves[-1])
            assert left_count + right_count == len(lengths)
            left_parts = parts[:left_count]
            title_lines.append(' '.join(left_parts))
            right_parts = parts[-right_count:]
            right_parts.append(str(test_number))
            title_lines.append(' '.join(right_parts))
        else:
            title_words = ' '.join(parts)
            if 'schematic example' in title_words:
                space = ''
            else:
                space = ' '
            title = '{}{}{}'.format(title_words, space, test_number)
            title_lines.append(title)
        return title_lines

    @staticmethod
    def write_test_output(
        output,
        full_file_name,
        test_function_name,
        cache_ly=False,
        cache_pdf=False,
        go=False,
        render_pdf=False,
        ):
        r'''Writes test output.

        Returns none.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        from abjad.tools import topleveltools
        if go:
            cache_ly = cache_pdf = render_pdf = True
        if not any([cache_ly, cache_pdf, render_pdf]):
            return
        if isinstance(output, scoretools.Score):
            lilypond_file = \
                lilypondfiletools.make_floating_time_signature_lilypond_file(
                    output)
            TestManager.apply_additional_layout(lilypond_file)
            score = output
        elif isinstance(output, lilypondfiletools.LilyPondFile):
            lilypond_file = output
            score = lilypond_file.score_block[0]
        else:
            message = 'output must be score or LilyPond file: {!r}.'
            message = message.format(output)
            raise TypeError(message)
        title_lines = TestManager.test_function_name_to_title_lines(
            test_function_name)
        lilypond_file.header_block.title = \
            markuptools.make_centered_title_markup(
                title_lines,
                font_size=6,
                vspace_before=2,
                vspace_after=4,
                )
        parent_directory_name = os.path.dirname(full_file_name)
        if render_pdf:
            topleveltools.show(lilypond_file)
        if cache_pdf:
            file_name = '{}.pdf'.format(test_function_name)
            pdf_path_name = os.path.join(parent_directory_name, file_name)
            topleveltools.persist(lilypond_file).as_pdf(pdf_path_name)
        if cache_ly:
            file_name = '{}.ly'.format(test_function_name)
            ly_path_name = os.path.join(parent_directory_name, file_name)
            with open(ly_path_name, 'w') as f:
                f.write(format(score))
