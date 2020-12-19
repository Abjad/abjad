LilyPond context concatenation
==============================

Abjad users should know this: **LilyPond lets you use a control file to glue together
separate LilyPond files that segment your score into horizontal chunks of music.** Abjad
calls this feature "LilyPond context concatenation."

**Consider adding this pattern to your workflow.** The motivation is performance. Shorter
score semgents will always compile faster and be easier to debug than longer score
segments.

----

**Preliminaries.** The following two LilyPond examples produce identical output.

Without context concatenation:

..  code-block:: console

    \context Score = "Score" {
        \context Staff = "Violin" { c'4 d' e' f' g' a' b' c'' }
    }

With context concatenation:

..  code-block:: console

    
    \context Score = "Score" {
        \context Staff = "Violin" { c'4 d' e' f' }
        \context Staff = "Violin" { g' a' b' c'' }
    }

**The reason this works is because the two staff contexts share the same name:**
``"Violin"``.

This shows that you can segment LilyPond input into horizontal chunks. Doing this in a
single file, like here, isn't highly motivated. But this is the simplest way to
illustrate the feature.

----

**The pattern.** LilyPond's context concatenation becomes highly motivated when we ask
LilyPond to glue together entire scores written in separate files.

The simplest example requires three files:

    * ``music.ly``
    * ``segment-01.ily``
    * ``segment-02.ily``

Contents of ``music.ly``:

..  code-block:: console

    \version "2.21.80"
    \language "english"


    \score
    {
        {
        \include "segment-01.ily"
        \include "segment-02.ily"
        }
    }

Contents of ``segment-01.ily``:

..  code-block:: console

    \context Score = "Score"
    {
        \context Staff = "Violin" { c'4 d' e' f' }
    }

Contents of ``segment-02.ily``:

..  code-block:: console

    \context Score = "Score"
    {
        \context Staff = "Violin" { g'4 a' b' c'' }
    }

Calling LilyPond on ``music.ly`` produces a single score with a single staff.

**The reason this works is because the two staff contexts share the same name AND because
the two score contexts share the same name:** ``"Vioin"`` **and** ``"Score"``,
**respectively.**
    
----

**Discussion.**

* LilyPond context concatenation becomes essential to Abjad users during score build.

* Score build best practices do not yet appear in Abjad's docs. But, in short,
  building a score means creating a build directory, adding assets to it, and producing a
  PDF of your score for distribution. Part of this involves collecting LilyPond files
  produced separately for each score segment and gluing them together. LilyPond context
  concatenation makes that possible.

* LilyPond context concatenation is the reason real-world scores composed in Abjad use
  LilyPond's ``\context`` command instead of LilyPond's ``\new`` command. Only LilyPond
  contexts created with LilyPond's context command can be named. Only named contexts can
  be concatenated.

* LilyPond filename suffixes are conventional.

* Abjad users conventionally add ``.ly`` to mark the control file in multifile patterns
  like this one.

* Abjad users conventionally add ``.ily`` mark included files.

* The recommended naming pattern Abjad score directories specifies two-digit Arabic
  numerals ``01``, ``02``, ``03`` beginning at one.

* The recommended naming pattern for LilyPond files extracted from segment directories
  specifies hyphen-delimited lowercase filenames ``segment-01.ily``, ``segment-02.ily``,
  ``segment-03.ily`` that correspond to the directories in which they were created.

----

*Contributed: Bača (3.2).*
