def graph(argument, format_="pdf", layout="dot",) -> None:
    r"""
    Graphs ``argument``.

    ..  container:: example

        Graphs staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.graph(staff) # doctest: +SKIP

        ..  docs::

            >>> print(format(staff.__graph__(), 'graphviz'))
            digraph G {
                graph [style=rounded];
                node [fontname=Arial,
                    shape=none];
                Staff_0 [label=<
                    <TABLE BORDER="2" CELLPADDING="5">
                        <TR>
                            <TD BORDER="0">Staff</TD>
                        </TR>
                    </TABLE>>,
                    margin=0.05,
                    style=rounded];
                subgraph Staff {
                    graph [color=grey75,
                        penwidth=2];
                    Note_0 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">c'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_1 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">d'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_2 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">e'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_3 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">f'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                }
                Staff_0 -> Note_0;
                Staff_0 -> Note_1;
                Staff_0 -> Note_2;
                Staff_0 -> Note_3;
            }

    ..  container:: example

        Graphs rhythm tree:

        >>> rtm_syntax = '(3 ((2 (2 1)) 2))'
        >>> parser = abjad.rhythmtrees.RhythmTreeParser()
        >>> rhythm_tree = parser(rtm_syntax)[0]
        >>> abjad.graph(rhythm_tree) # doctest: +SKIP

        ..  docs::

            >>> print(format(rhythm_tree.__graph__(), 'graphviz'))
            digraph G {
                graph [bgcolor=transparent,
                    truecolor=true];
                node_0 [label="3",
                    shape=triangle];
                node_1 [label="2",
                    shape=triangle];
                node_2 [label="2",
                    shape=box];
                node_3 [label="1",
                    shape=box];
                node_4 [label="2",
                    shape=box];
                node_0 -> node_1;
                node_0 -> node_4;
                node_1 -> node_2;
                node_1 -> node_3;
            }

    Opens image in default image viewer.
    """
    import abjad.iox

    return abjad.iox.graph(argument, format_=format_, layout=layout,)
