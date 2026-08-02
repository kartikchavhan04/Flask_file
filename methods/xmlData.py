from flask import Flask , request,jsonify
import xmltodict

app = Flask(__name__)

@app.route("/emp", methods=["POST"])
def employee():

    data = request.get_data()
    xml_data = xmltodict.parse(data)

    undata = xmltodict.unparse(xml_data)



    return jsonify(undata)

if __name__ == "__main__":
    app.run(debug=True)