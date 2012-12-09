import multiprocessing
import os
import shutil
import tempfile
from abjad.tools import documentationtools
from abjad.tools import sequencetools


def on_builder_inited(app):
    from abjad.docs.source._ext.AbjadBookWorker import AbjadBookWorker
    tmp_directory = app.builder._abjadbook_tempdir = \
        os.path.abspath(tempfile.mkdtemp(dir=app.builder.outdir))
    img_directory = os.path.join(app.builder.outdir, '_images', 'api')
    if not os.path.exists(img_directory):
        os.makedirs(img_directory)
    task_queue = app.builder._abjadbook_task_queue = multiprocessing.JoinableQueue()
    done_queue = app.builder._abjadbook_done_queue = multiprocessing.Queue()
    workers = app.builder._abjadbook_workers = [
        AbjadBookWorker(task_queue, done_queue, tmp_directory, img_directory) 
        for _ in range(multiprocessing.cpu_count() * 2)]
    for worker in workers:
        worker.start()


def on_doctree_read(app, doctree):
    from abjad.docs.source._ext.AbjadBookDoctreeProcessor import AbjadBookDoctreeProcessor
    should_process = app.config.abjadbook_should_process
    transform_path = app.config.abjadbook_transform_path
    doctree_processor = AbjadBookDoctreeProcessor(app, doctree)
    if not should_process:
        return
    #print ''
    #print doctree_processor.docname
    if not doctree_processor.docname.startswith(transform_path):
        return
    result = doctree_processor()
    if not result:
        pass    


def on_build_finished(app, exc):
    workers = app.builder._abjadbook_workers
    task_queue = app.builder._abjadbook_task_queue
    done_queue = app.builder._abjadbook_done_queue
    for worker in workers:
        task_queue.put(None)
    task_queue.join()
    task_queue.close()
    done_queue.close()
    for worker in workers:
        worker.join()
    shutil.rmtree(app.builder._abjadbook_tempdir)


def setup(app):
    app.add_config_value('abjadbook_should_process', False, 'env')
    app.add_config_value('abjadbook_transform_path', 'api/tools/', 'env')
    app.connect('builder-inited', on_builder_inited)
    app.connect('doctree-read', on_doctree_read)
    app.connect('build-finished', on_build_finished)

