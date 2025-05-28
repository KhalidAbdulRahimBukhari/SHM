# 1. Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

# 3. Define your settings here
settings = {
    # Change when needed
    "file_path": "C:/Users/90552/Desktop/Data/.xls/GS-400 (1).xlsx",
     # Time column
    "timestamp_col": "s",
    # Sensor reading column
    "data_column": "mm",
    # Sensor name (for title)
    "sensor_name": "SWA",
    # True or False
    "zoom": True,
    # Zoom start (minutes)
    "start_minute": 10,
    # Zoom end (minutes)
    "end_minute": 30
}

# 2. Define the function


def plot_data_completeness(file_path, timestamp_col, data_column, sensor_name, zoom=False, start_minute=None, end_minute=None):
    """
    Plot cumulative data completeness over time.
    Inputs are passed as arguments, not from global variables.
    """
    # --- Load data ---
    try:
        df = pd.read_excel(file_path, engine='openpyxl', skiprows=2)
    except ImportError:
        raise ImportError("Please install openpyxl: pip install openpyxl")

    # Clean column names
    df.columns = df.columns.str.replace(r'\s+', '', regex=True)

    # Convert timestamp
    df['timestamp'] = pd.to_timedelta(df[timestamp_col], unit='s')

    # Define missing data
    def is_missing(x):
        return pd.isna(x) or x == 0

    df['is_valid'] = ~df[data_column].apply(is_missing)

    # --- Calculate cumulative valid and total seconds ---
    df['delta_time'] = df[timestamp_col].diff().fillna(0)
    if df['delta_time'].iloc[1] == 0:
        df.loc[df.index[1], 'delta_time'] = df['delta_time'].iloc[2]

    df['valid_seconds'] = df['delta_time'] * df['is_valid']
    df['cumulative_valid_seconds'] = df['valid_seconds'].cumsum()
    df['cumulative_total_seconds'] = df[timestamp_col] - df[timestamp_col].iloc[0]

    df['cumulative_completeness'] = df['cumulative_valid_seconds'] / \
        df['cumulative_total_seconds']
    df['cumulative_completeness'] = df['cumulative_completeness'].fillna(
        1.0).clip(upper=1.0)

    # --- Resample ---
    resampled = df.set_index('timestamp').resample('60S').mean()
    resampled['time_minutes'] = resampled.index.total_seconds() / 60

    # --- Zoom logic ---
    if zoom and start_minute is not None and end_minute is not None:
        resampled = resampled[(resampled['time_minutes'] >= start_minute) & (
            resampled['time_minutes'] <= end_minute)]
        zoom_title = f"(Zoomed: {start_minute}-{end_minute} min)"
    else:
        zoom_title = "(Full Duration)"

    # --- Plot ---
    plt.figure(figsize=(10, 4))
    plt.plot(
        resampled['time_minutes'],
        resampled['cumulative_completeness'],
        color='royalblue',
        linewidth=1.5,
        alpha=0.8
    )

    if (resampled['cumulative_completeness'] < 1.0).any():
        plt.fill_between(
            resampled['time_minutes'],
            resampled['cumulative_completeness'],
            1,
            where=(resampled['cumulative_completeness'] < 1.0),
            color='red',
            alpha=0.2
        )

    # Final completeness for the entire dataset
    final_completeness = df['is_valid'].mean()

    # If zoom is applied, calculate completeness for the zoomed period
    if zoom:
        zoom_completeness = resampled['cumulative_completeness'].iloc[-1]
        final_completeness = zoom_completeness

    # Completeness text box for the current dataset (or zoomed period)
    plt.text(
        0.95, 1.1,
        f'Completeness: {final_completeness:.1%}',
        transform=plt.gca().transAxes,
        ha='right', va='top',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
    )

    existing_data_patch = mlines.Line2D([], [], color='royalblue', marker='s',
                                        linestyle='None', markersize=5, label='Existing Data')
    missing_data_patch = mlines.Line2D([], [], color='red', marker='s',
                                       linestyle='None', markersize=8, alpha=0.3, label='Missing Data')

    plt.legend(handles=[existing_data_patch,
               missing_data_patch], loc='lower right')

    plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
               ['0%', '20%', '40%', '60%', '80%', '100%'])
    plt.ylim(0, 1.05)

    plt.title(
        f'Cumulative Completeness {zoom_title} Sensor: {sensor_name}', pad=30)
    plt.xlabel('Time (minutes)', labelpad=10)
    plt.ylabel('Cumulative Completeness', labelpad=10)

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


# 4. Call the function with the settings
plot_data_completeness(**settings)
