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


def pick_variant(company: str, email: str) -> str:
    text = f"{company or ''} {email or ''}".lower()
    travel_keys = ['travel', 'skift', 'phocuswire', 'travelweekly', 'tourism']
    business_keys = ['forbes', 'bloomberg', 'financial', 'afr', 'fortune', 'business']
    if any(k in text for k in travel_keys):
        return 'travel'
    if any(k in text for k in business_keys):
        return 'business'
    return 'tech'


def build_body(greet, signature_html, variant='tech'):
    if variant == 'travel':
        body = '''
<p>Mennan Yelkenci here, Founder of <a href="https://www.booked.ai" target="_blank" rel="noopener noreferrer">Booked AI</a>.</p>

<p>Thought this may be relevant to your travel coverage. We launched with a chat-first AI booking experience and saw strong conversation volume, but weak completion at checkout.</p>

<p>So we changed the booking experience - users now type what they want once in a Google-style search bar, then complete through a familiar online booking interface.</p>

<p><strong>That single shift reduced token burn and exponentially increased conversions.</strong></p>

<p>The industry is currently treating “more chat” as the default answer to everything. What we’re seeing is simpler - travellers still want speed and certainty when money is on the line.</p>

<p>If fit for coverage, happy to share a concise before-and-after breakdown and jump on a quick 15-minute call.</p>
'''
    elif variant == 'business':
        body = '''
<p>Mennan Yelkenci here, Founder of <a href="https://www.booked.ai" target="_blank" rel="noopener noreferrer">Booked AI</a>.</p>

<p>Sharing this from a consumer behavior and commercial performance angle.</p>

<p>We launched with a chat-first booking model and found a familiar issue in AI products: high engagement, low transaction completion. We then shifted to intent capture up front (Google-style search) and a traditional booking interface for payment and completion.</p>

<p><strong>That single shift reduced token burn and exponentially increased conversions.</strong></p>

<p>There’s a lot of capital being deployed on the assumption that “more chat = better product.” In our case, reducing conversational friction materially improved outcomes.</p>

<p>If fit for coverage, happy to share a concise before-and-after breakdown and speak briefly this week.</p>
'''
    else:
        body = '''
<p>Mennan Yelkenci here, Founder of <a href="https://www.booked.ai" target="_blank" rel="noopener noreferrer">Booked AI</a>.</p>

<p>We’re seeing a product trend that may be useful for your AI coverage: engagement and conversion are not the same metric.</p>

<p>Booked launched chat-first. Users interacted heavily, but booking completion lagged. We shifted to one-shot intent capture via a Google-style search input, with AI still behind the scenes, followed by a structured booking flow.</p>

<p><strong>That single shift reduced token burn and exponentially increased conversions.</strong></p>

<p>Right now, much of the market seems to assume the interface should always become “more conversational.” Our data suggests the opposite in high-intent purchase flows.</p>

<p>If fit for coverage, happy to share the before-and-after product changes and key metrics.</p>
'''

    return f'''<p>{greet}</p>

{body}
<p>Kind regards,</p>
<p>Mennan</p>

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
        variant = pick_variant(c.get('company', ''), to_email)
        body_html = build_body(greet, signature_html, variant=variant)
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
