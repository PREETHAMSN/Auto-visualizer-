import pandas as pd
import re

def parse_logs_from_file(log_file_path):
    # Define the path for the new CSV file
    csv_file_path = r"C:\Users\LENOVO\Downloads\processed_log_data.csv"
    
    # Initialize empty lists to store parsed data
    timestamps = []
    log_levels = []
    components = []
    messages = []

    # Define a regular expression to match log line pattern (adjust according to your log format)
    log_pattern = r'(?P<Timestamp>\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})\s+(?P<LogLevel>[A-Z]+)\s+(?P<Component>[\w-]+):\s+(?P<Message>.+)'

    # Read the log file and parse each line
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            # Match the log line with the regular expression
            match = re.match(log_pattern, line.strip())
            if match:
                # Extract data from matched groups
                timestamps.append(match.group('Timestamp'))
                log_levels.append(match.group('LogLevel'))
                components.append(match.group('Component'))
                messages.append(match.group('Message'))

    # Create a DataFrame from the parsed data
    log_df = pd.DataFrame({
        'Timestamp': timestamps,
        'LogLevel': log_levels,
        'Component': components,
        'Message': messages
    })

    # Convert the Timestamp column to datetime format
    log_df['Timestamp'] = pd.to_datetime(log_df['Timestamp'], format='%d/%m/%y %H:%M:%S')

    # Clean data (if necessary)
    log_df['LogLevel'] = log_df['LogLevel'].str.upper()  # Convert log levels to uppercase (if required)
    log_df['Component'] = log_df['Component'].str.strip()  # Remove any leading/trailing spaces

    # Map severity based on log level
    severity_mapping = {
        'INFO': 'Low',
        'WARN': 'Medium',
        'ERROR': 'High',
        'DEBUG': 'Low'
    }
    log_df['Severity'] = log_df['LogLevel'].map(severity_mapping)

    # Sort data by Timestamp
    log_df.sort_values(by='Timestamp', inplace=True)

    # Extract additional columns (date, time, hour)
    log_df['Date'] = log_df['Timestamp'].dt.date  # Extract just the date
    log_df['Time'] = log_df['Timestamp'].dt.time  # Extract just the time
    log_df['Hour'] = log_df['Timestamp'].dt.hour  # Extract the hour of the log entry

    # Save the parsed data to a CSV file
    log_df.to_csv(csv_file_path, index=False)

    # Return the DataFrame (optional, if needed for further processing)
    return log_df

# Usage example
log_file_path = r"C:\Users\LENOVO\Downloads\spark-driver.log"
log_df = parse_logs_from_file(log_file_path)
print(f"Log data has been successfully parsed and saved to CSV.")
