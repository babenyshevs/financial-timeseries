from typing import List, Tuple

import numpy as np


def split_sequences(
    sequences: np.ndarray, n_steps_in: int, n_steps_out: int
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Splits sequences into input-output pairs for a time series prediction task.

    Args:
        sequences (np.ndarray): The input sequences, where each row represents a time step.
        n_steps_in (int): Number of input time steps.
        n_steps_out (int): Number of output time steps.

    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing the input sequences and corresponding output sequences.
            The input sequences have shape (num_samples, n_steps_in, num_features),
            and the output sequences have shape (num_samples, n_steps_out).
    """
    X, y = list(), list()
    for i in range(len(sequences)):
        # find the end of this pattern
        end_ix = i + n_steps_in
        out_end_ix = end_ix + n_steps_out - 1
        # check if we are beyond the dataset
        if out_end_ix > len(sequences):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix - 1 : out_end_ix, -1]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)
