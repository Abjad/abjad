# -*- encoding: utf-8 -*-
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools


# TODO: move to lilypondfiletools
def insert_expr_into_lilypond_file(expr, tagline=False):
    r'''Inserts `expr` into LilyPond file.

    Returns LilyPond file.
    '''
    from abjad.tools import contexttools

    if isinstance(expr, lilypondfiletools.LilyPondFile):
        lilypond_file = expr
    elif isinstance(expr, contexttools.Context):
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
    if not tagline:
        try:
            lilypond_file.header_block.tagline = markuptools.Markup('""')
        except:
            pass
    return lilypond_file
