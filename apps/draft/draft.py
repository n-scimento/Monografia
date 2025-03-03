import numpy as np
import matplotlib.pyplot as plt
from nelson_siegel_svensson import NelsonSiegelSvenssonCurve
from nelson_siegel_svensson.calibrate import calibrate_nss_ols


def main():
    # Generate synthetic bond yields (time to maturity in years and corresponding yields)
    t = np.array([0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])  # maturities in years
    y = np.array([0.5, 0.7, 1.0, 1.5, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0])  # yields in %

    # Calibrate the NSS curve
    nss_curve, _ = calibrate_nss_ols(t, y)

    # Generate fitted yield curve values
    t_fit = np.linspace(0.1, 30, 100)
    y_fit = nss_curve(t_fit)

    # Plot the results
    plt.figure(figsize=(8, 5))
    plt.scatter(t, y, color='red', label='Observed Yields')
    plt.plot(t_fit, y_fit, label='Fitted NSS Curve', linestyle='--')
    plt.xlabel("Maturity (Years)")
    plt.ylabel("Yield (%)")
    plt.title("Nelson-Siegel-Svensson Yield Curve Calibration")
    plt.legend()
    plt.grid()
    plt.show()
    plt.savefig("plot.png")

    # Print the estimated parameters
    print("Estimated Parameters:")
    print(f"Beta0: {nss_curve.beta0}")
    print(f"Beta1: {nss_curve.beta1}")
    print(f"Beta2: {nss_curve.beta2}")
    print(f"Beta3: {nss_curve.beta3}")
    print(f"Tau1: {nss_curve.tau1}")
    print(f"Tau2: {nss_curve.tau2}")


if __name__ == "__main__":
    main()
