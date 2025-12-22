def compute_mean_lfp(filtered_trials, trial_indices):
    return np.mean(filtered_trials[trial_indices], axis=0)
