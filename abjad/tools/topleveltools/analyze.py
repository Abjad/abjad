import collections


def analyze(argument):
    r'''Makes tonal analysis agent.

    Returns tonal analysis agent.
    '''
    import abjad
    leaves = abjad.select(argument).leaves()
    return abjad.tonalanalysistools.TonalAnalysis(leaves)
