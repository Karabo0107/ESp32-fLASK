from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from threading import Lock

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

data_lock = Lock()
esp_data = {"analog_input": 0, "button": False, "fan_pot": 0}
control_data = {
    "led_enabled": False,
    "brightness": 0,
    "fan_enabled": False,
    "fan_speed": 0
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>IoT Control Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        .dashboard {
            display: flex;
            flex-direction: column;
            gap: 30px;
            max-width: 800px;
            margin: 0 auto;
        }
        .panel {
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 25px;
            border: 1px solid #e0e0e0;
        }
        .panel-header {
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
            color: #444;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .status-item:last-child {
            border-bottom: none;
        }
        .status-label {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 500;
            color: #555;
        }
        .status-value {
            font-weight: 400;
            color: #333;
        }
        .online {
            color: #4CAF50;
        }
        .offline {
            color: #F44336;
        }
        .icon {
            font-size: 1.2em;
            width: 24px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1><i class="fas fa-microchip"></i> IoT Control Dashboard</h1>
    </div>
    
    <div class="dashboard">
        <div class="panel">
            <div class="panel-header">
                <i class="fas fa-robot"></i>
                <h2>ESP32 Sensor Data</h2>
            </div>
            <div class="status-item">
                <span class="status-label">
                    <i class="fas fa-lightbulb icon"></i>
                    <span>Light Level</span>
                </span>
                <span class="status-value">{{ esp_data.analog_input }} lx</span>
            </div>
            <div class="status-item">
                <span class="status-label">
                    <i class="fas fa-running icon"></i>
                    <span>Motion Detection</span>
                </span>
                <span class="status-value {{ 'online' if esp_data.button else 'offline' }}">
                    {{ 'Detected' if esp_data.button else 'None' }}
                </span>
            </div>
            <div class="status-item">
                <span class="status-label">
                    <i class="fas fa-sliders-h icon"></i>
                    <span>Fan Potentiometer</span>
                </span>
                <span class="status-value">{{ esp_data.fan_pot }}%</span>
            </div>
            <div class="status-item">
                <span class="status-label">
                    <i class="fas fa-ruler-vertical icon"></i>
                    
                </span>
                <span class="status-value">{{ esp_data.analog_input }} cm</span>
            </div>
        </div>
        
        <div class="panel">
            <div class="panel-header">
                <i class="fas fa-tablet-alt"></i>
                <h2>Control Status</h2>
            </div>
            <div class="status-item">
                <span class="status-label">
                    <i class="fas fa-lightbulb icon"></i>
                    <span>Light Status</span>
                </span>
                <span class="status-value {{ 'online' if controls.led_enabled else 'offline' }}">
                    {{ 'ON' if controls.led_enabled else 'OFF' }}
                </span>
            </div>
            <div class="status-item">
                <span class="status-label">
                    <i class="fas fa-sun icon"></i>
                    <span>Light Brightness</span>
                </span>
                <span class="status-value">{{ controls.brightness }}%</span>
            </div>
            <div class="status-item">
                <span class="status-label">
                    <i class="fas fa-fan icon"></i>
                    <span>Fan Status</span>
                </span>
                <span class="status-value {{ 'online' if controls.fan_enabled else 'offline' }}">
                    {{ 'ON' if controls.fan_enabled else 'OFF' }}
                </span>
            </div>
            <div class="status-item">
                <span class="status-label">
                    <i class="fas fa-tachometer-alt icon"></i>
                    <span>Fan Speed</span>
                </span>
                <span class="status-value">{{ controls.fan_speed }}%</span>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE, 
                               esp_data=esp_data,
                               controls=control_data)

@app.route('/esp/update', methods=['POST'])
def update_esp():
    with data_lock:
        esp_data.update(request.json)
    return jsonify({"message": "Updated"}), 200

@app.route('/esp/control')
def get_control():
    with data_lock:
        return jsonify(control_data), 200

@app.route('/flet/update', methods=['POST'])
def update_flet():
    with data_lock:
        control_data.update(request.json)
    return jsonify({"message": "Updated"}), 200

@app.route('/api/status')
def get_status():
    with data_lock:
        return jsonify({
            "sensors": esp_data,
            "controls": control_data
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)