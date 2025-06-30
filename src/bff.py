from flask import Flask, request, jsonify

app = Flask(__name__)

# put main logic here
# inference = main object

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data["message"]
        response = inference(user_message)
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True) #  For development only.  Don't use debug=True in production.

