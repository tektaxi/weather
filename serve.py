from flask import Flask
from flask.helpers import send_from_directory, url_for
import parser as p
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/script.js')
def home_script():
    return send_from_directory('static', 'script.js')

@app.route('/style.css')
def home_style():
    return send_from_directory('static', 'style.css')

@app.route('/api/weather-<location>')
def backend(location):
    #return json file
    weatherjson = p.get_weather(location)
    return weatherjson

# prevent cached responses
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
        

if __name__ == '__main__':
    app.run(port=5000, debug=True)
