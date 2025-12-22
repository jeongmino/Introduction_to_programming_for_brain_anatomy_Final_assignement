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


