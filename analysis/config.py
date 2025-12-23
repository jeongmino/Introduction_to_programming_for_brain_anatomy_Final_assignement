from dataclasses import dataclass
import numpy as np


@dataclass
class LFPConfig:
    
    fs: float = 10000.0                     # Sampling frequency (Hz)
    lowpass_cutoff: float = 1000.0          # Low-pass filter cutoff frequency (Hz)
    filter_order: int = 10
    max_analysis_freq: float = 200.0        # Maximum frequency for analysis (Hz)
    freq_bin_width: float = 5.0             # Frequency bin width (Hz)
    window_length: int = 256
    window_overlap: int = 255
    nfft: int = 2048
    stim_onset_sample: int = 1000
    stim_offset_sample: int = 1500
    baseline_duration_sec: float = 0.1      # Baseline window for RMS (seconds)
    rms_threshold: float = 3.0              # RMS threshold (mean + N*std)
    ptp_threshold: float = 5.0              # Peak-to-peak MAD threshold

    @property
    def nyquist(self) -> float:             #Nyquist frequency.
        return self.fs / 2.0

    @property
    def freq_bins(self) -> np.ndarray:      #Frequency bins for spectral analysis.
        return np.arange(
            0,
            self.max_analysis_freq + self.freq_bin_width,
            self.freq_bin_width
        )

    @property
    def stim_onset_ms(self) -> float:       #Stimulus onset time in milliseconds.
        return self.stim_onset_sample / self.fs * 1000.0

    @property
    def stim_offset_ms(self) -> float:      #Stimulus offset time in milliseconds.
        return self.stim_offset_sample / self.fs * 1000.0
