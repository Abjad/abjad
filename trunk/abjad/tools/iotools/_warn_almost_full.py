from abjad.tools import configurationtools


# TODO: make public and possibly improve function name
def _warn_almost_full(last_number):
    from abjad import ABJCFG

    ABJADOUTPUT = ABJCFG['abjad_output']
    max_number = 10000
    lines = [
        '',
        'WARNING: Abjad output directory almost full!',
        'Abjad output directory contains %s files and only %s are allowed.' % (
            last_number, max_number),
        'Please empty %s soon!' % ABJADOUTPUT,
        '']
    for line in lines:
        print line.center(80)
