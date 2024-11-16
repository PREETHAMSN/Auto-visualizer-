from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import tailer
import pandas as pd
import plotly.express as px
import os
import csv
# Print current working directory for debugging
print("Current working directory:", os.getcwd())

# Define the path to your custom templates folder (cybersecurity folder)
template_folder_path = os.path.join(os.getcwd(), 'cybersecurity')

# Initialize Flask app with the custom template folder path
app = Flask(__name__, template_folder=template_folder_path)
socketio = SocketIO(app, cors_allowed_origins="*")

# Path to your log file
log_file_path = r"C:\Users\LENOVO\Downloads\processed_log_data.csv"


# Function to read data from CSV file
def read_csv_data(file_path):
    logs = {'INFO': [], 'WARN': [], 'ERROR': []}
    with open(file_path, newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            log_level = row.get('LogLevel')
            if log_level == 'INFO':
                logs['INFO'].append(row)
            elif log_level == 'WARN':
                logs['WARN'].append(row)
            elif log_level == 'ERROR':
                logs['ERROR'].append(row)
    return logs

# Stream logs to the front-end
def stream_logs():
    try:
        with open(log_file_path) as f:
            for line in tailer.follow(f):
                socketio.emit('new_log', {'log': line})  # Emit log line to the front-end
                time.sleep(0.1)  # Simulate real-time streaming
    except Exception as e:
        print(f"Error streaming logs: {e}")

# Serve the real-time viewer front-end
@app.route('/logs')
def logs_viewer():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real-Time Logs</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
    </head>
    <body>
        <h1>Real-Time Logs</h1>
        <div id="logs"></div>
        <script>
            const socket = io();
            socket.on('new_log', function(data) {
                const logDiv = document.getElementById('logs');
                const newLog = document.createElement('p');
                newLog.textContent = data.log;
                logDiv.appendChild(newLog);
            });
        </script>
    </body>
    </html>
    """
    return html_template

# Serve your dashboard
@app.route('/')
def index():
    # Load log data
   # df = pd.read_csv(log_file_path)
    #if 'Timestamp' not in df.columns or 'LogLevel' not in df.columns or 'Component' not in df.columns:
     #   return "CSV file missing required columns"
    
        # Replace with the path to your CSV file
    csv_file_path =r"C:\Users\LENOVO\Downloads\processed_log_data.csv"
    log_data = read_csv_data(csv_file_path)  # Read data from CSV file
    # Count of INFO logs
    info_count = len(log_data['INFO'])

    # Logs for WARN and ERROR
    warn_error_logs = log_data['WARN'] + log_data['ERROR']

    #df['Hour'] = pd.to_datetime(df['Timestamp']).dt.hour
    # Create a Plotly bar chart
   # fig = px.bar(df, x='Hour', y='LogLevel', color='Severity', title="Logs by Hour and Severity")
   # graph_json = fig.to_json()

    return render_template('index.html', info_count=info_count, warn_error_logs=warn_error_logs)# Start log streaming in the background

# Visualization 1 route
@app.route('/General_visualizations')
def General_visualizations():
    return render_template('General_visualizations.html')

# Visualization 2 route
@app.route('/ddos_visualizations')
def ddos_visualizations():
    return render_template('ddos_visualizations.html')


@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(stream_logs)

# Entry point
if __name__ == '__main__':
    socketio.run(app, debug=True)
