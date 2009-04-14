from abjad.cfg.cfg import ABJADOUTPUT
import os


def log( ):
   os.system('vi %s%slily.log' % (ABJADOUTPUT, os.sep))
