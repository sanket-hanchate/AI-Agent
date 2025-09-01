from flask import Flask, request, render_template, url_for, send_file
from planning_agent import run_planning_agent
import markdown 
import json 
import os 
from gtts import gTTS 
import time 
import pyttsx3
from reportlab.lib.pagesizes import letter 
from reportlab.pdfgen import canvas
import io 

app = Flask(__name__)

html_result = ""
# Keep index.html as your main landing page
@app.route("/", methods=["GET", "POST"])
def home():
    plan = None
    goal = None
    if request.method == "POST":
        goal = request.form["goal"]
        plan = run_planning_agent(goal)
    return render_template('index.html', goal=goal, plan=plan)

# Route for your actual main input form
@app.route('/main', methods=["GET"])
def main():
    return render_template('main.html')


@app.route('/loading', methods=["POST"])
def loading():
    prompt = request.form.get('prompt')
    return render_template('loading.html', prompt=prompt)


# Route that processes the form and shows the result page
@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form.get("prompt")

    if not prompt:
        return render_template("result.html", result="No prompt provided.")

    # Run your AI planning agent
    raw_result = run_planning_agent(prompt)
    html_result = markdown.markdown(raw_result)

    summary_text = " ".join(raw_result.split(".")[:2])
    if not summary_text.strip():
        summary_text = raw_result[:150]

    audio_path = "static/audio/summary.mp3"
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    engine.save_to_file(summary_text, audio_path)
    engine.runAndWait()

    #pass audio file path to template
    return render_template(
        "result.html",
        result = html_result,
        audio_file = audio_path
    )

@app.route("/download-pdf")
def download_pdf():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Generated Report")
    p.drawString(100, 730, "-----------------")
    text = html_result.replace("<br>", "\n")  # Convert HTML line breaks
    p.drawString(100, 710, text)
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="report.pdf", mimetype="application/pdf")
if __name__ == "__main__":
    app.run(debug=True) 