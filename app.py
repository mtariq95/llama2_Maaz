from flask import Flask, render_template, request, redirect, url_for
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    # Replace this with actual logic to load user from a database
    users = {'1': User('1', 'john'), '2': User('2', 'minam')}
    return users.get(user_id)

# Load the tokenizer and model

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-13b-chat-hf")

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        input_text = data.get('input_text')
        if input_text is None:
            raise ValueError("Missing 'input_text' parameter")

        print(f"Received input_text: {input_text}")

        input_ids = tokenizer.encode(input_text, return_tensors="pt")
        output = model.generate(input_ids)
        decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

        return jsonify({'generated_output': decoded_output})
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'An error occurred while processing the request'}), 400

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        username = request.form['username']

        # Validate user credentials (replace with your authentication logic)
        # In a real-world scenario, you might check against a database
        if user_id and username:
            user = User(user_id, username)
            login_user(user)
            return render_template('index.html')
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8000)

