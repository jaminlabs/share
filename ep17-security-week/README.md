# Security week patch check (Oct 21, 2026)

Two fixes from this week that take a couple of minutes each. No security background needed.

## 1. Is your website's PHP patched? (PHP2Shell)

On Oct 21, 2026 PHP fixed two critical bugs (CVE-2026-109618, CVE-2026-109619, CVSS 9.2) that let a stranger run code on a PHP server without logging in. The fix lives in PHP itself, so your server or hosting company has to update it. A WordPress plugin can't fix it.

**WordPress, no terminal:** WP Admin > Tools > Site Health > Info tab > Server > "PHP version".

**With SSH:**

```sh
php -v
```

Patched versions (or newer):

| Branch | Patched in |
|---|---|
| 8.5 | 8.5.12 |
| 8.4 | 8.4.27 |
| 8.3 | 8.3.36 |
| 8.2 | 8.2.35 |
| 8.1 or older | no official fix, so ask your host or upgrade |

If your host manages PHP for you, open a support ticket and ask: "Is PHP on my plan updated for CVE-2026-109618 and CVE-2026-109619?"

Source: [php.net security advisory, Oct 21, 2026](https://www.php.net/). php.net says there are no complete workarounds and updating is the only safe choice.

## 2. Is your browser blocking the bad certificates? (eMudhra)

Eight eMudhra intermediate certificates had private keys that could be guessed (one was the number 4). Chrome, Firefox and Apple now block them, but only after an update.

- **Chrome:** Settings > About Chrome, then Relaunch if it asks.
- **Firefox:** Settings > General > Firefox Updates, then Restart to update.
- **iPhone / Mac:** install the latest system update.

Running servers or apps that keep their own certificate store (Java, Node.js, Python `certifi`, IoT devices)? Check whether anything you run still trusts eMudhra intermediates, and update the CA bundle.

Source: [The Register, Oct 20, 2026](https://www.theregister.com/security/2026/10/20/indian-certification-authority-emudhras-private-keys-compromised-one-of-them-was-the-number-4/5304312).

## What I'm not saying

I'm not a security expert. This is a checklist from public advisories, not an audit of your setup. As of Oct 20, no attacks using the eMudhra keys had been confirmed.
