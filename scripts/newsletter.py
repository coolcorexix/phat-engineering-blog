#!/usr/bin/env python3
"""Send a blog post as a newsletter email through a personal Gmail account.

Each recipient gets their own message (nobody sees anyone else's address).
The Gmail App Password is read from the macOS Keychain, never from the repo:

    security add-generic-password -s blog-newsletter -a coolcore.xix@gmail.com -w

Usage:
    # preview the email in a browser, send nothing
    scripts/newsletter.py _posts/2026-10-12-foo.md --preview

    # test send to yourself
    scripts/newsletter.py _posts/2026-10-12-foo.md --to coolcore.xix@gmail.com

    # send to everyone in the subscribers CSV (Google Form responses export)
    scripts/newsletter.py _posts/2026-10-12-foo.md --subscribers subscribers.csv

Addresses already sent a given post are logged in ~/.config/blog-newsletter/sent/
and skipped on re-runs, so a half-finished send can simply be run again.
"""

import argparse
import csv
import html
import re
import smtplib
import ssl
import subprocess
import sys
import time
import webbrowser
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from pathlib import Path

import certifi
import markdown
import yaml

SITE_URL = "https://blogs.nemothecollector.dev"
SITE_TITLE = "Phat Or Nemo"
GMAIL_USER = "coolcore.xix@gmail.com"
FROM_NAME = "Phạm Huy Phát"
KEYCHAIN_SERVICE = "blog-newsletter"
STATE_DIR = Path.home() / ".config" / "blog-newsletter"
LOCAL_TZ = timezone(timedelta(hours=7))
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def load_post(path):
    text = Path(path).read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        sys.exit(f"{path}: missing front matter")
    meta = yaml.safe_load(match.group(1))
    return meta, match.group(2).strip()


def post_date(meta):
    # GitHub Pages builds in UTC, so a +0700 midnight post lands on the previous day.
    date = meta["date"]
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z")
    elif not isinstance(date, datetime):
        date = datetime(date.year, date.month, date.day)
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)
    return date.astimezone(timezone.utc)


def post_url(path, meta):
    # Mirrors Jekyll's default permalink (/:categories/:year/:month/:day/:title.html).
    date = post_date(meta)
    categories = meta.get("categories") or []
    if isinstance(categories, str):
        categories = categories.split()
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", Path(path).stem)
    parts = [c.lower() for c in categories] + [date.strftime("%Y/%m/%d"), f"{slug}.html"]
    return f"{SITE_URL}/" + "/".join(parts)


def recent_posts(current, limit=3):
    """The newest other posts, like the blog's "Read more from me" list."""
    posts = []
    for path in Path(current).parent.glob("*.m*d*"):
        if path.resolve() == Path(current).resolve():
            continue
        meta, _ = load_post(path)
        if meta.get("published") is False:
            continue
        posts.append((post_date(meta), meta["title"], post_url(path, meta)))
    return sorted(posts, reverse=True)[:limit]


def absolutize(fragment):
    return re.sub(r'(src|href)="/(?!/)', rf'\1="{SITE_URL}/', fragment)


def build_message(meta, body, url, more):
    title = meta["title"]
    cover = meta.get("image")
    if cover:
        # The post repeats its cover at the bottom; in the email it sits on top instead.
        body = re.sub(rf"\n*!\[[^\]]*\]\({re.escape(cover)}\)\s*$", "", body)

    content = absolutize(markdown.markdown(body, extensions=["extra", "sane_lists"]))
    # Markdown output is unstyled; email clients need inline styles.
    content = (content
        .replace("<h2>", '<h2 style="font-size:20px;line-height:1.35;margin:32px 0 12px;font-weight:600">')
        .replace("<p>", '<p style="margin:0 0 16px">')
        .replace("<img ", '<img style="max-width:100%;height:auto" '))
    cover_html = (
        f'<img src="{SITE_URL}{cover}" alt="" width="600" '
        f'style="display:block;width:100%;max-width:600px;height:auto;border-radius:6px;margin:0 0 28px">'
        if cover else ""
    )
    more_html = "".join(
        f'<p style="margin:0 0 14px"><a href="{u}" style="color:#222;font-weight:600;text-decoration:none">{html.escape(t)}</a>'
        f'<br><span style="font-size:13px;color:#999">{d.astimezone(LOCAL_TZ):%b %-d, %Y}</span></p>'
        for d, t, u in more
    )
    if more_html:
        more_html = (
            '<p style="margin:40px 0 14px;font-size:13px;font-weight:600;letter-spacing:0.06em;'
            f'text-transform:uppercase;color:#888">Read more from me</p>{more_html}'
        )
    unsubscribe = f"mailto:{GMAIL_USER}?subject=huy%20dang%20ky"

    html_body = f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#fdfdfd">
<div style="max-width:600px;margin:0 auto;padding:32px 20px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;font-size:17px;line-height:1.65;color:#222">
  {cover_html}
  <h1 style="font-size:26px;line-height:1.3;margin:0 0 24px;font-weight:600">
    <a href="{url}" style="color:#222;text-decoration:none">{html.escape(title)}</a>
  </h1>
  <div class="content">{content}</div>
  <p style="margin:36px 0 0"><a href="{url}" style="color:#2f9e44">Đọc trên blog →</a></p>
  {more_html}
  <hr style="border:none;border-top:1px solid #e8e8e8;margin:32px 0 16px">
  <p style="font-size:13px;line-height:1.5;color:#888;margin:0">
    Bạn nhận thư này vì đã đăng ký nhận bài từ <a href="{SITE_URL}" style="color:#888">{SITE_TITLE}</a>.
    Cứ reply thư này nếu muốn nói gì đó. Không muốn nhận nữa thì reply chữ “huỷ” là được.
  </p>
</div>
</body></html>
"""
    more_text = "".join(f"- {t}: {u}\n" for _, t, u in more)
    more_text = f"\nRead more from me:\n{more_text}" if more else ""
    text_body = f"{title}\n\n{body}\n\n---\nĐọc trên blog: {url}\n{more_text}\nKhông muốn nhận nữa thì reply chữ “huỷ”.\n"

    msg = EmailMessage()
    msg["Subject"] = title
    msg["From"] = formataddr((FROM_NAME, GMAIL_USER))
    msg["List-Unsubscribe"] = f"<{unsubscribe}>"
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")
    return msg, html_body


def read_subscribers(path):
    emails = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            for cell in row:
                for found in EMAIL_RE.findall(cell):
                    if found.lower() not in (e.lower() for e in emails):
                        emails.append(found)
    return emails


def app_password():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-a", GMAIL_USER, "-w"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit(
            "Gmail App Password not found in Keychain. Add it with:\n"
            f"  security add-generic-password -s {KEYCHAIN_SERVICE} -a {GMAIL_USER} -w"
        )
    return result.stdout.strip().replace(" ", "")


def check_live(url):
    # curl uses the macOS trust store; python.org builds of Python ship without CA certs.
    result = subprocess.run(["curl", "-sfI", "-o", "/dev/null", url], capture_output=True)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("post", help="path to the post in _posts/")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--preview", action="store_true", help="open the rendered email in a browser")
    target.add_argument("--to", action="append", help="send to this address (repeatable)")
    target.add_argument("--subscribers", help="CSV with subscriber emails in any column")
    args = parser.parse_args()

    meta, body = load_post(args.post)
    url = post_url(args.post, meta)
    msg, html_body = build_message(meta, body, url, recent_posts(args.post))

    if args.preview:
        out = STATE_DIR / "preview.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html_body, encoding="utf-8")
        print(f"Preview: {out}\nPost URL: {url}")
        webbrowser.open(out.as_uri())
        return

    if not check_live(url):
        sys.exit(f"Post is not live yet (or the URL guess is wrong): {url}")

    recipients = args.to or read_subscribers(args.subscribers)
    sent_log = STATE_DIR / "sent" / f"{Path(args.post).stem}.txt"
    sent_log.parent.mkdir(parents=True, exist_ok=True)
    already = set(sent_log.read_text().split()) if sent_log.exists() and args.subscribers else set()
    pending = [r for r in recipients if r.lower() not in already]
    print(f"{meta['title']}\n{url}\n{len(pending)} to send, {len(recipients) - len(pending)} already sent")
    if not pending:
        return

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context(cafile=certifi.where())) as smtp:
        smtp.login(GMAIL_USER, app_password())
        for i, rcpt in enumerate(pending, 1):
            del msg["To"], msg["Message-ID"]
            msg["To"] = rcpt
            msg["Message-ID"] = make_msgid(domain="gmail.com")
            smtp.send_message(msg)
            if args.subscribers:
                with sent_log.open("a") as log:
                    log.write(rcpt.lower() + "\n")
            print(f"  [{i}/{len(pending)}] {rcpt}")
            time.sleep(1)


if __name__ == "__main__":
    main()
