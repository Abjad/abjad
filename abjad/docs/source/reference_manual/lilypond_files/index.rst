LilyPond files
==============


Making LilyPond files
---------------------

Make a basic LilyPond file with the ``lilypondfiletools`` package:

::

   >>> staff = Staff("c'4 d'4 e'4 f'4")
   >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)


::

   >>> lilypond_file
   <LilyPondFile(4)>


::

   >>> f(lilypond_file)
   % 2014-05-23 12:15
   
   \version "2.19.6"
   \language "english"
   
   \header {}
   
   \layout {}
   
   \paper {}
   
   \score {
       \new Staff {
           c'4
           d'4
           e'4
           f'4
       }
   }


::

   >>> show(lilypond_file)

.. image:: images/index-1.png



Getting header, layout and paper blocks
---------------------------------------

Basic LilyPond files also come equipped with header, layout and paper blocks:

::

   >>> lilypond_file.header_block
   <Block(name='header')>


::

   >>> lilypond_file.layout_block
   <Block(name='layout')>


::

   >>> lilypond_file.paper_block
   <Block(name='paper')>



Setting global staff size and default paper size
------------------------------------------------

Set default LilyPond global staff size and paper size like this:

::

   >>> lilypond_file.global_staff_size = 14
   >>> lilypond_file.default_paper_size = 'A7', 'portrait'


::

   >>> f(lilypond_file)
   \version "2.19.6"
   \language "english"
   
   #(set-default-paper-size "A7" 'portrait)
   #(set-global-staff-size 14)
   
   \header {
       tagline = \markup {}
   }
   
   \layout {
       indent = #0
       ragged-right = ##t
       \context {
           \Score
           \remove Bar_number_engraver
           \override SpacingSpanner #'strict-grace-spacing = ##t
           \override SpacingSpanner #'strict-note-spacing = ##t
           \override SpacingSpanner #'uniform-stretching = ##t
           \override TupletBracket #'bracket-visibility = ##t
           \override TupletBracket #'minimum-length = #3
           \override TupletBracket #'padding = #2
           \override TupletBracket #'springs-and-rods = #ly:spanner::set-spacing-rods
           \override TupletNumber #'text = #tuplet-number::calc-fraction-text
           proportionalNotationDuration = #(ly:make-moment 1 32)
           tupletFullLength = ##t
       }
   }
   
   \paper {
       left-margin = 1\in
   }
   
   \score {
       \new Staff {
           c'4
           d'4
           e'4
           f'4
       }
   }


::

   >>> show(lilypond_file)

.. image:: images/index-2.png



Setting title, subtitle and composer information
------------------------------------------------

Use the LilyPond file header block to set title, subtitle and composer
information:

::

   >>> lilypond_file.header_block.title = markuptools.Markup('Missa sexti tonus')
   >>> lilypond_file.header_block.composer = markuptools.Markup('Josquin')


::

   >>> f(lilypond_file)
   \version "2.19.6"
   \language "english"
   
   #(set-default-paper-size "A7" 'portrait)
   #(set-global-staff-size 12)
   
   \header {
       composer = \markup { Josquin }
       tagline = \markup {}
       title = \markup { Missa sexti tonus }
   }
   
   \layout {
       indent = #0
       ragged-right = ##t
       \context {
           \Score
           \remove Bar_number_engraver
           \override SpacingSpanner #'strict-grace-spacing = ##t
           \override SpacingSpanner #'strict-note-spacing = ##t
           \override SpacingSpanner #'uniform-stretching = ##t
           \override TupletBracket #'bracket-visibility = ##t
           \override TupletBracket #'minimum-length = #3
           \override TupletBracket #'padding = #2
           \override TupletBracket #'springs-and-rods = #ly:spanner::set-spacing-rods
           \override TupletNumber #'text = #tuplet-number::calc-fraction-text
           proportionalNotationDuration = #(ly:make-moment 1 32)
           tupletFullLength = ##t
       }
       \context {
           \Score
           \remove Bar_number_engraver
           \override SpacingSpanner #'strict-grace-spacing = ##t
           \override SpacingSpanner #'strict-note-spacing = ##t
           \override SpacingSpanner #'uniform-stretching = ##t
           \override TupletBracket #'bracket-visibility = ##t
           \override TupletBracket #'minimum-length = #3
           \override TupletBracket #'padding = #2
           \override TupletBracket #'springs-and-rods = #ly:spanner::set-spacing-rods
           \override TupletNumber #'text = #tuplet-number::calc-fraction-text
           proportionalNotationDuration = #(ly:make-moment 1 32)
           tupletFullLength = ##t
       }
   }
   
   \paper {
       left-margin = 1\in
   }
   
   \score {
       \new Staff {
           c'4
           d'4
           e'4
           f'4
       }
   }


::

   >>> show(lilypond_file)

.. image:: images/index-3.png

