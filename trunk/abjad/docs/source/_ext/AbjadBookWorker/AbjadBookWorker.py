import multiprocessing
import os
import subprocess
from abjad.tools.abctools import AbjadObject


class AbjadBookWorker(multiprocessing.Process, AbjadObject):

    def __init__(self, task_queue, done_queue, tmp_directory, img_directory):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.done_queue = done_queue 
        self.tmp_directory = tmp_directory
        self.img_directory = img_directory

    def run(self):
        while True:
            job = self.task_queue.get()
            if job is None:
                self.task_queue.task_done()
                break
            else:
                result = self.process_job(job)
                self.done_queue.put(result)
                self.task_queue.task_done()
        return

    def process_job(self, all_md5hashes):

        old_directory = os.curdir
        os.chdir(self.tmp_directory)

        for md5hash in all_md5hashes[:]:
            if os.path.exists(os.path.join(self.img_directory, md5hash + '.png')):
                all_md5hashes.remove(md5hash)

        all_ly_file_names = [x + '.ly' for x in all_md5hashes]
        command = 'lilypond --png -dresolution=300 -djob-count={} {}'.format(
            multiprocessing.cpu_count(), ' '.join(all_ly_file_names))
        subprocess.call(command, shell=True)

        for md5hash in all_md5hashes:
            tmp_png_file_name = os.path.join(self.tmp_directory, md5hash + '.png')
            img_png_file_name = os.path.join(self.img_directory, md5hash + '.png')
            command = 'convert {} -trim -resample 40%% {}'.format(
                tmp_png_file_name, tmp_png_file_name)
            subprocess.call(command, shell=True)
            os.rename(tmp_png_file_name, img_png_file_name)

        #name, extension = os.path.splitext(os.path.basename(ly_file_name))
        #tmp_png_file_name = os.path.join(self.tmp_directory, name + '.png')
        #img_png_file_name = os.path.join(self.img_directory, name + '.png')
        # don't repeat image generation
        #if not os.path.exists(img_png_file_name):
        #    command = 'lilypond --png -dresolution=300 -o {} {}'.format(
        #        tmp_png_file_name[:-4], ly_file_name)
        #    subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #    command = 'convert {} -trim -resample 40%% {}'.format(
        #        tmp_png_file_name, tmp_png_file_name)
        #    subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #    if os.path.exists(tmp_png_file_name):
        #        os.rename(tmp_png_file_name, img_png_file_name)

        os.chdir(old_directory)

        print '\t...returning'

        return True
