'''
Created on Mar 30, 2014

@author: ignacio
'''
import subprocess
import sys
import re


RE_VIDEO_RES = 'Video:.* (\d+x\d+),'
RE_VIDEO_FPS = 'Video:.* ([\d.]+) fps'

class VideoData():
    def __init__(self, path, width, height, fps):
        self.path = path
        self.width = int(width)
        self.height = int(height)
        self.fps = round(float(fps))

    def __str__(self):
        return "VideoData:[%s: %sx%s@%s]" % (self.path, self.width, self.height, self.fps)

def _extract_video_data(video):
    command = ["avprobe", video]
    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    output = proc.stderr.read()
    w, h = re.search(RE_VIDEO_RES, output).group(1).split("x")
    fps = re.search(RE_VIDEO_FPS, output).group(1)
    data = VideoData(video, w, h, fps)
    return data

def main():
    data = _extract_video_data(sys.argv[1])
    print data


if __name__ == "__main__":
    main()
