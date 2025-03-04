import matplotlib.pyplot as plt
import numpy as np


def plot_curve(curve, y, t, output_name='plot'):
    t_fit = np.linspace(0, 12000, 12000)
    y_fit = curve(t_fit)

    plt.figure(figsize=(8, 5))
    plt.scatter(t, y, color='red', label='Observed Yields')
    plt.plot(t_fit, y_fit, label='Fitted NSS Curve', linestyle='--')
    plt.xlabel("Maturity (Years)")
    plt.xlim(0, 3600)  # Set x-axis limit
    plt.ylabel("Yield (%)")
    plt.title("Nelson-Siegel-Svensson Yield Curve Calibration")
    plt.legend()
    plt.grid()
    plt.savefig(f"plots/images/{output_name}.png")
    return plt
