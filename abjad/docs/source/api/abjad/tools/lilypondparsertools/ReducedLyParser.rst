.. _abjad--tools--lilypondparsertools--ReducedLyParser:

ReducedLyParser
===============

.. automodule:: abjad.tools.lilypondparsertools.ReducedLyParser

.. currentmodule:: abjad.tools.lilypondparsertools.ReducedLyParser

.. container:: svg-container

   .. inheritance-diagram:: abjad
      :lineage: abjad.tools.lilypondparsertools.ReducedLyParser

.. autoclass:: ReducedLyParser

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: ReducedLyParser.__call__

   .. automethod:: ReducedLyParser.__format__

   .. automethod:: ReducedLyParser.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: ReducedLyParser.p_apostrophes__APOSTROPHE

   .. automethod:: ReducedLyParser.p_apostrophes__apostrophes__APOSTROPHE

   .. automethod:: ReducedLyParser.p_beam__BRACKET_L

   .. automethod:: ReducedLyParser.p_beam__BRACKET_R

   .. automethod:: ReducedLyParser.p_chord_body__chord_pitches

   .. automethod:: ReducedLyParser.p_chord_body__chord_pitches__positive_leaf_duration

   .. automethod:: ReducedLyParser.p_chord_pitches__CARAT_L__pitches__CARAT_R

   .. automethod:: ReducedLyParser.p_commas__COMMA

   .. automethod:: ReducedLyParser.p_commas__commas__commas

   .. automethod:: ReducedLyParser.p_component__container

   .. automethod:: ReducedLyParser.p_component__fixed_duration_container

   .. automethod:: ReducedLyParser.p_component__leaf

   .. automethod:: ReducedLyParser.p_component__tuplet

   .. automethod:: ReducedLyParser.p_component_list__EMPTY

   .. automethod:: ReducedLyParser.p_component_list__component_list__component

   .. automethod:: ReducedLyParser.p_container__BRACE_L__component_list__BRACE_R

   .. automethod:: ReducedLyParser.p_dots__EMPTY

   .. automethod:: ReducedLyParser.p_dots__dots__DOT

   .. automethod:: ReducedLyParser.p_error

   .. automethod:: ReducedLyParser.p_fixed_duration_container__BRACE_L__FRACTION__BRACE_R

   .. automethod:: ReducedLyParser.p_leaf__leaf_body__post_events

   .. automethod:: ReducedLyParser.p_leaf_body__chord_body

   .. automethod:: ReducedLyParser.p_leaf_body__note_body

   .. automethod:: ReducedLyParser.p_leaf_body__rest_body

   .. automethod:: ReducedLyParser.p_measure__PIPE__FRACTION__component_list__PIPE

   .. automethod:: ReducedLyParser.p_negative_leaf_duration__INTEGER_N__dots

   .. automethod:: ReducedLyParser.p_note_body__pitch

   .. automethod:: ReducedLyParser.p_note_body__pitch__positive_leaf_duration

   .. automethod:: ReducedLyParser.p_note_body__positive_leaf_duration

   .. automethod:: ReducedLyParser.p_pitch__PITCHNAME

   .. automethod:: ReducedLyParser.p_pitch__PITCHNAME__apostrophes

   .. automethod:: ReducedLyParser.p_pitch__PITCHNAME__commas

   .. automethod:: ReducedLyParser.p_pitches__pitch

   .. automethod:: ReducedLyParser.p_pitches__pitches__pitch

   .. automethod:: ReducedLyParser.p_positive_leaf_duration__INTEGER_P__dots

   .. automethod:: ReducedLyParser.p_post_event__beam

   .. automethod:: ReducedLyParser.p_post_event__slur

   .. automethod:: ReducedLyParser.p_post_event__tie

   .. automethod:: ReducedLyParser.p_post_events__EMPTY

   .. automethod:: ReducedLyParser.p_post_events__post_events__post_event

   .. automethod:: ReducedLyParser.p_rest_body__RESTNAME

   .. automethod:: ReducedLyParser.p_rest_body__RESTNAME__positive_leaf_duration

   .. automethod:: ReducedLyParser.p_rest_body__negative_leaf_duration

   .. automethod:: ReducedLyParser.p_slur__PAREN_L

   .. automethod:: ReducedLyParser.p_slur__PAREN_R

   .. automethod:: ReducedLyParser.p_start__EMPTY

   .. automethod:: ReducedLyParser.p_start__start__component

   .. automethod:: ReducedLyParser.p_start__start__measure

   .. automethod:: ReducedLyParser.p_tie__TILDE

   .. automethod:: ReducedLyParser.p_tuplet__FRACTION__container

   .. automethod:: ReducedLyParser.t_FRACTION

   .. automethod:: ReducedLyParser.t_INTEGER_N

   .. automethod:: ReducedLyParser.t_INTEGER_P

   .. automethod:: ReducedLyParser.t_PITCHNAME

   .. automethod:: ReducedLyParser.t_error

   .. automethod:: ReducedLyParser.t_newline

   .. automethod:: ReducedLyParser.tokenize

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: ReducedLyParser.debug

   .. autoattribute:: ReducedLyParser.lexer

   .. autoattribute:: ReducedLyParser.lexer_rules_object

   .. autoattribute:: ReducedLyParser.logger

   .. autoattribute:: ReducedLyParser.logger_path

   .. autoattribute:: ReducedLyParser.output_path

   .. autoattribute:: ReducedLyParser.parser

   .. autoattribute:: ReducedLyParser.parser_rules_object

   .. autoattribute:: ReducedLyParser.pickle_path