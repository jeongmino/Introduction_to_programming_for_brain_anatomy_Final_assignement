# analysis/preprocessing.py

import numpy as np
from scipy.signal import butter, filtfilt


# --------------------------------------------------
# Outlier detection
# --------------------------------------------------

def detect_outliers(
    lfp_trials: np.ndarray,
    fs: float,
    baseline_duration_sec: float,
    rms_threshold: float,
    ptp_threshold: float,
    ) -> np.ndarray:
    """
    Detect noisy LFP trials based on RMS and peak-to-peak criteria.

    Parameters
    ----------
    lfp_trials : np.ndarray
        LFP trials with shape (n_trials, n_samples)
    fs : float
        Sampling frequency (Hz)
    baseline_duration_sec : float
        Duration of baseline window in seconds
    rms_threshold : float
        Threshold for RMS outlier detection (mean + N * std)
    ptp_threshold : float
        Threshold for peak-to-peak MAD outlier detection

    Returns
    -------
    np.ndarray
        Boolean mask indicating valid trials
    """

    baseline_end = int(baseline_duration_sec * fs)
    baseline = lfp_trials[:, :baseline_end]

    # RMS-based rejection
    rms = np.sqrt(np.mean(baseline ** 2, axis=1))
    rms_limit = rms.mean() + rms_threshold * rms.std()
    good_rms = rms < rms_limit

    # Peak-to-peak-based rejection
    ptp = np.ptp(lfp_trials, axis=1)
    ptp_median = np.median(ptp)
    ptp_mad = np.median(np.abs(ptp - ptp_median))
    ptp_limit = ptp_median + ptp_threshold * ptp_mad
    good_ptp = ptp < ptp_limit

    return good_rms & good_ptp


# --------------------------------------------------
# Filtering
# --------------------------------------------------

class LowpassFilter:
    """
    Low-pass filter for LFP signals.
    """

    def __init__(self, fs: float, cutoff_freq: float, order: int = 10):
        nyquist = fs / 2.0
        normalized_cutoff = cutoff_freq / nyquist
        self.b, self.a = butter(order, normalized_cutoff, btype="low")

    def apply(self, signal: np.ndarray) -> np.ndarray:
        """
        Apply low-pass filtering to a 1D signal.
        """
        return filtfilt(self.b, self.a, signal)


def apply_filter_to_trials(
    lfp_trials: np.ndarray,
    filter_obj: LowpassFilter
    ) -> np.ndarray:
    """
    Apply a filter to all trials in a session.

    Parameters
    ----------
    lfp_trials : np.ndarray
        Raw LFP trials (n_trials, n_samples)
    filter_obj : LowpassFilter
        Initialized filter object

    Returns
    -------
    np.ndarray
        Filtered LFP trials
    """
    return np.array([filter_obj.apply(trial) for trial in lfp_trials])
