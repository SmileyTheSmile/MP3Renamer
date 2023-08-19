from __future__ import unicode_literals, print_function
from tqdm import tqdm
import contextlib
import ffmpeg
import gevent
import gevent.monkey; gevent.monkey.patch_all(thread=False)
import os
import shutil
import socket
import sys
import tempfile
    
@contextlib.contextmanager
def _tmpdir_scope():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


def _do_watch_progress(filename, sock, handler):
    """Function to run in a separate gevent greenlet to read progress
    events from a unix-domain socket."""
    connection, client_address = sock.accept()
    data = b''
    try:
        while True:
            more_data = connection.recv(16)
            if not more_data:
                break
            data += more_data
            lines = data.split(b'\n')
            for line in lines[:-1]:
                line = line.decode()
                parts = line.split('=')
                key = parts[0] if len(parts) > 0 else None
                value = parts[1] if len(parts) > 1 else None
                handler(key, value)
            data = lines[-1]
    finally:
        connection.close()
    
@contextlib.contextmanager
def _watch_progress(handler):
    """Context manager for creating a unix-domain socket and listen for
    ffmpeg progress events.

    The socket filename is yielded from the context manager and the
    socket is closed when the context manager is exited.

    Args:
        handler: a function to be called when progress events are
            received; receives a ``key`` argument and ``value``
            argument. (The example ``show_progress`` below uses tqdm)

    Yields:
        socket_filename: the name of the socket file.
    """
    with _tmpdir_scope() as tmpdir:
        socket_filename = os.path.join(tmpdir, 'sock')
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        with contextlib.closing(sock):
            sock.bind(socket_filename)
            sock.listen(1)
            child = gevent.spawn(_do_watch_progress, socket_filename, sock, handler)
            try:
                yield socket_filename
            except:
                gevent.kill(child)
                raise
        
@contextlib.contextmanager
def show_progress_old(total_duration) -> str:
    """
    Create a unix-domain socket to watch progress and render tqdm
    progress bar.
    """
    with tqdm(total=round(total_duration, 2)) as bar:
        def handler(key, value):
            if key == 'out_time_ms':
                time = round(float(value) / 1000000., 2)
                bar.update(time - bar.n)
            elif key == 'progress' and value == 'end':
                bar.update(bar.total - bar.n)
        with _watch_progress(handler) as socket_filename:
            yield socket_filename    
    
        
@contextlib.contextmanager
def show_progress(total_duration) -> str:
    """
    Create a unix-domain socket to watch progress and render tqdm
    progress bar.
    """
    progress = 0
    def handler(key, value):
        if key == 'out_time_ms':
            time = round(float(value) / 1000000., 2)
            progress = time - progress
        elif key == 'progress' and value == 'end':
            progress = total_duration - progress
        print(progress)
    with _watch_progress(handler) as socket_filename:
        yield socket_filename    

def metadata_factory(metadata: dict):
    return {
        f'metadata:g:{i}': f"{key}={value}"
        for i, (key, value) in enumerate(metadata.items())
    }

class Converter:
    def convert_to_audio():
        pass

in_filename = "/home/dannyboy/Documents/Projects/MP3Renamer/downloads/Monsoon Love Jukebox - Pehchan Music  Monsoon Special Songs 2018.mp4"
out_filename = "/home/dannyboy/Documents/Projects/MP3Renamer/downloads/1.mp3"

metadata = {
        "title": "sdf",
        "artist": "202sdgs3",
        "album": "wedgw",
        "year": "2023",
    }

total_duration = float(ffmpeg.probe(in_filename)['format']['duration'])


with show_progress(total_duration) as socket_filename:
    try:
        video = ffmpeg.input(in_filename)
        stream = ffmpeg.output(
            video.audio,
            filename=out_filename,
            **metadata_factory(metadata),
        )
        stream = stream.global_args(
            '-progress',
            f'unix://{socket_filename}'
        )
        stream = stream.run(
            capture_stdout=True,
            capture_stderr=True,
            overwrite_output=True,
        )
    except ffmpeg.Error as e:
        print(e.stderr, file=sys.stderr)
        sys.exit(1)








'''
from converter import Converter
conv = Converter()
conv.thumbnail
#info = conv.probe('Monsoon Love Jukebox - Pehchan Music  Monsoon Special Songs 2018.mp4')
info = conv.probe("1 - Don't Deal With The Devil.mp3")
for key, value in vars(info.format).items():
    print(f"{key}: {value}")

convert = conv.convert(
    "/home/dannyboy/Documents/Projects/MP3Renamer/1 - Don't Deal With The Devil.mp3",
    '/home/dannyboy/Documents/Projects/MP3Renamer/test1.mp3', {
    'format': 'mp3',
    'audio':
        {
            'codec': 'mp3',
            'samplerate': 320,
        },
    'metadata':
        {
            'genre': 'dsdsdsd'
        }
    },
)

for timecode in convert:
    print(f'\rConverting ({timecode:.2f}) ...')
'''

import gevent.monkey; gevent.monkey.patch_all()

import contextlib
import ffmpeg
import gevent
import os
import shutil
import socket
import subprocess
import sys
import tempfile


@contextlib.contextmanager
def _tmpdir_scope():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


def _watch_progress(filename, sock, handler):
    connection, client_address = sock.accept()
    data = ''
    with contextlib.closing(connection):
        while True:
            more_data = connection.recv(16)
            if not more_data:
                break
            data += more_data
            lines = data.split('\n')
            for line in lines[:-1]:
                parts = line.split('=')
                key = parts[0] if len(parts) > 0 else None
                value = parts[1] if len(parts) > 1 else None
                handler(key, value)
            data = lines[-1]


@contextlib.contextmanager
def watch_progress(handler):
    with _tmpdir_scope() as tmpdir:
        filename = os.path.join(tmpdir, 'sock')
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        with contextlib.closing(sock):
            sock.bind(filename)
            sock.listen(1)
            child = gevent.spawn(_watch_progress, filename, sock, handler)
            try:
                yield filename
            except:
                gevent.kill(child)
                raise


def metadata_factory(metadata: dict):
    return {
        f'metadata:g:{i}': f"{key}={value}"
        for i, (key, value) in enumerate(metadata.items())
    }

class Converter:
    def convert_to_audio():
        pass

in_filename = "/home/dannyboy/Documents/Projects/MP3Renamer/downloads/Monsoon Love Jukebox - Pehchan Music  Monsoon Special Songs 2018.mp4"
out_filename = "/home/dannyboy/Documents/Projects/MP3Renamer/downloads/1.mp3"


duration = float(ffmpeg.probe(in_filename)['format']['duration'])

prev_text = None

def handler(key, value):
    global prev_text
    if key == 'out_time_ms':
        text = '{:.02f}%'.format(float(value) / 10000. / duration)
        if text != prev_text:
            print(text)
            prev_text = text
            
metadata = {
    "title": "sdf",
    "artist": "202sdgs3",
    "album": "wedgw",
    "year": "2023",
}

with watch_progress(handler) as filename:
    video = ffmpeg.input(in_filename)
    p = subprocess.Popen(
        (video
            .output(
                video.audio,
                filename=out_filename,
                **metadata_factory(metadata),
            )
            .global_args(
                '-progress',
                f'unix://{filename}'
            )
            .overwrite_output()
            .compile()
        ),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out = p.communicate()

if p.returncode != 0:
    sys.stderr.write(out[1])
    sys.exit(1)
