"""
Lecture 2.7: The Fly’s Eye and the DVS — Biology Meets Silicon
"""

# -----------------------------------------------------
# The Biological Blueprint: Fly Photoreceptors and LMCs

"""
The LMCs (Large Monopolar Cells) have a beautifully specific function.
Their input-output relationship is approximately:

V_LMC(t) ≈ −d/dt [log(I(t))]
That is, the LMC voltage is approximately the negative time derivative of
the logarithm of light intensity. When light brightens, the log-intensity
increases and the LMC hyperpolarizes (becomes more negative). When light dims,
the LMC depolarizes (becomes more positive). When light is constant
— even very bright light — the LMC returns to rest.
"""

# ---------------------------------------
# From Biology to Circuits: The DVS Pixel

"""
Each DVS pixel contains:

1. A logarithmic photoreceptor circuit. A photodiode converts incident
photons to a current. A transimpedance amplifier with a specific nonlinearity
converts this current to a voltage proportional to log(I). This compresses
the dynamic range, just as the fly’s photoreceptors do.

2. A differentiator circuit. The pixel continuously computes d/dt [log(I)]
— the rate of change of log-intensity. This is implemented as a capacitor
that tracks the current log-intensity value and a comparator that measures
deviation from that tracked value.

3. Two comparators with thresholds. When the deviation exceeds +C (brightening),
an ON event is generated. When it exceeds −C (darkening), an OFF event is generated.
After an event, the tracked value is reset to the current log-intensity,
ready to detect the next change.

4. An asynchronous event output circuit. Events are output as digital pulses
with (x, y, polarity) encoded, along with a timestamp from an on-chip microsecond
clock. Each pixel operates entirely independently of all other pixels
— there is no global shutter, no row-select timing, no synchronization whatsoever.
"""

# -
# Common Mistakes to Avoid

"""
Students sometimes expect the DVS to produce exactly one event per threshold
crossing, with perfect precision. In practice, pixel circuit mismatch means
that different pixels have slightly different effective thresholds
— some fire at 45% contrast, others at 70%, even with the same nominal
threshold setting. This is called threshold variation and is the primary
source of fixed-pattern noise in DVS sensors. Modern sensors include per-pixel
calibration circuits to reduce this variation, but it cannot be eliminated entirely.

Another misunderstanding is that the DVS timestamp is the exact moment
a photon changed the light level. In reality, there is a small delay
— typically 10–100 microseconds — between the physical event in the
scene and the output of the pixel circuit.
"""
