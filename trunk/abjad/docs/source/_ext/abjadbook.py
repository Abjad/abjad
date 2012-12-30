import docutils
import hashlib
import multiprocessing
import os
import posixpath
import shutil
import subprocess
import tempfile
from abjad.tools import documentationtools
from abjad.tools import sequencetools


class abjad_book_block(docutils.nodes.General, docutils.nodes.Element):
    pass


def on_builder_inited(app):
    tmp_directory = app.builder._abjadbook_tempdir = \
        os.path.abspath(tempfile.mkdtemp(dir=app.builder.outdir))
    if hasattr(app.builder, 'imgpath'):
        img_directory = os.path.join(app.builder.outdir, '_images')
        if not os.path.exists(img_directory):
            os.makedirs(img_directory)


def rewrite_line(line):
    if line.strip().startswith(('f(', 'play(', 'print ', 'redo(', 'z(', 'iotools.log(')):
        return '', False
    elif not line.startswith(('show(', 'iotools.graph')):
        return line, False
    if line.startswith('show('):
        object_name = line[5:]
        kind = 'lilypond'
    elif line.startswith('iotools.graph('):
        object_name = line[14:]
        kind = 'graphviz'
    object_name = object_name.rpartition(')')[0]
    if ')' in object_name:
        object_name = object_name.rpartition(')')[0] + ')'
    elif ',' in object_name:
        object_name = object_name.rpartition(',')[0]
    object_name = object_name.strip()
    if kind == 'lilypond':
        return '__abjad_book__ = ({!r}, ' \
            'documentationtools.make_reference_manual_lilypond_file({}).lilypond_format)'.format(
            kind, object_name), True
    elif kind == 'graphviz':
        return '__abjad_book__ = ({!r}, ' \
            'documentationtools.make_reference_manual_graphviz_graph({}).graphviz_format)'.format(
            kind, object_name), True


def is_valid_node(node):
    if isinstance(node, 
        (docutils.nodes.literal_block, docutils.nodes.doctest_block)
        ):
        return True
    return False


def scan_doctree(doctree):
    should_process = False
    literal_blocks = [x for x in doctree.traverse(is_valid_node)]
    literal_lines = []
    for literal_block in literal_blocks:
        lines = []
        for i, line in enumerate(literal_block[0].splitlines()):
            if line.startswith(('>>>', '... ')):
                rewritten_line, has_image = rewrite_line(line[4:])
                should_process = should_process or has_image
                lines.append((i, rewritten_line))
        literal_lines.append(tuple(lines))
    return zip(literal_blocks, literal_lines), should_process
    

def on_doctree_read(app, doctree):
    transform_path = app.config.abjadbook_transform_path
    docname = doctree['source'][:-4].partition(app.srcdir)[-1][1:]

    if not docname.startswith(transform_path):
        return

    environment = {'__builtins__': __builtins__}
    exec('from abjad import *\n', environment)

    literal_block_pairs, should_process = scan_doctree(doctree)
    if not should_process:
        return
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
                except:
                    pass
                kind, code = environment['__abjad_book__']
                new_abjad_book_block = abjad_book_block()
                new_abjad_book_block['kind'] = kind
                new_abjad_book_block['code'] = code
                text = '\n'.join(original_lines[previous_line_number:i + 1])
                new_literal_block = literal_block.deepcopy()
                new_literal_block.rawsource = text
                new_literal_block[0].rawsource = text
                new_literal_block[0].text = text
                replacement_blocks.extend([new_literal_block, new_abjad_book_block])
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


def on_build_finished(app, exc):
    if os.path.exists(app.builder._abjadbook_tempdir):
        shutil.rmtree(app.builder._abjadbook_tempdir)


def render_graphviz(self, code, absolute_path, file_format='png'):
    assert file_format in ('png', 'pdf')
    tmp_path = os.path.join(self.builder._abjadbook_tempdir,
        os.path.basename(os.path.splitext(absolute_path)[0])) + '.dot'
    with open(tmp_path, 'w') as f:
        f.write(code)
    commands = []
    if file_format == 'png':
        commands.append('dot -v -Tpng -o {} {}'.format(absolute_path, tmp_path))
        commands.append('convert -trim -resample 50%% {} {}'.format(absolute_path, absolute_path))
    elif file_format == 'pdf':
        commands.append('dot -v -Tpdf -o {} {}'.format(absolute_path, tmp_path))
        commands.append('pdfcrop {} {}'.format(absolute_path, absolute_path))
    for command in commands:
        subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def render_lilypond(self, code, absolute_path, file_format='png'):
    assert file_format in ('png', 'pdf')
    # LilyPond insists on appending an extension, even if you already did it yourself.
    abs_path = os.path.splitext(absolute_path)[0]
    tmp_path = os.path.join(self.builder._abjadbook_tempdir,
        os.path.basename(os.path.splitext(absolute_path)[0])) + '.ly'
    with open(tmp_path, 'w') as f:
        f.write(code)
    commands = []
    if file_format == 'png':
        commands.append('lilypond --png -dresolution=300 -o {} {}'.format(abs_path, tmp_path))
        commands.append('convert -trim -resample 50%% {} {}'.format(absolute_path, absolute_path))
    elif file_format == 'pdf':
        commands.append('lilypond -o {} {}'.format(abs_path, tmp_path))
        commands.append('pdfcrop {} {}'.format(absolute_path, absolute_path))
    for command in commands:
        subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def render_abjad_book_node(self, code, kind, file_format='png'):
    prefix = 'blah'
    hashkey = code.encode('utf-8') + kind
    file_name = '{}-{}.{}'.format(
        kind,
        hashlib.sha1(hashkey).hexdigest(),
        file_format)
    if hasattr(self.builder, 'imgpath'): # HTML
        relative_path = posixpath.join(self.builder.imgpath, file_name)
        absolute_path = os.path.join(self.builder.outdir, '_images', file_name)
    else: # LaTeX
        relative_path = file_name
        absolute_path = os.path.join(self.builder.outdir, file_name)
    if os.path.isfile(absolute_path):
        return relative_path, absolute_path
    # render
    if kind == 'lilypond':
        render_lilypond(self, code, absolute_path, file_format)
    elif kind == 'graphviz':
        render_graphviz(self, code, absolute_path, file_format)
    return relative_path, absolute_path


def visit_abjad_book_html(self, node):
    relative_path, absolute_path = render_abjad_book_node(
        self, node['code'], node['kind'], file_format='png')
    wrapper = 'p'
    alt = self.encode(node['code']).strip()
    self.body.append(self.starttag(node, wrapper, CLASS='abjadbook'))
    self.body.append('<img src="{}" alt="{}" />'.format(relative_path, alt))
    self.body.append('</{}>\n'.format(wrapper))
    raise docutils.nodes.SkipNode


def visit_abjad_book_latex(self, node):
    relative_path, absolute_path = render_abjad_book_node(
        self, node['code'], node['kind'], file_format='pdf')
    self.body.append('\n\\includegraphics{' + relative_path + '}\n')
    raise docutils.nodes.SkipNode


def setup(app):
    app.add_node(abjad_book_block,
        html=(visit_abjad_book_html, None),
        latex=(visit_abjad_book_latex, None),
        # we can add more rendering options later
        #texinfo=(visit_abjad_book_texinfo, None),
        #text=(visit_abjad_book_text, None),
        #man=(visit_abjad_book_man, None)
        )
    app.connect('builder-inited', on_builder_inited)
    app.connect('doctree-read', on_doctree_read)
    app.connect('build-finished', on_build_finished)
    app.add_config_value('abjadbook_transform_path', 'api/tools/', 'env')

