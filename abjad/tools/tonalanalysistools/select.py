# -*- coding: utf-8 -*-


def select(argument):
    r'''Select `argument` for tonal analysis.

    Returns tonal analysis selection.
    '''
    from abjad.tools import scoretools
    from abjad.tools import tonalanalysistools
    if isinstance(argument, scoretools.Component):
        return tonalanalysistools.TonalAnalysisAgent(argument)
    elif hasattr(argument, '_music'):
        music = argument._music
        return tonalanalysistools.TonalAnalysisAgent(music)
    else:
        return tonalanalysistools.TonalAnalysisAgent(argument)
