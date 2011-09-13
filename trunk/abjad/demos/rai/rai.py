from abjad.demos.presentation.presentation import *


title = "Rhythmic slicing and dicing"
subtitle = "A reconstruction of the first few measure of Stephen Leman's 'Rai' "
abstract = 'We are interested in having an irregular rhythmic sequence based on prime numbers. We will construct our score additively, concatenating durations regardless of any metric hierarchy.'


# statements
statements = [ ]

text = "We first define a sequence of primes."
code ='durations = [5, 7, 2, 11, 13, 5, 13, 3,]'
s = Statement(text, code)
statements.append(s)


text = "Let's set our duration 'quatum' to one sixteenth and create \
duration tokens."
code = ['durations = sequencetools.zip_sequences_cyclically(durations, 16)', 'durations']
s = Statement(text, code)
statements.append(s)


text = 'From these duration tokens we now create a list of Notes.'
code = 'notes = notetools.make_notes(0, durations)'
s = Statement(text, code)
statements.append(s)


text = "Let's put these notes inside a rhythmic sketch staff and see what \
we've got."
code = ['s = stafftools.make_rhythmic_sketch_staff(notes)', "show(s, 'tirnaveni')"]
s = Statement(text, code)
statements.append(s)


#code = ['spannertools.MetricGridSpanner(s, [(4, 4), (4, 4), (4, 4), (11, 16)])',
#         's.meter.clear( )', 's.bar_line.clear( )', "show(s, 'tirnaveni')"]
code = ['spannertools.MetricGridSpanner(s, [(4, 4), (4, 4), (4, 4), (11, 16)])',
            'del(s.override.time_signature)', 'del(s.override.bar_line)', "show(s, 'tirnaveni')"]
text = "Let's then apply a MetricGrid spanner on our staff."
s = Statement(text, code)
statements.append(s)


code = ['meters = [(1, 4)] * 4 + [(2, 4)] + [(1, 4)] * 6 + [(2, 4)] + \
[(3, 16)]', 'partition.leaves_cyclic_unfractured_by_durations(s, meters)']
text = "Notice how some notes span more than one measure (i.e. they extend over the bar lines). This is a good thing because it shows that note durations and meter are treated independently. We do not want these spanning notes in our final score, however. We also want to give the performer a visual reference of where the beats are, so we will split the notes accordingly. To do this we will slice the music to a second sequence of meters."
s = Statement(text, code)
statements.append(s)


text = "Let's see the final result. The final score is a sequence of notes that together represent our original sequence of durations, but that are now subsumed to a series of measures and beat subdivisions."
code = "show(s, 'tirnaveni')"

s = Statement(text, code)
statements.append(s)

p = Presentation(title, abstract, statements, subtitle)

p.setup.append('from abjad import *')
p.setup.append('from abjad.tools import leaftools')


if __name__ == '__main__':
    import sys
    if 1 < len(sys.argv):
        p.run(sys.argv[1])
    else:
        p.run( )
else:
    for expr in p.setup:
        exec(expr)
