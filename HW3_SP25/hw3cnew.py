def is_symmetric(A):
    # Get the size of the matrix A
    n = len(A)
    # Check each element to see if A is symmetric
    for i in range(n):
        for j in range(n):
            if A[i][j] != A[j][i]:
                return False
    return True


def is_positive_definite(A):
    # Get the size of the matrix A
    n = len(A)
    # Check the diagonal elements to ensure all are positive
    for i in range(n):
        if A[i][i] <= 0:
            return False
    return True


def cholesky_solve(A, b):
    # Get the size of the matrix A
    n = len(A)
    # Initialize L matrix with zeros
    L = [[0.0] * n for _ in range(n)]

    # Decompose matrix A into L * L.T
    for i in range(n):
        for j in range(i + 1):
            if i == j:  # Diagonal elements
                sum_k = sum(L[i][k] ** 2 for k in range(j))
                L[i][j] = (A[i][i] - sum_k) ** 0.5
            else:  # Off-diagonal elements
                sum_k = sum(L[i][k] * L[j][k] for k in range(j))
                L[i][j] = (A[i][j] - sum_k) / L[j][j]

    # Solve L * y = b
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(L[i][j] * y[j] for j in range(i))) / L[i][i]

    # Solve L.T * x = y
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(L[j][i] * x[j] for j in range(i + 1, n))) / L[i][i]

    return x


def doolittle_solve(A, b):
    # Get the size of the matrix A
    n = len(A)
    # Initialize L and U matrices with zeros
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    # Decompose matrix A into L * U
    for i in range(n):
        L[i][i] = 1  # Diagonal elements of L are 1
        for j in range(i, n):  # Calculate U
            sum1 = sum(U[k][j] * L[i][k] for k in range(i))
            U[i][j] = A[i][j] - sum1
        for j in range(i + 1, n):  # Calculate L
            sum2 = sum(U[k][i] * L[j][k] for k in range(i))
            L[j][i] = (A[j][i] - sum2) / U[i][i]

    # Solve L * y = b
    y = [0.0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

    # Solve U * x = y
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

    return x


def solve_system(A, b):
    # Choose the solving method based on matrix properties
    if is_symmetric(A) and is_positive_definite(A):
        method = "Cholesky"
        x = cholesky_solve(A, b)
    else:
        method = "Doolittle"
        x = doolittle_solve(A, b)
    return x, method


def main():
    # List of system matrices and vectors
    systems = [
        ([[1, -1, 3, 2], [-1, 5, -5, -2], [3, -5, 19, 3], [2, -2, 3, 21]], [15, -35, 94, 1]),
        ([[4, 2, 4, 0], [2, 2, 3, 2], [4, 3, 6, 3], [0, 2, 3, 9]], [20, 36, 60, 122])
    ]

    # Solve each system and print the solution
    for i, (A, b) in enumerate(systems):
        x, method = solve_system(A, b)
        print(f"System {i + 1} solution using {method} method: {x}")


if __name__ == "__main__":
    main()
