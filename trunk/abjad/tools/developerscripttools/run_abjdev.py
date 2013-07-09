def run_abjdev():
    '''Entry point for setuptools.

    One-line wrapper around AbjDevScript.
    '''
    from abjad.tools import developerscripttools

    developerscripttools.AbjDevScript()()
