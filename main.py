{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os, random, time\
import openai\
from twilio.rest import Client\
from datetime import datetime\
\
# Load config\
openai.api_key = os.getenv("OPENAI_API_KEY")\
twilio_sid = os.getenv("TWILIO_SID")\
twilio_auth = os.getenv("TWILIO_AUTH_TOKEN")\
twilio_phone = os.getenv("TWILIO_PHONE")\
girlfriend_phone = os.getenv("GIRLFRIEND_PHONE")\
\
client = Client(twilio_sid, twilio_auth)\
\
MEMORIES = [\
    "that rainy day we shared one umbrella",\
    "how she loves sunflowers",\
    "our trip to Paris",\
    "her laugh that makes me melt",\
    "the time we danced in the kitchen",\
    "her favorite vanilla latte on Sunday mornings"\
]\
\
def generate_message():\
    memory = random.choice(MEMORIES)\
    prompt = f"""\
    Write a short, loving, casual text for my girlfriend Emma.\
    Make it sweet, warm, reference \{memory\} naturally.\
    Keep it under 200 characters.\
    """\
    resp = openai.chat.completions.create(\
        model="gpt-4o-mini",\
        messages=[\{"role": "user", "content": prompt\}]\
    )\
    return resp.choices[0].message.content.strip()\
\
def send_message(msg):\
    msg = client.messages.create(\
        body=msg,\
        from_=twilio_phone,\
        to=girlfriend_phone\
    )\
    print(f"\uc0\u9989  Sent at \{datetime.now()\}: \{msg\}")\
\
def wait_random():\
    # Pick next send time: between 1\'963 days, between 7\uc0\u8239 AM\'9610\u8239 PM local time\
    days = random.randint(1, 3)\
    total_seconds = days * 24 * 3600\
    target = time.time() + total_seconds\
    # If within disallowed hours, shift to 7\uc0\u8239 AM\
    local = time.localtime(target)\
    if local.tm_hour < 7 or local.tm_hour > 22:\
        tomorrow = time.mktime((\
            local.tm_year, local.tm_mon, local.tm_mday + 1, 7, 0, 0,\
            local.tm_wday, local.tm_yday, local.tm_isdst\
        ))\
        return tomorrow - time.time()\
    return total_seconds\
\
if __name__ == "__main__":\
    print("\uc0\u55357 \u56460  Girlfriend AI Messenger started")\
    while True:\
        msg = generate_message()\
        send_message(msg)\
        wait = wait_random()\
        hrs = wait / 3600\
        print(f"\uc0\u9203  Sleeping ~\{hrs:.1f\} hours")\
        time.sleep(wait)}