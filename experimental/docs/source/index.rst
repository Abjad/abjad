Abjad Experimental API
======================

Demos and example packages
--------------------------

.. toctree::
   :maxdepth: 1

:py:mod:`microlanguage <('abjad.tools.', 'abjad.demos.')microlanguage>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   demos/microlanguage/ToyLanguageParser/ToyLanguageParser

:py:mod:`windungen <('abjad.tools.', 'abjad.demos.')windungen>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   demos/windungen/WindungenScoreTemplate/WindungenScoreTemplate

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   demos/windungen/make_base_list_of_compressed_rotation_tuples
   demos/windungen/make_base_list_of_rotation_tuples
   demos/windungen/make_base_list_of_uncompressed_rotation_tuples
   demos/windungen/make_windungen_score
   demos/windungen/mirror_base_list_of_rotation_tuples

Unstable packages (load manually)
---------------------------------

.. toctree::
   :maxdepth: 1

:py:mod:`breakpointtools <('abjad.tools.', 'abjad.demos.')breakpointtools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   tools/breakpointtools/BreakPoint/BreakPoint
   tools/breakpointtools/BreakPointFunctionSet/BreakPointFunctionSet

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/breakpointtools/BreakPointFunction/BreakPointFunction

:py:mod:`constrainttools <('abjad.tools.', 'abjad.demos.')constrainttools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/constrainttools/AbsoluteIndexConstraint/AbsoluteIndexConstraint
   tools/constrainttools/Domain/Domain
   tools/constrainttools/FixedLengthStreamSolver/FixedLengthStreamSolver
   tools/constrainttools/GlobalConstraint/GlobalConstraint
   tools/constrainttools/GlobalCountsConstraint/GlobalCountsConstraint
   tools/constrainttools/GlobalReferenceConstraint/GlobalReferenceConstraint
   tools/constrainttools/RelativeCountsConstraint/RelativeCountsConstraint
   tools/constrainttools/RelativeIndexConstraint/RelativeIndexConstraint
   tools/constrainttools/VariableLengthStreamSolver/VariableLengthStreamSolver

:py:mod:`divisiontools <('abjad.tools.', 'abjad.demos.')divisiontools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/divisiontools/Division/Division
   tools/divisiontools/DivisionList/DivisionList

:py:mod:`handlertools <('abjad.tools.', 'abjad.demos.')handlertools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   tools/handlertools/Handler/Handler
   tools/handlertools/articulations/ArticulationHandler/ArticulationHandler
   tools/handlertools/dynamics/DynamicHandler/DynamicHandler
   tools/handlertools/pitch/PitchHandler/PitchHandler

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/handlertools/articulations/PatternedArticulationsHandler/PatternedArticulationsHandler
   tools/handlertools/articulations/ReiteratedArticulationHandler/ReiteratedArticulationHandler
   tools/handlertools/articulations/RepeatedMarkupHandler/RepeatedMarkupHandler
   tools/handlertools/articulations/StemTremoloHandler/StemTremoloHandler
   tools/handlertools/dynamics/NoteAndChordHairpinHandler/NoteAndChordHairpinHandler
   tools/handlertools/dynamics/NoteAndChordHairpinsHandler/NoteAndChordHairpinsHandler
   tools/handlertools/dynamics/ReiteratedDynamicHandler/ReiteratedDynamicHandler
   tools/handlertools/dynamics/TerracedDynamicsHandler/TerracedDynamicsHandler
   tools/handlertools/pitch/DiatonicClusterHandler/DiatonicClusterHandler
   tools/handlertools/pitch/OctaveTranspositionHandler/OctaveTranspositionHandler
   tools/handlertools/pitch/TimewisePitchClassHandler/TimewisePitchClassHandler

:py:mod:`helpertools <('abjad.tools.', 'abjad.demos.')helpertools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/helpertools/AttributeNameEnumeration/AttributeNameEnumeration
   tools/helpertools/Callback/Callback
   tools/helpertools/KlassInventory/KlassInventory
   tools/helpertools/SegmentIdentifierExpression/SegmentIdentifierExpression

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   tools/helpertools/configure_multiple_voice_rhythmic_staves
   tools/helpertools/expr_to_component_name
   tools/helpertools/expr_to_score_name
   tools/helpertools/expr_to_segment_name
   tools/helpertools/index_to_slice_pair
   tools/helpertools/is_background_element_klass
   tools/helpertools/is_counttime_component_klass_expr
   tools/helpertools/read_test_output
   tools/helpertools/write_test_output

:py:mod:`interpretertools <('abjad.tools.', 'abjad.demos.')interpretertools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   tools/interpretertools/Interpreter/Interpreter

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/interpretertools/ConcreteInterpreter/ConcreteInterpreter

:py:mod:`lyrictools <('abjad.tools.', 'abjad.demos.')lyrictools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/lyrictools/AddLyrics/AddLyrics
   tools/lyrictools/LyricExtender/LyricExtender
   tools/lyrictools/LyricHyphen/LyricHyphen
   tools/lyrictools/LyricSpace/LyricSpace
   tools/lyrictools/LyricText/LyricText
   tools/lyrictools/Lyrics/Lyrics

:py:mod:`metricmodulationtools <('abjad.tools.', 'abjad.demos.')metricmodulationtools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   tools/metricmodulationtools/yield_prolation_rewrite_pairs

:py:mod:`parsertools <('abjad.tools.', 'abjad.demos.')parsertools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/parsertools/ENPParser/ENPParser

:py:mod:`requesttools <('abjad.tools.', 'abjad.demos.')requesttools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   tools/requesttools/Request/Request

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/requesttools/AbsoluteRequest/AbsoluteRequest
   tools/requesttools/CommandRequest/CommandRequest
   tools/requesttools/HandlerRequest/HandlerRequest
   tools/requesttools/StatalServerRequest/StatalServerRequest

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   tools/requesttools/apply_request_transforms
   tools/requesttools/expr_to_request

:py:mod:`segmenttools <('abjad.tools.', 'abjad.demos.')segmenttools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   tools/segmenttools/Segment/Segment

:py:mod:`settingtools <('abjad.tools.', 'abjad.demos.')settingtools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   tools/settingtools/Command/Command
   tools/settingtools/OffsetPositionedExpression/OffsetPositionedExpression
   tools/settingtools/Setting/Setting

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/settingtools/DivisionCommand/DivisionCommand
   tools/settingtools/MultipleContextSetting/MultipleContextSetting
   tools/settingtools/MultipleContextSettingInventory/MultipleContextSettingInventory
   tools/settingtools/OffsetPositionedDivisionList/OffsetPositionedDivisionList
   tools/settingtools/OffsetPositionedRhythmExpression/OffsetPositionedRhythmExpression
   tools/settingtools/RhythmCommand/RhythmCommand
   tools/settingtools/RotationIndicator/RotationIndicator
   tools/settingtools/SingleContextSetting/SingleContextSetting
   tools/settingtools/SingleContextSettingInventory/SingleContextSettingInventory

:py:mod:`specificationtools <('abjad.tools.', 'abjad.demos.')specificationtools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   tools/specificationtools/Specification/Specification

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/specificationtools/ContextProxy/ContextProxy
   tools/specificationtools/ContextProxyDictionary/ContextProxyDictionary
   tools/specificationtools/ScoreSpecification/ScoreSpecification
   tools/specificationtools/SegmentSpecification/SegmentSpecification
   tools/specificationtools/SegmentSpecificationInventory/SegmentSpecificationInventory

:py:mod:`statalservertools <('abjad.tools.', 'abjad.demos.')statalservertools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/statalservertools/StatalServer/StatalServer

:py:mod:`symbolictimetools <('abjad.tools.', 'abjad.demos.')symbolictimetools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   tools/symbolictimetools/Selector/Selector
   tools/symbolictimetools/SymbolicTimeObject/SymbolicTimeObject
   tools/symbolictimetools/SymbolicTimespan/SymbolicTimespan
   tools/symbolictimetools/VoiceSelector/VoiceSelector

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   tools/symbolictimetools/BackgroundMeasureSelector/BackgroundMeasureSelector
   tools/symbolictimetools/BeatSelector/BeatSelector
   tools/symbolictimetools/CounttimeComponentSelector/CounttimeComponentSelector
   tools/symbolictimetools/DivisionSelector/DivisionSelector
   tools/symbolictimetools/MixedSourceSymbolicTimespan/MixedSourceSymbolicTimespan
   tools/symbolictimetools/ScoreSelector/ScoreSelector
   tools/symbolictimetools/SegmentSelector/SegmentSelector
   tools/symbolictimetools/SymbolicOffset/SymbolicOffset
