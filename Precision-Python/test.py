import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


def calculate_rolling_snr(file_path, data_column, window_size=500):
    """
    Calculate and plot rolling SNR over time for bridge SHM sensor data.

    Args:
        file_path (str): Path to CSV file.
        data_column (str): Column name with sensor data.
        window_size (int): Number of samples in each rolling window.
    """
    # Load and clean data
    df = pd.read_csv(file_path)
    timestamp_col = df.columns[0]
    df['DateTime'] = pd.to_datetime(df[timestamp_col])
    df = df.dropna(subset=[data_column])

    data = df[data_column].values
    time = df['DateTime'].values

    # Compute rolling SNR
    rolling_snr = []
    snr_times = []

    for i in range(len(data) - window_size):
        window = data[i:i + window_size]
        signal_power = np.mean(window ** 2)
        noise_power = np.var(window)
        snr_db = 10 * np.log10(signal_power /
                               noise_power) if noise_power != 0 else np.inf
        rolling_snr.append(snr_db)
        # middle time of the window
        snr_times.append(time[i + window_size // 2])

    # Plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(snr_times, rolling_snr, 'r-',
            label=f'Rolling SNR (window= 1 Day)')

    ax.set_xlabel("Date")
    ax.set_ylabel("SNR (dB)")
    ax.set_title(f'Rolling SNR Over Time - Temperature')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d\n%H:%M"))
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.show()


# Usage:
settings = {
    "file_path": "C:/Users/90552/Desktop/Data/.xls/Anytwin_KBB_Messdaten.csv",
    "data_column": "26270TA-_UaKaSo-",
    "window_size": 288  # You can adjust this
}

calculate_rolling_snr(**settings)
