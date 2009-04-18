from abjad.cfg.cfg import ABJADOUTPUT
import os


def log( ):
   os.system('vi %s' % os.path.join(ABJADOUTPUT, 'lily.log'))
