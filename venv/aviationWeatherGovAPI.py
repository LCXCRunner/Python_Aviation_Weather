from flask import Flask, render_template_string, send_from_directory
import os

# Set the parent directory as the root folder for templates and static files
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, 
            static_folder=parent_dir,
            template_folder=parent_dir)

@app.route('/')
def index():
    # Read the HTML file from parent directory
    html_path = os.path.join(parent_dir, 'index.html')
    with open(html_path, 'r') as f:
        html_content = f.read()
    
    # Replace "Airport 1" with "KSLC" in the first h2 tag
    html_content = html_content.replace('<h2>Airport 1</h2>', '<h2>KSLC</h2>', 1)
    
    return render_template_string(html_content)

@app.route('/styles.css')
def stylesheet():
    # Serve the CSS file from parent directory
    return send_from_directory(parent_dir, 'styles.css')

@app.route('/Typescript/testfile.js')
def javascript():
    # Serve the JavaScript file from Typescript directory
    typescript_dir = os.path.join(parent_dir, 'Typescript')
    return send_from_directory(typescript_dir, 'testfile.js')

@app.route('/button-click')
def button_click():
    # This runs on the server when the button is clicked
    print('hello world')
    return 'OK'

if __name__ == '__main__':
    print("Starting simple Flask app...")
    print(f"Serving files from: {parent_dir}")
    print("Visit http://localhost:5000 to view the page")
    app.run(debug=True, host='0.0.0.0', port=5000)
