#!/usr/bin/env python3
import json
import random
import re
import time
from pathlib import Path
import requests

OPENCLAW_CFG = Path('/Users/mennanyelkenci/.openclaw/openclaw.json')
OUTREACH_DATA = Path('/Users/mennanyelkenci/.openclaw/workspace/booked-dashboard/outreach-data.json')
SIG_PATH = Path('/Users/mennanyelkenci/.openclaw/workspace/templates/mennan-signature.html')

SUBJECT = 'Coverage opportunity - a contrarian AI conversion story - Booked AI'


def load_env():
    cfg = json.loads(OPENCLAW_CFG.read_text())
    env = cfg.get('env', {})
    return {
        'tenant': env.get('MS_TENANT_ID'),
        'client': env.get('MS_CLIENT_ID'),
        'secret': env.get('MS_CLIENT_SECRET'),
        'sender': env.get('OUTLOOK_USER', 'mennan@booked.ai'),
    }


def get_token(tenant, client, secret):
    url = f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'
    data = {
        'client_id': client,
        'client_secret': secret,
        'grant_type': 'client_credentials',
        'scope': 'https://graph.microsoft.com/.default',
    }
    r = requests.post(url, data=data, timeout=20)
    r.raise_for_status()
    return r.json()['access_token']


def greeting(name, email):
    em = (email or '').lower()
    if any(x in em for x in ['tips@', 'editor@', 'newsroom@', 'press@', 'hello@']):
        return 'Hi Team,'
    n = (name or '').strip()
    if not n or n.lower() == 'unknown':
        return 'Hi Team,'
    first = re.split(r'\s+', n)[0].strip(',')
    return f'Hi {first},'


def build_body(greet, signature_html):
    return f'''<p>{greet}</p>

<p>Mennan Yelkenci here, Founder of Booked AI. Thought this might be relevant to your AI and product coverage.</p>

<p>When Booked first launched with a chat-first travel experience, we noticed that people were super happy to chat, but more than 95% of them dropped off before completing a booking.</p>

<p>We've identified two reasons for this. First, many consumers still do not fully trust AI agents to finalise payments. Second, a long back-and-forth conversation is often a worse buying experience than a fast, familiar online booking path.</p>

<p>So we've made a deliberate commercial bet from a conversion perspective by building a Google-style search bar where we let AI capture intent up front, then move users into a traditional online booking interface to complete the purchase.</p>

<ul>
  <li>That single shift reduced token burn and exponentially increased conversions.</li>
</ul>

<p>We think the lack of requirement for an LLM chat interface is useful for coverage and challenges the product trends coming to market today.</p>

<p>Open to sharing a concise before-and-after breakdown and the exact product changes we made. Happy to jump on a quick 15-minute call this week.</p>

<p>Kind regards,</p>

<br/><br/>{signature_html}'''


def pick_contacts(data, limit=2):
    contacts = data.get('contacts', [])
    candidates = [
        c for c in contacts
        if (c.get('email') and c.get('status') in (None, '', 'Not sent', 'Drafted'))
    ]
    return candidates[:limit]


def send_email(token, sender, to_email, cc_email, subject, body_html):
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {
        'message': {
            'subject': subject,
            'body': {'contentType': 'HTML', 'content': body_html},
            'toRecipients': [{'emailAddress': {'address': to_email}}],
            'ccRecipients': [{'emailAddress': {'address': cc_email}}],
        },
        'saveToSentItems': True,
    }
    r = requests.post(f'https://graph.microsoft.com/v1.0/users/{sender}/sendMail', headers=headers, json=payload, timeout=30)
    return r.status_code, r.text[:300]


def main():
    if not OUTREACH_DATA.exists():
        raise SystemExit('outreach-data.json not found')

    env = load_env()
    missing = [k for k, v in env.items() if not v]
    if missing:
        raise SystemExit(f'Missing config in openclaw.json env: {missing}')

    signature_html = SIG_PATH.read_text() if SIG_PATH.exists() else '<p>Mennan Yelkenci</p>'
    token = get_token(env['tenant'], env['client'], env['secret'])

    data = json.loads(OUTREACH_DATA.read_text())
    chosen = pick_contacts(data, limit=2)
    if not chosen:
        print('sent_count=0 reason=no_pending_contacts')
        return

    sent_count = 0
    for i, c in enumerate(chosen):
        to_email = c['email'].strip().lower()
        greet = greeting(c.get('name', ''), to_email)
        body_html = build_body(greet, signature_html)
        status, _ = send_email(token, env['sender'], to_email, 'info@booked.ai', SUBJECT, body_html)
        if status in (200, 202):
            c['status'] = 'Sent'
            c['lastTouch'] = time.strftime('%Y-%m-%dT%H:%M:%S')
            notes = (c.get('notes') or '').strip()
            stamp = f'Sent batch subject: {SUBJECT}'
            c['notes'] = (notes + (' | ' if notes else '') + stamp)[:700]
            sent_count += 1
        else:
            c['status'] = c.get('status') or 'Not sent'
            notes = (c.get('notes') or '').strip()
            c['notes'] = (notes + (' | ' if notes else '') + f'Send failed ({status})')[:700]

        # random spacing between first and second send (overarching rule keeps 2 per 11 mins)
        if i == 0 and len(chosen) > 1:
            time.sleep(random.randint(70, 260))

    data['updatedAt'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    OUTREACH_DATA.write_text(json.dumps(data, indent=2))
    print(f'sent_count={sent_count}')


if __name__ == '__main__':
    main()
