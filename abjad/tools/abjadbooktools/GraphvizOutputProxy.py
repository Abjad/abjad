# -*- coding: utf-8 -*-
import copy
import hashlib
import platform
import os
import subprocess
import sys
from abjad.tools import systemtools
from abjad.tools.abjadbooktools.ImageOutputProxy import ImageOutputProxy


class GraphvizOutputProxy(ImageOutputProxy):
    r'''A Graphviz output proxy.

    ::

        >>> from abjad.tools import abjadbooktools
        >>> meter = metertools.Meter((4, 4))
        >>> proxy = abjadbooktools.GraphvizOutputProxy(meter)
        >>> print(format(proxy))
        abjadbooktools.GraphvizOutputProxy(
            documentationtools.GraphvizGraph(
                attributes={
                    'bgcolor': 'transparent',
                    'fontname': 'Arial',
                    'penwidth': 2,
                    'truecolor': True,
                    },
                children=(
                    documentationtools.GraphvizNode(
                        attributes={
                            'label': '4/4',
                            'shape': 'triangle',
                            },
                        ),
                    documentationtools.GraphvizNode(
                        attributes={
                            'label': '1/4',
                            'shape': 'box',
                            },
                        ),
                    documentationtools.GraphvizNode(
                        attributes={
                            'label': '1/4',
                            'shape': 'box',
                            },
                        ),
                    documentationtools.GraphvizNode(
                        attributes={
                            'label': '1/4',
                            'shape': 'box',
                            },
                        ),
                    documentationtools.GraphvizNode(
                        attributes={
                            'label': '1/4',
                            'shape': 'box',
                            },
                        ),
                    documentationtools.GraphvizSubgraph(
                        attributes={
                            'style': 'rounded',
                            },
                        children=(
                            documentationtools.GraphvizNode(
                                attributes={
                                    'color': 'white',
                                    'fillcolor': 'black',
                                    'fontcolor': 'white',
                                    'fontname': 'Arial bold',
                                    'shape': 'Mrecord',
                                    'style': 'filled',
                                    },
                                children=(
                                    documentationtools.GraphvizGroup(
                                        children=(
                                            documentationtools.GraphvizField(
                                                label='0',
                                                ),
                                            documentationtools.GraphvizField(
                                                label='++',
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            documentationtools.GraphvizNode(
                                attributes={
                                    'color': 'white',
                                    'fillcolor': 'black',
                                    'fontcolor': 'white',
                                    'fontname': 'Arial bold',
                                    'shape': 'Mrecord',
                                    'style': 'filled',
                                    },
                                children=(
                                    documentationtools.GraphvizGroup(
                                        children=(
                                            documentationtools.GraphvizField(
                                                label='1/4',
                                                ),
                                            documentationtools.GraphvizField(
                                                label='+',
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            documentationtools.GraphvizNode(
                                attributes={
                                    'color': 'white',
                                    'fillcolor': 'black',
                                    'fontcolor': 'white',
                                    'fontname': 'Arial bold',
                                    'shape': 'Mrecord',
                                    'style': 'filled',
                                    },
                                children=(
                                    documentationtools.GraphvizGroup(
                                        children=(
                                            documentationtools.GraphvizField(
                                                label='1/2',
                                                ),
                                            documentationtools.GraphvizField(
                                                label='+',
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            documentationtools.GraphvizNode(
                                attributes={
                                    'color': 'white',
                                    'fillcolor': 'black',
                                    'fontcolor': 'white',
                                    'fontname': 'Arial bold',
                                    'shape': 'Mrecord',
                                    'style': 'filled',
                                    },
                                children=(
                                    documentationtools.GraphvizGroup(
                                        children=(
                                            documentationtools.GraphvizField(
                                                label='3/4',
                                                ),
                                            documentationtools.GraphvizField(
                                                label='+',
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            documentationtools.GraphvizNode(
                                attributes={
                                    'shape': 'Mrecord',
                                    },
                                children=(
                                    documentationtools.GraphvizGroup(
                                        children=(
                                            documentationtools.GraphvizField(
                                                label='1',
                                                ),
                                            documentationtools.GraphvizField(
                                                label='++',
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        edge_attributes={
                            },
                        is_cluster=True,
                        name='cluster_offsets',
                        node_attributes={
                            },
                        ),
                    ),
                edge_attributes={
                    'penwidth': 2,
                    },
                is_digraph=True,
                name='G',
                node_attributes={
                    'fontname': 'Arial',
                    'fontsize': 12,
                    'penwidth': 2,
                    },
                ),
            layout='dot',
            )

    ::

        >>> proxy.as_latex(relative_output_directory='assets')
        ['\\noindent\\includegraphics{assets/graphviz-31410f5aefd17473e91ebc219ddff36e.pdf}']

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Output Proxies'

    __slots__ = (
        '_layout',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        payload,
        layout='dot',
        image_layout_specifier=None,
        image_render_specifier=None,
        ):
        ImageOutputProxy.__init__(
            self,
            image_layout_specifier=image_layout_specifier,
            image_render_specifier=image_render_specifier,
            )
        #payload = pickle.loads(pickle.dumps(payload))
        graphviz_graph = copy.deepcopy(payload.__graph__())
        self._payload = graphviz_graph
        self._layout = layout

    ### PRIVATE METHODS ###

    def _render_pdf_source(
        self,
        temporary_directory_path,
        ):
        dot_file_path = os.path.join(
            temporary_directory_path,
            self.file_name_without_extension + '.dot',
            )
        source = str(self.payload)
        with open(dot_file_path, 'w') as file_pointer:
            file_pointer.write(source)
        pdf_file_path = os.path.join(
            temporary_directory_path,
            self.file_name_without_extension + '.pdf',
            )
        if platform.system() == 'Darwin':
            command = '{} -v -Tpdf:quartz:quartz {} -o {}'
        else:
            command = '{} -v -Tpdf {} -o {}'
        command = command.format(
            self.layout,
            dot_file_path,
            pdf_file_path,
            )
        exit_code = subprocess.call(
            command,
            shell=True,
            #stdout=subprocess.PIPE,
            #stderr=subprocess.PIPE,
            )
        if exit_code:
            print(source)
            raise AssertionError
        assert os.path.exists(pdf_file_path)
        assert systemtools.IOManager.find_executable('pdfcrop')
        command = 'pdfcrop {path} {path}'.format(path=pdf_file_path)
        exit_code = subprocess.call(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        assert exit_code == 0
        return pdf_file_path

    ### PUBLIC METHODS ###

    def as_docutils(
        self,
        configuration=None,
        output_directory=None,
        ):
        r'''Creates a docutils node representation of the output proxy.

        ::

            >>> for node in proxy.as_docutils():
            ...     print(node.pformat())
            ...
            <abjad_output_block image_layout_specifier image_render_specifier layout="dot" renderer="graphviz" xml:space="preserve">
                digraph G {
                    graph [bgcolor=transparent,
                        fontname=Arial,
                        penwidth=2,
                        truecolor=true];
                    node [fontname=Arial,
                        fontsize=12,
                        penwidth=2];
                    edge [penwidth=2];
                    node_0 [label="4/4",
                        shape=triangle];
                    node_1 [label="1/4",
                        shape=box];
                    node_2 [label="1/4",
                        shape=box];
                    node_3 [label="1/4",
                        shape=box];
                    node_4 [label="1/4",
                        shape=box];
                    subgraph cluster_cluster_offsets {
                        graph [style=rounded];
                        node_5_0 [color=white,
                            fillcolor=black,
                            fontcolor=white,
                            fontname="Arial bold",
                            label="{ <f_0_0> 0 | <f_0_1> ++ }",
                            shape=Mrecord,
                            style=filled];
                        node_5_1 [color=white,
                            fillcolor=black,
                            fontcolor=white,
                            fontname="Arial bold",
                            label="{ <f_0_0> 1/4 | <f_0_1> + }",
                            shape=Mrecord,
                            style=filled];
                        node_5_2 [color=white,
                            fillcolor=black,
                            fontcolor=white,
                            fontname="Arial bold",
                            label="{ <f_0_0> 1/2 | <f_0_1> + }",
                            shape=Mrecord,
                            style=filled];
                        node_5_3 [color=white,
                            fillcolor=black,
                            fontcolor=white,
                            fontname="Arial bold",
                            label="{ <f_0_0> 3/4 | <f_0_1> + }",
                            shape=Mrecord,
                            style=filled];
                        node_5_4 [label="{ <f_0_0> 1 | <f_0_1> ++ }",
                            shape=Mrecord];
                    }
                    node_0 -> node_1;
                    node_0 -> node_2;
                    node_0 -> node_3;
                    node_0 -> node_4;
                    node_1 -> node_5_0 [style=dotted];
                    node_1 -> node_5_1 [style=dotted];
                    node_2 -> node_5_1 [style=dotted];
                    node_2 -> node_5_2 [style=dotted];
                    node_3 -> node_5_2 [style=dotted];
                    node_3 -> node_5_3 [style=dotted];
                    node_4 -> node_5_3 [style=dotted];
                    node_4 -> node_5_4 [style=dotted];
                }
            <BLANKLINE>

        Returns list of docutils nodes.
        '''
        from abjad.tools import abjadbooktools
        result = []
        try:
            code = str(self.payload)
            if sys.version_info[0] == 2:
                code = code.decode('utf-8')
            node = abjadbooktools.abjad_output_block(code, code)
            node['image_layout_specifier'] = self.image_layout_specifier
            node['image_render_specifier'] = self.image_render_specifier
            node['layout'] = self.layout
            node['renderer'] = 'graphviz'
            result.append(node)
        except UnicodeDecodeError:
            print()
            print(type(self))
            for line in code.splitlines():
                print(repr(line))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def file_name_prefix(self):
        r'''Gets file name prefix of Graphviz output proxy.

        Returns string.
        '''
        return 'graphviz'

    @property
    def file_name_without_extension(self):
        r'''Gets file name extension of Graphviz output proxy.

        Returns string.
        '''
        payload = '\n'.join(str(self.payload))
        md5 = hashlib.md5(payload.encode()).hexdigest()
        return '-'.join((self.file_name_prefix, md5))

    @property
    def layout(self):
        r'''Gets layout engine name of Graphviz output.

        Returns string.
        '''
        return self._layout
