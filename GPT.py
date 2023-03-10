import openai
import json
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request

# set up Twilio account credentials
account_sid = 'AC0eb057fb44d08943f92000230268f4ae'
auth_token = 'ca527dd2c4c6bd16be8c9e15ebe128cc'
twilio_phone_number = '+19295564501'
client = Client(account_sid, auth_token)

# set up OpenAI API credentials
openai.api_key = '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'

#This is the part of code that generates the response
def generate_response(message):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": str(message)}],
    )
    #json converson
    completion = str(response)

    data = json.loads(completion)

    content = data['choices'][0]['message']['content']
    return content

# Message takes the text and the resto of the code passes it to the copletion function
#completion function completes it that twillo sends it to the website'

def handle_sms(request):
    message = request.form['Body']
    response = generate_response(message)
    twilio_response = MessagingResponse()
    twilio_response.message(response)
    return str(twilio_response)

# set up Flask app
app = Flask(__name__)

#the wbbhook has the contents of the response
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    return handle_sms(request)

# start Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
