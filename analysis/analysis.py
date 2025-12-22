# analysis/analysis.py

import numpy as np
from scipy.signal import spectrogram
from analysis.config import LFPConfig

# --------------------------------------------------
# Mean LFP analysis
# --------------------------------------------------

def compute_mean_lfp(
    lfp_trials: np.ndarray,
    trial_indices: np.ndarray
) -> np.ndarray:
    """
    Compute the mean LFP signal across selected trials.

    Parameters
    ----------
    lfp_trials : np.ndarray
        Filtered LFP trials with shape (n_trials, n_samples)
    trial_indices : np.ndarray
        Indices of trials to include in the average

    Returns
    -------
    np.ndarray
        Mean LFP signal
    """
    if len(trial_indices) == 0:
        raise ValueError("No trials provided for mean LFP computation.")

    return np.mean(lfp_trials[trial_indices], axis=0)


# --------------------------------------------------
# Spectral analysis
# --------------------------------------------------

def compute_spectrogram(
    signal: np.ndarray,
    fs: float,
    max_freq: float,
    window_length: int,
    window_overlap: int,
    nfft: int
):
    """
    Compute spectrogram of an LFP signal.

    Parameters
    ----------
    signal : np.ndarray
        1D LFP signal
    fs : float
        Sampling frequency (Hz)
    max_freq : float
        Maximum frequency to include (Hz)
    window_length : int
        Length of analysis window
    window_overlap : int
        Number of overlapping samples
    nfft : int
        FFT length

    Returns
    -------
    f : np.ndarray
        Frequency axis (Hz)
    t : np.ndarray
        Time axis (s)
    Sxx : np.ndarray
        Power spectral density
    """

    f, t, Sxx = spectrogram(
        signal,
        fs=fs,
        window="hann",
        nperseg=window_length,
        noverlap=window_overlap,
        nfft=nfft,
        scaling="density"
    )

    freq_mask = f <= max_freq
    return f[freq_mask], t, Sxx[freq_mask, :]


def compute_condition_means(
    data: np.ndarray,
    low_idx: list[int],
    high_idx: list[int],
    config: LFPConfig,
    baseline: bool = True
):
    """
    Compute baseline-corrected mean LFP for low/high tone.
    """
    low_trials = data[low_idx]
    high_trials = data[high_idx]

    low_mean = np.mean(low_trials, axis=0)
    high_mean = np.mean(high_trials, axis=0)

    if baseline:
        low_mean = baseline_correct(low_mean, config)
        high_mean = baseline_correct(high_mean, config)

    return low_mean, high_mean


def compute_session_average(
    session_means: list[np.ndarray]
) -> np.ndarray:
    """
    Average across sessions.
    """
    return np.mean(np.stack(session_means), axis=0)
