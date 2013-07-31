# -*- encoding: utf-8 -*-
def run_abjadbook():
    r'''Entry point for setuptools.

    One-line wrapper around AbjadBookScript.
    '''
    from abjad.tools import abjadbooktools

    abjadbooktools.AbjadBookScript()()
