# -*- encoding: utf-8 -*-
from __future__ import print_function
import docutils
import hashlib
import importlib
import os
import pickle
import posixpath
import shutil
import sphinx
import subprocess
import tempfile
import traceback
from abjad import abjad_configuration
from abjad.tools import documentationtools
from abjad.tools import systemtools
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class abjad_book_block(docutils.nodes.General, docutils.nodes.Element):
    pass


class abjad_literal_block(docutils.nodes.General, docutils.nodes.Element):
    pass


class AbjadBookDirective(sphinx.util.compat.Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'errors-ok': docutils.parsers.rst.directives.flag,
        'hidden': docutils.parsers.rst.directives.flag,
        'strip-prompt': docutils.parsers.rst.directives.flag,
        }

    def run(self):
        self.assert_has_content()
        code = u'\n'.join(self.content)
        literal = abjad_literal_block(code, code)
        literal['errors-ok'] = 'errors-ok' in self.options
        literal['hidden'] = 'hidden' in self.options
        literal['strip-prompt'] = 'strip-prompt' in self.options
        sphinx.util.nodes.set_source_info(self, literal)
        return [literal]


class ShellDirective(sphinx.util.compat.Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        self.assert_has_content()
        os.chdir(abjad_configuration.abjad_directory)
        result = []
        for line in self.content:
            prompt = '{}$ '.format(os.path.basename(os.path.abspath(os.path.curdir)))
            prompt += line
            result.append(prompt)
            proc = subprocess.Popen(
                line,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                )
            out, err = proc.communicate()
            result.extend(out.splitlines())
            result.extend(err.splitlines())
        code = u'\n'.join(result)
        literal = docutils.nodes.literal_block(code, code)
        literal['language'] = 'console'
        sphinx.util.nodes.set_source_info(self, literal)
        return [literal]


def on_builder_inited(app):
    app.builder._abjad_book_tempdir = os.path.abspath(
        tempfile.mkdtemp(dir=app.builder.outdir)
        )
    if hasattr(app.builder, 'imgpath'):
        img_directory = os.path.join(app.builder.outdir, '_images')
        if not os.path.exists(img_directory):
            os.makedirs(img_directory)


def rewrite_literal_block_line(line):
    if line.strip().startswith((
        'f(',
        'play(',
        'print ',
        'print(',
        'redo(',
        )):
        return '', False
    elif not line.startswith((
        'show(',
        'topleveltools.graph(',
        'graph(',
        )):
        return line, False
    if line.startswith('show('):
        object_name = line[5:]
        kind = 'lilypond'
    elif line.startswith('graph('):
        object_name = line[len('graph('):]
        kind = 'graphviz'
    elif line.startswith('topleveltools.graph('):
        object_name = line[len('topleveltools.graph('):]
        kind = 'graphviz'
    object_name = object_name.rpartition(')')[0]
    if ')' in object_name:
        object_name = object_name.rpartition(')')[0] + ')'
    elif ',' in object_name:
        object_name = object_name.rpartition(',')[0]
    object_name = object_name.strip()
    if kind in ('lilypond', 'graphviz'):
        return '__abjad_book__ = ({!r}, {})'.format(kind, object_name), True


def scan_doctree_for_literal_blocks(doctree):
    def is_valid_node(node):
        if isinstance(node,
            (docutils.nodes.literal_block, docutils.nodes.doctest_block)
            ):
            return True
        return False
    should_process = False
    literal_blocks = [x for x in doctree.traverse(is_valid_node)]
    literal_lines = []
    for literal_block in literal_blocks:
        lines = []
        for i, line in enumerate(literal_block[0].splitlines()):
            if line.startswith(('>>>', '... ')):
                rewritten_line, has_image = rewrite_literal_block_line(line[4:])
                should_process = should_process or has_image
                lines.append((i, rewritten_line))
        literal_lines.append(tuple(lines))
    return zip(literal_blocks, literal_lines), should_process


def scan_doctree_for_abjad_literal_blocks(doctree):
    abjad_literal_blocks = [x for x in doctree.traverse(abjad_literal_block)]
    should_process = 0 < len(abjad_literal_blocks)
    return abjad_literal_blocks, should_process


def process_literal_block_pairs(literal_block_pairs):
    environment = {
        '__builtins__': __builtins__,
        'print_function': print_function,
        }
    exec('from abjad import *\n', environment)
    try:
        experimental = importlib.import_module('experimental')
        environment.update(experimental.__dict__)
    except ImportError:
        pass
    string_io = StringIO()
    with systemtools.RedirectedStreams(stdout=string_io):
        for literal_block, all_lines in literal_block_pairs:
            original_lines = literal_block[0].splitlines()
            replacement_blocks = []
            lines_to_execute = []
            previous_line_number = 0
            for i, line in all_lines:
                lines_to_execute.append(line)
                if line.startswith('__abjad_book__ ='):
                    if '__abjad_book__' in environment:
                        del(environment['__abjad_book__'])
                    try:
                        exec('\n'.join(lines_to_execute), environment)
                    except Exception:
                        traceback.print_exc()
                    text = '\n'.join(original_lines[previous_line_number:i + 1])
                    new_literal_block = literal_block.deepcopy()
                    new_literal_block.rawsource = text
                    new_literal_block[0].rawsource = text
                    new_literal_block[0].text = text
                    replacement_blocks.append(new_literal_block)
                    if '__abjad_book__' not in environment:
                        print('ERROR: no __abjad_book__ variable found')
                    else:
                        kind, obj = environment['__abjad_book__']
                        new_abjad_book_block = abjad_book_block()
                        new_abjad_book_block['kind'] = kind
                        if kind == 'lilypond':
                            lilypond_file = documentationtools.make_reference_manual_lilypond_file(obj)
                            new_abjad_book_block['code'] = format(lilypond_file)
                            new_abjad_book_block['raw_code'] = format(obj)
                        elif kind == 'graphviz':
                            graphviz_graph = documentationtools.make_reference_manual_graphviz_graph(obj)
                            new_abjad_book_block['code'] = str(graphviz_graph)
                        replacement_blocks.append(new_abjad_book_block)
                    lines_to_execute = []
                    previous_line_number = i + 1
            if lines_to_execute:
                try:
                    exec('\n'.join(lines_to_execute), environment)
                except:
                    pass
                if replacement_blocks:
                    text = '\n'.join(original_lines[previous_line_number:])
                    new_literal_block = literal_block.deepcopy()
                    new_literal_block.rawsource = text
                    new_literal_block[0].rawsource = text
                    new_literal_block[0].text = text
                    replacement_blocks.append(new_literal_block)
            if replacement_blocks:
                literal_block.replace_self(replacement_blocks)


def process_abjad_literal_blocks(abjad_literal_blocks):
    # setup pipe
    pipe = documentationtools.Pipe()
    pipe.read_wait()
    pipe.write('from abjad import *\n')
    pipe.read_wait()

    for abjad_literal_block in abjad_literal_blocks:
        pass

    # cleanup pipe
    pipe.write('quit()\n')
    pipe.close()


def on_doctree_read(app, doctree):
    transform_path = app.config.abjad_book_transform_path
    docname = doctree['source'][:-4].partition(app.srcdir)[-1][1:]
    if not docname.startswith(transform_path):
        return
    result_a = scan_doctree_for_literal_blocks(doctree)
    result_b = scan_doctree_for_abjad_literal_blocks(doctree)
    should_process = result_a[1] or result_b[1]
    if not should_process:
        return
    literal_block_pairs = result_a[0]
    abjad_literal_blocks = result_b[0]
    process_literal_block_pairs(literal_block_pairs)
    #process_abjad_literal_blocks(abjad_literal_blocks)


def on_build_finished(app, exc):
    if os.path.exists(app.builder._abjad_book_tempdir):
        shutil.rmtree(app.builder._abjad_book_tempdir)


def render_graphviz_image(self, code, paths, file_format='png',
    is_latex=False, is_pickled=False, keep_original=False):
    assert file_format in ('png', 'pdf')
    primary_path = paths['primary_absolute_path']
    secondary_path = paths['secondary_absolute_path']
    tmp_path = os.path.join(self.builder._abjad_book_tempdir,
        os.path.basename(os.path.splitext(primary_path)[0])) + '.dot'
    # if we pickled a documentationtools.GraphvizGraph instance
    # in order to support conditional reformatting for LaTeX vs HTML...

    if is_pickled:
        graph = pickle.loads(code)
        alt = str(graph)
        if is_latex:
            graph.attributes['fontsize'] = 10
            graph.attributes['ranksep'] = 0.25
            graph.attributes['ratio'] = 'compress'
            graph.attributes['size'] = 6.5
            graph.node_attributes['fontsize'] = 8
            graph.node_attributes['margin'] = (0.06, 0.06)
        code = graph.unflattened_graphviz_format
    else:
        alt = code
    with open(tmp_path, 'w') as f:
        f.write(code)
    commands = []
    if file_format == 'pdf':
        commands.append('dot -Tpdf -o {} {}'.format(primary_path, tmp_path))
        commands.append('pdfcrop {} {}'.format(primary_path, primary_path))
    elif file_format == 'png':
        commands.append('dot -Tpdf -o {} {}'.format(secondary_path, tmp_path))
        commands.append('dot -Tpng -o {} {}'.format(primary_path, tmp_path))
        commands.append('convert -debug Exception -trim -resize 50%% -resize 800x9999">" {} {}'.format(
            primary_path, primary_path))
    for command in commands:
        subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #subprocess.call(command, shell=True)
    if not keep_original and os.path.exists(secondary_path):
        os.remove(secondary_path)
    return alt


def render_lilypond_image(self, code, paths, file_format='png', keep_original=False):
    assert file_format in ('png', 'pdf')
    absolute_path = paths['primary_absolute_path']
    # LilyPond insists on appending an extension, even if you already did it yourself.
    abs_path = os.path.splitext(absolute_path)[0]
    tmp_path = os.path.join(self.builder._abjad_book_tempdir,
        os.path.basename(os.path.splitext(absolute_path)[0])) + '.ly'
    with open(tmp_path, 'w') as f:
        f.write(code)
    commands = []
    if file_format == 'png':
        commands.append('lilypond --png -dresolution=300 -o {} {}'.format(abs_path, tmp_path))
        commands.append('convert -trim -resample 50%% {} {}'.format(absolute_path, absolute_path))
#        commands.append('lilypond --png -dresolution=600 -o {} {}'.format(abs_path, tmp_path))
#        commands.append('convert -units PixelsPerInch {} -trim -resample 150 -density 72 {}'.format(
#            absolute_path,
#            absolute_path,
#            ))
    elif file_format == 'pdf':
        commands.append('lilypond -o {} {}'.format(abs_path, tmp_path))
        commands.append('pdfcrop {} {}'.format(absolute_path, absolute_path))
    for command in commands:
        subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def render_abjad_book_node(self, node, file_format='png', linked=False):
    code = node['code']
    kind = node['kind']
    keep_original = node.get('keep_original', False)
    is_pickled = node.get('is_pickled', False)
    suffix = 'original'
    hashkey = code.encode('utf-8') + kind
    hexdigest = hashlib.sha1(hashkey).hexdigest()
    # primary in the target format, but secondary always in full-quality PDF
    primary_file_name = '{}-{}.{}'.format(
        kind, hexdigest, file_format)
    secondary_file_name = '{}-{}-{}.pdf'.format(
        kind, hexdigest, suffix)
    paths = {}
    if self.builder.format == 'latex':
        is_latex = True
        paths['primary_relative_path'] = primary_file_name
        paths['primary_absolute_path'] = os.path.join(
            self.builder.outdir, primary_file_name)
        paths['secondary_relative_path'] = secondary_file_name
        paths['secondary_absolute_path'] = os.path.join(
            self.builder.outdir, secondary_file_name)
    else:
        is_latex = False
        img_directory = os.path.join(self.builder.outdir, '_images')
        if not os.path.exists(img_directory):
            os.makedirs(img_directory)
        paths['primary_relative_path'] = posixpath.join(
            self.builder.imgpath, primary_file_name)
        paths['primary_absolute_path'] = os.path.join(
            self.builder.outdir, '_images', primary_file_name)
        paths['secondary_relative_path'] = posixpath.join(
            self.builder.imgpath, secondary_file_name)
        paths['secondary_absolute_path'] = os.path.join(
            self.builder.outdir, '_images', secondary_file_name)
    # TODO: The `alt` handling here is completely hackish, and must be
    #       refactored with the next pass on abjadbooktools.
    alt = node.get('raw_code', '')
    if os.path.isfile(paths['primary_absolute_path']):
        return paths, alt
    if kind == 'lilypond':
        render_lilypond_image(self, code, paths, file_format,
            keep_original=keep_original)
    elif kind == 'graphviz':
        alt = render_graphviz_image(self, code, paths, file_format,
            is_latex=is_latex,
            is_pickled=is_pickled,
            keep_original=keep_original,
            )
    else:
        raise Exception('Unknown node kind, {!r}'.format(kind))
    return paths, alt


def visit_abjad_book_html(self, node):
    result = render_abjad_book_node(self, node, file_format='png')
    paths, alt = result
    alt = self.encode(alt).strip()
    self.body.append('<div class="abjad-book">\n')
    self.body.append('<img src="{}" alt="Click to view source." title="Click to view source."/>\n'.format(
        paths['primary_relative_path']))
    self.body.append('<pre>\n{}\n</pre>\n'.format(alt))
    self.body.append('</div>\n')
    raise docutils.nodes.SkipNode


def visit_abjad_book_latex(self, node):
    paths, alt = render_abjad_book_node(
        self, node, file_format='pdf',
        )
    self.body.append('\n\\includegraphics{' + paths['primary_relative_path'] + '}\n')
    raise docutils.nodes.SkipNode


def setup(app):
    app.add_directive('abjad', AbjadBookDirective)
    app.add_directive('shell', ShellDirective)
    app.add_node(abjad_book_block,
        html=(visit_abjad_book_html, None),
        latex=(visit_abjad_book_latex, None),
        )
    app.connect('builder-inited', on_builder_inited)
    app.connect('doctree-read', on_doctree_read)
    app.connect('build-finished', on_build_finished)
    app.add_config_value('abjad_book_transform_path', 'api/tools/', 'env')