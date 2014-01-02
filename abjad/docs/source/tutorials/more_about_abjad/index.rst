More about Abjad
================


How it works
------------

How does Python suddenly know what musical notes are?
And how to make musical score?

Use Python's ``dir()`` built-in to get a sense of the answer:

::

   >>> dir()
   ['Articulation', 'Beam', 'Chord', 'Clef', 'Container', 'Crescendo',
   'Decrescendo', 'Duration', 'Dynamic', 'Fraction', 'Glissando', 'Hairpin',
   'KeySignature', 'Markup', 'Measure', 'Multiplier', 'NamedPitch', 'Note',
   'Offset', 'Rest', 'Score', 'Slur', 'Staff', 'StaffGroup', 'Tempo', 'Tie',
   'TimeSignature', 'Tuplet', 'Voice', '__builtins__', '__doc__', '__name__',
   '__package__', 'abctools', 'abjad_configuration', 'abjadbooktools',
   'agenttools', 'attach', 'contextualize', 'datastructuretools', 'detach',
   'developerscripttools', 'documentationtools', 'durationtools',
   'exceptiontools', 'f', 'indicatortools', 'inspect', 'instrumenttools',
   'iterate', 'labeltools', 'layouttools', 'lilypondfiletools',
   'lilypondnametools', 'lilypondparsertools', 'markuptools', 'mathtools',
   'metertools', 'mutate', 'new', 'override', 'parse', 'persist',
   'pitcharraytools', 'pitchtools', 'play', 'quantizationtools',
   'rhythmmakertools', 'rhythmtreetools', 'schemetools', 'scoretools', 'select',
   'selectiontools', 'sequencetools', 'show', 'sievetools', 'spannertools',
   'stringtools', 'systemtools', 'templatetools', 'timespantools',
   'tonalanalysistools', 'topleveltools']


Calling ``from abjad import *`` causes Python to load hundreds or thousands of
lines of Abjad's code into the global namespace for you to use.  Abjad's code
is organized into a collection of several dozen different score-related
packages.  These packages comprise hundreds of classes that model things like
notes and rests and more than a thousand functions that let you do things like
transpose music or change the way beams look in your score.

Inspecting output
-----------------

Use ``dir()`` to take a look at the contents of the ``systemtools`` package:

::

   >>> dir(systemtools)
   ['AbjadConfiguration', 'BenchmarkScoreMaker', 'Configuration', 'IOManager',
   'ImportManager', 'LilyPondFormatBundle', 'LilyPondFormatManager',
   'RedirectedStreams', 'StorageFormatManager', 'StorageFormatSpecification',
   'TestManager', 'Timer', 'UpdateManager', 'WellformednessManager',
   '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__',
   '_documentation_section', 'requires']


The ``systemtools`` package implements I/O functions that help you work with the
files you create in Abjad.

Use ``systemtools.view_last_ly()`` to see the last LilyPond input file created
in Abjad:

::

    % Abjad revision 12452
    % 2013-10-22 13:32

    \version "2.17.3"
    \language "english"

    \header {
        tagline = \markup {  }
    }

    \score {
        c'4
    }

Notice:

1.  Abjad inserts two lines of %-prefixed comments at the top of the LilyPond 
    files it creates.

2.  Abjad includes version and language commands automatically.

3.  Abjad includes a special abjad.scm file resident somewhere on your 
    computer.

4.  Abjad includes dummy LilyPond header.

5.  Abjad includes a one-note score expression similar to the one you created 
    in the last tutorial.

When you called ``show(note)`` Abjad created the LilyPond input file shown
above.  Abjad then called LilyPond on that ``.ly`` file to create a PDF.

(Quit your text editor in the usual way to return to the Python interpreter.)

Now use ``systemtools.view_last_log()`` to see the output LilyPond created as
it ran:

::

    GNU LilyPond 2.17.3
    Processing `7721.ly'
    Parsing...
    Interpreting music...
    Preprocessing graphical objects...
    Finding the ideal number of pages...
    Fitting music on 1 page...
    Drawing systems...
    Layout output to `7721.ps'...
    Converting to `./7721.pdf'...
    Success: compilation successfully completed

This will look familiar from the previous tutorial where we created a LilyPond
file by hand.

(Quit your text editor in the usual way to return to the Python interpreter.)
