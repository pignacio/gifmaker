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


RE_VIDEO_RES = 'Video:.* (\d+x\d+)[, ]'
RE_VIDEO_FPS = 'Video:.* ([\d.]+) fps'

VideoData = namedtuple('VideoData', ['path', 'width', 'height', 'fps'])

def _extract_video_data(video):
    command = ["avprobe", video]
    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    output = proc.stderr.read()
    w, h = re.search(RE_VIDEO_RES, output).group(1).split("x")
    fps = re.search(RE_VIDEO_FPS, output).group(1)
    data = VideoData(path=video, width=int(w), height=int(h), fps=round(float(fps)))
    return data

def main():
    data = _extract_video_data(sys.argv[1])
    print data
    tmp_dir = tempfile.mkdtemp()
    logging.info("Temporal dir: '%s'", tmp_dir)
    try:
        pass
    finally:
        os.system("rm -rf %s" % tmp_dir)


if __name__ == "__main__":
    main()
