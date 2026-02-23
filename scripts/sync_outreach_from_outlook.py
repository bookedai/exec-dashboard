#!/usr/bin/env python3
import json
import datetime as dt
from pathlib import Path
import requests

OPENCLAW_CFG = Path('/Users/mennanyelkenci/.openclaw/openclaw.json')
OUTREACH_DATA = Path('/Users/mennanyelkenci/.openclaw/workspace/booked-dashboard/outreach-data.json')


def load_env():
    cfg = json.loads(OPENCLAW_CFG.read_text())
    env = cfg.get('env', {})
    return {
        'tenant': env.get('MS_TENANT_ID'),
        'client': env.get('MS_CLIENT_ID'),
        'secret': env.get('MS_CLIENT_SECRET'),
        'user': env.get('OUTLOOK_USER', 'mennan@booked.ai'),
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


def fetch_recent_sent(token, user, top=200):
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        '$select': 'subject,sentDateTime,toRecipients,ccRecipients',
        '$orderby': 'sentDateTime desc',
        '$top': str(top),
    }
    url = f'https://graph.microsoft.com/v1.0/users/{user}/mailFolders/SentItems/messages'
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json().get('value', [])


def extract_emails(msg):
    emails = []
    for field in ('toRecipients', 'ccRecipients'):
        for rec in msg.get(field, []) or []:
            addr = ((rec.get('emailAddress') or {}).get('address') or '').strip().lower()
            if addr:
                emails.append(addr)
    return sorted(set(emails))


def sync_outreach(data, sent_items):
    contacts = data.get('contacts', [])
    by_email = { (c.get('email') or '').strip().lower(): c for c in contacts }
    changed = 0

    for msg in sent_items:
        sent_at = msg.get('sentDateTime')
        subject = (msg.get('subject') or '').strip()
        recipients = extract_emails(msg)
        if not recipients:
            continue

        for email in recipients:
            c = by_email.get(email)
            if not c:
                continue

            prior = json.dumps(c, sort_keys=True)
            # mark sent lifecycle fields
            if c.get('status') in (None, '', 'Not sent', 'Drafted'):
                c['status'] = 'Sent'
            c['lastTouch'] = sent_at or c.get('lastTouch') or ''
            notes = (c.get('notes') or '').strip()
            tag = f"Sent: {subject}" if subject else 'Sent'
            if tag not in notes:
                c['notes'] = (notes + (' | ' if notes else '') + tag)[:500]

            after = json.dumps(c, sort_keys=True)
            if prior != after:
                changed += 1

    data['updatedAt'] = dt.datetime.now().isoformat()
    return changed


def main():
    if not OUTREACH_DATA.exists():
        raise SystemExit('outreach-data.json not found')

    env = load_env()
    missing = [k for k, v in env.items() if not v]
    if missing:
        raise SystemExit(f'Missing config in openclaw.json env: {missing}')

    token = get_token(env['tenant'], env['client'], env['secret'])
    sent_items = fetch_recent_sent(token, env['user'])

    data = json.loads(OUTREACH_DATA.read_text())
    changed = sync_outreach(data, sent_items)

    if changed > 0:
        OUTREACH_DATA.write_text(json.dumps(data, indent=2))
    print(f'updated_contacts={changed}')


if __name__ == '__main__':
    main()
