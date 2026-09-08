"""
Lecture 2.3: Synchronous vs. Asynchronous Processing
"""

# --------------------------------------------
# The Asynchronous Paradigm: Compute on Demand

"""
An asynchronous system has no global clock.
Components communicate by sending events and each component wakes up, does
its computation, and goes back to sleep when it has nothing to do.
The system is entirely data-driven: activity is proportional to the rate of
incoming events, not to the passage of time.

This causes:
- low latency
- low power consumption
"""

# ------------------------
# Common Mistakes to avoid

"""
Asynchronous processing is not universally superior.
For tasks involving dense, uniformly sampled data — audio recording,
financial modeling, scientific simulation — the synchronous paradigm is
often more appropriate. The insight of neuromorphic engineering is not
that clocks are bad, but that for perception and real-time interaction with
a sparse, dynamic physical world, asynchrony is the right match.
"""
