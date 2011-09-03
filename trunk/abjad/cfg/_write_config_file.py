from abjad.cfg.cfg import ABJADCONFIG
from abjad.cfg.cfg import ABJADPATH
from abjad.cfg.cfg import HOME
import os
import time


def _write_config_file(path, dict):

    preamble = '# -*- coding: utf-8 -*-\n'
    preamble += '# \n'
    preamble += '# Abjad configuration file, created by Abjad on %s.\n' % \
        time.strftime("%d %B %Y %H:%M:%S")
    preamble += '#\n'
    preamble += '# This file is Python execfile()d and should thus follow\n'
    preamble += "# Python's syntax.\n"
    preamble += '\n\n'
    preamble += "# Configuration Variables ---------------------------------"
    preamble += '\n\n'

    abjad_config_dir = os.path.dirname(ABJADCONFIG)
    if not os.path.isdir(abjad_config_dir):
        os.mkdir(abjad_config_dir)

    # write file
    f = open(path, 'w')

    f.write(preamble)

    for key in sorted(dict.keys( )):
        f.write(dict[key]['comment'] + '\n')
        f.write('%s = ' % key)
        if isinstance(dict[key]['value'], str):
            f.write("'%s'\n\n" % dict[key]['value'])
        else:
            f.write("%s\n\n" % dict[key]['value'])

    f.close( )
