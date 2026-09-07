"""
Lecture 2.1: The Problem with Frames
"""

# ---------------------------------------------
# The Frame-Based Camera: How It Actually Works

"""
Three deep problems for real-time perception:

1. Temporal resolution is locked to frame rate.
If something moves between frames, you miss it.
2. Redundant data floods the pipeline.
In a typical scene, most pixels don’t change much between frames.
3. Latency is baked in. Because a frame-based system must wait until
an entire frame is assembled before it can begin processing,
there is an inherent delay of at least one frame period (16.7 ms at 60 fps)
"""

# ----------------------------
# What the Retina Does Instead

"""
A conventional camera asks: “What does the scene look like right now?”
The retina asks: “What changed since the last moment?”. It is an event-driven device.
"""

# ------------------------
# Common Mistakes to Avoid

"""
some students assume that event-based sensing is only useful
for tracking moving objects. In reality, a stationary observer in a moving scene,
or a moving observer in a stationary scene, both generate rich event streams.
The key is relative motion between the sensor and the visual scene
— not absolute motion of specific objects.
"""
