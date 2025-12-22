from scipy.io import loadmat
import numpy as np

class MouseLFPData:
    def __init__(self, mat_file):
        mat = loadmat(mat_file)
        self.data = mat['DATA']
        self.n_sessions = self.data.shape[0]

    def get_lfp(self, session):
        return self.data[session, 0]

    def get_tones(self, session):
        return self.data[session, 4].flatten()

    def get_tone_types(self, session):
        return np.unique(self.get_tones(session))