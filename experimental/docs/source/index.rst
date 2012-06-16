Abjad Experimental API
======================

Unstable Abjad composition packages (load manually)
---------------------------------------------------

.. toctree::
   :maxdepth: 1

:py:mod:`abjadbooktools <experimental.abjadbooktools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/abjadbooktools/OutputFormat/OutputFormat

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/abjadbooktools/AbjadBookProcessor/AbjadBookProcessor
   experimental/abjadbooktools/AbjadBookScript/AbjadBookScript
   experimental/abjadbooktools/CodeBlock/CodeBlock
   experimental/abjadbooktools/HTMLOutputFormat/HTMLOutputFormat
   experimental/abjadbooktools/LaTeXOutputFormat/LaTeXOutputFormat
   experimental/abjadbooktools/ReSTOutputFormat/ReSTOutputFormat

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

:py:mod:`developerscripttools <experimental.developerscripttools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/developerscripttools/CountLinesScript/CountLinesScript
   experimental/developerscripttools/DeveloperScript/DeveloperScript
   experimental/developerscripttools/DirectoryScript/DirectoryScript
   experimental/developerscripttools/ReplaceInFilesScript/ReplaceInFilesScript
   experimental/developerscripttools/ReplacePromptsScript/ReplacePromptsScript

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/developerscripttools/AbjDevScript/AbjDevScript
   experimental/developerscripttools/BuildAbjadApiScript/BuildAbjadApiScript
   experimental/developerscripttools/BuildExperimentalApiScript/BuildExperimentalApiScript
   experimental/developerscripttools/CleanScript/CleanScript
   experimental/developerscripttools/CountLinewidthsScript/CountLinewidthsScript
   experimental/developerscripttools/CountToolsScript/CountToolsScript
   experimental/developerscripttools/SvnAddAllScript/SvnAddAllScript
   experimental/developerscripttools/SvnCommitScript/SvnCommitScript
   experimental/developerscripttools/SvnMessageScript/SvnMessageScript
   experimental/developerscripttools/SvnUpdateScript/SvnUpdateScript

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   experimental/developerscripttools/get_developer_script_classes

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

:py:mod:`lyricstools <experimental.lyricstools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/lyricstools/AddLyrics/AddLyrics
   experimental/lyricstools/LyricExtender/LyricExtender
   experimental/lyricstools/LyricHyphen/LyricHyphen
   experimental/lyricstools/LyricSpace/LyricSpace
   experimental/lyricstools/LyricText/LyricText
   experimental/lyricstools/Lyrics/Lyrics

:py:mod:`quantizationtools <experimental.quantizationtools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/quantizationtools/QEvent/QEvent
   experimental/quantizationtools/QGrid/QGrid
   experimental/quantizationtools/QGridQuantizer/QGridQuantizer
   experimental/quantizationtools/QGridSearchTree/QGridSearchTree
   experimental/quantizationtools/QGridTempoLookup/QGridTempoLookup

.. rubric:: functions

.. toctree::
   :maxdepth: 1

   experimental/quantizationtools/is_valid_beatspan
   experimental/quantizationtools/millisecond_pitch_pairs_to_q_events
   experimental/quantizationtools/milliseconds_to_q_events
   experimental/quantizationtools/tempo_scaled_leaves_to_q_events
   experimental/quantizationtools/tempo_scaled_rational_to_milliseconds
   experimental/quantizationtools/tempo_scaled_rationals_to_q_events

:py:mod:`specificationtools <experimental.specificationtools>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rubric:: abstract classes

.. toctree::
   :maxdepth: 1

   experimental/specificationtools/BaseSetting/BaseSetting

.. rubric:: concrete classes

.. toctree::
   :maxdepth: 1

   experimental/specificationtools/AttributeNameEnumeration/AttributeNameEnumeration
   experimental/specificationtools/AttributeRetrievalIndicator/AttributeRetrievalIndicator
   experimental/specificationtools/AttributeRetrievalRequest/AttributeRetrievalRequest
   experimental/specificationtools/Callback/Callback
   experimental/specificationtools/ContextDictionary/ContextDictionary
   experimental/specificationtools/ContextProxy/ContextProxy
   experimental/specificationtools/ContextSelection/ContextSelection
   experimental/specificationtools/Directive/Directive
   experimental/specificationtools/DirectiveInventory/DirectiveInventory
   experimental/specificationtools/Division/Division
   experimental/specificationtools/DivisionList/DivisionList
   experimental/specificationtools/DivisionRetrievalRequest/DivisionRetrievalRequest
   experimental/specificationtools/HandlerRequest/HandlerRequest
   experimental/specificationtools/PartIndicator/PartIndicator
   experimental/specificationtools/RegionDivisionList/RegionDivisionList
   experimental/specificationtools/ResolvedSetting/ResolvedSetting
   experimental/specificationtools/ScopedValue/ScopedValue
   experimental/specificationtools/ScoreObjectIndicator/ScoreObjectIndicator
   experimental/specificationtools/ScoreSpecification/ScoreSpecification
   experimental/specificationtools/SegmentDivisionList/SegmentDivisionList
   experimental/specificationtools/SegmentInventory/SegmentInventory
   experimental/specificationtools/SegmentSpecification/SegmentSpecification
   experimental/specificationtools/Selection/Selection
   experimental/specificationtools/Setting/Setting
   experimental/specificationtools/SettingInventory/SettingInventory
   experimental/specificationtools/Specification/Specification
   experimental/specificationtools/StatalServer/StatalServer
   experimental/specificationtools/StatalServerRequest/StatalServerRequest
   experimental/specificationtools/TemporalCursor/TemporalCursor
   experimental/specificationtools/Timespan/Timespan
   experimental/specificationtools/ValueRetrievalIndicator/ValueRetrievalIndicator
   experimental/specificationtools/ValueRetrievalRequest/ValueRetrievalRequest
   experimental/specificationtools/VoiceDivisionList/VoiceDivisionList
