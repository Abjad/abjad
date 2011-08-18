from abjad.cfg.cfg import ABJADVERSIONFILE
import os


def _write_abjad_version_file():
    version = os.popen('svnversion').read().strip()
    file(ABJADVERSIONFILE, 'w').write(version)
