#!/usr/bin/env python3
"""Generates the static Latchkey support site into docs/. Run: python3 build.py"""
import html, json, os, re

BASE = "https://levan2002.github.io/latchkey/"
STORE = "https://apps.apple.com/app/id6819347011"
ISSUES = "https://github.com/Levan2002/latchkey/issues"
EULA = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"
DATE = "2026-10-05"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


def strip(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s))).strip()


def esc(s):
    return html.escape(s, quote=True)


def head(title, desc, path, r, og_type="website", jsonld=(), noindex=False):
    url = BASE + path
    ld = "\n".join('<script type="application/ld+json">\n%s\n</script>' % json.dumps(j, indent=1, ensure_ascii=False) for j in jsonld)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#0E3B2E">
<meta name="apple-itunes-app" content="app-id=6819347011">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" sizes="32x32" href="{r}favicon.png">
<link rel="apple-touch-icon" href="{r}apple-touch-icon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Latchkey">
<meta property="og:image" content="{BASE}img/icon-512.png">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{r}style.css">
{ld}
</head>
"""


NAV = [("help.html", "Help"), ("guides/", "Guides"), ("privacy.html", "Privacy"), ("terms.html", "Terms")]


def header(r, current=""):
    links = "".join(
        '<a href="%s%s"%s>%s</a>' % (r, href, ' aria-current="page"' if href == current else "", label)
        for href, label in NAV
    )
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="bar"><div class="wrap">
<a class="brand" href="{r}"><img src="{r}img/icon-96.png" width="36" height="36" alt="">Latchkey</a>
<nav aria-label="Main">{links}</nav>
</div></header>
"""


def footer(r):
    return f"""<footer><div class="wrap">
<nav aria-label="Footer"><a href="{r}help.html">Help &amp; FAQ</a><a href="{r}guides/">Guides</a><a href="{r}privacy.html">Privacy Policy</a><a href="{r}terms.html">Terms</a><a href="{ISSUES}">Report a problem</a><a href="{STORE}">App Store</a></nav>
<p>Latchkey: Authenticator App, by Levani Topchishvili (individual developer).</p>
<p>&copy; 2026 Levani Topchishvili. Apple, iPhone, iPad, Face ID and App Store are trademarks of Apple Inc.</p>
</div></footer>
</body>
</html>
"""


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def prose_page(path, title, desc, h1, body, current="", meta=None, jsonld=()):
    r = "../" * path.count("/")
    page = head(title, desc, path, r, jsonld=jsonld) + header(r, current)
    page += f'<main id="main"><div class="wrap page">\n<h1>{h1}</h1>\n'
    if meta:
        page += f'<p class="meta">{meta}</p>\n'
    page += body + "\n</div></main>\n" + footer(r)
    write(path, page)


def breadcrumbs(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)
        ],
    }


def cta_block(text="Get Latchkey on the App Store"):
    return f'<p><a class="cta" href="{STORE}">{text}</a></p>'


# ---------------------------------------------------------------- index
def build_index():
    r = ""
    desc = "Latchkey is a free 2FA authenticator for iPhone. Scan a QR code or type a setup key, follow step-by-step guides for 56 services, import from Google Authenticator, 2FAS, Aegis and Raivo. No account, no ads, no analytics."
    ld = [{
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Latchkey: Authenticator App",
        "operatingSystem": "iOS",
        "applicationCategory": "UtilitiesApplication",
        "url": BASE,
        "installUrl": STORE,
        "description": desc,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "author": {"@type": "Person", "name": "Levani Topchishvili"},
    }]
    p = head("Latchkey: Authenticator App for iPhone (2FA codes, no account)", desc, "", r, jsonld=ld) + header(r)
    p += f"""<main id="main">
<section class="hero"><div class="wrap">
<div>
<p class="kicker">Two-factor authenticator for iPhone</p>
<h1>Your sign-in codes, kept under your own key.</h1>
<p class="lede">Latchkey makes the six-digit codes that protect your accounts. No sign-up, no ads, no analytics, no server: your codes stay on your iPhone.</p>
<div class="cta-row"><a class="cta" href="{STORE}">Download on the App Store</a><a class="cta alt" href="guides/">Read the guides</a></div>
<p class="fine">Free to use. Latchkey Pro is optional.</p>
</div>
<div class="tags" aria-hidden="true">
<div class="tag"><div class="who"><b>GitHub</b><span>work</span></div><div class="code">482 913</div><div class="t"><i></i></div></div>
<div class="tag"><div class="who"><b>Instagram</b><span>personal</span></div><div class="code">207 645</div><div class="t"><i></i></div></div>
<div class="tag"><div class="who"><b>Google</b><span>me</span></div><div class="code">931 028</div><div class="t"><i></i></div></div>
</div>
</div></section>

<div class="wrap wide">
<section class="section" aria-labelledby="why">
<h2 id="why">Everything a good authenticator should do, free</h2>
<div class="grid">
<div class="card"><h3>Add accounts any way</h3><p>Scan a QR code with the camera, pick one from a screenshot or photo, paste an <code>otpauth://</code> link, or type the setup key. Codes use 6 to 8 digits and SHA-1, SHA-256 or SHA-512; time-based and counter-based both work.</p></div>
<div class="card"><h3>56 step-by-step setup guides</h3><p>Instagram, Google, Microsoft, Discord, Roblox, GitHub, Amazon, PayPal, Coinbase and more. Each guide shows the exact menu path, then hands you straight to the code.</p></div>
<div class="card"><h3>Backup codes, saved per account</h3><p>Keep each service's one-time recovery codes next to its account, so they are there the day you lose a phone.</p></div>
<div class="card"><h3>Locked with Face ID or your passcode</h3><p>Require unlock when you open Latchkey, and hide codes until you tap them so nobody reads them over your shoulder.</p></div>
<div class="card"><h3>Bring your codes with you</h3><p>Import from Google Authenticator transfer QR codes, 2FAS (plain or encrypted), Aegis (unencrypted JSON), Raivo JSON, and any text file of <code>otpauth://</code> links, such as exports from Ente or Bitwarden.</p></div>
<div class="card"><h3>Backup and move, on your terms</h3><p>Save an encrypted <code>.latchkey</code> backup file (AES-256-GCM, with a password you choose), or show transfer QR codes to move to another phone.</p></div>
</div>
</section>

<section class="section" aria-labelledby="pro">
<h2 id="pro">Free, with an optional Pro upgrade</h2>
<p>Adding accounts, codes, setup guides, backup codes, the lock, import, backup file and moving to another phone are all free. Pro adds the conveniences that need more from iOS:</p>
<div class="tablewrap"><table>
<caption>What is in each plan</caption>
<thead><tr><th scope="col">Feature</th><th scope="col">Free</th><th scope="col">Pro</th></tr></thead>
<tbody>
<tr><th scope="row">Unlimited accounts and codes</th><td>Yes</td><td>Yes</td></tr>
<tr><th scope="row">Setup guides, backup codes, lock, import, backup file, transfer QR codes</th><td>Yes</td><td>Yes</td></tr>
<tr><th scope="row">iCloud Keychain sync across iPhone and iPad</th><td>No</td><td>Yes</td></tr>
<tr><th scope="row">One-time-code AutoFill in Safari and apps</th><td>No</td><td>Yes</td></tr>
<tr><th scope="row">Home Screen and Lock Screen widgets</th><td>No</td><td>Yes</td></tr>
<tr><th scope="row">Folders</th><td>No</td><td>Yes</td></tr>
</tbody></table></div>
<p>Pro costs $1.99 a month or $12.99 a year (with a 1-week free trial), or $29.99 once for lifetime. Prices are shown in US dollars and vary by country. Manage or cancel any time in your Apple Account settings; <a href="help.html#subscription">here is how</a>.</p>
</section>

<section class="panel" aria-labelledby="priv">
<h2 id="priv">Private by construction</h2>
<p>Latchkey has no accounts and no server. The developer collects no data, and the app has no ads and no analytics. Your secrets stay on your iPhone, and travel through Apple's iCloud Keychain only if you switch on sync yourself. Read the <a href="privacy.html">privacy policy</a>.</p>
</section>

<section class="section" aria-labelledby="honest">
<h2 id="honest">What Latchkey is not</h2>
<p>To save you a download: Latchkey does not have an Apple Watch app, push-notification approvals (the "tap Approve" kind), a password manager, or passkeys. It is a focused authenticator for the one-time codes that websites and apps ask for.</p>
</section>

<section class="section" aria-labelledby="learn">
<h2 id="learn">New to two-factor authentication?</h2>
<ul class="guide-list">
<li><a class="card" href="guides/set-up-two-factor-authentication-instagram.html"><h3>How to set up two-factor authentication on Instagram with an authenticator app</h3><p>Step by step, including where to save your backup codes.</p></a></li>
<li><a class="card" href="guides/move-authenticator-codes-to-new-iphone.html"><h3>How to move your authenticator codes to a new iPhone</h3><p>Three ways to do it, and what to check before you wipe the old phone.</p></a></li>
<li><a class="card" href="guides/import-google-authenticator-codes.html"><h3>How to import codes from Google Authenticator to another app</h3><p>Export, scan, verify, then clean up.</p></a></li>
</ul>
<p><a href="guides/">All guides</a> &middot; <a href="help.html">Help and FAQ</a></p>
</section>
</div>
</main>
""" + footer(r)
    write("index.html", p)


# ---------------------------------------------------------------- help
FAQ = [
    ("Adding accounts", [
        ("add", "How do I add an account?",
         """<p>On the Codes tab, tap <span class="path">+</span> and choose how to add it:</p>
<ul><li><strong>Scan QR Code:</strong> point the camera at the QR code on the website's two-factor setup page.</li>
<li><strong>Choose a Screenshot:</strong> setting up on this same iPhone? Take a screenshot of the QR code, then pick it from your photos.</li>
<li><strong>Paste Setup Link or Key:</strong> if you copied the key or an <code>otpauth://</code> link.</li>
<li><strong>Enter Setup Key:</strong> type the key the website shows under "Can't scan?".</li>
<li><strong>Follow a Setup Guide:</strong> the Guides tab has 56 services with the exact menu path.</li></ul>
<p>After you add it, the website asks you to type the six-digit code back to finish turning on two-factor. Do not skip that step.</p>"""),
        ("noscan", "I can't scan the QR code. What is the setup key?",
         """<p>The setup key (also called a secret or manual entry key) is the same information as the QR code, written as letters and numbers. Websites show it under a link such as "Can't scan?" or "Enter a code manually". Choose <span class="path">+ &rsaquo; Enter Setup Key</span>, type the key, and give the account a name. Keys use only the letters A to Z and the digits 2 to 7, so a 0, 1 or 8 means a typo.</p>
<p>If you are on your iPhone, you can't point the camera at its own screen. Use <strong>Choose a Screenshot</strong>, or copy the key and use <strong>Paste Setup Link or Key</strong>.</p>
<p>Leave the Advanced settings (digits, algorithm, period) alone unless the website lists different values. Most use 6 digits, SHA-1 and 30 seconds.</p>"""),
        ("invalid", "The website says my code is invalid. What is wrong?",
         """<p>Codes are calculated from the current time, so if your iPhone's clock is off, every code will be rejected. Open <span class="path">Settings &rsaquo; General &rsaquo; Date &amp; Time</span> and turn on <strong>Set Automatically</strong>. Then try the next code that appears.</p>
<p>Other common causes: you are using the code for a different account; the code expired while you were typing it (wait for the next one); or, for counter-based accounts, you need to tap <strong>Next code</strong> to move on.</p>"""),
    ]),
    ("Backup and a new phone", [
        ("newphone", "How do I move to a new phone?",
         """<p>There are three ways, and you can combine them. Keep the old iPhone working until you have checked a code from every account on the new one.</p>
<ol><li><strong>Latchkey Pro sync:</strong> turn on <span class="path">Settings &rsaquo; iCloud Keychain sync</span> on the old phone, install Latchkey on the new one and sign in with the same Apple Account. Your accounts appear there.</li>
<li><strong>Transfer QR codes (free):</strong> on the old phone open <span class="path">Settings &rsaquo; Move to another phone &rsaquo; Show Transfer Codes</span>. On the new phone choose <span class="path">+ &rsaquo; Import &rsaquo; Scan a Transfer QR Code</span> and scan each code, swiping to the next one on the old phone.</li>
<li><strong>Backup file (free):</strong> make a backup (next question), move the file with AirDrop, Files or iCloud Drive, then import it on the new phone.</li></ol>
<p>The transfer codes contain your secrets, so show them only in private and close the screen when done. <a href="guides/move-authenticator-codes-to-new-iphone.html">Our full guide</a> goes through each method.</p>"""),
        ("backup", "How do I back up and restore?",
         """<p><strong>Back up:</strong> <span class="path">Settings &rsaquo; Back up to a file</span>. Choose a password of at least 8 characters, save the <code>.latchkey</code> file to Files, iCloud Drive or a USB drive. The file is encrypted with AES-256-GCM, with a key derived from your password. <strong>Write the password down: nobody, including us, can recover it.</strong></p>
<p><strong>Restore:</strong> <span class="path">Settings &rsaquo; Import from another app &rsaquo; Choose a File</span>, pick the <code>.latchkey</code> file and enter its password. Latchkey shows what it found and lets you choose which accounts to add. Nothing is uploaded; the file is read on your iPhone.</p>
<p>A backup file is a snapshot. Make a fresh one after adding accounts.</p>"""),
        ("lost", "I lost my phone. What now?",
         """<p>Latchkey has no server and no account, so we cannot see or restore your codes. What helps, in order:</p>
<ol><li>If you used <strong>iCloud Keychain sync</strong> (Pro) or kept a <strong>backup file</strong>, install Latchkey on the new phone and restore. Your codes are back.</li>
<li>Otherwise, sign in to each service using the <strong>backup (recovery) codes</strong> it gave you when you turned on two-factor. Latchkey can store these per account (<span class="path">Account &rsaquo; Details &amp; Backup Codes</span>), but they will not be on a lost phone with no sync or backup, so also keep a copy somewhere else, such as a printout.</li>
<li>If you have neither, use the service's account recovery. Each one differs and may take days.</li></ol>
<p>Once back in, turn two-factor on again with a new Latchkey setup, and generate fresh backup codes. Consider using <a href="https://support.apple.com/find-my">Find My</a> to lock or erase the lost device.</p>"""),
        ("backupcodes", "What are backup codes and where do I keep them in Latchkey?",
         """<p>When you turn on two-factor, most services give you a list of one-time recovery codes. Each works once, as a stand-in for your authenticator. Open the account in Latchkey, tap <strong>Details &amp; Backup Codes</strong> and add them, or edit the list as you use them. You can also print them. Keep a second copy somewhere that is not this phone.</p>"""),
    ]),
    ("Importing from another app", [
        ("import-overview", "Which apps can I import from?",
         """<p>Latchkey reads Google Authenticator transfer QR codes, 2FAS backups (plain or encrypted), Aegis unencrypted JSON, Raivo JSON, other Latchkey backups, and any text file containing <code>otpauth://</code> links (Ente Auth, Bitwarden and many others). Start at <span class="path">Settings &rsaquo; Import from another app</span> (or <span class="path">+ &rsaquo; Import</span>). Latchkey shows a review screen and lets you choose which accounts to add, and marks ones that are already in Latchkey.</p>
<p>The menus below are as best we know them; apps move things between versions. If a menu has changed, look for "export" or "transfer" in that app's settings. <strong>Keep the old app until you have checked a code from each account in Latchkey.</strong> Export files hold your secrets in readable form, so delete them when you are finished.</p>"""),
        ("import-google", "Google Authenticator",
         """<ol><li>In Google Authenticator, tap the <span class="path">&#8943;</span> menu, then <span class="path">Transfer accounts</span> &rsaquo; <span class="path">Export accounts</span>, and select the accounts.</li>
<li>It shows one or more QR codes. In Latchkey choose <span class="path">+ &rsaquo; Import &rsaquo; Scan a Transfer QR Code</span> and scan each (you need a second device to show them).</li>
<li>If you have only one phone, a screenshot of the QR code works if your version of Google Authenticator lets you take one: choose <strong>Choose a Photo of the QR Code</strong> in Latchkey, then delete the screenshot.</li></ol>
<p>Full walkthrough: <a href="guides/import-google-authenticator-codes.html">How to import codes from Google Authenticator</a>.</p>"""),
        ("import-2fas", "2FAS",
         """<ol><li>In 2FAS open <span class="path">Settings &rsaquo; Backup</span> (wording differs by version) and export to a file. You can export encrypted with a password or without.</li>
<li>Save the file to Files or iCloud Drive.</li>
<li>In Latchkey choose <span class="path">Import from another app &rsaquo; Choose a File</span>, pick the file and, if it is encrypted, enter the password you set.</li></ol>"""),
        ("import-aegis", "Aegis (Android)",
         """<p>Aegis is an Android app, so this is for moving from an Android phone to an iPhone.</p>
<ol><li>In Aegis open <span class="path">Settings &rsaquo; Backups</span> (or the export option), and export as <strong>JSON without encryption</strong>. Latchkey reads unencrypted Aegis JSON; encrypted Aegis vaults are not supported, so turn encryption off for the export.</li>
<li>Get the file to your iPhone (AirDrop is not available from Android; use email to yourself, a cloud drive or a USB transfer to Files).</li>
<li>In Latchkey: <span class="path">Import from another app &rsaquo; Choose a File</span>. Delete the file afterwards.</li></ol>"""),
        ("import-raivo", "Raivo",
         """<ol><li>In Raivo open <span class="path">Settings &rsaquo; Export</span> and export your OTPs (the export is a ZIP archive containing JSON).</li>
<li>In Files, tap the ZIP to unpack it, so you have the JSON file.</li>
<li>In Latchkey: <span class="path">Import from another app &rsaquo; Choose a File</span> and pick the JSON.</li></ol>"""),
        ("import-otpauth", "Ente Auth, Bitwarden and other apps",
         """<p>Latchkey scans any text, CSV or JSON file for <code>otpauth://</code> links, which is the standard way one-time-code secrets are written.</p>
<ul><li><strong>Ente Auth:</strong> open its Settings, find the Data or Export section, and export as plain text (the unencrypted option). Import the file in Latchkey.</li>
<li><strong>Bitwarden:</strong> export your vault as an unencrypted <code>.json</code> or <code>.csv</code> (web vault: Tools &rsaquo; Export vault). Logins that have an authenticator key include it as an <code>otpauth://</code> link, which Latchkey finds. Delete the export afterwards: it also contains your passwords.</li>
<li><strong>Anything else:</strong> if the app can export a file with <code>otpauth://</code> links, it will work. If Latchkey says it found nothing, the file did not contain any, for example an encrypted export.</li></ul>"""),
    ]),
    ("Features", [
        ("autofill", "How do I turn on one-time-code AutoFill? (Pro)",
         """<ol><li>In iOS open <span class="path">Settings &rsaquo; General &rsaquo; AutoFill &amp; Passwords &rsaquo; Verification Codes</span> and choose <strong>Latchkey</strong>. (In Latchkey, <span class="path">Settings &rsaquo; AutoFill codes</span> has a button that opens it.)</li>
<li>Make sure each account has its website set; Latchkey knows many already. For others, open the account and add its AutoFill website, like <code>github.com</code>.</li>
<li>Sign in as usual. When the code field appears, tap the Latchkey suggestion above the keyboard.</li></ol>
<p>AutoFill needs Latchkey Pro. If a code does not show up, check the website setting on the account, and that Latchkey is selected under Verification Codes.</p>"""),
        ("widgets", "How do I add a widget? (Pro)",
         """<ol><li>On the Codes screen, tap <span class="path">&#8943;</span> on an account and choose <strong>Show in Widgets</strong>.</li>
<li>Touch and hold the Home Screen, tap <span class="path">Edit &rsaquo; Add Widget</span>, find Latchkey and add it.</li></ol>
<p>Widgets hide codes while your iPhone is locked.</p>"""),
        ("lock", "How do I lock Latchkey with Face ID? Can I hide the codes?",
         """<p>Open <span class="path">Settings</span> in Latchkey and turn on <strong>Lock with Face ID</strong> (it says Touch ID or Passcode if that is what your device uses). <strong>Require</strong> sets how long Latchkey may stay unlocked: immediately, or after 1, 5 or 15 minutes. If Face ID fails, your iPhone passcode unlocks it.</p>
<p>Turn on <strong>Hide codes until tapped</strong> to blur every code until you tap it. <strong>Show the next code early</strong> displays the upcoming code when the current one is about to expire. Tapping a code copies it, and it clears from the clipboard after 90 seconds.</p>"""),
        ("folders", "Can I organize accounts into folders? (Pro)",
         """<p>Yes. Open an account's <span class="path">&#8943;</span> menu, choose <strong>Folder</strong> and pick one or create a new folder. Use folders to keep work, family and gaming accounts apart.</p>"""),
        ("sync", "What does iCloud Keychain sync do? (Pro)",
         """<p>With <span class="path">Settings &rsaquo; iCloud Keychain sync</span> on, your accounts are stored in your own iCloud Keychain, so they appear on your other iPhones and iPads signed in to the same Apple Account, and on a new phone. Apple's end-to-end protection for iCloud Keychain applies. This is the only way your secrets ever leave the device, and the developer never has access to them. iCloud Keychain must be switched on in iOS (<span class="path">Settings &rsaquo; your name &rsaquo; iCloud &rsaquo; Passwords &amp; Keychain</span>).</p>"""),
    ]),
    ("Subscriptions", [
        ("subscription", "How do I cancel, restore or manage Latchkey Pro?",
         """<p><strong>Cancel:</strong> on your iPhone open <span class="path">Settings &rsaquo; your name &rsaquo; Subscriptions &rsaquo; Latchkey Pro</span> and tap Cancel (or Cancel Free Trial). Do it at least a day before the renewal date. You keep Pro until the end of the period you paid for. Deleting the app does not cancel a subscription.</p>
<p><strong>Restore on a new phone:</strong> sign in with the same Apple Account, then in Latchkey open <span class="path">Settings &rsaquo; Restore Purchases</span>. This restores the monthly, yearly or lifetime Pro purchase.</p>
<p><strong>Refunds:</strong> Apple handles billing and refunds. Visit <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</p>
<p>Prices: $1.99 a month or $12.99 a year (1-week free trial), or $29.99 lifetime, in US dollars; other countries see local prices. Subscriptions renew automatically unless cancelled and are governed by <a href="{EULA}">Apple's standard Terms of Use</a>.</p>""".replace("{EULA}", EULA)),
        ("cancel-codes", "What happens to my codes if I cancel Pro?",
         """<p>Your accounts and codes stay on the device and keep working. Pro features (sync, AutoFill, widgets, folders) turn off. Nothing is deleted.</p>"""),
    ]),
    ("Other questions", [
        ("watch", "Is there an Apple Watch app, push approval, or passkey support?",
         """<p>No. Latchkey is a one-time-code authenticator. It does not have an Apple Watch app, push-notification approvals, a password manager or passkeys.</p>"""),
        ("contact", "How do I report a problem or ask something else?",
         """<p>Open an issue at <a href="{I}">{I}</a> (a free GitHub account is required), or use the support link on Latchkey's <a href="{S}">App Store page</a>. Please do not post secrets, setup keys or codes anywhere public.</p>""".replace("{I}", ISSUES).replace("{S}", STORE)),
    ]),
]


def build_help():
    toc = "".join('<li><a href="#g%d">%s</a></li>' % (i, g) for i, (g, _) in enumerate(FAQ))
    body = f"""<p>Answers to the most common questions about Latchkey: Authenticator App. Can't find yours? See <a href="#contact">how to contact us</a>.</p>
<nav class="toc" aria-label="On this page"><b>On this page</b><ul>{toc}</ul></nav>
"""
    entities = []
    for i, (g, items) in enumerate(FAQ):
        body += f'<h2 id="g{i}">{g}</h2>\n'
        for qid, q, a in items:
            body += f'<details id="{qid}"><summary>{q}</summary><div class="ans">{a}</div></details>\n'
            if qid in ("add", "noscan", "invalid", "newphone", "backup", "lost", "autofill", "subscription", "import-overview"):
                entities.append({"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}})
    body += f'<div class="note"><p><strong>Still stuck?</strong> Open an issue at <a href="{ISSUES}">GitHub</a> or write to us through the <a href="{STORE}">App Store</a> support link.</p></div>'
    # open details that are linked via hash
    body += """<script>(function(){function o(){var h=location.hash.slice(1);if(!h)return;var e=document.getElementById(h);if(e&&e.tagName==='DETAILS'){e.open=true;e.scrollIntoView()}}o();addEventListener('hashchange',o)})()</script>"""
    ld = [
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities},
        breadcrumbs([("Latchkey", BASE), ("Help", BASE + "help.html")]),
    ]
    prose_page("help.html", "Help and FAQ: Latchkey Authenticator for iPhone",
               "How to add accounts, move to a new iPhone, back up and restore, import from Google Authenticator, 2FAS, Aegis and Raivo, set up AutoFill and widgets, and manage Latchkey Pro.",
               "Help and FAQ", body, current="help.html", jsonld=ld)


# ---------------------------------------------------------------- privacy / terms
def build_privacy():
    body = f"""<p><strong>In short:</strong> Latchkey has no account and no server. The developer collects no data from you. Your codes and secrets never leave your device, except through your own iCloud Keychain if you turn on sync.</p>

<h2>Who we are</h2>
<p>Latchkey: Authenticator App is made by Levani Topchishvili, an individual developer. This policy covers the Latchkey app for iPhone and iPad and this website.</p>

<h2>What the app stores, and where</h2>
<p>The accounts you add (names, setup secrets, backup codes, folders, settings) are stored on your device, in the iOS Keychain and app storage. They are not sent to the developer or to any server operated by the developer. Latchkey has no sign-up, no ads, no analytics, no tracking SDKs and no crash-reporting service.</p>
<ul>
<li><strong>iCloud Keychain sync (Latchkey Pro, off by default):</strong> if you switch it on, your accounts are stored in your own iCloud Keychain so they appear on your other devices. That data is handled by Apple under Apple's terms and privacy practices, and the developer cannot access it.</li>
<li><strong>Backup files and transfer QR codes:</strong> created only when you ask. Backup files are encrypted with a password you choose (AES-256-GCM). They are saved to a location you pick; Latchkey does not upload them.</li>
<li><strong>Imports:</strong> files and photos you choose to import are read on your device and are not uploaded.</li>
<li><strong>Camera and photos:</strong> the camera is used only to scan QR codes, and photos only when you choose a screenshot or picture of a QR code. Images are processed on the device.</li>
<li><strong>Face ID:</strong> used through Apple's system prompt to unlock the app. Latchkey never receives your biometric data.</li>
<li><strong>Clipboard:</strong> when you copy a code, it is cleared from the clipboard after 90 seconds.</li>
</ul>

<h2>Purchases (RevenueCat)</h2>
<p>Latchkey Pro subscriptions and the lifetime purchase are processed by Apple. To check whether you have Pro and to restore purchases, the app uses <a href="https://www.revenuecat.com">RevenueCat</a>, a purchase-management service. RevenueCat receives your purchase history and an anonymous app user ID generated for the app. This is used only for app functionality (unlocking Pro). It is not linked to your identity, is not used for tracking, and is not combined with other data to follow you across apps or websites. RevenueCat's own handling is described in <a href="https://www.revenuecat.com/privacy">its privacy policy</a>. Apple handles payment details; the developer never sees your card or name.</p>

<h2>App Store privacy summary</h2>
<div class="tablewrap"><table>
<caption>What the App Store privacy label reflects</caption>
<thead><tr><th scope="col">Data</th><th scope="col">Collected by the developer?</th><th scope="col">Purpose</th></tr></thead>
<tbody>
<tr><th scope="row">Codes, secrets, accounts, backup codes</th><td>No</td><td>Stay on your device (or your iCloud Keychain if you enable sync)</td></tr>
<tr><th scope="row">Purchase history</th><td>Processed by RevenueCat, not linked to you</td><td>App functionality (Pro)</td></tr>
<tr><th scope="row">Anonymous user ID</th><td>Processed by RevenueCat, not linked to you</td><td>App functionality (Pro)</td></tr>
<tr><th scope="row">Analytics, advertising, tracking</th><td>None</td><td>Not used</td></tr>
</tbody></table></div>

<h2>This website</h2>
<p>This site is hosted by GitHub Pages. It has no cookies of its own, no analytics and no forms, and loads no third-party scripts or fonts. GitHub, as the host, may log standard connection data (such as your IP address) under <a href="https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement">its own privacy statement</a>.</p>

<h2>Children</h2>
<p>Latchkey does not knowingly collect any personal information from anyone, including children.</p>

<h2>Your choices</h2>
<p>You can delete accounts in the app, delete the app to remove its local data, turn off sync, and remove Latchkey items from iCloud Keychain through iOS settings. Because the developer holds no data about you, there is nothing for us to export or erase on our side. For purchase data held by RevenueCat, see its privacy policy.</p>

<h2>Changes and contact</h2>
<p>If this policy changes, the new version is posted here with a new date. Questions? Open an issue at <a href="{ISSUES}">{ISSUES}</a>, or write to us through the support link on the <a href="{STORE}">App Store listing</a>. Please do not post codes or secrets publicly.</p>
"""
    prose_page("privacy.html", "Privacy Policy: Latchkey Authenticator",
               "Latchkey collects no data. Codes and secrets stay on your device. RevenueCat processes purchase history and an anonymous ID only to unlock Pro.",
               "Privacy Policy", body, current="privacy.html", meta="Last updated 5 October 2026",
               jsonld=[breadcrumbs([("Latchkey", BASE), ("Privacy Policy", BASE + "privacy.html")])])


def build_terms():
    body = f"""<p>These terms apply to Latchkey: Authenticator App ("Latchkey", "the app") and this website, provided by Levani Topchishvili ("the developer").</p>

<h2>Using the app</h2>
<p>Latchkey generates one-time codes for accounts you add. You may use it for your own accounts and any accounts you are authorized to access. The app is provided free of charge, with optional paid features (Latchkey Pro).</p>

<h2>Apple's standard license</h2>
<p>The app is licensed to you under Apple's standard Licensed Application End User License Agreement: <a href="{EULA}">{EULA}</a>. If these terms and that agreement conflict, Apple's agreement governs.</p>

<h2>Subscriptions and purchases</h2>
<ul>
<li>Latchkey Pro is offered as an auto-renewing subscription ($1.99 per month or $12.99 per year, US prices, with a 1-week free trial for new subscribers) or as a one-time lifetime purchase ($29.99). Prices vary by country.</li>
<li>Payment is charged to your Apple Account at confirmation of purchase. Subscriptions renew automatically unless cancelled at least 24 hours before the end of the current period. Your account is charged for renewal within 24 hours before the period ends.</li>
<li>Manage or cancel in <span class="path">Settings &rsaquo; your name &rsaquo; Subscriptions</span>. Any unused part of a free trial is forfeited when you purchase a subscription.</li>
<li>Billing, cancellations and refunds are handled by Apple under its terms.</li>
</ul>

<h2>Your responsibility for your codes</h2>
<p>Latchkey has no server and no account, so the developer cannot recover your codes, backup passwords or lost devices. Keep each service's backup codes, make a backup file, and remember its password. Latchkey is provided "as is", without warranties of any kind, to the extent permitted by law. To the extent permitted by law, the developer is not liable for lost access to accounts, lost codes or indirect damages.</p>

<h2>Acceptable use</h2>
<p>Do not use the app or site to break the law, reverse engineer the app beyond what the law allows, or gain unauthorized access to accounts that are not yours.</p>

<h2>Changes and contact</h2>
<p>These terms may be updated; the current version is always at this address. See also the <a href="privacy.html">Privacy Policy</a>. Contact: <a href="{ISSUES}">{ISSUES}</a>, or the support link on the <a href="{STORE}">App Store listing</a>.</p>
"""
    prose_page("terms.html", "Terms of Use: Latchkey Authenticator",
               "Terms of use for Latchkey: Authenticator App. Subscriptions are governed by Apple's standard licensed application end user license agreement.",
               "Terms of Use", body, current="terms.html", meta="Last updated 5 October 2026",
               jsonld=[breadcrumbs([("Latchkey", BASE), ("Terms of Use", BASE + "terms.html")])])


# ---------------------------------------------------------------- guides
GUIDES = []


def guide(slug, title, desc, steps_ld, body, short):
    path = f"guides/{slug}.html"
    url = BASE + path
    GUIDES.append((slug, title, short))
    crumbs = f'<p class="crumbs"><a href="../">Latchkey</a> &rsaquo; <a href="./">Guides</a> &rsaquo; {esc(title)}</p>'
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
         "author": {"@type": "Person", "name": "Levani Topchishvili"},
         "publisher": {"@type": "Person", "name": "Levani Topchishvili"},
         "datePublished": DATE, "dateModified": DATE, "mainEntityOfPage": url,
         "image": BASE + "img/icon-512.png"},
        breadcrumbs([("Latchkey", BASE), ("Guides", BASE + "guides/"), (title, url)]),
    ]
    if steps_ld:
        ld.insert(1, {"@context": "https://schema.org", "@type": "HowTo", "name": title, "description": desc,
                      "totalTime": steps_ld[0],
                      "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": url + "#step-%d" % (i + 1)}
                               for i, (n, t) in enumerate(steps_ld[1])]})
    r = "../"
    page = head(title + " | Latchkey", desc, path, r, og_type="article", jsonld=ld) + header(r, "guides/")
    page += f'<main id="main"><article class="wrap page">\n{crumbs}\n<h1>{esc(title)}</h1>\n<p class="meta">Updated 5 October 2026 &middot; by Levani Topchishvili, developer of Latchkey</p>\n{body}\n'
    page += f"""<div class="panel"><h2>Get Latchkey</h2><p>Latchkey is a free two-factor authenticator for iPhone: no account, no ads, no analytics, codes stay on your device. Setup guides for 56 services, imports from other authenticators, and an encrypted backup.</p><p><a class="cta" href="{STORE}">Download on the App Store</a></p></div>
<p><a href="./">&larr; More guides</a> &middot; <a href="../help.html">Help and FAQ</a></p>
</article></main>
""" + footer(r)
    write(path, page)


def build_guides():
    guide(
        "set-up-two-factor-authentication-instagram",
        "How to set up two-factor authentication on Instagram with an authenticator app",
        "Turn on two-factor authentication for Instagram using an authenticator app on iPhone: the menu path, adding the key to Latchkey, confirming the code and saving your backup codes.",
        ("PT10M", [
            ("Open Instagram's two-factor settings", "In Instagram go to Settings and activity, Accounts Center, Password and security, Two-factor authentication, and choose your account."),
            ("Choose Authentication app", "Select Authentication app and confirm your password if asked. Instagram shows a setup key."),
            ("Add the key to Latchkey", "Copy the key, then in Latchkey tap + and choose Paste Setup Link or Key, or scan the QR code if Instagram shows one."),
            ("Enter the code to confirm", "Type the six-digit code Latchkey shows back into Instagram and finish."),
            ("Save your backup codes", "Copy Instagram's recovery codes into the account's Details and Backup Codes in Latchkey and keep another copy elsewhere."),
        ]),
        """<p>Two-factor authentication (2FA) means that signing in to Instagram needs two things: your password and a short-lived six-digit code. An authenticator app generates that code on your phone, so a stolen password alone is not enough. It is also more reliable than text messages, which can be delayed, intercepted through SIM-swapping, or unavailable when you travel. This guide takes about ten minutes.</p>

<h2>Before you start</h2>
<ul><li>Install an authenticator app. These steps use <a href="STORE">Latchkey</a> (free), but any standard authenticator works the same way.</li>
<li>Have your Instagram password to hand, and sign in to Instagram on your iPhone.</li>
<li>Make sure your iPhone's clock is set automatically (<span class="path">Settings &rsaquo; General &rsaquo; Date &amp; Time &rsaquo; Set Automatically</span>), because codes depend on the time.</li></ul>

<h2>Step by step</h2>
<ol class="steps">
<li id="step-1"><strong>Open the two-factor settings.</strong> In Instagram tap your profile, then the menu, and go to <span class="path">Settings and activity &rsaquo; Accounts Center &rsaquo; Password and security &rsaquo; Two-factor authentication</span>. Choose the Instagram account you want to protect. Instagram changes this layout from time to time; if you do not see these names, search "two-factor" in settings.</li>
<li id="step-2"><strong>Choose Authentication app.</strong> Instagram offers a few methods (text message, authentication app, and sometimes security keys or WhatsApp). Pick <strong>Authentication app</strong>. It may ask you to confirm your password first.</li>
<li id="step-3"><strong>Get the setup key.</strong> Instagram shows a setup key, usually with a Copy option, and may show a QR code. A phone cannot scan its own screen, so copy the key.</li>
<li id="step-4"><strong>Add it to Latchkey.</strong> Open Latchkey, tap <span class="path">+</span> and choose <strong>Paste Setup Link or Key</strong>, then paste. (If you are setting up from a computer, choose <strong>Scan QR Code</strong> and point the camera at the code on screen. Setting up on this phone with a QR code? Take a screenshot of it and use <strong>Choose a Screenshot</strong>.) Name the account "Instagram" and save. Latchkey also has a built-in Instagram setup guide under the Guides tab that shows this menu path.</li>
<li id="step-5"><strong>Confirm with a code.</strong> Latchkey now shows a six-digit code that changes every 30 seconds. Tap it to copy, return to Instagram, enter it and tap Next. Enter it before it refreshes; if it fails, wait for the next one. Instagram confirms that two-factor is on.</li>
<li id="step-6"><strong>Save your backup codes.</strong> Back in Instagram's two-factor settings, look for <strong>Backup codes</strong> (also called recovery codes). Copy them. In Latchkey, open the Instagram account, tap <strong>Details &amp; Backup Codes</strong> and paste them in. Each works once if you lose access to your authenticator. Keep a second copy somewhere that is not your phone.</li>
</ol>

<h2>Signing in afterwards</h2>
<p>When Instagram asks for a code on a new device, open Latchkey, tap the Instagram code to copy it and paste it. If you use Latchkey Pro, one-time-code AutoFill can suggest the code above the keyboard in Safari and apps.</p>

<h2>Common problems</h2>
<ul>
<li><strong>"Code is invalid".</strong> Check Date &amp; Time is set automatically, and that you are using the code for Instagram, not another account. Wait for a fresh code and try again.</li>
<li><strong>I changed phones.</strong> Move your codes <em>before</em> you wipe the old phone: see <a href="move-authenticator-codes-to-new-iphone.html">how to move your authenticator codes to a new iPhone</a>.</li>
<li><strong>I lost the phone with the authenticator.</strong> Use a backup code to sign in, then set two-factor up again with the new phone and generate fresh codes. Without backup codes you must go through Instagram's account recovery, which can be slow.</li>
<li><strong>Several Instagram accounts.</strong> Each account has its own key. Add each to Latchkey and name them clearly.</li>
</ul>

<div class="note"><p><strong>Tip:</strong> turn on the lock in Latchkey (<span class="path">Settings &rsaquo; Lock with Face ID</span>) so that someone holding your unlocked phone cannot read your codes.</p></div>""".replace("STORE", STORE),
        "Menu path, the setup key, confirming and saving backup codes.")

    guide(
        "move-authenticator-codes-to-new-iphone",
        "How to move your authenticator codes to a new iPhone",
        "Three ways to move two-factor codes to a new iPhone without getting locked out: iCloud Keychain sync, transfer QR codes and an encrypted backup file, plus what to check before wiping the old phone.",
        ("PT15M", [
            ("Keep the old iPhone working", "Do not erase or trade in the old phone until you have confirmed a code from every account on the new one."),
            ("Pick a method", "Use iCloud Keychain sync (Latchkey Pro), transfer QR codes, or an encrypted backup file."),
            ("Move the accounts", "Sync, scan the transfer codes, or import the backup file on the new iPhone."),
            ("Check every account", "Compare the new codes with the old ones, or sign in with each service."),
            ("Clean up", "Delete backup files and screenshots, and only then retire the old phone."),
        ]),
        """<p>Getting a new iPhone is exciting until you realise your two-factor codes did not come with it. Many authenticators keep their secrets only on the device, so a new phone starts empty, and if you have already wiped the old one you are left using backup codes and account recovery. This guide shows how to move your codes safely. It uses Latchkey for the examples; the principle (export first, verify, then clean up) applies to any authenticator.</p>

<h2>The golden rule: keep the old phone until you have checked</h2>
<p>Do not erase, trade in or sell the old iPhone until each account works on the new one. Until then you have a fallback; afterwards you may not.</p>

<h2>Method 1: iCloud Keychain sync (Latchkey Pro)</h2>
<p>The easiest option if you use Latchkey Pro. Your accounts are stored in your own iCloud Keychain, so they follow your Apple Account.</p>
<ol class="steps">
<li id="step-1"><strong>On the old phone</strong>, open Latchkey, go to <span class="path">Settings</span> and turn on <strong>iCloud Keychain sync</strong>. iCloud Keychain must be enabled in iOS under <span class="path">Settings &rsaquo; your name &rsaquo; iCloud &rsaquo; Passwords &amp; Keychain</span>.</li>
<li id="step-2"><strong>On the new phone</strong>, sign in with the same Apple Account, install <a href="STORE">Latchkey</a>, and open it. If Pro is not active, tap <span class="path">Settings &rsaquo; Restore Purchases</span>.</li>
<li id="step-3">Your accounts appear. Continue to "Check everything" below.</li>
</ol>

<h2>Method 2: transfer QR codes (free)</h2>
<p>This works without Pro, and without any cloud. You need both phones in front of you.</p>
<ol class="steps">
<li id="step-4"><strong>On the old phone</strong>: <span class="path">Settings &rsaquo; Move to another phone &rsaquo; Show Transfer Codes</span>. Latchkey shows your accounts as QR codes, a few at a time.</li>
<li id="step-5"><strong>On the new phone</strong>: install Latchkey and tap <span class="path">+ &rsaquo; Import &rsaquo; Scan a Transfer QR Code</span>. Scan the first code. Swipe the old phone to the next code and scan again until all are in ("Code 1 of 3", and so on).</li>
<li id="step-6">Review what Latchkey found and add the accounts. Then tap <strong>Hide Codes</strong> on the old phone. These QR codes contain your secrets, so do this in private and do not photograph them.</li>
</ol>

<h2>Method 3: an encrypted backup file (free)</h2>
<p>Best when you cannot have both phones side by side, or as a safety net alongside the other methods.</p>
<ol class="steps">
<li id="step-7"><strong>Create the backup:</strong> <span class="path">Settings &rsaquo; Back up to a file</span>. Choose a password of at least 8 characters and write it down. Latchkey makes a <code>.latchkey</code> file encrypted with AES-256-GCM, with a key derived from the password using PBKDF2. Save it to Files, iCloud Drive or a USB drive.</li>
<li id="step-8"><strong>Move the file</strong> to the new phone (AirDrop, iCloud Drive or Files).</li>
<li id="step-9"><strong>Restore:</strong> on the new phone choose <span class="path">Settings &rsaquo; Import from another app &rsaquo; Choose a File</span>, pick the file and enter the password. Pick which accounts to add.</li>
</ol>
<p>Without the password nobody, including the developer, can open the file, so store it separately from the file itself.</p>

<h2>Check everything</h2>
<p>Before you retire the old phone:</p>
<ul>
<li>Compare a code from each account on both phones; they should match at the same moment. Or, for important accounts, sign in on a device you do not usually use.</li>
<li>If you use hide-codes or the Face ID lock, set those up again on the new phone under Settings.</li>
<li>Turn on AutoFill under <span class="path">Settings &rsaquo; General &rsaquo; AutoFill &amp; Passwords &rsaquo; Verification Codes</span> on the new phone if you use it.</li>
<li>Make sure your backup codes came across: open an account and tap <strong>Details &amp; Backup Codes</strong>.</li>
</ul>

<h2>Clean up</h2>
<p>Delete any backup files you no longer need from Downloads and Files, and clear screenshots of QR codes from Photos (and Recently Deleted). Only then erase or hand over the old iPhone.</p>

<div class="note"><p><strong>If codes are rejected on the new phone,</strong> check <span class="path">Settings &rsaquo; General &rsaquo; Date &amp; Time &rsaquo; Set Automatically</span> first. A wrong clock is the most common cause.</p></div>

<p>Moving from a different authenticator instead? See <a href="import-google-authenticator-codes.html">how to import from Google Authenticator</a> or the <a href="../help.html#import-overview">import guide for 2FAS, Aegis, Raivo and others</a>.</p>""".replace("STORE", STORE),
        "iCloud sync, transfer QR codes or a backup file, and what to check first.")

    guide(
        "import-google-authenticator-codes",
        "How to import codes from Google Authenticator to another app",
        "Export your accounts from Google Authenticator as a transfer QR code and import them into Latchkey on iPhone, then verify each code before removing the old ones.",
        ("PT10M", [
            ("Open the export screen", "In Google Authenticator tap the three-dot menu, then Transfer accounts, then Export accounts."),
            ("Select your accounts", "Choose the accounts to move; Google shows one or more QR codes."),
            ("Scan them in Latchkey", "In Latchkey tap +, Import, Scan a Transfer QR Code, and scan each code in turn."),
            ("Review and add", "Check the list Latchkey found and add the accounts."),
            ("Verify, then clean up", "Confirm the codes work, then remove accounts from Google Authenticator and delete any screenshots."),
        ]),
        """<p>Google Authenticator is where many people first meet two-factor codes. There are good reasons to want your accounts elsewhere: a backup you control, a lock for the app, setup guides, or moving from Android to iPhone. The good news is that Google Authenticator can export your accounts as a QR code, and apps like Latchkey can read it. This guide walks through it safely.</p>

<h2>What you need</h2>
<ul><li>Google Authenticator on a phone that still has your accounts.</li>
<li><a href="STORE">Latchkey</a> installed on your iPhone (free; importing does not require Pro).</li>
<li>A second device to show the QR code if both apps are on the same iPhone, or a screenshot (see below).</li></ul>

<h2>How it works</h2>
<p>When you choose Export accounts, Google Authenticator packs the secret keys for the accounts you select into one or more QR codes in a special <code>otpauth-migration://</code> format. Latchkey understands it. Because the QR code contains the secrets themselves, treat it like a password: do not share it, and delete any screenshot when finished.</p>

<h2>Step by step</h2>
<ol class="steps">
<li id="step-1"><strong>Open the export screen.</strong> In Google Authenticator, tap the <span class="path">&#8943;</span> menu, then <span class="path">Transfer accounts</span> and <span class="path">Export accounts</span>. Menus change between versions; if you cannot find them, look for "transfer" or "export" in the app's menu. You may be asked to unlock with Face ID or your passcode.</li>
<li id="step-2"><strong>Select accounts.</strong> Tick the accounts you want to move, or all of them. Google shows a QR code, and if you selected many accounts, several ("1 of 3").</li>
<li id="step-3"><strong>Scan with Latchkey.</strong> On the iPhone with Latchkey, tap <span class="path">+ &rsaquo; Import &rsaquo; Scan a Transfer QR Code</span> (or <span class="path">Settings &rsaquo; Import from another app</span>) and point the camera at the first QR code. Move to the next one in Google Authenticator and scan again.</li>
<li id="step-4"><strong>Review and add.</strong> Latchkey shows how many accounts it found, marks any it already has, and lets you choose which to add. Tap <strong>Add</strong>.</li>
<li id="step-5"><strong>Verify.</strong> This is the important step. Compare the code for each account in Latchkey with the one in Google Authenticator at the same moment; they should be identical. For accounts you care about most, sign in using the Latchkey code.</li>
</ol>

<h2>Only one phone?</h2>
<p>A phone camera cannot scan its own screen. Options:</p>
<ul>
<li>Show the QR codes on one device (an old phone, an iPad) and scan with the other.</li>
<li>If your version of Google Authenticator lets you take a screenshot of the export screen, use Latchkey's <strong>Choose a Photo of the QR Code</strong> to pick it. Delete the screenshot afterwards, including from Recently Deleted.</li>
</ul>

<h2>After you import</h2>
<ul>
<li><strong>Do not delete anything from Google Authenticator yet.</strong> Keep it until every account has been checked in Latchkey. Having both temporarily is harmless; both apps produce the same codes from the same secret.</li>
<li>Then remove the accounts from Google Authenticator (or leave it as a spare; it is your decision).</li>
<li>Make a backup in Latchkey: <span class="path">Settings &rsaquo; Back up to a file</span>, with a password you will remember.</li>
<li>Add the backup codes you got from each service to the account in Latchkey (<strong>Details &amp; Backup Codes</strong>).</li>
<li>Optionally turn on the Face ID lock under Settings.</li>
</ul>

<h2>Troubleshooting</h2>
<ul>
<li><strong>"Nothing found" or an unreadable QR code.</strong> Increase the screen brightness, hold steady, and make sure the whole QR code is in frame. With several codes, scan them one at a time.</li>
<li><strong>Codes do not match.</strong> Check Date &amp; Time is set automatically on both phones.</li>
<li><strong>Some accounts are missing.</strong> Export again and select them. Some services use settings Latchkey shows as advanced (digits, SHA algorithm, period); those carry over with the import.</li>
</ul>

<p>Importing from something else? The <a href="../help.html#import-overview">Help page</a> has the menu steps for 2FAS, Aegis, Raivo, Ente and Bitwarden. Planning to change phones? Read <a href="move-authenticator-codes-to-new-iphone.html">how to move your codes to a new iPhone</a>.</p>""".replace("STORE", STORE),
        "Export from Google, scan with Latchkey, verify, then clean up.")

    # hub
    items = "".join(
        f'<li><a class="card" href="{s}.html"><h2>{esc(t)}</h2><p>{esc(d)}</p></a></li>' for s, t, d in GUIDES
    )
    body = f"""<p>Practical guides to two-factor authentication on iPhone. Looking for a specific app? Latchkey's Guides tab has 56 in-app setup guides with the exact menu path for each service.</p>
<ul class="guide-list">{items}</ul>
<p><a href="../help.html">Help and FAQ</a> &middot; <a href="../">Latchkey home</a></p>
{cta_block()}"""
    r = "../"
    path = "guides/index.html"
    ld = [breadcrumbs([("Latchkey", BASE), ("Guides", BASE + "guides/")])]
    page = head("Two-factor authentication guides | Latchkey", "How-to guides for two-factor authentication on iPhone: set up Instagram 2FA, move codes to a new iPhone, import from Google Authenticator.", "guides/", r, jsonld=ld) + header(r, "guides/")
    page += f'<main id="main"><div class="wrap page">\n<h1>Guides</h1>\n{body}\n</div></main>\n' + footer(r)
    write(path, page)


# ---------------------------------------------------------------- 404, robots, sitemap
def build_misc():
    r = "/latchkey/"
    p = head("Page not found | Latchkey", "This page does not exist.", "404.html", r, noindex=True) + header(r)
    p += f"""<main id="main"><div class="wrap page"><h1>That page isn't here</h1>
<p>The link may be old or mistyped. Try one of these:</p>
<ul><li><a href="{r}">Latchkey home</a></li><li><a href="{r}help.html">Help and FAQ</a></li><li><a href="{r}guides/">Guides</a></li><li><a href="{r}privacy.html">Privacy Policy</a></li></ul>
{cta_block()}</div></main>
""" + footer(r)
    write("404.html", p)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    urls = ["", "help.html", "guides/"] + [f"guides/{s}.html" for s, _, _ in GUIDES] + ["privacy.html", "terms.html"]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{DATE}</lastmod></url>\n" for u in urls)
    xml += "</urlset>\n"
    write("sitemap.xml", xml)
    write(".nojekyll", "")


build_index()
build_help()
build_privacy()
build_terms()
build_guides()
build_misc()
print("built")
