# -*- coding: utf-8 -*-


def analyze(argument):
    r'''Makes tonal analysis agent.

    Returns tonal analysis agent.
    '''
    import abjad
    if isinstance(argument, abjad.Component):
        return abjad.tonalanalysistools.TonalAnalysisAgent(argument)
    elif hasattr(argument, '_music'):
        music = argument._music
        return abjad.tonalanalysistools.TonalAnalysisAgent(music)
    else:
        return abjad.tonalanalysistools.TonalAnalysisAgent(argument)
