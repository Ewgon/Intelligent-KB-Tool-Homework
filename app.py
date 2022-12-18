from flask import Flask, render_template, request, jsonify
import db_processing
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#API : Update the database
@app.route("/send", methods=["POST"])
def insertName():
    details = request.get_json(force=True)
    result = db_processing.updateDatabase(details["name-choice"], details["names-selection"])
    return jsonify(result)

#API : Get a list of possible names
@app.route("/get")
def getNamesFromChars():
    chars = request.args.get("get")
    result = db_processing.getNamesFromCharsIntoDb(chars)
    return jsonify(result)

#API : Get the entire database to be displayed
@app.route('/display')
def list():
    result = db_processing.getFullTable()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug = True)