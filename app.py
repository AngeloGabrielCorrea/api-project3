from flask import Flask, jsonify, request, abort
import asyncio
import os
from scraper import salvar_destaques

app = Flask(__name__)
SCHEDULER_TOKEN = os.getenv("SCHEDULER_TOKEN", "minha_senha")

@app.route("/run-scheduler")
def run_scheduler():
    token = request.args.get("token")
    if token != SCHEDULER_TOKEN:
        abort(403)
    asyncio.run(salvar_destaques())
    return jsonify({"status": "ok"})

@app.route("/data/<filename>")
def serve_data(filename):
    return app.send_static_file(f"../data/{filename}")

@app.route("/")
def index():
    return "🟢 Scraper Flask com Playwright no ar!"

if __name__ == "__main__":
    app.run(debug=True)
