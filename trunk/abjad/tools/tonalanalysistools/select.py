# -*- encoding: utf-8 -*-


def select(expr):
    r'''Select `expr` for tonal analysis.

    Return tonal analysis selection.
    '''
    from abjad.tools import componenttools
    from abjad.tools import tonalanalysistools
    if isinstance(expr, componenttools.Component):
        return tonalanalysistools.TonalAnalysisSelection(expr)
    elif hasattr(expr, '_music'):
        music = expr._music
        return tonalanalysistools.TonalAnalysisSelection(music)
    else:
        return tonalanalysistools.TonalAnalysisSelection(expr)
