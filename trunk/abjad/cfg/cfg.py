import os


HOME = os.environ.get('HOME') or os.environ.get('HOMEPATH')
ABJADCONFIG = os.path.join(HOME, '.abjad', 'config.py')
ABJADPATH = os.path.abspath(os.path.dirname(__file__).rstrip('cfg'))
ABJADVERSIONFILE = os.path.join(ABJADPATH, '.version')
