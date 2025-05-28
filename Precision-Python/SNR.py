import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


def analyze_temperature_snr(file_path, data_column, window_size=30):
    """
    Properly compute and visualize SNR for temperature data.
    """
    # Load data
    df = pd.read_csv(file_path)
    df['DateTime'] = pd.to_datetime(df.iloc[:, 0])  # First column = timestamp
    df = df.dropna(subset=[data_column])
    y = df[data_column].values
    time = df['DateTime']

    # --- STEP 1: Estimate Signal (Trend) ---
    y_signal = df[data_column].rolling(window=window_size, center=True).mean()

    # --- STEP 2: Compute Noise ---
    noise = y - y_signal

    # --- STEP 3: Calculate SNR ---
    signal_power = np.mean(y_signal**2)
    noise_power = np.mean(noise**2)
    snr_db = 10 * np.log10(signal_power /
                           noise_power) if noise_power != 0 else np.inf

    # --- STEP 4: Plot (Clear Labels!) ---
    plt.figure(figsize=(15, 6))

    # Raw data (blue)
    plt.plot(time, y, 'b-', alpha=0.5, label='Raw Temperature Data')

    # Signal (red)
    plt.plot(time, y_signal, 'r-', linewidth=2,
             label='Seasonal Trend (Signal)')

    # Noise (gray, optional)
    plt.plot(time, noise, 'gray', linestyle='--', alpha=0.3,
             label='Short-Term Fluctuations (Noise)')

    # SNR annotation
    plt.text(0.02, 0.95, f'Avg SNR = {snr_db:.2f} dB', transform=plt.gca().transAxes,
             fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    # Formatting
    plt.title(
        f'Temperature Sensor Analysis: Signal vs. Noise\n{data_column}', fontsize=14)
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.legend()  # Now explains all lines!
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    return snr_db


# Usage
settings = {
    "file_path": "C:/Users/90552/Desktop/Data/.xls/Anytwin_KBB_Messdaten.csv",
    "data_column": "26270TA-_UaKaSo-",
    "Window_Size": 288,
}

snr_db = analyze_temperature_snr(**settings)
