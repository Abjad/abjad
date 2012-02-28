import os


# Python evaluates the clauses in an or-statement one at a time from left to right.
# Python returns true on the first clause that evaluates to true, or false if none eval to true.
# So the order of the cascade here is set to HOME then HOMEPATH then APPDATA.
# The reason for this is that HOME should be defined for all OS X and Linux distros.
# Windows will not define HOME but will usually define both HOMEPATH and APPDATA.
# But note that Windows usually defines HOMEPATH and APPDATA differently.
# So hand testing between Windows and OS X.
# Windows appears to set HOMEPATH similarly to the way OS X sets HOME.
# As a final fallback, accept the setting of APPDATA under Windows.
#HOME = os.environ.get('HOME') or os.environ.get('APPDATA') or os.environ.get('HOMEPATH')
HOME = os.environ.get('HOME') or os.environ.get('HOMEPATH') or os.environ.get('APPDATA')

ABJADCONFIG = os.path.join(HOME, '.abjad', 'config.py')
ABJADPATH = os.path.abspath(os.path.dirname(__file__).rstrip('cfg'))
ABJADVERSIONFILE = os.path.join(ABJADPATH, '.version')

abjad_version_number = '2.7'
