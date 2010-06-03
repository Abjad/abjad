import os


home_path = os.environ.get('HOME') or os.environ.get('HOMEPATH')

ABJADCONFIG = os.path.join(home_path, '.abjad', 'config.py')
ABJADPATH = os.path.dirname(__file__).rstrip('cfg')
ABJADVERSIONFILE = os.path.join(ABJADPATH, '.version')
