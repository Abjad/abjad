from abjad import *
from abjad.cfg.cfg import  ABJADPATH
from abjad.cfg.cfg import  PDFVIEWER
from abjad.cfg.open_file import _open_file
from abjad.demos.desordre.helpers import *
import os

pitches_file = ABJADPATH +  os.sep.join(['demos', 'desordre', 'desordre_pitches.txt'])

def run_demo( ):
   print "\n* * * Patterns and polymetric music * * * "
   print "a reconstruction of the first measures of Ligeti's 'Desordre'"
   raw_input("\nLet's first see what we are after. Hit [Enter] to continue...")
   _open_file(ABJADPATH + \
      os.sep.join(['demos', 'desordre', 'desordre.pdf']), PDFVIEWER)
   raw_input("Notice how the first several bars of the piece are made up of a single pattern, a two voice nucleus comprised of an octave in the upper staff and a run of 1/8th notes in the lower voice. Let's call this a 'Ligeti class'. The pitch sequences in the piece, however, are less redundant...")

   raw_input("\nLet's see the raw pitch data used by Ligeti...")
   _open_file(pitches_file)

   line =  'pitches = load_desordre_pitches(pitches_file)'
   raw_input("\nLet's load our raw pitch data into 'pitches'...")
   print line
   exec(line)
   #print pitches
   raw_input("\n'pitches' is a depth-2 list. pitches[i] are all the pitches in the i'th hand, pitches[i][j] are the pitches in the j'th measure, and pitces[i][j][k] are the pitches making up the k'th 'Ligeti object'...")

   line = 'run = desordre_run(pitches[0][0][0])'
   print "\nWe construct a single 'Ligeti object' like so:"
   print line
   exec(line)
   raw_input("\nLet's display what we have created...")
   show(Staff([run]), 'tirnaveni')

   line = 'multimeasures = multimeasure_build(pitches[0])'
   raw_input("\nLet's exploit the pattern further and use higher level constructs. The fact that the 'Ligeti objects' are subsumed in the measures, so let's use a measure builder...")
   print line
   exec(line)
   raw_input("\nLet's display what we have created...")
   show(Staff(multimeasures), 'tirnaveni')

   line = 'desordre = desordre_build(pitches)'
   raw_input("\nThis is, of course, only one hand. Let's create the complete opening of the score with our even higher construct: desordre_build( )")
   print line
   exec(line)
   raw_input("\nLet's display what we have created...")
   show(desordre, 'tirnaveni')

   line = 'for run in pitches[0]: run[0].reverse( ); run.reverse( )'
   raw_input("\nNow that we have 'Desordre' encoded in Abjad, we can play around with the data in the piece. Let's shuffle the sequences around a bit...")
   print line
   exec(line)

   line = 'desordre_retro = desordre_build(pitches)'
   raw_input("\nWe now reconstruct the modified Ligeti...")
   print line
   exec(line)
   raw_input("\nLet's display what we have created...")
   show(desordre_retro, 'tirnaveni')

   



if __name__ == '__main__':
   run_demo( )
