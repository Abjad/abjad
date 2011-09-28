from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from abjad.tools.iotools._template_name_to_template_path import _template_name_to_template_path


def _insert_expr_into_lilypond_file(expr, template=None, tagline=False):
    from abjad.tools.contexttools._Context import _Context

    if isinstance(expr, lilypondfiletools.LilyPondFile):
        lilypond_file = expr
    elif isinstance(expr, _Context):
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(expr)
        lilypond_file._is_temporary = True
    else:
        lilypond_file = lilypondfiletools.make_basic_lilypond_file()
        score_block = lilypondfiletools.ScoreBlock()
        score_block.append(expr)
        # NOTE: don't quite understand the logic here.
        # why append a score_block and then set the score_block attribute
        # to the same thing?
        lilypond_file.append(score_block)
        #lilypond_file.score = score_block
        lilypond_file.score_block = score_block
        lilypond_file._is_temporary = True

    if template is not None:
        template_path = _template_name_to_template_path(template)
        lilypond_file.file_initial_user_includes.append(template_path)

    if not tagline:
        lilypond_file.header_block.tagline = markuptools.Markup('""')

    return lilypond_file
