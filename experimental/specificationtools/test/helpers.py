from abjad.tools import *
import baca.library as library
import os


def read_test_output(full_file_name, current_function_name):
    segment_ly_file_name = '{}.ly'.format(current_function_name)
    directory_name = os.path.dirname(full_file_name)
    segment_ly_path_name = os.path.join(directory_name, segment_ly_file_name)
    return file(segment_ly_path_name, 'r').read()


def write_test_output(score, full_file_name, test_function_name, 
    cache_ly=False, cache_pdf=False, go=False, render_pdf=False):
    if go: cache_ly = cache_pdf = render_pdf = True
    if not any([cache_ly, cache_pdf, render_pdf]): return
    lilypond_file = library.apply_baca_letter_layout(score)
    parts = test_function_name.split('_')
    test_number = int(parts[-1])
    title_words = ' '.join(parts[1:-1])
    title = '{} {}'.format(title_words, test_number)
    lilypond_file.header_block.title = markuptools.make_centered_title_markup(title, font_size=6)
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
        file(ly_path_name, 'w').write(score.format)
