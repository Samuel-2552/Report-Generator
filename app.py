from flask import Flask, render_template, send_from_directory
import os
import xml.etree.ElementTree as ET
import base64

app = Flask(__name__)
static_folder = 'static/ctds'

@app.route('/')
def index():
    # List all .ctd files in the static folder
    ctd_files = [f for f in os.listdir(static_folder) if f.endswith('.ctd')]
    return render_template('index.html', files=ctd_files)

@app.route('/file/<filename>')
def display_file(filename):
    # Parse the selected .ctd file
    file_path = os.path.join(static_folder, filename)
    tree = ET.parse(file_path)
    root = tree.getroot()

    nodes = []
    
    # Extract nodes and their findings
    for node in root.findall('.//node'):
        # for rt in node.findall('rich_text'):
        #     print(rt.text)
        findings = {
            'name': node.attrib.get('name'),
            'rich_text': [rt.text for rt in node.findall('rich_text')],
            'images': []
        }
        
        # Handle encoded images
        encoded_png = node.find('encoded_png')
        if encoded_png is not None:
            findings['images'].append(encoded_png.text)

        nodes.append(findings)

    return render_template('file.html', nodes=nodes)

if __name__ == '__main__':
    app.run(debug=True)
