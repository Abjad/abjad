from abjad.tools import documentationtools
from abjad.tools import scoretools
from abjad.tools import systemtools


class TestCase(systemtools.TestCase):

    def test_01(self):
        manager = documentationtools.DocumentationManager()
        documenter = documentationtools.ClassDocumenter(
            manager=manager,
            client=scoretools.Note,
            )
        rst = documenter.build_rst()
        assert self.normalize("""
            ..  currentmodule:: abjad.tools.scoretools

            Note
            ====

            ..  autoclass:: Note

            Lineage
            -------

            ..  container:: graphviz

                ..  graphviz::

                    digraph InheritanceGraph {
                        graph [background=transparent,
                            bgcolor=transparent,
                            color=lightslategrey,
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
                        subgraph cluster_scoretools {
                            graph [label=scoretools];
                            "abjad.tools.scoretools.Component.Component" [color=3,
                                group=2,
                                label=Component,
                                shape=oval,
                                style=bold];
                            "abjad.tools.scoretools.Leaf.Leaf" [color=3,
                                group=2,
                                label=Leaf,
                                shape=oval,
                                style=bold];
                            "abjad.tools.scoretools.Note.Note" [color=black,
                                fontcolor=white,
                                group=2,
                                label=<<B>Note</B>>,
                                shape=box,
                                style="filled, rounded"];
                            "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Leaf.Leaf";
                            "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Note.Note";
                        }
                        subgraph cluster_builtins {
                            graph [label=builtins];
                            "builtins.object" [color=2,
                                group=1,
                                label=object,
                                shape=box];
                        }
                        "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.Component.Component";
                        "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
                    }

            Bases
            -----

            - :py:class:`abjad.tools.scoretools.Leaf`

            - :py:class:`abjad.tools.scoretools.Component`

            - :py:class:`abjad.tools.abctools.AbjadObject`

            - :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

            - :py:class:`builtins.object`

            ..  only:: html

                Attribute summary
                -----------------

                ..  autosummary::

                    ~abjad.tools.scoretools.Note.Note.name
                    ~abjad.tools.scoretools.Note.Note.note_head
                    ~abjad.tools.scoretools.Note.Note.written_duration
                    ~abjad.tools.scoretools.Note.Note.written_pitch
                    ~abjad.tools.scoretools.Note.Note.__copy__
                    ~abjad.tools.scoretools.Note.Note.__eq__
                    ~abjad.tools.scoretools.Note.Note.__format__
                    ~abjad.tools.scoretools.Note.Note.__hash__
                    ~abjad.tools.scoretools.Note.Note.__illustrate__
                    ~abjad.tools.scoretools.Note.Note.__mul__
                    ~abjad.tools.scoretools.Note.Note.__ne__
                    ~abjad.tools.scoretools.Note.Note.__repr__
                    ~abjad.tools.scoretools.Note.Note.__rmul__
                    ~abjad.tools.scoretools.Note.Note.__str__

            Read/write properties
            ---------------------

            ..  only:: html

                ..  container:: inherited

                    ..  autoattribute:: abjad.tools.scoretools.Note.Note.name

            ..  autoattribute:: abjad.tools.scoretools.Note.Note.note_head

            ..  autoattribute:: abjad.tools.scoretools.Note.Note.written_duration

            ..  autoattribute:: abjad.tools.scoretools.Note.Note.written_pitch

            Special methods
            ---------------

            ..  only:: html

                ..  container:: inherited

                    ..  automethod:: abjad.tools.scoretools.Note.Note.__copy__

            ..  only:: html

                ..  container:: inherited

                    ..  automethod:: abjad.tools.scoretools.Note.Note.__eq__

            ..  only:: html

                ..  container:: inherited

                    ..  automethod:: abjad.tools.scoretools.Note.Note.__format__

            ..  only:: html

                ..  container:: inherited

                    ..  automethod:: abjad.tools.scoretools.Note.Note.__hash__

            ..  only:: html

                ..  container:: inherited

                    ..  automethod:: abjad.tools.scoretools.Note.Note.__illustrate__

            ..  only:: html

                ..  container:: inherited

                    ..  automethod:: abjad.tools.scoretools.Note.Note.__mul__

            ..  only:: html

                ..  container:: inherited

                    ..  automethod:: abjad.tools.scoretools.Note.Note.__ne__

            ..  only:: html

                ..  container:: inherited

                    ..  automethod:: abjad.tools.scoretools.Note.Note.__repr__

            ..  only:: html

                ..  container:: inherited

                    ..  automethod:: abjad.tools.scoretools.Note.Note.__rmul__

            ..  only:: html

                ..  container:: inherited

                    ..  automethod:: abjad.tools.scoretools.Note.Note.__str__
            """) + '\n' == rst.rest_format
