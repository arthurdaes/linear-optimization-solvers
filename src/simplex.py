import numpy as np

SIMPLEX_MIN = 0
SIMPLEX_MAX = 1

def simplex_method(c, A, b, min_or_max=SIMPLEX_MAX):
    # Convert inputs to numpy arrays
    c = np.array(c, dtype=float)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    # Check dimensions and make sure they match to avoid errors
    m, n = A.shape

    if len(c) != n:
        raise ValueError(f"Length of cost vector c ({len(c)}) must match number of variables ({n})")
    if len(b) != m:
        raise ValueError(f"Length of constraints vector b ({len(b)}) must match number of constraints ({m})")

    # create the tableau

    tableau = np.zeros((m + 1, n + m + 1))

    tableau[1 : m + 1, 0 : n] = A # stores the A matrix in the leftmost n columns
    tableau[1 : m + 1, n : n + m] = np.eye(m) # stores the identity matrix in the next m columns
    tableau[1 : m + 1, -1] = b # stores the b vector in the last column
    tableau[0, 0 : n] = c if min_or_max == SIMPLEX_MIN else -c # stores the cost vector in the first row

    # first iteration with basic variables which are the slack variables
    basic_vars = list(range(n, n + m))

    while True:
        # here we only check the first row because it contains the objective function
        pivot_col = np.argmin(tableau[0, 0 : n]) # find the column with the minimum value in the first row
        min_val = tableau[0, pivot_col] # get the minimum value

        # if the minimum value is greater than or equal to 0, we have found the optimal solution
        if min_val >= 0: break

        ratios = []

        # here we calculate the ratios of the last column (b vector) divided by the pivot column
        for i in range(1, m + 1):
            col_val = tableau[i, pivot_col]

            if col_val > 0:
                ratios.append(tableau[i, -1] / col_val)
            else:
                ratios.append(np.inf)

        pivot_row_relative = np.argmin(ratios) # find the row with the minimum ratio

        if ratios[pivot_row_relative] == np.inf:
            raise ValueError("Unbounded problem, check the constraints and objective function.")

        pivot_row = pivot_row_relative + 1 # correct the index to match the tableau itself

        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_element

        for r in range(m + 1):
            if r != pivot_row: # skip the pivot row
                factor = tableau[r, pivot_col]
                tableau[r, :] -= factor * tableau[pivot_row, :] # gauss-jordan elimination

        basic_vars[pivot_row_relative] = pivot_col # update which variable is basic

    x = np.zeros(n)

    for i in range(m):
        bv_index = basic_vars[i]
        if bv_index < n:
            x[bv_index] = tableau[i + 1, -1]

    z = tableau[0, -1]

    return x, z