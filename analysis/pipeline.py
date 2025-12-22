# analysis/pipeline.py

import numpy as np

from analysis.config import LFPConfig
from analysis.data_loader import MouseLFPData
from analysis.preprocessing import (
    detect_outliers,
    LowpassFilter,
    apply_filter_to_trials,
)
from analysis.analysis import (
    compute_mean_lfp,
    compute_spectrogram,
)


def run_pipeline(mat_file: str):
    """
    Run the full LFP analysis pipeline.

    Parameters
    ----------
    mat_file : str
        Path to the MATLAB .mat file containing LFP data.

    Returns
    -------
    dict
        Nested dictionary containing analysis results for each session.
    """

    config = LFPConfig()
    data = MouseLFPData(mat_file)

    results = {}

    # Initialize filter once (reused across sessions)
    lowpass_filter = LowpassFilter(
        fs=config.fs,
        cutoff_freq=config.lowpass_cutoff,
        order=config.filter_order,
    )

    for session in range(data.n_sessions):
        # ------------------------------------------
        # Load raw data
        # ------------------------------------------
        lfp_trials = data.get_lfp(session)
        tones = data.get_tones(session)

        # ------------------------------------------
        # Outlier rejection
        # ------------------------------------------
        good_mask = detect_outliers(
            lfp_trials=lfp_trials,
            fs=config.fs,
            baseline_duration_sec=config.baseline_duration_sec,
            rms_threshold=config.rms_threshold,
            ptp_threshold=config.ptp_threshold,
        )

        # ------------------------------------------
        # Filtering
        # ------------------------------------------
        filtered_trials = apply_filter_to_trials(
            lfp_trials,
            lowpass_filter
        )

        # ------------------------------------------
        # Tone-based trial selection
        # ------------------------------------------
        unique_tones = np.unique(tones)
        session_results = {}

        for tone in unique_tones:
            trial_indices = data.get_tone_indices(
                session=session,
                tone_value=tone,
                good_mask=good_mask,
            )

            if len(trial_indices) == 0:
                continue

            # --------------------------------------
            # Mean LFP
            # --------------------------------------
            mean_lfp = compute_mean_lfp(
                filtered_trials,
                trial_indices
            )

            # --------------------------------------
            # Spectrogram
            # --------------------------------------
            f, t, Sxx = compute_spectrogram(
                signal=mean_lfp,
                fs=config.fs,
                max_freq=config.max_analysis_freq,
                window_length=config.window_length,
                window_overlap=config.window_overlap,
                nfft=config.nfft,
            )

            session_results[tone] = {
                "mean_lfp": mean_lfp,
                "spectrogram": {
                    "frequencies": f,
                    "times": t,
                    "power": Sxx,
                },
                "n_trials": len(trial_indices),
            }

        results[f"session_{session+1}"] = session_results

    return results
