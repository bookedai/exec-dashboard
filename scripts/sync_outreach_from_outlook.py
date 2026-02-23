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


def fetch_recent_inbox(token, user, top=200):
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        '$select': 'subject,receivedDateTime,from,isRead',
        '$orderby': 'receivedDateTime desc',
        '$top': str(top),
    }
    url = f'https://graph.microsoft.com/v1.0/users/{user}/mailFolders/inbox/messages'
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json().get('value', [])


def extract_recipient_emails(msg):
    emails = []
    for field in ('toRecipients', 'ccRecipients'):
        for rec in msg.get(field, []) or []:
            addr = ((rec.get('emailAddress') or {}).get('address') or '').strip().lower()
            if addr:
                emails.append(addr)
    return sorted(set(emails))


def extract_sender_email(msg):
    return (((msg.get('from') or {}).get('emailAddress') or {}).get('address') or '').strip().lower()


def append_note(contact, note):
    notes = (contact.get('notes') or '').strip()
    if note in notes:
        return
    contact['notes'] = (notes + (' | ' if notes else '') + note)[:700]


def sync_sent(data, sent_items):
    contacts = data.get('contacts', [])
    by_email = { (c.get('email') or '').strip().lower(): c for c in contacts }
    changed = 0

    for msg in sent_items:
        sent_at = msg.get('sentDateTime')
        subject = (msg.get('subject') or '').strip()
        recipients = extract_recipient_emails(msg)
        for email in recipients:
            c = by_email.get(email)
            if not c:
                continue
            prior = json.dumps(c, sort_keys=True)
            if c.get('status') in (None, '', 'Not sent', 'Drafted'):
                c['status'] = 'Sent'
            c['lastTouch'] = sent_at or c.get('lastTouch') or ''
            append_note(c, f"Sent: {subject}" if subject else 'Sent')
            after = json.dumps(c, sort_keys=True)
            if prior != after:
                changed += 1

    return changed


def sync_replies(data, inbox_items):
    contacts = data.get('contacts', [])
    by_email = { (c.get('email') or '').strip().lower(): c for c in contacts }
    changed = 0

    for msg in inbox_items:
        sender = extract_sender_email(msg)
        if not sender:
            continue
        c = by_email.get(sender)
        if not c:
            continue
        prior = json.dumps(c, sort_keys=True)
        c['replied'] = True
        if c.get('status') not in ('Coverage won',):
            c['status'] = 'Replied'
        c['lastTouch'] = msg.get('receivedDateTime') or c.get('lastTouch') or ''
        subj = (msg.get('subject') or '').strip()
        append_note(c, f"Reply: {subj}" if subj else 'Reply received')
        after = json.dumps(c, sort_keys=True)
        if prior != after:
            changed += 1

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
    inbox_items = fetch_recent_inbox(token, env['user'])

    data = json.loads(OUTREACH_DATA.read_text())
    changed_sent = sync_sent(data, sent_items)
    changed_replies = sync_replies(data, inbox_items)
    changed = changed_sent + changed_replies

    data['updatedAt'] = dt.datetime.now().isoformat()
    if changed > 0:
        OUTREACH_DATA.write_text(json.dumps(data, indent=2))

    print(f'updated_contacts={changed} sent_updates={changed_sent} reply_updates={changed_replies}')


if __name__ == '__main__':
    main()
