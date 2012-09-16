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
   experimental/divisiontools/DivisionRegionDivisionList/DivisionRegionDivisionList
   experimental/divisiontools/RhythmRegionDivisionList/RhythmRegionDivisionList
   experimental/divisiontools/SegmentDivisionList/SegmentDivisionList
   experimental/divisiontools/VoiceDivisionList/VoiceDivisionList

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

   experimental/interpretertools/Command/Command
   experimental/interpretertools/Interpreter/Interpreter

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/interpretertools/ConcreteInterpreter/ConcreteInterpreter
   experimental/interpretertools/DivisionCommand/DivisionCommand
   experimental/interpretertools/RhythmCommand/RhythmCommand
   experimental/interpretertools/RhythmExpression/RhythmExpression

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

:py:mod:`quantizationtools <experimental.quantizationtools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/quantizationtools/AttackPointOptimizer/AttackPointOptimizer
   experimental/quantizationtools/GraceHandler/GraceHandler
   experimental/quantizationtools/Heuristic/Heuristic
   experimental/quantizationtools/JobHandler/JobHandler
   experimental/quantizationtools/QEvent/QEvent
   experimental/quantizationtools/QSchema/QSchema
   experimental/quantizationtools/QSchemaItem/QSchemaItem
   experimental/quantizationtools/QTarget/QTarget
   experimental/quantizationtools/SearchTree/SearchTree

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/quantizationtools/BeatHierarchy/BeatHierarchy
   experimental/quantizationtools/BeatwiseQSchema/BeatwiseQSchema
   experimental/quantizationtools/BeatwiseQSchemaItem/BeatwiseQSchemaItem
   experimental/quantizationtools/BeatwiseQTarget/BeatwiseQTarget
   experimental/quantizationtools/CollapsingGraceHandler/CollapsingGraceHandler
   experimental/quantizationtools/ComplexSearchTree/ComplexSearchTree
   experimental/quantizationtools/ConcatenatingGraceHandler/ConcatenatingGraceHandler
   experimental/quantizationtools/DiscardingGraceHandler/DiscardingGraceHandler
   experimental/quantizationtools/DistanceHeuristic/DistanceHeuristic
   experimental/quantizationtools/MeasurewiseAttackPointOptimizer/MeasurewiseAttackPointOptimizer
   experimental/quantizationtools/MeasurewiseQSchema/MeasurewiseQSchema
   experimental/quantizationtools/MeasurewiseQSchemaItem/MeasurewiseQSchemaItem
   experimental/quantizationtools/MeasurewiseQTarget/MeasurewiseQTarget
   experimental/quantizationtools/NaiveAttackPointOptimizer/NaiveAttackPointOptimizer
   experimental/quantizationtools/NullAttackPointOptimizer/NullAttackPointOptimizer
   experimental/quantizationtools/ParallelJobHandler/ParallelJobHandler
   experimental/quantizationtools/ParallelJobHandlerWorker/ParallelJobHandlerWorker
   experimental/quantizationtools/PitchedQEvent/PitchedQEvent
   experimental/quantizationtools/QEventProxy/QEventProxy
   experimental/quantizationtools/QEventSequence/QEventSequence
   experimental/quantizationtools/QGrid/QGrid
   experimental/quantizationtools/QGridContainer/QGridContainer
   experimental/quantizationtools/QGridLeaf/QGridLeaf
   experimental/quantizationtools/QTargetBeat/QTargetBeat
   experimental/quantizationtools/QTargetMeasure/QTargetMeasure
   experimental/quantizationtools/QuantizationJob/QuantizationJob
   experimental/quantizationtools/Quantizer/Quantizer
   experimental/quantizationtools/SerialJobHandler/SerialJobHandler
   experimental/quantizationtools/SilentQEvent/SilentQEvent
   experimental/quantizationtools/SimpleSearchTree/SimpleSearchTree
   experimental/quantizationtools/TerminalQEvent/TerminalQEvent

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   experimental/quantizationtools/millisecond_pitch_pairs_to_q_events
   experimental/quantizationtools/milliseconds_to_q_events
   experimental/quantizationtools/tempo_scaled_leaves_to_q_events
   experimental/quantizationtools/tempo_scaled_rational_to_milliseconds
   experimental/quantizationtools/tempo_scaled_rationals_to_q_events

:py:mod:`requesttools <experimental.requesttools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/requesttools/AbsoluteRequest/AbsoluteRequest
   experimental/requesttools/CommandRequest/CommandRequest
   experimental/requesttools/HandlerRequest/HandlerRequest
   experimental/requesttools/MaterialRequest/MaterialRequest
   experimental/requesttools/Request/Request
   experimental/requesttools/RhythmRequest/RhythmRequest
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

:py:mod:`selectortools <experimental.selectortools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/selectortools/InequalitySelector/InequalitySelector
   experimental/selectortools/RatioPartSelector/RatioPartSelector
   experimental/selectortools/Selector/Selector
   experimental/selectortools/SliceSelector/SliceSelector

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/selectortools/BackgroundMeasureSelector/BackgroundMeasureSelector
   experimental/selectortools/CountRatioPartSelector/CountRatioPartSelector
   experimental/selectortools/CounttimeComponentSelector/CounttimeComponentSelector
   experimental/selectortools/DivisionSelector/DivisionSelector
   experimental/selectortools/OffsetSelector/OffsetSelector
   experimental/selectortools/SegmentSelector/SegmentSelector
   experimental/selectortools/SingleSegmentSelector/SingleSegmentSelector
   experimental/selectortools/TimeRatioPartSelector/TimeRatioPartSelector

:py:mod:`settingtools <experimental.settingtools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/settingtools/Setting/Setting

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/settingtools/MultipleContextSetting/MultipleContextSetting
   experimental/settingtools/MultipleContextSettingInventory/MultipleContextSettingInventory
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

:py:mod:`timespaninequalitytools <experimental.timespaninequalitytools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/timespaninequalitytools/TimeObjectInequality/TimeObjectInequality

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/timespaninequalitytools/TimepointInequality/TimepointInequality
   experimental/timespaninequalitytools/TimespanInequality/TimespanInequality

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   experimental/timespaninequalitytools/timepoint_happens_after_timespan_starts
   experimental/timespaninequalitytools/timepoint_happens_after_timespan_stops
   experimental/timespaninequalitytools/timepoint_happens_before_timespan_starts
   experimental/timespaninequalitytools/timepoint_happens_before_timespan_stops
   experimental/timespaninequalitytools/timepoint_happens_during_timespan
   experimental/timespaninequalitytools/timepoint_happens_when_timespan_starts
   experimental/timespaninequalitytools/timepoint_happens_when_timespan_stops
   experimental/timespaninequalitytools/timespan_2_contains_timespan_1_improperly
   experimental/timespaninequalitytools/timespan_2_curtails_timespan_1
   experimental/timespaninequalitytools/timespan_2_delays_timespan_1
   experimental/timespaninequalitytools/timespan_2_happens_during_timespan_1
   experimental/timespaninequalitytools/timespan_2_intersects_timespan_1
   experimental/timespaninequalitytools/timespan_2_is_congruent_to_timespan_1
   experimental/timespaninequalitytools/timespan_2_overlaps_all_of_timespan_1
   experimental/timespaninequalitytools/timespan_2_overlaps_start_of_timespan_1
   experimental/timespaninequalitytools/timespan_2_overlaps_start_of_timespan_1_only
   experimental/timespaninequalitytools/timespan_2_overlaps_stop_of_timespan_1
   experimental/timespaninequalitytools/timespan_2_overlaps_stop_of_timespan_1_only
   experimental/timespaninequalitytools/timespan_2_starts_after_timespan_1_starts
   experimental/timespaninequalitytools/timespan_2_starts_after_timespan_1_stops
   experimental/timespaninequalitytools/timespan_2_starts_before_timespan_1_starts
   experimental/timespaninequalitytools/timespan_2_starts_before_timespan_1_stops
   experimental/timespaninequalitytools/timespan_2_starts_during_timespan_1
   experimental/timespaninequalitytools/timespan_2_starts_when_timespan_1_starts
   experimental/timespaninequalitytools/timespan_2_starts_when_timespan_1_stops
   experimental/timespaninequalitytools/timespan_2_stops_after_timespan_1_starts
   experimental/timespaninequalitytools/timespan_2_stops_after_timespan_1_stops
   experimental/timespaninequalitytools/timespan_2_stops_before_timespan_1_starts
   experimental/timespaninequalitytools/timespan_2_stops_before_timespan_1_stops
   experimental/timespaninequalitytools/timespan_2_stops_during_timespan_1
   experimental/timespaninequalitytools/timespan_2_stops_when_timespan_1_starts
   experimental/timespaninequalitytools/timespan_2_stops_when_timespan_1_stops
   experimental/timespaninequalitytools/timespan_2_trisects_timespan_1

:py:mod:`timespantools <experimental.timespantools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/timespantools/SymbolicTimespan/SymbolicTimespan

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/timespantools/MixedSourceSymbolicTimespan/MixedSourceSymbolicTimespan
   experimental/timespantools/SingleSourceSymbolicTimespan/SingleSourceSymbolicTimespan
   experimental/timespantools/SymbolicTimepoint/SymbolicTimepoint
   experimental/timespantools/TimespanConstant/TimespanConstant
   experimental/timespantools/TimespanInventory/TimespanInventory

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   experimental/timespantools/expr_to_timespan
