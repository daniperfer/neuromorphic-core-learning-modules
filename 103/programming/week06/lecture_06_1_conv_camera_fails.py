"""
Lecture 6.1: Why Conventional Cameras Fail for Neuromorphic Systems

How does information from the physical world get converted
into spike-based signals that neuromorphic hardware can actually process?
"""

# -----------------------------------
# The Frame-Based Camera Architecture

"""
The resulting snapshot is a frame: a 2D array of intensity values
representing the scene at one instant. The camera then discards
whatever it has seen, waits for the next sample time, and repeats.
The numbers, however, are revealing. A 1080p camera operating at
60 frames per second captures 1,920 × 1,080 pixels per frame:
1920 × 1080 × 3 bytes × 60 fps ≈ 374 MB/s
The data volumes are large enough that significant compression and
processing infrastructure is required just to manage the stream,
before any useful computation has occurred.
"""

# --------------------------
# Three Fundamental Problems

"""
Problem 1: Temporal resolution is limited by the frame rate.
Any event that occurs faster than camera temporal resolution cannot be resolved.

Problem 2: Most of the data is redundant.
Vast majority of pixels do not change significantly from frame to frame.

Problem 3: Latency is at minimum one full frame period.
A downstream processor cannot begin working on a frame until the entire frame has been captured.

These are all structural properties of the frame-based architecture,
not implementation deficiencies. Building a faster frame camera generates more data;
it does not eliminate redundancy.
"""

# ---------------------------------------------------------------------
# Worked Example: Comparing a DVS and a Frame Camera on Fly Wing Motion

"""
The DVS wins on latency (1 μs vs. 1 ms), on temporal resolution (no aliasing constraint),
and on data efficiency (orders of magnitude less data for the same scene).
The frame camera wins on absolute brightness information.
For a motion-detection task, this trade-off is strongly in the DVS’s favor.
"""
