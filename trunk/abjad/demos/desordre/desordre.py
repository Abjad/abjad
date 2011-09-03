from abjad.demos.presentation.presentation import *


title = "Patterns and polymetric music"
abstract = "A reconstruction of the first measures of Ligeti's 'Desordre'"

statements = [ ]

# statements
text = "Let's first see what we are after."
code = 'open_file(desordre)'
s = Statement(text, code)
statements.append(s)


text = "Notice how the first several bars of the piece are made up of a single pattern, a two voice nucleus comprised of an octave in the upper voice and a run of 1/8th notes in the lower voice. Let's call this a 'Ligeti cell'. The pitch sequences in the piece, however, are less redundant."
code = [ ]
s = Statement(text, code)
statements.append(s)


text = "Let's see the raw pitch data used by Ligeti."
code = 'open_file(pitches_file)'
s = Statement(text, code)
statements.append(s)


text = "Let's load our raw pitch data into 'pitches'."
code =  'pitches = load_desordre_pitches(pitches_file)'
s = Statement(text, code)
statements.append(s)


text = "'pitches' is a depth-2 list. pitches[i] are all the pitches in the i'th hand, pitches[i][j] are the pitches in the j'th measure, and pitces[i][j][k] are the pitches making up the k'th 'Ligeti object'. \nWe construct a single 'Ligeti object' like so:"
code = 'run = desordre_cell(pitches[0][0][0])'
s = Statement(text, code)
statements.append(s)


text = "Let's display what we have created."
code = "show(Staff([run]), 'tirnaveni')"
s = Statement(text, code)
statements.append(s)


text = "Let's exploit the pattern further and use higher level constructs. Observe that the 'Ligeti objects' are subsumed in the measures, so let's use a measure builder..."
code = 'measure = measure_build(pitches[0][0])'
s = Statement(text, code)
statements.append(s)


text = "Let's display what we have created."
code = "show(Staff([measure]), 'tirnaveni')"
s = Statement(text, code)
statements.append(s)


text = "The measure builder can make any number of 'Ligeti cells'."
code = 'measure = measure_build([[0,2], [0,2,0,2], [0,2,0,2,0]])'
s = Statement(text, code)
statements.append(s)


text = "Let's display what we have created."
code = "show(Staff([measure]), 'tirnaveni')"
s = Statement(text, code)
statements.append(s)


text = "Now let's create several measures at a time using the staff_build..."
code = 'multimeasures = staff_build(pitches[0])'
s = Statement(text, code)
statements.append(s)


text = "Let's display what we have created."
code = "show(multimeasures, 'tirnaveni')"
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

text = "And let's hear it too."
code = "play(desordre)"
s = Statement(text, code)
statements.append(s)


text = "Now that we have 'Desordre' encoded in Abjad, we can play around with the data in the piece. Let's shuffle the sequences around a bit."
code = 'for measure in pitches[0]: measure[0].reverse( ); measure.reverse( )'
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


text = "And let's hear it too."
code = "play(desordre_retro)"
s = Statement(text, code)
statements.append(s)


# presentation
p = Presentation(title, abstract, statements)
p.setup.append('from abjad import *')
p.setup.append('from abjad.cfg.cfg import ABJADPATH')
p.setup.append('from abjad.cfg._open_file import _open_file as open_file')
p.setup.append('from abjad.demos.desordre.helpers import *')
p.setup.append('import os')
p.setup.append("desordre = ABJADPATH + \
os.path.join('demos', 'desordre', 'desordre.pdf')")
p.setup.append("pitches_file = ABJADPATH +  \
os.path.join('demos', 'desordre', 'desordre_pitches.txt')")


if __name__ == '__main__':
    import sys
    if 1 < len(sys.argv):
        p.run(sys.argv[1])
    else:
        p.run( )
else:
    for expr in p.setup:
        exec(expr)
