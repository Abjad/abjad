import os


## TODO: Implement list_settings( ) helper to print all of these
##       settings at the interpreter in a friendly way
##       to allow composers who are not reading the soruce
##       code to inspect these settings.

accidental_spelling = 'mixed'
home_path = os.environ.get('HOME') or os.environ.get('HOMEPATH')

ABJADCONFIG = os.path.join(home_path, '.abjad', 'config')
ABJADOUTPUT = os.environ.get('ABJADOUTPUT', 
         os.path.join(home_path, '.abjad', 'output'))
ABJADPATH = os.path.dirname(__file__).rstrip('cfg')

ABJADTEMPLATES = [ ]
user = os.environ.get('ABJADTEMPLATES', None)
if user is not None:
   ABJADTEMPLATES.extend(user.split(os.path.pathsep))
ABJADTEMPLATES.append(ABJADPATH + 'templates')
ABJADTEMPLATES = os.path.join(ABJADTEMPLATES)

ABJADVERSIONFILE = ABJADPATH + '.version'
ABJADVERSIONFILE = os.path.join(ABJADPATH, '.version')
LILYPONDINCLUDES = os.environ.get('LILYPONDINCLUDES', None)
LILYPONDLANG = os.environ.get('LILYPONDLANG', 'english')
MIDIPLAYER = os.environ.get('MIDIPLAYER')
PDFVIEWER = os.environ.get('PDFVIEWER')
