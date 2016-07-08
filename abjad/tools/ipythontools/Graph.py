# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import tempfile


class Graph(object):
    r'''IPython replacement callable for `topleveltools.graph()`.
    '''

    ### SPECIAL METHODS ###

    def __call__(
        self,
        expr,
        layout='dot',
        graph_attributes=None,
        node_attributes=None,
        edge_attributes=None,
        **kwargs
        ):
        r'''A replacement for Ajbad's graph function for IPython Notebook.
        '''
        from abjad.tools import systemtools
        from IPython.core.display import display_png

        if isinstance(expr, str):
            graphviz_format = expr
        else:
            assert hasattr(expr, '__graph__')
            graphviz_graph = expr.__graph__(**kwargs)
            if graph_attributes:
                graphviz_graph.attributes.update(graph_attributes)
            if node_attributes:
                graphviz_graph.node_attributes.update(node_attributes)
            if edge_attributes:
                graphviz_graph.edge_attributes.update(edge_attributes)
            graphviz_format = str(graphviz_graph)

        valid_layouts = (
            'circo',
            'dot',
            'fdp',
            'neato',
            'osage',
            'sfdp',
            'twopi',
            )
        assert layout in valid_layouts

        message = 'cannot find `{}` command-line tool.'
        message = message.format(layout)
        message += ' Please download Graphviz from graphviz.org.'
        assert systemtools.IOManager.find_executable(layout), message
        assert systemtools.IOManager.find_executable('convert')

        temporary_directory = tempfile.mkdtemp()
        dot_path = os.path.join(temporary_directory, 'graph.dot')
        pdf_path = os.path.join(temporary_directory, 'graph.pdf')
        png_path = os.path.join(temporary_directory, 'graph.png')

        with open(dot_path, 'w') as file_pointer:
            file_pointer.write(graphviz_format)

        command = '{} -v -Tpdf {} -o {}'
        command = command.format(layout, dot_path, pdf_path)
        subprocess.call(command, shell=True)

        command = 'convert {} -trim {}'
        command = command.format(pdf_path, png_path)
        subprocess.call(command, shell=True)

        systemtools.IOManager.spawn_subprocess(command)
        with open(png_path, 'rb') as file_pointer:
            png = file_pointer.read()
        shutil.rmtree(temporary_directory)
        display_png(png, raw=True)
