# -*- encoding: utf-8 -*-
import hashlib
import pickle
import platform
import os
import subprocess
from abjad.tools import systemtools
from abjad.tools.abjadbooktools.ImageOutputProxy import ImageOutputProxy


class GraphvizOutputProxy(ImageOutputProxy):
    r'''A Graphviz output proxy.

    ::

        >>> from abjad.tools import abjadbooktools
        >>> meter = metertools.Meter((4, 4))
        >>> proxy = abjadbooktools.GraphvizOutputProxy(meter)

    ::

        >>> print(proxy.as_latex(relative_output_directory='assets'))
        ['\\noindent\\includegraphics{assets/graphviz-12601707db5ddc467e3296e8c680ba43.pdf}']

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_layout',
        )

    ### INITIALIZER ###

    def __init__(self, payload, layout='dot'):
        payload = pickle.loads(pickle.dumps(payload))
        graphviz_graph = payload.__graph__()
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
        from abjad.tools import abjadbooktools
        code = str(self.payload)
        block = abjadbooktools.SphinxDocumentHandler.abjad_output_block(code, code)
        block['renderer'] = 'graphviz'
        return [block]

    ### PUBLIC PROPERTIES ###

    @property
    def file_name_prefix(self):
        return 'graphviz'

    @property
    def file_name_without_extension(self):
        payload = '\n'.join(str(self.payload))
        md5 = hashlib.md5(payload.encode()).hexdigest()
        return '-'.join((self.file_name_prefix, md5))

    @property
    def layout(self):
        return self._layout