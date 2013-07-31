# -*- encoding: utf-8 -*-
def run_abjdev():
    r'''Entry point for setuptools.

    One-line wrapper around AbjDevScript.
    '''
    from abjad.tools import developerscripttools

    developerscripttools.AbjDevScript()()
