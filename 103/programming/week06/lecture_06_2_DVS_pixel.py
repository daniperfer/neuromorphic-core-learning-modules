"""
Lecture 6.2: The DVS Pixel — From Biology to Silicon
"""

# ------------------------------------------------
# The Biological Circuit: LMCs in the Fly’s Lamina

"""
The fly’s compound eye consists of approximately 700 ommatidia,
each containing six photoreceptor cells (R1–R6) that project to the lamina.
The lamina is the first stage of visual processing, it contains the large monopolar cells
— L1 through L5 — which receive direct synaptic input from the photoreceptors.

The LMC (large monopolar cell) circuit does two things:


1. Logarithmic encoding.
The photoreceptors do not pass their raw output to the LMCs.
Instead, the synapse between photoreceptor and LMC performs a logarithmic transformation:
the signal is proportional to log(luminance), not luminance itself.
The visual system encodes relative changes in luminance, not absolute intensity.

2. Temporal high-pass filtering:
Formally, the LMC output is approximately proportional to d(log L)/dt — the time derivative
of log luminance.
When luminance is constant, the LMC output is near zero.
When luminance changes the LMC fires strongly with polarity: ON for increases, OFF for decreases.
"""

# ---------------------
# The DVS Pixel Circuit

"""
Each DVS pixel operates as follows:

1: Log conversion.
photodiode + transistor operating in subthreshold = voltage proportional to log(luminance).
Call this signal V_log.

2: Temporal differentiation via stored reference.
The pixel continuously computes the difference between the current V_log and this reference:
ΔV = V_log − V_ref.

3: Threshold crossing generates an event.
When ΔV exceeds a positive threshold +θ (typically about 15% change in luminance — in log space),
the pixel fires an ON event and resets V_ref to the current V_log.
When ΔV falls below a negative threshold −θ (a -15%), the pixel fires an OFF and resets V_ref.

4: Event output.
The event is encoded as a tuple (x, y, t, p), where x and y are the pixel’s coordinates,
t is the timestamp of the event with microsecond resolution,
and p is the polarity — 1 for ON, 0 for OFF.

The event rate for a given pixel is therefore proportional to
the speed of the luminance change — fast-moving edges generate higher event rates
than slow-moving ones.
"""

# -------------------------------
# The (x, y, t, p) Tuple Grounded

"""
The asynchronous timestamp is the critical point. There is no frame clock.
Each pixel fires independently, at its own time,
driven only by the dynamics of the scene in its receptive field.
The event stream is a variable-length, irregularly-timed sequence of (x, y, t, p) tuples.
"""

# ------------------------
# Common Mistakes to Avoid

"""
Students sometimes confuse the threshold θ with a signal-to-noise filter.
While a larger θ does reduce noise (spurious events from thermal noise and transistor mismatch),
the threshold is fundamentally a sensitivity control, not a noise filter.
Setting θ too small generates a flood of noise events;
setting it too large makes the sensor insensitive to slow or small-amplitude changes.
The appropriate threshold depends on the application and must be tuned empirically.
"""
