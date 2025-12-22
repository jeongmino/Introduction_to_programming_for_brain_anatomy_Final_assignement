# # main.py

# from analysis.pipeline import run_pipeline
# from analysis.visualization import plot_mean_lfp, plot_spectrogram

# def main():
#     results = run_pipeline("mouseLFP.mat")

#     session = "session_1"
#     tone = list(results[session].keys())[0]

#     mean_lfp = results[session][tone]["mean_lfp"]
#     spec = results[session][tone]["spectrogram"]

#     plot_mean_lfp(mean_lfp, title=f"{session} - Tone {tone}")
#     plot_spectrogram(
#         spec["frequencies"],
#         spec["times"],
#         spec["power"],
#         title=f"{session} - Tone {tone} Spectrogram"
#     )

# if __name__ == "__main__":
#     main()

# main.py

from analysis.pipeline import run_pipeline
from analysis.visualization import (
    plot_low_high_overlay,
    plot_session_consistency,
)
from analysis.config import LFPConfig


MAT_FILE = "mouseLFP.mat"


def main():
    config = LFPConfig()
    results = run_pipeline(MAT_FILE)

    # -------------------------------
    # Low vs High tone (per session)
    # -------------------------------
    low_means_across_sessions = []

    for session_name, session_data in results.items():
        tones = sorted(session_data.keys())

        if len(tones) < 2:
            continue

        low_tone = tones[0]
        high_tone = tones[-1]

        low_mean = session_data[low_tone]["mean_lfp"]
        high_mean = session_data[high_tone]["mean_lfp"]

        # Save for session consistency plot
        low_means_across_sessions.append(low_mean)

        # Plot overlay
        plot_low_high_overlay(
            low_mean=low_mean,
            high_mean=high_mean,
            session_id=session_name,
            config=config
        )

    # -------------------------------
    # Session consistency (Low tone)
    # -------------------------------
    if len(low_means_across_sessions) > 1:
        plot_session_consistency(
            session_means=low_means_across_sessions,
            config=config
        )


if __name__ == "__main__":
    main()
