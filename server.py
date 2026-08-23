from flask import Flask, request, jsonify, render_template
from rag.generation import answer_query

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return "Flask is running. Use POST/chat to send questions."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("question")
	
    if not question:
        return jsonify({"error": "Missing 'question' field in JSON body"}), 400
	
    result = answer_query(question)
    return jsonify(result)

@app.route("/ui", methods=["GET"])
def ui():
    return render_template("ui.html")


if __name__ == "__main__":
    print(">>> RUNNING FILE:", __file__)
    app.run(debug=True)
