from flask import Flask, request, render_template, redirect, url_for
import google.generativeai as genai
from PIL import Image
import os
 
# Initialize the Flask app
app = Flask(__name__)
 
# Configure Google Generative AI
key = 'AIzaSyDOdPE4a0qOrWfozEzXZrFa19u-QNxrYSQ'
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-1.5-flash')
 
# Route to the homepage
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        image_file = request.files.get("image")
 
        if prompt and image_file:
            # Save the uploaded image
            image_path = os.path.join("static", image_file.filename)
            image_file.save(image_path)
 
            # Generate AI content based on prompt and image
            with Image.open(image_path) as img:
                response = model.generate_content([
                    prompt,
                    img
                ], stream=True)
                response.resolve()
 
            # Get the generated content
            generated_text = response.text
 
            return render_template("result.html", content=generated_text, image_path=image_path)
 
    return render_template("index.html")
 
# Route for the result page
@app.route("/result")
def result():
    return render_template("result.html")
 
# Main function
if __name__ == "__main__":
    app.run(debug=True)