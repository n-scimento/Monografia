import matplotlib.pyplot as plt
import numpy as np


def plot_curve(curve, y, t, date, rate, output_name='plot'):

    if rate == 'pre':
        rate = 'DI x Pré'
    elif rate == 'dic':
        rate ='DI x IPCA'

    t_fit = np.linspace(0, 10, 10000)
    y_fit = curve(t_fit)

    plt.figure(figsize=(8, 5))
    plt.scatter(t, y, color='red', label='ETTJ Observada')

    plt.plot(t_fit, y_fit, label='NSS', linestyle='--')
    plt.xlabel("Vértice em DU")
    # plt.xlim(0, 3600)  # Define o limite do eixo x
    # plt.ylim(0.0, 0.2)
    plt.ylabel("Taxa ao ano (%)")
    plt.title(f"{date} - Calibração da Curva Nelson-Siegel-Svensson ({rate})")
    plt.legend()
    plt.grid()
    plt.savefig(f"plots_fixed/{output_name}.png")
    return plt