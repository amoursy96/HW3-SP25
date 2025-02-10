import math
def gamma_function(alpha):
    if alpha == int(alpha):
        return math.factorial(int(alpha) - 1)  # Gamma(n) = (n-1)!
    else:
        p = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059,
             12.507343278686905, -0.13857109526572012, 9.9843695780195736e-6, 1.5056327351493116e-7] #chatgpt
        g = 7
        alpha -= 1
        z = p[0]
        for i in range(1, g + 2):
            z += p[i] / (alpha + i)
        t = alpha + g + 0.5
        return math.sqrt(2 * math.pi) * (t ** (alpha + 0.5)) * math.exp(-t) * z
    #intergrand for t-dist
def integrand(u, m):
        return (1 + (u ** 2 / m)) ** (-(m + 1) / 2)
    #calc K_m function
def compute_K_m(m):
        numerator = gamma_function(m / 2 + 1 / 2)
        denominator = (math.sqrt(m * math.pi) * gamma_function(m / 2))
        K_m = numerator / denominator
        return K_m
#trapezoidal rule (25-30 chatgpt)
def integrate_trapezoidal(func, a, b, m, n=1000):
        h = (b - a) / n
        integral = 0.5 * (func(a, m) + func(b, m))
        for i in range(1, n):
            integral += func(a + i * h, m)
        return integral * h

def compute_probability(m, z):
        K_m = compute_K_m(m)
        integral = integrate_trapezoidal(integrand, -100, z, m)
        F_z = K_m * integral
        return F_z

def main():
    #degrees of freedom
    m = int(input("Enter the degrees of freedom (m): "))
    if m <= 0:
        print("Degrees of freedom (m) must be a positive integer.")
        return
    #3 values
    z_values = []
    for i in range(3):
        z = float(input(f"Enter z value {i + 1}: "))
        z_values.append(z)

    for z in z_values:
        probability = compute_probability(m, z)
        print(f"F({z}) for m={m} degrees of freedom is approximately: {probability:.6f}")


if __name__ == "__main__":
    main()