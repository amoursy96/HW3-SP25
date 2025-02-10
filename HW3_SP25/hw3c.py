import numpy as np

def is_symmetric(A):
    return np.allclose(A, A.T)

def is_positive_definite(A):
    return np.all(np.linalg.eigvals(A) > 0)
#methods of solving 
def cholesky_solve(A, b):
    L = np.linalg.cholesky(A)
    y = np.linalg.solve(L, b)
    x = np.linalg.solve(L.T, y)
    return x

def doolittle_solve(A, b):
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    # LU decomposition
    for i in range(n):
        L[i][i] = 1
        for j in range(i, n):
            sum1 = sum(U[k][j] * L[i][k] for k in range(i))
            U[i][j] = A[i][j] - sum1
        for j in range(i + 1, n):
            sum2 = sum(U[k][i] * L[j][k] for k in range(i))
            L[j][i] = (A[j][i] - sum2) / U[i][i]

    # Solve Ly = b
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

    # Solve Ux = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
         x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

    return x

def solve_system(A, b):
    if is_symmetric(A) and is_positive_definite(A):
        method = "Cholesky"
        x = cholesky_solve(A, b)
    else:
        method = "Doolittle"
        x = doolittle_solve(A, b)
    return x, method
def main():
    # Define the systems
    systems = [
        (np.array([
            [1, -1, 3, 2],
            [-1, 5, -5, -2],
            [3, -5, 19, 3],
            [2, -2, 3, 21]
        ]), np.array([15, -35, 94, 1])),

        (np.array([
            [4, 2, 4, 0],
            [2, 2, 3, 2],
            [4, 3, 6, 3],
            [0, 2, 3, 9]
        ]), np.array([20, 36, 60, 122]))
    ]

    # Solve each system
    for i, (A, b) in enumerate(systems):
        x, method = solve_system(A, b)
        print(f"System {i + 1} solution using {method} method: {x}")

if __name__ == "__main__":
    main()
