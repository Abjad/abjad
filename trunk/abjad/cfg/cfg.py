from os import environ

ABJADOUTPUT = environ.get('ABJADOUTPUT', '/home/abjad/output/')
VERSIONFILE = ABJADOUTPUT + '.version'
PDFVIEWER = environ.get('PDFVIEWER', 'open')
