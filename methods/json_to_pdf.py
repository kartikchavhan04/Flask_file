from flask import Flask, request, jsonify, send_file
from reportlab.pdfgen import canvas
import xmltodict


app = Flask(__name__)

@app.route('/json-to-pdf', methods=['POST'])
def json_to_pdf():
    xml_data = request.get_data()
    data = xmltodict.parse(xml_data)

    student= data["student"] 

    file_name = "student_data.pdf"
    c = canvas.Canvas(file_name)

    c.drawString(100, 750, f"Name: {student['name']}")
    c.drawString(100, 730, f"Age: {student['age']}")   
    c.drawString(100, 710, f"Grade: {student['grade']}")
    c.drawString(100, 690, f"Email: {student['email']}")
    c.drawString(100, 670, f"Address: {student['address']}")

    c.save()
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':  
    app.run(debug=True)