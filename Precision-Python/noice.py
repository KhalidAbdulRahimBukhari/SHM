import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def calculate_snr(file_path, data_column):
    """
    Calculate and plot SNR for bridge sensor data.
    
    Args:
        file_path (str): Path to CSV file
        data_column (str): Column name with sensor data (e.g., '26270GR-_UaKaSo-')
    """
    # Load data (skip 1 row if needed)
    df = pd.read_csv(file_path)
    
    # Convert timestamp column (first column)
    timestamp_col = df.columns[0]  # Should be 'Timestamp'
    df['DateTime'] = pd.to_datetime(df[timestamp_col])
    df = df.dropna(subset=[data_column])
    data = df[data_column]
    # Calculate SNR
    signal_power = np.mean(data**2)
    noise_power = np.var(data)
    snr_db = 10 * np.log10(signal_power / noise_power) if noise_power != 0 else np.inf
    
    print(f"SNR: {snr_db:.2f} dB")
    
    # Plot data
    fig, ax = plt.subplots(figsize=(15, 5))
    
    # Plot full data in light blue (background)
    ax.plot(df['DateTime'], data, 'b-', alpha=0.3, label='Full Data')
    
    
    # Formatting
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d\n%H:%M"))
    fig.autofmt_xdate()
    ax.set_xlabel('Date')
    ax.set_ylabel('Amplitude')
    ax.set_title(f'Bridge SHM - {data_column}')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
    
    return snr_db

# Example usage - replace with your actual data column
settings = {
    "file_path": "C:/Users/90552/Desktop/Data/.xls/Anytwin_KBB_Messdaten.csv",
    "data_column": "26270TA-_UaKaSo-"  # Replace with your target column
}

snr = calculate_snr(**settings)


#Interpretation:

#A high SNR (dB) means the signal is much stronger than the noise (good quality).

#A low SNR (dB) means the noise is significant compared to the signal (poor quality).

#If SNR is inf, the signal has no noise (perfect signal).

#-------------------------------------------------------------------------------------------------------------

#Assumptions:

#The signal is assumed to be the mean of the data.

#The noise is assumed to be the deviations from the mean (variance).

#This is a basic SNR calculation; in some contexts, noise may be estimated differently (e.g., using a reference noise segment).
