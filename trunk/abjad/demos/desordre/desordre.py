#from abjad import *
#from abjad.cfg.cfg import  ABJADPATH
#from abjad.cfg.cfg import  PDFVIEWER
#from abjad.cfg.open_file import _open_file
#from abjad.demos.desordre.helpers import *
#import os

from abjad.demos.presentation.presentation import *


title = "Patterns and polymetric music"
abstract = "A reconstruction of the first measures of Ligeti's 'Desordre'"

statements = [ ]

### statements
text = "Let's first see what we are after."
code = '_open_file(desordre, PDFVIEWER)'
s = Statement(text, code)
statements.append(s)

text = "Notice how the first several bars of the piece are made up of a single pattern, a two voice nucleus comprised of an octave in the upper voice and a run of 1/8th notes in the lower voice. Let's call this a 'Ligeti class'. The pitch sequences in the piece, however, are less redundant."
code = [ ]
s = Statement(text, code)
statements.append(s)


text = "Let's see the raw pitch data used by Ligeti."
code = '_open_file(pitches_file)'
s = Statement(text, code)
statements.append(s)


text = "Let's load our raw pitch data into 'pitches'."
code =  'pitches = load_desordre_pitches(pitches_file)'
s = Statement(text, code)
statements.append(s)


text = "'pitches' is a depth-2 list. pitches[i] are all the pitches in the i'th hand, pitches[i][j] are the pitches in the j'th measure, and pitces[i][j][k] are the pitches making up the k'th 'Ligeti object'. \nWe construct a single 'Ligeti object' like so:"
code = 'run = desordre_run(pitches[0][0][0])'
s = Statement(text, code)
statements.append(s)


text = "Let's display what we have created."
code = "show(Staff([run]), 'tirnaveni')"
s = Statement(text, code)
statements.append(s)


text = "Let's exploit the pattern further and use higher level constructs. Observe that the 'Ligeti objects' are subsumed in the measures, so let's use a measures builder..."
code = 'multimeasures = multimeasure_build(pitches[0])'
s = Statement(text, code)
statements.append(s)

text = "Let's display what we have created."
code = "show(Staff(multimeasures), 'tirnaveni')"
s = Statement(text, code)
statements.append(s)


text = "This is, of course, only one hand. Let's create the complete opening of the score with an even higher construct: desordre_build( )"
code = 'desordre = desordre_build(pitches)'
s = Statement(text, code)
statements.append(s)


text = "Let's display what we have created."
code = "show(desordre, 'tirnaveni')"
s = Statement(text, code)
statements.append(s)

text = "Now that we have 'Desordre' encoded in Abjad, we can play around with the data in the piece. Let's shuffle the sequences around a bit."
code = 'for run in pitches[0]: run[0].reverse( ); run.reverse( )'
s = Statement(text, code)
statements.append(s)


code = 'desordre_retro = desordre_build(pitches)'
text = "We now reconstruct the modified Ligeti."
s = Statement(text, code)
statements.append(s)


text = "Let's display what we have created."
code = "show(desordre_retro, 'tirnaveni')"
s = Statement(text, code)
statements.append(s)


### presentation
p = Presentation(title, abstract, statements)
p.setup.append('from abjad.cfg.cfg import ABJADPATH')
p.setup.append('from abjad.cfg.cfg import PDFVIEWER')
p.setup.append('from abjad.demos.desordre.helpers import *')
p.setup.append('import os')
p.setup.append('from abjad.cfg.open_file import _open_file')
p.setup.append("desordre = ABJADPATH + \
os.sep.join(['demos', 'desordre', 'desordre.pdf'])")
p.setup.append("pitches_file = ABJADPATH +  \
os.sep.join(['demos', 'desordre', 'desordre_pitches.txt'])")



if __name__ == '__main__':
   p.run( )
   
