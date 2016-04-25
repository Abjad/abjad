# -*- coding: utf-8 -*-


def inspect_(expr):
    r'''Inspects `expr`.

    Factory function.

    Returns inspect agent.
    '''
    from abjad.tools import agenttools
    return agenttools.InspectionAgent(expr)
