from scipy.signal import butter, filtfilt
import numpy as np

class LowpassFilter:
    def __init__(self, fs, cutoff, order=10):
        nyq = fs / 2
        self.b, self.a = butter(order, cutoff / nyq, btype='low')

    def apply(self, signal):
        return filtfilt(self.b, self.a, signal)


def detect_outliers(lfp_trials, fs, rms_thresh=3, ptp_thresh=5):
    baseline_end = int(0.1 * fs)
    baseline = lfp_trials[:, :baseline_end]

    rms = np.sqrt(np.mean(baseline**2, axis=1))
    rms_good = rms < (rms.mean() + rms_thresh * rms.std())

    ptp = np.ptp(lfp_trials, axis=1)
    ptp_good = ptp < (np.median(ptp) + ptp_thresh * np.median(np.abs(ptp - np.median(ptp))))

    return rms_good & ptp_good
