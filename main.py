# main.py

from analysis.pipeline import run_pipeline
from analysis.visualization import plot_mean_lfp, plot_spectrogram

def main():
    results = run_pipeline("mouseLFP.mat")

    session = "session_1"
    tone = list(results[session].keys())[0]

    mean_lfp = results[session][tone]["mean_lfp"]
    spec = results[session][tone]["spectrogram"]

    plot_mean_lfp(mean_lfp, title=f"{session} - Tone {tone}")
    plot_spectrogram(
        spec["frequencies"],
        spec["times"],
        spec["power"],
        title=f"{session} - Tone {tone} Spectrogram"
    )

if __name__ == "__main__":
    main()
