"""
Lecture 6.3: DVS Generations and the DAVIS Sensor
"""

# -----------------------
# The Original DVS (2008)

"""
ETH Zurich in 2008, had a 128×128 pixel array. Each pixel was 40 μm × 40 μm.

Dynamic range: approximately 120 dB — roughly 60 dB better than conventional CMOS image sensors,
because the logarithmic encoding handles both very dark and very bright regions simultaneously.

Minimum detectable latency: approximately 1 ms in the original chip
(later generations pushed this to 1 μs).

Output: asynchronous events in Address Event Representation (AER) format
— a standard encoding used in neuromorphic circuits.
"""

# -----------------
# DVS240 and DVS346

"""
The subsequent generation DVS240 increased resolution to 240×180 pixels
while reducing pixel pitch to 24 μm. Improved CMOS process technology
(from the original 0.35 μm to 0.18 μm). Noise characteristics improved significantly.

The DVS346 is a 346×260 pixel device with an 18.5 μm pixel pitch.
- Minimum event latency: approximately 20 μs (limited by readout circuit bandwidth)
- Typical event rate: 1–10 million events per second for natural scenes
- Maximum event rate: approximately 50 million events per second (readout bandwidth limit)
- Power consumption: approximately 140 mW (dominated by readout and interface electronics)
"""

# ---------------------------
# Pixel Noise and Its Sources

"""
Shot noise:
in the photocurrent generates random fluctuations in V_log, occasionally crossing
the threshold θ and generating spurious events. This is most pronounced at low light levels.

Transistor mismatch:
between pixels causes systematic differences in threshold — some pixels have
a slightly lower effective θ than others. This produces “hot pixels” that
generate events continuously regardless of scene content.

Leakage currents:
in the pixel circuit cause slow drift in V_log even when the scene is static,
eventually triggering threshold crossings. This is the “background activity”
visible in DVS event streams even for completely static scenes.
"""

# -------------------------------------------
# The DAVIS Sensor: Two Modalities, One Pixel

"""
The Dynamic and Active-pixel Vision Sensor (DAVIS), at ETH Zurich (published 2014):
integrates both a DVS event circuit and
a conventional Active Pixel Sensor (APS) circuit within the same pixel.

Two complete subcircuits sharing the same photodiode:

The DVS path:
Log converter → difference amplifier → comparator → event generator.
Operates continuously and asynchronously, exactly as described in Lecture 6.2.

The APS path:
Direct photodiode readout → sample-and-hold → column amplifier → analog-to-digital converter.
Produces conventional grayscale frames when triggered. Operates synchronously, on-demand,
at any frame rate from 0 to the maximum supported by the readout circuit.

Simultaneously outputs an asynchronous event stream and synchronous grayscale frames
from the same spatial locations, with perfect pixel-to-pixel alignment.

The DAVIS346:
- Frame resolution: 346×260 (same as DVS path)
- Frame rate: up to ~55 fps
- Bit depth: 8 bits per pixel
- APS and DVS share the same photodiode — they observe the same scene simultaneously
"""

# --------------------
# Why a Hybrid Sensor?

"""
Many event-based processing algorithms are developed and validated by comparing
their outputs to ground-truth information that is more easily extracted from conventional frames.

DAVIS also handles tasks where absolute brightness information is necessary
but temporal precision matters.

The cost of the hybrid design is pixel area: the DAVIS pixel is larger
than a DVS-only pixel of the same generation.
The trade-off is appropriate for research sensors intended for algorithm development.
"""

# ------------------------
# Common Mistakes to Avoid

"""
Students sometimes assume that all event cameras are DVS-derived.
The Prophesee Metavision sensors (used in automotive applications),
the IniVation DAVIS series, and the Samsung DVXplorer use different pixel architectures
and readout circuits. The DVS pixel described in Lecture 6.2 is the canonical design,
but commercial event cameras vary in their detailed circuit implementations.
"""
