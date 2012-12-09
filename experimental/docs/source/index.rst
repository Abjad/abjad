Abjad Experimental API
======================

Unstable packages (load manually)
---------------------------------

.. toctree::
   :maxdepth: 1

:py:mod:`constrainttools <experimental.constrainttools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/constrainttools/AbsoluteIndexConstraint/AbsoluteIndexConstraint
   experimental/constrainttools/Domain/Domain
   experimental/constrainttools/FixedLengthStreamSolver/FixedLengthStreamSolver
   experimental/constrainttools/GlobalConstraint/GlobalConstraint
   experimental/constrainttools/GlobalCountsConstraint/GlobalCountsConstraint
   experimental/constrainttools/GlobalReferenceConstraint/GlobalReferenceConstraint
   experimental/constrainttools/RelativeCountsConstraint/RelativeCountsConstraint
   experimental/constrainttools/RelativeIndexConstraint/RelativeIndexConstraint
   experimental/constrainttools/VariableLengthStreamSolver/VariableLengthStreamSolver

:py:mod:`divisiontools <experimental.divisiontools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/divisiontools/Division/Division
   experimental/divisiontools/DivisionList/DivisionList

:py:mod:`handlertools <experimental.handlertools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/handlertools/Handler/Handler
   experimental/handlertools/articulations/ArticulationHandler/ArticulationHandler
   experimental/handlertools/dynamics/DynamicHandler/DynamicHandler
   experimental/handlertools/pitch/PitchHandler/PitchHandler

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/handlertools/articulations/PatternedArticulationsHandler/PatternedArticulationsHandler
   experimental/handlertools/articulations/ReiteratedArticulationHandler/ReiteratedArticulationHandler
   experimental/handlertools/articulations/RepeatedMarkupHandler/RepeatedMarkupHandler
   experimental/handlertools/articulations/StemTremoloHandler/StemTremoloHandler
   experimental/handlertools/dynamics/NoteAndChordHairpinHandler/NoteAndChordHairpinHandler
   experimental/handlertools/dynamics/NoteAndChordHairpinsHandler/NoteAndChordHairpinsHandler
   experimental/handlertools/dynamics/ReiteratedDynamicHandler/ReiteratedDynamicHandler
   experimental/handlertools/dynamics/TerracedDynamicsHandler/TerracedDynamicsHandler
   experimental/handlertools/pitch/DiatonicClusterHandler/DiatonicClusterHandler
   experimental/handlertools/pitch/OctaveTranspositionHandler/OctaveTranspositionHandler
   experimental/handlertools/pitch/TimewisePitchClassHandler/TimewisePitchClassHandler

:py:mod:`helpertools <experimental.helpertools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/helpertools/AttributeNameEnumeration/AttributeNameEnumeration
   experimental/helpertools/Callback/Callback
   experimental/helpertools/KlassInventory/KlassInventory
   experimental/helpertools/SegmentIdentifierExpression/SegmentIdentifierExpression

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   experimental/helpertools/configure_multiple_voice_rhythmic_staves
   experimental/helpertools/expr_to_component_name
   experimental/helpertools/expr_to_score_name
   experimental/helpertools/expr_to_segment_name
   experimental/helpertools/index_to_slice_pair
   experimental/helpertools/is_background_element_klass
   experimental/helpertools/is_counttime_component_klass_expr
   experimental/helpertools/read_test_output
   experimental/helpertools/write_test_output

:py:mod:`interpretertools <experimental.interpretertools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/interpretertools/Interpreter/Interpreter

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/interpretertools/ConcreteInterpreter/ConcreteInterpreter

:py:mod:`lyrictools <experimental.lyrictools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/lyrictools/AddLyrics/AddLyrics
   experimental/lyrictools/LyricExtender/LyricExtender
   experimental/lyrictools/LyricHyphen/LyricHyphen
   experimental/lyrictools/LyricSpace/LyricSpace
   experimental/lyrictools/LyricText/LyricText
   experimental/lyrictools/Lyrics/Lyrics

:py:mod:`metricmodulationtools <experimental.metricmodulationtools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   experimental/metricmodulationtools/yield_prolation_rewrite_pairs

:py:mod:`requesttools <experimental.requesttools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/requesttools/Request/Request

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/requesttools/AbsoluteRequest/AbsoluteRequest
   experimental/requesttools/CommandRequest/CommandRequest
   experimental/requesttools/HandlerRequest/HandlerRequest
   experimental/requesttools/MaterialRequest/MaterialRequest
   experimental/requesttools/StatalServerRequest/StatalServerRequest

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   experimental/requesttools/apply_request_transforms
   experimental/requesttools/expr_to_request
   experimental/requesttools/set_transforms_on_request

:py:mod:`segmenttools <experimental.segmenttools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/segmenttools/Segment/Segment

:py:mod:`settingtools <experimental.settingtools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/settingtools/Command/Command
   experimental/settingtools/OffsetPositionedExpression/OffsetPositionedExpression
   experimental/settingtools/Setting/Setting

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/settingtools/DivisionCommand/DivisionCommand
   experimental/settingtools/MultipleContextSetting/MultipleContextSetting
   experimental/settingtools/MultipleContextSettingInventory/MultipleContextSettingInventory
   experimental/settingtools/OffsetPositionedDivisionList/OffsetPositionedDivisionList
   experimental/settingtools/OffsetPositionedRhythmExpression/OffsetPositionedRhythmExpression
   experimental/settingtools/RhythmCommand/RhythmCommand
   experimental/settingtools/RotationIndicator/RotationIndicator
   experimental/settingtools/SingleContextSetting/SingleContextSetting
   experimental/settingtools/SingleContextSettingInventory/SingleContextSettingInventory

:py:mod:`specificationtools <experimental.specificationtools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/specificationtools/Specification/Specification

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/specificationtools/ContextProxy/ContextProxy
   experimental/specificationtools/ContextProxyDictionary/ContextProxyDictionary
   experimental/specificationtools/ScoreSpecification/ScoreSpecification
   experimental/specificationtools/SegmentSpecification/SegmentSpecification
   experimental/specificationtools/SegmentSpecificationInventory/SegmentSpecificationInventory

:py:mod:`statalservertools <experimental.statalservertools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/statalservertools/StatalServer/StatalServer

:py:mod:`symbolictimetools <experimental.symbolictimetools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/symbolictimetools/MixedSourceSymbolicTimespan/MixedSourceSymbolicTimespan
   experimental/symbolictimetools/RatioPartSymbolicTimespan/RatioPartSymbolicTimespan
   experimental/symbolictimetools/SymbolicTimespan/SymbolicTimespan
   experimental/symbolictimetools/TimeRelationSymbolicTimespan/TimeRelationSymbolicTimespan
   experimental/symbolictimetools/TimespanSymbolicTimespan/TimespanSymbolicTimespan

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/symbolictimetools/BackgroundMeasureSymbolicTimespan/BackgroundMeasureSymbolicTimespan
   experimental/symbolictimetools/CountRatioPartSymbolicTimespan/CountRatioPartSymbolicTimespan
   experimental/symbolictimetools/CounttimeComponentSymbolicTimespan/CounttimeComponentSymbolicTimespan
   experimental/symbolictimetools/DivisionSymbolicTimespan/DivisionSymbolicTimespan
   experimental/symbolictimetools/OffsetSymbolicTimespan/OffsetSymbolicTimespan
   experimental/symbolictimetools/ScoreSymbolicTimespan/ScoreSymbolicTimespan
   experimental/symbolictimetools/SegmentSymbolicTimespan/SegmentSymbolicTimespan
   experimental/symbolictimetools/SingleSegmentSymbolicTimespan/SingleSegmentSymbolicTimespan
   experimental/symbolictimetools/SymbolicOffset/SymbolicOffset
   experimental/symbolictimetools/TimeRatioPartSymbolicTimespan/TimeRatioPartSymbolicTimespan
