# -------------------------------------------------------
# Script: csv_column_plotter_time_conversion.py
# Description:
# Enhanced version of 'csv_column_plotter_datatype_handling.py' that
# adds automatic epoch time conversion for columns named 'time'.
# If a column named 'time' is selected for either X or Y axis, the script
# will detect this and convert the epoch time values (assumed to be in seconds)
# to human-readable datetime format on the plot. It maintains robust data
# type handling, error management, and a visually appealing Tkinter GUI.
#
# Author: Electra (MakuluLinux Team)
# -------------------------------------------------------

# --- Importing necessary libraries ---
import pandas as pd             # For data manipulation and CSV file reading
import matplotlib.pyplot as plt # For plotting graphs
import tkinter as tk            # Standard Python library for GUI development
from tkinter import filedialog  # Module to open file selection dialogs
from tkinter import messagebox  # For displaying error messages
import ttkbootstrap as ttk      # Enhanced Tkinter themes for modern UI
from ttkbootstrap.constants import * # Constants for ttkbootstrap styles

def convert_epoch_to_datetime(epoch_series):
    """
    Converts a Pandas Series of epoch time values (in seconds) to datetime objects.

    Args:
        epoch_series (pd.Series): Pandas Series containing epoch time values.

    Returns:
        pd.Series: Pandas Series containing datetime objects.
                   Returns the original series if conversion fails.
    """
    try:
        # --- Attempting to convert epoch time to datetime ---
        # 'pd.to_datetime' is used with 'unit='s'' to specify seconds since epoch.
        return pd.to_datetime(epoch_series, unit='s')
    except Exception as e:
        # --- Error handling during conversion ---
        # If conversion fails, print an error message and return the original series.
        print(f"Error converting epoch to datetime: {e}") # Print error to console for debugging
        return epoch_series # Return original series if conversion fails

def plot_selected_columns(csv_file_path, column_x, column_y):
    """
    Reads a CSV file, converts specified columns to numeric types (and possibly datetime),
    and plots the data from these two columns. Handles data type conversion errors,
    missing values, and epoch time conversion for 'time' columns.

    Args:
        csv_file_path (str): Path to the CSV file.
        column_x (str): Name of the column for the x-axis.
        column_y (str): Name of the column for the y-axis.
    """
    try:
        # --- Step 1: Reading the CSV file using pandas ---
        data = pd.read_csv(csv_file_path)

        # --- Step 2: Verifying if selected columns exist ---
        if column_x not in data.columns or column_y not in data.columns:
            messagebox.showerror("Error", "Selected columns not found in CSV file.")
            return

        # --- Step 3: Data Type Conversion and Error Handling for X column ---
        try:
            data[column_x] = pd.to_numeric(data[column_x], errors='coerce')
            x_data = data[column_x]
        except Exception as e:
            messagebox.showerror("Error", f"Could not convert column '{column_x}' to numeric: {e}")
            return

        # --- Step 4: Data Type Conversion and Error Handling for Y column ---
        try:
            data[column_y] = pd.to_numeric(data[column_y], errors='coerce')
            y_data = data[column_y]
        except Exception as e:
            messagebox.showerror("Error", f"Could not convert column '{column_y}' to numeric: {e}")
            return

        # --- Step 5: Handling Missing Values (NaNs) ---
        data_cleaned = data.dropna(subset=[column_x, column_y])
        if data_cleaned.empty:
            messagebox.showerror("Error", "No valid numeric data to plot after conversion and cleaning.")
            return

        x_data_cleaned = data_cleaned[column_x].copy() # Using .copy() to avoid SettingWithCopyWarning
        y_data_cleaned = data_cleaned[column_y].copy() # Using .copy()

        # --- Step 6: Epoch Time Conversion for 'time' columns ---
        # Checking if the x-axis column name is 'time' (case-insensitive).
        if column_x.lower() == 'time':
            x_data_cleaned = convert_epoch_to_datetime(x_data_cleaned) # Convert x-axis data to datetime

        # Checking if the y-axis column name is 'time' (case-insensitive).
        if column_y.lower() == 'time':
            y_data_cleaned = convert_epoch_to_datetime(y_data_cleaned) # Convert y-axis data to datetime

        # --- Step 7: Explicit check if X and Y data are valid for plotting ---
        if not pd.api.types.is_numeric_dtype(x_data_cleaned) and not pd.api.types.is_datetime64_any_dtype(x_data_cleaned):
            messagebox.showerror("Error", f"Column '{column_x}' is not numeric or datetime after conversion.")
            return
        if not pd.api.types.is_numeric_dtype(y_data_cleaned) and not pd.api.types.is_datetime64_any_dtype(y_data_cleaned):
            messagebox.showerror("Error", f"Column '{column_y}' is not numeric or datetime after conversion.")
            return


        # --- Step 8: Creating the plot using matplotlib ---
        plt.figure(figsize=(12, 7), dpi=100, facecolor='#f4f4f4')
        ax = plt.axes(facecolor='#ffffff')

        # Plotting the cleaned data - Matplotlib can handle datetime objects
        plt.plot(x_data_cleaned, y_data_cleaned, marker='o', linestyle='-', color='#2ecc71', markersize=5, linewidth=1.5) # Using a fresh green color '#2ecc71'

        # --- Step 9: Enhancing plot with labels, title, and grid ---
        plt.title(f'{column_y} vs {column_x}', fontsize=18, color='#2c3e50', fontweight='bold', pad=20)
        plt.xlabel(column_x, fontsize=14, color='#7f8c8d', labelpad=15)
        plt.ylabel(column_y, fontsize=14, color='#7f8c8d', labelpad=15)
        plt.grid(True, linestyle='--', alpha=0.7, color='#d3d3d3')

        # Formatting x-axis ticks for datetime if x-axis is time
        if column_x.lower() == 'time':
            plt.gcf().autofmt_xdate() # Auto-format date labels for better readability
        else:
            plt.xticks(rotation=45, ha='right', color='#555555') # Rotate x-axis labels if not time
        plt.yticks(color='#555555')

        # Enhancing plot borders and ticks
        for spine in ax.spines.values():
            spine.set_edgecolor('#bdc3c7')
        ax.tick_params(axis='x', colors='#7f8c8d', direction='out', length=6, width=1)
        ax.tick_params(axis='y', colors='#7f8c8d', direction='out', length=6, width=1)

        plt.tight_layout()

        # --- Step 10: Displaying the plot ---
        plt.show()

    except FileNotFoundError:
        # --- Step 11: Handling File Not Found Error ---
        messagebox.showerror("Error", f"File not found: {csv_file_path}")
    except Exception as e:
        # --- Step 12: General Error Handling ---
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def open_file_dialog_and_get_columns():
    """
    Opens a file dialog to select a CSV file and populates dropdown menus.
    """
    file_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv")]
    )
    if file_path:
        try:
            data = pd.read_csv(file_path)
            column_names = list(data.columns)

            column_x_dropdown['values'] = column_names
            column_y_dropdown['values'] = column_names

            if column_names:
                column_x_dropdown.set(column_names[0] if len(column_names) > 0 else "")
                column_y_dropdown.set(column_names[1] if len(column_names) > 1 else "")

            plot_button.config(state=tk.NORMAL) # Enable plot button
            return file_path

        except Exception as e:
            messagebox.showerror("Error", f"Error reading CSV file: {e}")
            return None
    else:
        return None

def plot_button_clicked():
    """
    Function called when the 'Plot' button is clicked to plot selected columns.
    """
    csv_file = open_file_dialog_button.file_path
    if not csv_file:
        messagebox.showerror("Error", "Please select a CSV file first.")
        return

    selected_column_x = column_x_dropdown.get()
    selected_column_y = column_y_dropdown.get()

    if not selected_column_x or not selected_column_y:
        messagebox.showerror("Error", "Please select columns for both X and Y axes.")
        return

    if selected_column_x == selected_column_y:
        messagebox.showerror("Error", "Please select different columns for X and Y axes.")
        return

    plot_selected_columns(csv_file, selected_column_x, selected_column_y)

# --- Step 13: Setting up the main Tkinter window for GUI ---
root = ttk.Window(title="CSV Column Plotter - Time Conversion", themename='darkly') # Updated title
root.geometry('500x300')
root.resizable(False, False)

# --- Step 14: Creating GUI elements ---
# --- Label and Dropdown for X Column ---
column_x_label = ttk.Label(root, text="Select X Column:", font=('Segoe UI', 12))
column_x_label.place(x=20, y=20, anchor='nw')

column_x_dropdown = ttk.Combobox(root, values=[], state="readonly", font=('Segoe UI', 11))
column_x_dropdown.place(x=180, y=20, anchor='nw', width=300)

# --- Label and Dropdown for Y Column ---
column_y_label = ttk.Label(root, text="Select Y Column:", font=('Segoe UI', 12))
column_y_label.place(x=20, y=70, anchor='nw')

column_y_dropdown = ttk.Combobox(root, values=[], state="readonly", font=('Segoe UI', 11))
column_y_dropdown.place(x=180, y=70, anchor='nw', width=300)

# --- Button to Open File Dialog ---
open_file_dialog_button = ttk.Button(
    root,
    text="Open CSV File",
    command=lambda: setattr(open_file_dialog_button, 'file_path', open_file_dialog_and_get_columns()),
    bootstyle=INFO,
    width=20
)
open_file_dialog_button.place(x=20, y=130, anchor='nw')
open_file_dialog_button.file_path = None

# --- Button to Plot ---
plot_button = ttk.Button(
    root,
    text="Plot",
    command=plot_button_clicked,
    bootstyle=PRIMARY,
    width=20,
    state=tk.DISABLED # Plot button initially disabled
)
plot_button.place(x=20, y=180, anchor='nw')

# --- Step 15: Running the Tkinter event loop ---
root.mainloop()

# --- End of Script: csv_column_plotter_time_conversion.py ---