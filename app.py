from flask import Flask, render_template, jsonify
import speedtest
import threading

app = Flask(__name__)
download_speed = 0
upload_speed = 0
ping = 0

def run_speedtest():
    global download_speed
    global upload_speed
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 10**6  # Convert to Mbps
    upload_speed = st.upload() / 10**6  # Convert to Mbps
    ping = st.results.ping

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result')
def result():
    return render_template('result.html', download_speed=download_speed, upload_speed=upload_speed)


@app.route('/speedtest')
def speedtest_endpoint():
    run_speedtest()
    speed_results = {
        'download_speed': round(download_speed, 2),
        'upload_speed': round(upload_speed, 2),
        'ping': round(ping)
    }
    return jsonify(speed_results)


if __name__ == '__main__':
    # Start a separate thread to run the speed test every 2 seconds
    threading.Timer(2.0, run_speedtest).start()

    # Start the Flask app
    app.run(debug=True)
