"""
Lecture 2.2: What Is an Event?
"""

# ---------------------------------------
# The Mathematical Definition of an Event

"""
An event-based sensor monitors the logarithm of light intensity at each pixel location.
Let L(x, y, t) denote the log-intensity at pixel (x, y) at time t.
A pixel at location (x, y) fires an event whenever the change in log-intensity since
the last event at that pixel exceeds a threshold C:

ΔL(x, y, t) = L(x, y, t) − L(x, y, t_last) = ±C

When this condition is met, the sensor emits
a single event described by exactly four numbers:

e = (x, y, t, p) is the fundamental unit of information in event-based computing.
There is no frame number, no global clock tick, no pixel value.
"""

# ------------------------
# Polarity: Why It Matters

"""
When a bright object moves against a dark background, it generates
ON events at its leading edge and OFF events at its trailing edge.
An algorithm that tracks the spatial relationship between
ON and OFF event clusters can directly infer the direction of
motion without any frame reconstruction at all.
"""

# ------------------------------------
# The Event Stream: A Sequence in Time

"""
E = {e₁, e₂, e₃, ..., eₙ} where e_i = (x_i, y_i, t_i, p_i) and t₁ ≤ t₂ ≤ ... ≤ tₙ

This asynchronous, data-driven character is the key distinction from
frame-based processing and the key connection to how neurons communicate via spikes.

Example: a fly moving from left to right.
From just these some events, spanning about
458 microseconds (~0.5 ms), we can already extract:

Velocity estimate: The fly’s dark body moved from x=120 to x=123 in roughly
458 µs → approximately 6,550 pixels/second horizontal motion.
Object width: The gap between the OFF event at x=120 and the ON event at x=120
is about 382 µs; combined with velocity, this suggests the fly’s body is
roughly 2.5 pixels wide at this row.
No frame needed: All of this was computed directly from event timestamps
and positions — no image reconstruction, no optical flow over full frames.
"""
