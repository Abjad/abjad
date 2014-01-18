# -*- encoding: utf-8 -*-
import inspect
import os


class TestManager(object):
    r'''Manages test logic.
    '''

    @staticmethod
    def apply_additional_layout(lilypond_file):
        r'''Configures multiple-voice rhythmic staves in `lilypond_file`.

        Operates in place.
        
        Returns none.
        '''
        from abjad.tools import layouttools
        from abjad.tools import scoretools
        from abjad.tools import topleveltools
        # configure multiple-voice rhythmic staves
        for staff in topleveltools.iterate(lilypond_file.score_block[0]
            ).by_class(scoretools.Staff):
            if staff.is_simultaneous:
                assert len(staff) == 2
                voice_1 = staff[0]
                topleveltools.override(voice_1).note_head.Y_offset = 0.5
                topleveltools.override(voice_1).stem.direction = Up
                voice_2 = staff[1]
                topleveltools.override(voice_2).note_head.Y_offset = -0.5
                topleveltools.override(voice_2).stem.direction = Down
                spacing_vector = layouttools.make_spacing_vector(0, 0, 6, 0)
                topleveltools.override(staff
                    ).vertical_axis_group.staff_staff_spacing = spacing_vector
        # provide more space between staves with pitched notes
        for staff in topleveltools.iterate(
            lilypond_file.score_block[0]).by_class(scoretools.Staff):
            if not isinstance(staff, scoretools.RhythmicStaff):
                for item in lilypond_file.layout_block.items:
                    if isinstance(item, lilypondfiletools.ContextBlock):
                        if item.context_name == 'StaffGroup':
                            break
                else:
                    message = 'no staff group context block found.'
                    raise Exception(message)
                spacing_vector = layouttools.make_spacing_vector(0, 0, 6, 0)
                topleveltools.override(context_block
                    ).vertical_axis_group.staff_staff_spacing = spacing_vector
            break

    @staticmethod
    def compare(string_1, string_2):
        r'''Compares `string_1` to `string_2`.

        Massage newlines.

        Returns boolean.
        '''
        if not isinstance(string_1, str):
            string_1 = format(string_1)
        split_lines = string_2.split('\n')
        if not split_lines[0] or split_lines[0].isspace():
            split_lines.pop(0)
        if not split_lines[-1] or split_lines[-1].isspace():
            split_lines.pop(-1)
        for indent_width, character in enumerate(split_lines[0]):
            if character != ' ':
                break
        tab_string = 4 * ' '
        massaged_lines = []
        for split_line in split_lines:
            massaged_line = split_line[indent_width:]
            #massaged_line = massaged_line.replace(tab_string, '\t')
            massaged_lines.append(massaged_line)
        massaged_string = '\n'.join(massaged_lines)
        return string_1.replace('\t', '    ') == massaged_string

    @staticmethod
    def get_current_function_name():
        r'''Gets current function name.

        ::

            >>> def foo():
            ...        function_name = systemtools.TestManager.get_current_function_name()
            ...        print 'Function name is {!r}.'.format(function_name)

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
        return file(segment_ly_path_name, 'r').read()

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
        from abjad.tools import schemetools
        from abjad.tools import scoretools
        from abjad.tools import systemtools
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
            raise TypeError(output)
        title_lines = TestManager.test_function_name_to_title_lines(
            test_function_name)
        lilypond_file.header_block.title = \
            markuptools.make_centered_title_markup(
                title_lines,
                font_size=6,
                vspace_before=2,
                vspace_after=4,
                )
        moment = schemetools.SchemeMoment((1, 48))
        topleveltools.set_(lilypond_file.score
            ).proportionalNotationDuration = moment
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
            file(ly_path_name, 'w').write(format(score))
