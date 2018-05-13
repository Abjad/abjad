.. _abjad--tools--rhythmtreetools--RhythmTreeParser:

RhythmTreeParser
================

.. automodule:: abjad.tools.rhythmtreetools.RhythmTreeParser

.. currentmodule:: abjad.tools.rhythmtreetools.RhythmTreeParser

.. container:: svg-container

   .. inheritance-diagram:: abjad
      :lineage: abjad.tools.rhythmtreetools.RhythmTreeParser

.. autoclass:: RhythmTreeParser

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: RhythmTreeParser.__call__

   .. automethod:: RhythmTreeParser.__format__

   .. automethod:: RhythmTreeParser.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: RhythmTreeParser.p_container__LPAREN__DURATION__node_list_closed__RPAREN

   .. automethod:: RhythmTreeParser.p_error

   .. automethod:: RhythmTreeParser.p_leaf__INTEGER

   .. automethod:: RhythmTreeParser.p_node__container

   .. automethod:: RhythmTreeParser.p_node__leaf

   .. automethod:: RhythmTreeParser.p_node_list__node_list__node_list_item

   .. automethod:: RhythmTreeParser.p_node_list__node_list_item

   .. automethod:: RhythmTreeParser.p_node_list_closed__LPAREN__node_list__RPAREN

   .. automethod:: RhythmTreeParser.p_node_list_item__node

   .. automethod:: RhythmTreeParser.p_toplevel__EMPTY

   .. automethod:: RhythmTreeParser.p_toplevel__toplevel__node

   .. automethod:: RhythmTreeParser.t_DURATION

   .. automethod:: RhythmTreeParser.t_error

   .. automethod:: RhythmTreeParser.t_newline

   .. automethod:: RhythmTreeParser.tokenize

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: RhythmTreeParser.debug

   .. autoattribute:: RhythmTreeParser.lexer

   .. autoattribute:: RhythmTreeParser.lexer_rules_object

   .. autoattribute:: RhythmTreeParser.logger

   .. autoattribute:: RhythmTreeParser.logger_path

   .. autoattribute:: RhythmTreeParser.output_path

   .. autoattribute:: RhythmTreeParser.parser

   .. autoattribute:: RhythmTreeParser.parser_rules_object

   .. autoattribute:: RhythmTreeParser.pickle_path