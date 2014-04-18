gifmaker
========

A tool for extracting gifs from videos.

Sample Usage:
-------------

*   To extract the first five seconds of a video:

    `python gifmaker.py -d 5 input.mp4 output.gif`

*   To extract the 5 to 10 second portion:

    `python gifmaker.py -s 5 -d 5 input.mp4 output.gif`

*   Want a looped gif? Just throw in a `-l`/`--loop`

    `python gifmaker.py -s 5 -d 5 --loop input.mp4 output.gif`


Reducing the output size / Gif optimizations
--------------------------------------------

Gifs are optimized by default, but output files might get quite big easily. In order to reduce the output file size, the following can be done:


*   Reduce the gif dimensions

    This can be accomplished via the `--scale` argument, which takes a float as an argument, and scales the output accordingly.

    For example:

    `python gifmaker.py --scale=0.5 input.mp4 output.gif`

    would scale the gif width and height to half the input dimensions.


*   Change the fuzz factor.

    Increasing the fuzz will decrease the output quality and file size. Between 2% and 5%, the quality isn't severely degraded and the output size will decrease dramatically.

    For example:

    `python gifmaker.py --fuzz 5 input.mp4 output.gif`

*   Skip frames.

    You may skip frames, thus reducing the framerate and the output size accordingly:

    `python gifmaker.py --frameskip 1/3 input.mp4 output.gif`

    would skip one third of the input frames.

*   I dont want my gif to be optimized!

    I have no idea why anyone would ever want this, but optimization can be avoided using the `--no-optimize` flag


