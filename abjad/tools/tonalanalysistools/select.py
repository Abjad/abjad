# -*- coding: utf-8 -*-


def select(expr):
    r'''Select `expr` for tonal analysis.

    Returns tonal analysis selection.
    '''
    from abjad.tools import scoretools
    from abjad.tools import tonalanalysistools
    if isinstance(expr, scoretools.Component):
        return tonalanalysistools.TonalAnalysisAgent(expr)
    elif hasattr(expr, '_music'):
        music = expr._music
        return tonalanalysistools.TonalAnalysisAgent(music)
    else:
        return tonalanalysistools.TonalAnalysisAgent(expr)
