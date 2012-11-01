from abjad.tools import *
import os


def write_test_output(score, full_file_name, test_function_name,
    cache_ly=False, cache_pdf=False, go=False, render_pdf=False):
    r'''.. versionadded:: 1.0
    '''
    from experimental import helpertools
    if go: cache_ly = cache_pdf = render_pdf = True
    if not any([cache_ly, cache_pdf, render_pdf]): return
    lilypond_file = lilypondfiletools.make_floating_time_signature_lilypond_file(score)
    helpertools.configure_multiple_voice_rhythmic_staves(lilypond_file)
    title_lines = test_function_name_to_title_lines(test_function_name)
    lilypond_file.header_block.title = markuptools.make_centered_title_markup(
        title_lines, font_size=6, vspace_before=2, vspace_after=4)
    lilypond_file.score.set.proportionalNotationDuration = schemetools.SchemeMoment((1, 48))
    parent_directory_name = os.path.dirname(full_file_name)
    if render_pdf:
        iotools.show(lilypond_file)
    if cache_pdf:
        file_name = '{}.pdf'.format(test_function_name)
        pdf_path_name = os.path.join(parent_directory_name, file_name)
        iotools.write_expr_to_pdf(lilypond_file, pdf_path_name)
    if cache_ly:
        file_name = '{}.ly'.format(test_function_name)
        ly_path_name = os.path.join(parent_directory_name, file_name)
        file(ly_path_name, 'w').write(score.lilypond_format)


def test_function_name_to_title_lines(test_function_name):
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
        halves = sequencetools.partition_sequence_by_ratio_of_weights(lengths, [1, 1])
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
        title = '{} {}'.format(title_words, test_number)
        title_lines.append(title)
    return title_lines
