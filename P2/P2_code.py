import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import iqr


#Assignment P2 - Part 1

# Load CTD Data with correct column names
file_path = "/Users/heiketihen/THNHAN002-SCDM2025/P1/CTD_Data.dat"

CTD_Data = pd.read_csv(file_path, 
                        names=['Date', 'Time', 'Depth (m)', 'Temperature (C)', 'Salinity (psu)'], 
                        sep=r"\s+", 
                        skiprows=1)  

# Convert to DataFrame
CTD_Data_dataframe = pd.DataFrame(CTD_Data)

# Clean column names (strip spaces)
CTD_Data_dataframe.columns = CTD_Data_dataframe.columns.str.strip()

# Convert columns to numeric
CTD_Data_dataframe["Depth (m)"] = pd.to_numeric(CTD_Data_dataframe["Depth (m)"], errors="coerce")
CTD_Data_dataframe["Temperature (C)"] = pd.to_numeric(CTD_Data_dataframe["Temperature (C)"], errors="coerce")
CTD_Data_dataframe["Salinity (psu)"] = pd.to_numeric(CTD_Data_dataframe["Salinity (psu)"], errors="coerce")

# Drop rows with missing values in critical columns
CTD_Data_dataframe = CTD_Data_dataframe.dropna(subset=["Depth (m)", "Temperature (C)", "Salinity (psu)"])

# Reverse data to ensure correct depth inversion
depth_column = CTD_Data_dataframe["Depth (m)"]
reversed_temperature_column = CTD_Data_dataframe["Temperature (C)"][::-1]
reversed_depth_column = depth_column[::-1]
reversed_salinity_column = CTD_Data_dataframe["Salinity (psu)"][::-1]

# Create figure with two subplots sharing the y-axis
fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(8, 6))

# Plot Temperature Profile
axes[0].plot(reversed_temperature_column, reversed_depth_column, color="red", linewidth=2)
axes[0].set_xlabel("Temperature (C)")
axes[0].set_ylabel("Depth (m)")
axes[0].set_title("Temperature Profile")
axes[0].grid(True, linestyle="--", alpha=0.5)

# Plot Salinity Profile
axes[1].plot(reversed_salinity_column, reversed_depth_column, color="blue", linewidth=1.5)
axes[1].set_xlabel("Salinity (psu)")
axes[1].set_title("Salinity Profile")
axes[1].grid(True, linestyle="--", alpha=0.5)

# Ensure Depth (0m) is at the Top
axes[0].invert_yaxis()
axes[1].invert_yaxis()

# Set correct depth limits
axes[0].set_ylim(max(depth_column), 0)
axes[1].set_ylim(max(depth_column), 0)

# Set Title Formatting to Match Graph
fig.suptitle("Temperature and Salinity data collected from CTD on the 29th of November 2008 at 06:52", fontsize=12)

# Adjust layout
plt.tight_layout()
plt.show()

# Save figure
fig.savefig("CTD_Profiles.png", facecolor="white", bbox_inches="tight", dpi=300)




#Assignment P2 - Part 2


# Load dataset
file_path = "/Users/heiketihen/THNHAN002-SCDM2025/P2/SAA2_WC_2017_metocean_10min_avg.csv"
df = pd.read_csv(file_path)

# Convert TIME_SERVER column to datetime format
df['TIME_SERVER'] = pd.to_datetime(df['TIME_SERVER'], format="%Y/%m/%d %H:%M")
df.set_index('TIME_SERVER', inplace=True)  
df.sort_index(inplace=True) 

# Define departure & arrival times
departure_time = pd.to_datetime("2017/06/28 17:10")
arrival_time = pd.to_datetime("2017/07/04 23:50")

# Filters data for the selected time range
df_filtered = df.loc[departure_time:arrival_time]

# Ensure no missing values in key columns
df_filtered = df_filtered.dropna(subset=['TSG_TEMP', 'TSG_SALINITY', 'WIND_SPEED_TRUE', 'AIR_TEMPERATURE', 'LATITUDE'])

# STEP 1: Time Series of Temperature 
plt.style.use("default")
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('white')

ax.plot(df_filtered.index, df_filtered['TSG_TEMP'], label="Sea Surface Temperature", color='black', linewidth=1.5)
ax.plot(df_filtered.index, df_filtered['AIR_TEMPERATURE'], label="Air Temperature", linestyle="dashed", color='gray', linewidth=1.2)

ax.set_title("Time Series of Sea Surface & Air Temperature\n(2017/06/28 - 2017/07/04)", fontsize=12)
ax.set_xlabel("Time")
ax.set_ylabel("Temperature (°C)")
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("timeseries_plot.png", dpi=300, bbox_inches="tight", facecolor='white')
plt.show()

# STEP 2: Histogram of Salinity Distribution
plt.figure(figsize=(8, 5))
plt.hist(df_filtered['TSG_SALINITY'], bins=np.arange(30, 35.5, 0.5), edgecolor='black', alpha=0.75)

plt.title("Salinity Distribution (30-35 PSU)", fontsize=12)
plt.xlabel("Salinity (PSU)")
plt.ylabel("Frequency")
plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("salinity_histogram.png", dpi=300, bbox_inches="tight", facecolor='white')
plt.show()

# STEP 3: Create and Save Table 
summary_stats = pd.DataFrame({
    "Parameter": ["Sea Surface Temperature (°C)", "Salinity (PSU)"],
    "Mean": [df_filtered['TSG_TEMP'].mean(), df_filtered['TSG_SALINITY'].mean()],
    "Standard Deviation": [df_filtered['TSG_TEMP'].std(), df_filtered['TSG_SALINITY'].std()],
    "Interquartile Range": [iqr(df_filtered['TSG_TEMP']), iqr(df_filtered['TSG_SALINITY'])]
})

# Create table with a title
fig, ax = plt.subplots(figsize=(10, 3))  
ax.set_title("Table showing mean, standard deviation, and the interquartile range\nfor temperature and salinity",
             fontsize=12, fontweight="bold", pad=15)
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=summary_stats.round(4).values,colLabels=summary_stats.columns, cellLoc='center', loc='center')

# Save table as an image with white background
plt.savefig("summary_statistics_high_quality.png", dpi=600, bbox_inches="tight", facecolor='white')
plt.show()

# Adjust font size for better readability
table.auto_set_font_size(False)
table.set_fontsize(12)
table.auto_set_column_width([0, 1, 2, 3])

# Print the summary statistics table in text format
print("\nSummary Statistics for Temperature and Salinity:\n")
print(summary_stats.to_string(index=False))

# STEP 4: Scatter Plot of Wind Speed vs Air Temperature
plt.figure(figsize=(8, 6))
sc = plt.scatter(df_filtered['WIND_SPEED_TRUE'], df_filtered['AIR_TEMPERATURE'], 
                 c=df_filtered['LATITUDE'], cmap='viridis', edgecolor='black', alpha=0.75)

plt.colorbar(sc, label="Latitude")
plt.title("Wind Speed vs Air Temperature (Colored by Latitude)", fontsize=12)
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Air Temperature (°C)")
plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("wind_temp_scatter.png", dpi=300, bbox_inches="tight", facecolor='white')
plt.show()