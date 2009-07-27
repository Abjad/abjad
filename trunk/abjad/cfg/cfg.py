import os


#accidental_spelling = 'mixed'
home_path = os.environ.get('HOME') or os.environ.get('HOMEPATH')

ABJADCONFIG = os.path.join(home_path, '.abjad', 'config.py')
#ABJADOUTPUT = os.environ.get('ABJADOUTPUT', 
#         os.path.join(home_path, '.abjad', 'output'))
ABJADPATH = os.path.dirname(__file__).rstrip('cfg')

#ABJADTEMPLATES = [ ]
#_user = os.environ.get('ABJADTEMPLATES', None)
#if _user is not None:
#   ABJADTEMPLATES.extend(_user.split(os.path.pathsep))
#ABJADTEMPLATES.append(ABJADPATH + 'templates')
#ABJADTEMPLATES = os.path.join(ABJADTEMPLATES)

ABJADVERSIONFILE = os.path.join(ABJADPATH, '.version')
#LILYPONDINCLUDES = os.environ.get('LILYPONDINCLUDES', None)
#LILYPONDLANG = os.environ.get('LILYPONDLANG', 'english')
