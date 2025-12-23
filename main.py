from analysis.pipeline import run_pipeline
from analysis.visualization import (
    plot_low_high_overlay,
    plot_session_consistency,
)
from analysis.config import LFPConfig


MAT_FILE = "mouseLFP.mat"


def main():
    config = LFPConfig()
    results = run_pipeline("mouseLFP.mat")

    for session_key, session_data in results.items():
        session_id = session_key.split("_")[1]

        if len(session_data) < 2:
            continue

        tones = list(session_data.keys())
        low = tones[0]
        high = tones[1]

        low_mean = session_data[low]["mean_lfp"]
        high_mean = session_data[high]["mean_lfp"]

        output_file = plot_low_high_overlay(
            low_mean,
            high_mean,
            session_id=session_id,
            config=config
        )

        print(
            f"[OK] {session_key}: "
            f"{session_data[low]['n_trials']} low / "
            f"{session_data[high]['n_trials']} high trials → "
            f"{output_file}"
        )

    print("LFP analysis completed successfully.")

if __name__ == "__main__":
    main()
