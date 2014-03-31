'''
Created on Mar 30, 2014

@author: ignacio
'''
from collections import namedtuple
import logging
import os
import re
import subprocess
import sys
import tempfile
from argparse import ArgumentParser


RE_VIDEO_RES = 'Video:.* (\d+x\d+)[, ]'
RE_VIDEO_FPS = 'Video:.* ([\d.]+) fps'

VideoData = namedtuple('VideoData', ['path', 'width', 'height', 'fps'])

def _get_arg_parser():
    parser = ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("-s", "--start", type=int, default=None)
    parser.add_argument("-d", "--duration", type=int, default=None)
    parser.add_argument("-l", "--loop", action='store_true', default=False)
    return parser

def _parse_args():
    return _get_arg_parser().parse_args()

def _extract_video_data(video):
    command = ["avprobe", video]
    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    output = proc.stderr.read()
    w, h = re.search(RE_VIDEO_RES, output).group(1).split("x")
    fps = re.search(RE_VIDEO_FPS, output).group(1)
    data = VideoData(path=video, width=int(w), height=int(h), fps=round(float(fps)))
    return data

def _extract_frames(video, output_dir, start=None, duration=None):
    command = ['avconv', '-i', video]
    if start is not None:
        command += ['-ss', str(start)]
    if duration is not None:
        command += ['-t', str(duration)]
    command.append(os.path.join(output_dir, 'frames%05d.gif'))
    subprocess.call(command)

def _make_gif(frames_dir, output, fps, start_frame=None, end_frame=None, loop=True):
    frames = sorted(os.listdir(frames_dir))
    if start_frame is None:
        start_frame = 0
    if end_frame is None:
        end_frame = len(frames)
    command = ['convert', '-delay', '1x%s' % int(fps)]
    if loop:
        command += ['-loop', '0']
    command += [os.path.join(frames_dir, f) for f in frames[start_frame:end_frame]]
    command.append(output)
    subprocess.call(command)

def main():
    logging.basicConfig(level=logging.INFO)
    options = _parse_args()
    logging.info("Extracting video data from '%s'", options.input)
    data = _extract_video_data(options.input)
    logging.info("Data: %s", data)
    tmp_dir = tempfile.mkdtemp()
    logging.info("Temporal dir: '%s'", tmp_dir)
    try:
        logging.info("Extracting frames...")
        _extract_frames(data.path, tmp_dir, options.start, options.duration)
        logging.info("Got %s frames...", len(os.listdir(tmp_dir)))
        logging.info("Making output gif: '%s'", options.output)
        _make_gif(tmp_dir, options.output, data.fps)
        logging.info("Done.")
    finally:
        os.system("rm -rf %s" % tmp_dir)

if __name__ == "__main__":
    main()
