import os

home_path = os.environ.get('HOME') or os.environ.get('HOMEPATH')

ABJADPATH = os.path.dirname(__file__).rstrip('cfg')
ABJADOUTPUT = os.environ.get('ABJADOUTPUT', 
         home_path + os.sep + os.sep.join(['.abjad', 'output']))
ABJADTEMPLATES = os.environ.get('ABJADTEMPLATES', ABJADPATH + 'templates')
ABJADVERSIONFILE = ABJADPATH + '.version'
LILYPONDINCLUDES = os.environ.get('LILYPONDINCLUDES', None)
LILYPONDLANG = os.environ.get('LILYPONDLANG', 'english')
PDFVIEWER = os.environ.get('PDFVIEWER')
MIDIPLAYER = os.environ.get('MIDIPLAYER')

accidental_spelling = 'mixed'


#### we don't need ABJADPATH defined as environment variable any more.
##ABJADPATH = os.environ.get(
##   'ABJADPATH', os.path.dirname(__file__).rstrip('/cfg')).rstrip(os.sep)
#ABJADPATH = os.path.dirname(__file__).rstrip('cfg').rstrip(os.sep)
#ABJADOUTPUT = os.environ.get(
#   'ABJADOUTPUT', ABJADPATH + '/.abjad/output').rstrip(os.sep)
#ABJADPERSISTENCE = os.environ.get(
#   'ABJADPERSISTENCE', ABJADPATH + '/persistence').rstrip(os.sep)
#ABJADTEMPLATES = os.environ.get(
#   'ABJADTEMPLATES', ABJADPATH + '/templates').rstrip(os.sep)
#LILYPONDINCLUDES = os.environ.get('LILYPONDINCLUDES', None)
#LILYPONDLANG = os.environ.get('LILYPONDLANG', 'english')
#PDFVIEWER = os.environ.get('PDFVIEWER', 'open')
##VERSIONFILE = ABJADOUTPUT + '.version'
#ABJADVERSIONFILE = ABJADPATH + '/.version'
##LILYPONDVERSIONFILE = ABJADOUTPUT + '/.version'
#
#accidental_spelling = 'mixed'
