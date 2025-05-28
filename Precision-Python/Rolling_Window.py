import pandas as pd
import matplotlib.pyplot as plt


def plot_rolling_stats_simple(file_path, column_name, window_days=7):
    """
    Plot rolling mean and standard deviation (classic style) for sensor data.

    Args:
        file_path (str): Path to the CSV file.
        column_name (str): Name of the sensor column to plot.
        window_days (int): Rolling window size in days.
    """
    # Load and preprocess data
    df = pd.read_csv(file_path)
    # assuming first column is datetime
    df['DateTime'] = pd.to_datetime(df[df.columns[0]])
    df = df.set_index('DateTime')
    df = df.dropna(subset=[column_name])

    # Calculate rolling window in 5-minute steps
    # e.g., 7 days = 2016 points

   # window_size = int((24 * 60 / 5) * window_days)

    y = df[column_name]

    # Calculate rolling statistics
    rolmean = y.rolling(window=f'{window_days}D').mean()
    rolstd = y.rolling(window=f'{window_days}D').std()

    # Plot
    plt.figure(figsize=(15, 6))
    plt.plot(y, color='blue', label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.xlabel("Date")
    plt.ylabel("Precipitation")  # change column name here
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


# Example usage
plot_rolling_stats_simple(
    file_path="C:/Users/90552/Desktop/Data/.xls/Anytwin_KBB_Messdaten.csv",
    column_name="26270TA-_UaKaSo-",  # Replace with your actual column name
    window_days = 7  # 30-day rolling window

    # You can pick based on your analysis goal:

    # Want to smooth out short-term weather noise? → window_days = 7

    # Interested in monthly or seasonal variability? → window_days = 30 or 90

    # Want to compare year-on-year behavior? → Try plotting window_days = 180 or even 365
)
