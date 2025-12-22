# analysis/visualization.py

import numpy as np
import matplotlib.pyplot as plt


def plot_mean_lfp(
    mean_lfp: np.ndarray,
    title: str = "",
    xlabel: str = "Time (samples)",
    ylabel: str = "Amplitude"
):
    """
    Plot mean LFP signal.
    """
    plt.figure(figsize=(10, 4))
    plt.plot(mean_lfp)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_spectrogram(
    frequencies: np.ndarray,
    times: np.ndarray,
    power: np.ndarray,
    title: str = "",
    vmin: float | None = None,
    vmax: float | None = None
):
    """
    Plot spectrogram in dB scale.
    """
    plt.figure(figsize=(10, 5))
    plt.pcolormesh(
        times,
        frequencies,
        10 * np.log10(power + 1e-12),
        shading="gouraud",
        vmin=vmin,
        vmax=vmax
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title(title)
    plt.colorbar(label="Power (dB)")
    plt.tight_layout()
    plt.show()
