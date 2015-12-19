# -*- coding: utf-8 -*-


def label(expr):
    r'''Labels `expr`.

    Returns label agent.
    '''
    from abjad.tools import agenttools
    return agenttools.LabelAgent(expr)