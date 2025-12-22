# analysis/data_loader.py

import numpy as np
from scipy.io import loadmat


class MouseLFPData:
    """
    Data loader and interface for mouse LFP MATLAB data.

    This class encapsulates the internal structure of the MATLAB .mat file
    and provides clean access methods for LFP signals and tone labels.
    """

    def __init__(self, mat_file: str):
        """
        Load MATLAB file and extract the DATA array.

        Parameters
        ----------
        mat_file : str
            Path to the MATLAB .mat file containing LFP data.
        """
        mat = loadmat(mat_file)
        self._data = mat["DATA"]

        self.n_sessions = self._data.shape[0]
        self.n_fields = self._data.shape[1]

    # --------------------------------------------------
    # Core accessors
    # --------------------------------------------------

    def get_lfp(self, session: int) -> np.ndarray:
        """
        Return LFP matrix for a given session.

        Shape: (n_trials, n_samples)
        """
        return self._data[session, 0]

    def get_tones(self, session: int) -> np.ndarray:
        """
        Return tone labels for a given session.

        Shape: (n_trials,)
        """
        return self._data[session, 4].flatten()

    # --------------------------------------------------
    # Convenience methods
    # --------------------------------------------------

    def get_unique_tones(self, session: int) -> np.ndarray:
        """
        Return unique tone values used in a session.
        """
        return np.unique(self.get_tones(session))

    def get_trial_counts(self, session: int) -> int:
        """
        Return number of trials in a session.
        """
        return self.get_lfp(session).shape[0]

    def get_sample_count(self, session: int) -> int:
        """
        Return number of samples per trial.
        """
        return self.get_lfp(session).shape[1]

    # --------------------------------------------------
    # Tone-based indexing
    # --------------------------------------------------

    def get_tone_indices(self, session: int, tone_value: float,
                         good_mask: np.ndarray | None = None) -> np.ndarray:
        """
        Return trial indices matching a given tone value.

        Parameters
        ----------
        session : int
            Session index.
        tone_value : float
            Tone value to select.
        good_mask : np.ndarray or None
            Optional boolean mask for valid trials.

        Returns
        -------
        np.ndarray
            Array of trial indices.
        """
        tones = self.get_tones(session)
        idx = np.where(tones == tone_value)[0]

        if good_mask is not None:
            idx = idx[good_mask[idx]]

        return idx
