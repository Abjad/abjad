def analyze(argument):
    r'''Makes tonal analysis agent.

    Returns tonal analysis agent.
    '''
    import abjad
    if isinstance(argument, abjad.Component):
        return abjad.tonalanalysistools.TonalAnalysis(argument)
    elif hasattr(argument, 'components'):
        components = argument.components
        return abjad.tonalanalysistools.TonalAnalysis(components)
    else:
        return abjad.tonalanalysistools.TonalAnalysis(argument)
