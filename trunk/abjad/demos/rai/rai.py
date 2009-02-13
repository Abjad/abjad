from abjad import *
from abjad.tools import construct
from abjad.demos.presentation.presentation import *


title = "Rhythmic slicing and dicing"
subtitle = "A reconstruction of the first few measure of Stephen Leman's 'Rai' "
abstract = 'We are interested in having an irregular rhythmic sequence based on prime numbers. We will construct our score additively, concatenating durations regardless of any metric hierarchy.'


### statements
statements = [ ]

text = "We first define a sequence of primes."
code ='durations = [5, 7, 2, 11, 13, 5, 13, 3,]'
s = Statement(text, code)
statements.append(s)


text = "Let's set our duration 'quatum' to one sixteenth and create \
duration tokens."
code = ['durations = zip_cycle(durations, 16)', 'durations']
s = Statement(text, code)
statements.append(s)


text = 'From these duration tokens we now create a list of Notes.'
code = 'notes = construct.notes(0, durations)'
s = Statement(text, code)
statements.append(s)


text = "Let's put these notes inside a RhythmicSketchStaff and see what \
we've got."
code = ['s = RhythmicSketchStaff(notes)', "show(s, 'tirnaveni')"]
s = Statement(text, code)
statements.append(s)


code = ['MetricGrid(s, [(4, 4), (4, 4), (4, 4), (11, 16)])', 
         's.meter.clear( )', 's.barline.clear( )', "show(s, 'tirnaveni')"]
text = "Let's then apply a MetricGrid spanner on our staff."
s = Statement(text, code)
statements.append(s)
   

code = ['meters = [(1, 4)] * 4 + [(2, 4)] + [(1, 4)] * 6 + [(2, 4)] + \
[(3, 16)]', 'metric_slice(s, meters)']
text = "Notice how some notes span more than one measure (i.e. they extend over the bar lines). This is a good thing because it shows that note durations and meter are treated independently. We do not want these spanning notes in our final score, however. We also want to give the performer a visual reference of where the beats are, so we will split the notes accordingly. To do this we will slice the music to a second sequence of meters."
s = Statement(text, code)
statements.append(s)


text = "Let's see the final result. The final score is a sequence of notes that together represent our original sequence of durations, but that are now subsumed to a series of measures and beat subdivisions."
code = "show(s, 'tirnaveni')"

s = Statement(text, code)
statements.append(s)

p = Presentation(title, abstract, statements, subtitle)



if __name__ == '__main__':
   p.run( )


#def run_demo( ):
#   print('''
#   * * * Rhythmic slicing and dicing * * *
#   A reconstruction of the first few measure of Stephen Leman's 'Rai'
#
#   We are interested in having an irregular rhythmic sequence based on prime numbers. We will construct our score additively, concatenating durations regardless of any metric hierarchy.''')
#   
#   line = 'durations = [5, 7, 2, 11, 13, 5, 13, 3,]'
#   #               5, 11, 3, 3, 11, 7, 3, 13, 2,
#   #               5, 2, 3, 7, 2, 3, 2, 11, 7, 3, 11, 2,
#   #            ]
#   raw_input("\nWe first define a sequence of primes... (press Enter)")
#   print line
#   exec(line)
#   
#   line = 'durations = zip_cycle(durations, 16)'
#   raw_input("\nLet's set our duration 'quatum' to one sixteenth and create duration tokens...")
#   print line
#   exec(line)
#   print durations
#
#   line = 'notes = construct.notes(0, durations)'
#   raw_input("\nFrom these duration tokens we now create a list of Notes...")
#   print line
#   exec(line)
#
#   line = 's = RhythmicSketchStaff(notes)'
#   raw_input("\nLet's put these notes inside a RhythmicSketchStaff and see what we've got...")
#   print line
#   exec(line)
#   show(s, 'tirnaveni')
#
#   lines = ['MetricGrid(s, [(4, 4), (4, 4), (4, 4), (11, 16)])', 
#            s.meter.clear, s.barline.clear]
#   raw_input("\nLet's then apply a MetricGrid spanner on our staff...")
#   for line in lines:
#      if isinstance(line, basestring):
#         print line
#         exec(line)
#      else:
#         line( )
#   show(s, 'tirnaveni')
#
#   lines = ['meters = [(1, 4)] * 4 + [(2, 4)] + [(1, 4)] * 6 + [(2, 4)] + [(3, 16)]',           'metric_slice(s, meters)']
#   raw_input("\nNotice how some notes span more than one measure (i.e. they extend over the bar lines). This is a good thing because it shows that note durations and meter are treated independently. We do not want these spanning notes in our final score, however. We also want to give the performer a visual reference of where the beats are, so we will split the notes accordingly. To do this we will slice the music to a second sequence of meters...")
#   for line in lines:
#      print line
#      exec(line)
#
#   raw_input("\nLet's see the final result...")
#   show(s, 'tirnaveni')
#   print "The final score is a sequence of notes that together represent our original sequence of durations, but that are now subsumed to a series of measures and beat subdivisions."
#

