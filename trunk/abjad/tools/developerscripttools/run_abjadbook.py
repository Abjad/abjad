def run_abjadbook():
    '''Entry point for setuptools.

    One-line wrapper around AbjadBookScript.
    '''
    from abjad.tools import abjadbooktools

    abjadbooktools.AbjadBookScript()()
