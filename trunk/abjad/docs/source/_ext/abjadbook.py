import docutils
import multiprocessing
import os
import posixpath
import shutil
import subprocess
import tempfile
from abjad.tools import documentationtools
from abjad.tools import sequencetools
from sphinx.util.osutil import relative_uri


class Worker(multiprocessing.Process):

    def __init__(self, job_queue, tmp_directory, img_directory):
        multiprocessing.Process.__init__(self)
        self.job_queue = job_queue
        self.tmp_directory = tmp_directory
        self.img_directory = img_directory

    def run(self):
        while True:
            job = self.job_queue.get()
            if job is None:
                self.job_queue.task_done()
                break
            else:
                self.process_job(job)
                self.job_queue.task_done()
        return

    def process_job(self, job):
        script_path, all_images = job
        process = subprocess.Popen(['python', script_path],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            )
        stderr = process.stderr.read()
        if stderr:
            print stderr
            return
        for file_name in all_images: 
            lilypond_file_name = os.path.join(self.tmp_directory, file_name + '.ly')
            tmp_png_file_name = os.path.join(self.tmp_directory, file_name + '.png')
            img_png_file_name = os.path.join(self.img_directory, file_name + '.png')

            command = 'lilypond --png -dresolution=300 -o {} {}'.format(
                os.path.join(self.tmp_directory, file_name), lilypond_file_name)
            subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            command = 'convert {} -trim -resample 40%% {}'.format(
                tmp_png_file_name, tmp_png_file_name)
            subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if os.path.exists(tmp_png_file_name):
                os.rename(tmp_png_file_name, img_png_file_name)

def add_image_block(literal_block, uri):
    image = docutils.nodes.image(
        candidates={'*': uri},
        uri=uri,
        )
    literal_block.replace_self([literal_block, image])


def builder_inited(app):
    tmp_directory = os.path.abspath(tempfile.mkdtemp(dir=app.builder.outdir))
    img_directory = os.path.join(app.builder.outdir, '_images', 'api')
    if not os.path.exists(img_directory):
        os.makedirs(img_directory)
    app.builder._abjadbook_tempdir = tmp_directory
    queue = app.builder._abjadbook_queue = multiprocessing.JoinableQueue()
    workers = app.builder._abjadbook_workers = [
        Worker(queue, tmp_directory, img_directory) 
        for _ in range(multiprocessing.cpu_count() * 2)]
    for worker in workers:
        worker.start()


def build_finished(app, exc):
    workers = app.builder._abjadbook_workers
    queue = app.builder._abjadbook_queue
    for worker in workers:
        queue.put(None)
    queue.join()
    queue.close()
    for worker in workers:
        worker.join()
    shutil.rmtree(app.builder._abjadbook_tempdir)


def collect_literal_block_pairs(doctree):
    pairs = []
    has_show_command = False
    for literal_block in doctree.traverse(docutils.nodes.literal_block):
        stripped_lines = []
        for line in literal_block[0].splitlines():
            if line.startswith(('>>> ', '... ')):
                line = line[4:]
                if line.startswith('show('):
                    has_show_command = True
                stripped_lines.append(line)
        pairs.append((literal_block, tuple(stripped_lines)))
    if has_show_command:
        return tuple(pairs)
    return None


def get_image_prefix(docname, transform_path):
    image_prefix = docname.partition(transform_path)[-1]
    if image_prefix.startswith('/'):
        image_prefix = image_prefix[1:]
    parts = image_prefix.split('/')
    unique_parts = [parts[0]]
    for part in parts[1:]:
        if part != unique_parts[-1]:
            unique_parts.append(part)
        else:
            break
    image_prefix = '__'.join(unique_parts)
    return image_prefix


def process_doctree(app, doctree, docname):

    abs_imgpath = os.path.join(app.builder.outdir, '_images', 'api')
    rel_imgpath = relative_uri(app.builder.get_target_uri(docname),
        os.path.join('_images', 'api'))

    if not (app.config.abjadbook_should_process and \
        docname.startswith(app.config.abjadbook_transform_path)):
        return

    pairs = collect_literal_block_pairs(doctree)
    if pairs is None:
        return

    # setup
    if not os.path.exists(abs_imgpath):
        os.mkdir(abs_imgpath)
    tmp_directory = app.builder._abjadbook_tempdir
    literal_block_images = {}

    image_prefix = get_image_prefix(docname, app.config.abjadbook_transform_path)
    image_count = 0

    assert os.path.exists(tmp_directory)

    # create tmp python file, create .ly files
    script_path = os.path.join(tmp_directory, 'tmp__{}.py'.format(image_prefix))
    with open(script_path, 'w') as f:
        f.write('from abjad import *\n')
        for literal_block, stripped_lines in pairs:
            for line in stripped_lines:
                if line.startswith('show('):
                    image_count += 1
                    file_name = '{}-{}'.format(image_prefix, image_count)

                    object_name = line[5:]
                    object_name = object_name.rpartition(')')[0]
                    if ')' in object_name:
                        object_name = object_name.rpartition(')')[0] + ')'
                    elif ',' in object_name:
                        object_name = object_name.rpartition(',')[0]

                    command = "iotools.write_expr_to_ly({}, {!r}, docs=True)".format(
                        object_name, os.path.join(tmp_directory, file_name))
                    f.write(command + '\n')
                    if literal_block not in literal_block_images:
                        literal_block_images[literal_block] = []
                    literal_block_images[literal_block].append(file_name)
                else:
                    f.write(line + '\n')

    all_images = tuple(sequencetools.flatten_sequence(literal_block_images.values()))
    app.builder._abjadbook_queue.put((script_path, all_images))

    # run LilyPond on generated .ly files, move 
    for literal_block, file_names in literal_block_images.items():
        for file_name in sorted(file_names):
            uri = os.path.join(rel_imgpath, file_name + '.png')
            add_image_block(literal_block, uri)


def setup(app):
    app.add_config_value('abjadbook_should_process', False, 'env')
    app.add_config_value('abjadbook_transform_path', 'api/tools/', 'env')
    app.connect('builder-inited', builder_inited)
    app.connect('doctree-resolved', process_doctree)
    app.connect('build-finished', build_finished)

