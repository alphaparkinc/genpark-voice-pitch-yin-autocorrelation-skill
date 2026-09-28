"""Voice Pitch Detection Engine (YIN Algorithm)
100% Python Standard Library (math).
"""

import math

class VoicePitchYINEngine:
    """Sub-sample fundamental frequency (F0) pitch estimator."""
    def __init__(self, sample_rate=16000, min_freq=50.0, max_freq=500.0, threshold=0.15):
        self.sample_rate = sample_rate
        self.min_lag = int(sample_rate / max_freq)
        self.max_lag = int(sample_rate / min_freq)
        self.threshold = threshold

    def detect_pitch(self, signal):
        w = len(signal) // 2
        if w <= self.max_lag:
            return {"detected": False, "pitch_hz": 0.0, "reason": "Signal buffer too short"}

        # Step 1: Difference Function d_t(tau)
        d = [0.0] * self.max_lag
        for tau in range(self.max_lag):
            s = 0.0
            for j in range(w):
                diff = signal[j] - signal[j + tau]
                s += diff * diff
            d[tau] = s

        # Step 2: Cumulative Mean Normalized Difference Function d'(tau)
        d_prime = [1.0] * self.max_lag
        running_sum = 0.0
        for tau in range(1, self.max_lag):
            running_sum += d[tau]
            if running_sum > 0:
                d_prime[tau] = d[tau] / (running_sum / tau)
            else:
                d_prime[tau] = 1.0

        # Step 3: Absolute Thresholding
        tau_selected = 0
        for tau in range(self.min_lag, self.max_lag):
            if d_prime[tau] < self.threshold:
                while tau + 1 < self.max_lag and d_prime[tau + 1] < d_prime[tau]:
                    tau += 1
                tau_selected = tau
                break

        if tau_selected == 0:
            min_val = float('inf')
            for tau in range(self.min_lag, self.max_lag):
                if d_prime[tau] < min_val:
                    min_val = d_prime[tau]
                    tau_selected = tau

        # Step 4: Parabolic Interpolation
        if 0 < tau_selected < self.max_lag - 1:
            alpha = d_prime[tau_selected - 1]
            beta = d_prime[tau_selected]
            gamma = d_prime[tau_selected + 1]
            denom = 2 * (2 * beta - alpha - gamma)
            if abs(denom) > 1e-6:
                better_tau = tau_selected + (alpha - gamma) / denom
            else:
                better_tau = float(tau_selected)
        else:
            better_tau = float(tau_selected)

        pitch_hz = self.sample_rate / better_tau if better_tau > 0 else 0.0
        harmonicity = 1.0 - min(1.0, d_prime[tau_selected])

        return {
            "detected": harmonicity > 0.4,
            "pitch_hz": round(pitch_hz, 2),
            "period_samples": round(better_tau, 2),
            "harmonicity_confidence": round(harmonicity, 4)
        }
