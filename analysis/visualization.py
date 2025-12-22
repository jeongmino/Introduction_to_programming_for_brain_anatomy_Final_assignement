# analysis/visualization.py

import numpy as np
import matplotlib.pyplot as plt
from analysis.config import LFPConfig

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


def plot_low_high_overlay(
    low_mean,
    high_mean,
    session_id: int,
    config: LFPConfig
):
    plt.figure(figsize=(10, 4))
    plt.plot(low_mean, label="Low tone", color="blue")
    plt.plot(high_mean, label="High tone", color="red")

    # stimulus onset
    plt.axvline(
        x=config.stim_onset_sample,
        color="k",
        linestyle="--",
        label="Stimulus onset"
    )

    plt.title(f"Session {session_id} – Low vs High Tone")
    plt.xlabel("Time (samples)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_session_consistency(
    session_means,
    config: LFPConfig
):
    plt.figure(figsize=(10, 4))

    for i, mean in enumerate(session_means):
        plt.plot(mean, alpha=0.7, label=f"Session {i+1}")

    plt.axvline(
        x=config.stim_onset_sample,
        color="k",
        linestyle="--",
        label="Stimulus onset"
    )

    plt.title("Session Consistency – Mean LFP")
    plt.xlabel("Time (samples)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.tight_layout()
    plt.show()
