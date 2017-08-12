# -*- coding: utf-8 -*-
from abjad.tools import documentationtools
from abjad.tools import scoretools
from abjad.tools import systemtools


class TestCase(systemtools.TestCase):

    def test_01(self):
        manager = documentationtools.DocumentationManager()
        documenter = documentationtools.PackageDocumenter(
            manager=manager,
            client=scoretools,
            )
        rst = documenter.build_rst()
        assert self.normalize("""
            ..  automodule:: abjad.tools.scoretools

            ..  container:: graphviz

                ..  graphviz::

                    digraph InheritanceGraph {
                        graph [bgcolor=transparent,
                            color=lightslategrey,
                            dpi=72,
                            fontname=Arial,
                            outputorder=edgesfirst,
                            overlap=prism,
                            penwidth=2,
                            rankdir=LR,
                            root="__builtin__.object",
                            splines=spline,
                            style="dotted, rounded",
                            truecolor=true];
                        node [colorscheme=pastel19,
                            fontname=Arial,
                            fontsize=12,
                            penwidth=2,
                            style="filled, rounded"];
                        edge [color=lightsteelblue2,
                            penwidth=2];
                        subgraph cluster_abctools {
                            graph [label=abctools];
                            "abjad.tools.abctools.AbjadObject.AbjadObject" [color=1,
                                group=0,
                                label=AbjadObject,
                                shape=box];
                            "abjad.tools.abctools.AbjadObject.AbstractBase" [color=1,
                                group=0,
                                label=AbstractBase,
                                shape=box];
                            "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
                        }
                        subgraph cluster_datastructuretools {
                            graph [label=datastructuretools];
                            "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                                group=2,
                                label=TypedCollection,
                                shape=oval,
                                style=bold];
                            "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                                group=2,
                                label=TypedList,
                                shape=box];
                            "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
                        }
                        subgraph cluster_scoretools {
                            graph [label=scoretools];
                            "abjad.tools.scoretools.Chord.Chord" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Chord,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Cluster.Cluster" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Cluster,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Component.Component" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Component,
                                shape=oval,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Container.Container" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Container,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Context.Context" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Context,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.DrumNoteHead.DrumNoteHead" [color=black,
                                fontcolor=white,
                                group=3,
                                label=DrumNoteHead,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer" [color=black,
                                fontcolor=white,
                                group=3,
                                label=FixedDurationContainer,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet" [color=black,
                                fontcolor=white,
                                group=3,
                                label=FixedDurationTuplet,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.GraceContainer.GraceContainer" [color=black,
                                fontcolor=white,
                                group=3,
                                label=GraceContainer,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Leaf.Leaf" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Leaf,
                                shape=oval,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Measure.Measure" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Measure,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.MultimeasureRest.MultimeasureRest" [color=black,
                                fontcolor=white,
                                group=3,
                                label=MultimeasureRest,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Note.Note" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Note,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.NoteHead.NoteHead" [color=black,
                                fontcolor=white,
                                group=3,
                                label=NoteHead,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.NoteHeadList.NoteHeadList" [color=black,
                                fontcolor=white,
                                group=3,
                                label=NoteHeadList,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Rest.Rest" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Rest,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Score.Score" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Score,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Skip.Skip" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Skip,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Staff.Staff" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Staff,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.StaffGroup.StaffGroup" [color=black,
                                fontcolor=white,
                                group=3,
                                label=StaffGroup,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Tuplet.Tuplet" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Tuplet,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Voice.Voice" [color=black,
                                fontcolor=white,
                                group=3,
                                label=Voice,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
                            "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Leaf.Leaf";
                            "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Cluster.Cluster";
                            "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Context.Context";
                            "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer";
                            "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.GraceContainer.GraceContainer";
                            "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Tuplet.Tuplet";
                            "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Score.Score";
                            "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Staff.Staff";
                            "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.StaffGroup.StaffGroup";
                            "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Voice.Voice";
                            "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer" -> "abjad.tools.scoretools.Measure.Measure";
                            "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Chord.Chord";
                            "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.MultimeasureRest.MultimeasureRest";
                            "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Note.Note";
                            "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Rest.Rest";
                            "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Skip.Skip";
                            "abjad.tools.scoretools.NoteHead.NoteHead" -> "abjad.tools.scoretools.DrumNoteHead.DrumNoteHead";
                            "abjad.tools.scoretools.Tuplet.Tuplet" -> "abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet";
                        }
                        subgraph cluster_builtins {
                            graph [label=builtins];
                            "builtins.object" [color=2,
                                group=1,
                                label=object,
                                shape=box];
                        }
                        "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
                        "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.Component.Component";
                        "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.NoteHead.NoteHead";
                        "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.scoretools.NoteHeadList.NoteHeadList";
                        "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
                    }

            --------

            Abstract Classes
            ----------------

            ..  autosummary::
                :nosignatures:

                ~abjad.tools.scoretools.Component.Component
                ~abjad.tools.scoretools.Leaf.Leaf

            --------

            Containers
            ----------

            ..  autosummary::
                :nosignatures:

                ~abjad.tools.scoretools.Cluster.Cluster
                ~abjad.tools.scoretools.Container.Container
                ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer
                ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet
                ~abjad.tools.scoretools.GraceContainer.GraceContainer
                ~abjad.tools.scoretools.Measure.Measure
                ~abjad.tools.scoretools.Tuplet.Tuplet

            --------

            Contexts
            --------

            ..  autosummary::
                :nosignatures:

                ~abjad.tools.scoretools.Context.Context
                ~abjad.tools.scoretools.Score.Score
                ~abjad.tools.scoretools.Staff.Staff
                ~abjad.tools.scoretools.StaffGroup.StaffGroup
                ~abjad.tools.scoretools.Voice.Voice

            --------

            Leaves
            ------

            ..  autosummary::
                :nosignatures:

                ~abjad.tools.scoretools.Chord.Chord
                ~abjad.tools.scoretools.MultimeasureRest.MultimeasureRest
                ~abjad.tools.scoretools.Note.Note
                ~abjad.tools.scoretools.Rest.Rest
                ~abjad.tools.scoretools.Skip.Skip

            --------

            Note heads
            ----------

            ..  autosummary::
                :nosignatures:

                ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead
                ~abjad.tools.scoretools.NoteHead.NoteHead
                ~abjad.tools.scoretools.NoteHeadList.NoteHeadList

            --------

            Functions
            ---------

            ..  autosummary::
                :nosignatures:

                ~abjad.tools.scoretools.append_spacer_skip_to_underfull_measure.append_spacer_skip_to_underfull_measure
                ~abjad.tools.scoretools.append_spacer_skips_to_underfull_measures.append_spacer_skips_to_underfull_measures
                ~abjad.tools.scoretools.apply_full_measure_tuplets_to_contents_of_measures.apply_full_measure_tuplets_to_contents_of_measures
                ~abjad.tools.scoretools.extend_measures_and_apply_full_measure_tuplets.extend_measures_and_apply_full_measure_tuplets
                ~abjad.tools.scoretools.fill_measures_with_full_measure_spacer_skips.fill_measures_with_full_measure_spacer_skips
                ~abjad.tools.scoretools.fill_measures_with_minimal_number_of_notes.fill_measures_with_minimal_number_of_notes
                ~abjad.tools.scoretools.fill_measures_with_repeated_notes.fill_measures_with_repeated_notes
                ~abjad.tools.scoretools.fill_measures_with_time_signature_denominator_notes.fill_measures_with_time_signature_denominator_notes
                ~abjad.tools.scoretools.get_measure.get_measure
                ~abjad.tools.scoretools.get_measure_that_starts_with_container.get_measure_that_starts_with_container
                ~abjad.tools.scoretools.get_measure_that_stops_with_container.get_measure_that_stops_with_container
                ~abjad.tools.scoretools.get_next_measure_from_component.get_next_measure_from_component
                ~abjad.tools.scoretools.get_previous_measure_from_component.get_previous_measure_from_component
                ~abjad.tools.scoretools.make_empty_piano_score.make_empty_piano_score
                ~abjad.tools.scoretools.make_leaves.make_leaves
                ~abjad.tools.scoretools.make_leaves_from_talea.make_leaves_from_talea
                ~abjad.tools.scoretools.make_multimeasure_rests.make_multimeasure_rests
                ~abjad.tools.scoretools.make_multiplied_quarter_notes.make_multiplied_quarter_notes
                ~abjad.tools.scoretools.make_notes.make_notes
                ~abjad.tools.scoretools.make_notes_with_multiplied_durations.make_notes_with_multiplied_durations
                ~abjad.tools.scoretools.make_percussion_note.make_percussion_note
                ~abjad.tools.scoretools.make_piano_score_from_leaves.make_piano_score_from_leaves
                ~abjad.tools.scoretools.make_piano_sketch_score_from_leaves.make_piano_sketch_score_from_leaves
                ~abjad.tools.scoretools.make_repeated_notes.make_repeated_notes
                ~abjad.tools.scoretools.make_repeated_notes_from_time_signature.make_repeated_notes_from_time_signature
                ~abjad.tools.scoretools.make_repeated_notes_from_time_signatures.make_repeated_notes_from_time_signatures
                ~abjad.tools.scoretools.make_repeated_notes_with_shorter_notes_at_end.make_repeated_notes_with_shorter_notes_at_end
                ~abjad.tools.scoretools.make_repeated_rests_from_time_signatures.make_repeated_rests_from_time_signatures
                ~abjad.tools.scoretools.make_repeated_skips_from_time_signatures.make_repeated_skips_from_time_signatures
                ~abjad.tools.scoretools.make_rests.make_rests
                ~abjad.tools.scoretools.make_skips.make_skips
                ~abjad.tools.scoretools.make_spacer_skip_measures.make_spacer_skip_measures
                ~abjad.tools.scoretools.make_tied_leaf.make_tied_leaf
                ~abjad.tools.scoretools.move_full_measure_tuplet_prolation_to_measure_time_signature.move_full_measure_tuplet_prolation_to_measure_time_signature
                ~abjad.tools.scoretools.move_measure_prolation_to_full_measure_tuplet.move_measure_prolation_to_full_measure_tuplet
                ~abjad.tools.scoretools.scale_measure_denominator_and_adjust_measure_contents.scale_measure_denominator_and_adjust_measure_contents
                ~abjad.tools.scoretools.set_measure_denominator_and_adjust_numerator.set_measure_denominator_and_adjust_numerator
        """) + '\n' == rst.rest_format
