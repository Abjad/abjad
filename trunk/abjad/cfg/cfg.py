import os


ABJADPATH = os.environ.get(
   'ABJADPATH', os.path.dirname(__file__).rstrip('/cfg')).rstrip(os.sep)
ABJADOUTPUT = os.environ.get(
   'ABJADOUTPUT', ABJADPATH + '/output').rstrip(os.sep)
ABJADPERSISTENCE = os.environ.get(
   'ABJADPERSISTENCE', ABJADPATH + '/persistence').rstrip(os.sep)
ABJADTEMPLATES = os.environ.get(
   'ABJADTEMPLATES', ABJADPATH + '/templates').rstrip(os.sep)
LILYPONDINCLUDES = os.environ.get('LILYPONDINCLUDES', None)
LILYPONDLANG = os.environ.get('LILYPONDLANG', 'english')
PDFVIEWER = os.environ.get('PDFVIEWER', 'open')
VERSIONFILE = ABJADOUTPUT + '.version'

accidental_spelling = 'mixed'
