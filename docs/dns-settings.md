# DNS & Domain Settings — pickleballreviewer.com

## Domain Registrar: Namecheap
**Domain:** `pickleballreviewer.com`
**DNS Location:** Namecheap → Dashboard → Domain List → `pickleballreviewer.com` → Advanced DNS

### Required DNS Records
Delete all old `@` and `www` records before adding these:

| Type | Host | Value | TTL | Hidden Proxy |
|------|------|-------|-----|:---:|
| **A Record** | `@` | `216.198.79.1` | Automatic | ❌ OFF |
| **CNAME Record** | `www` | `7f354a77b0bdb3df.vercel-dns-017.com.` | Automatic | ❌ OFF |

### Critical Notes
- **Hidden Proxy MUST be OFF** for both records — Namecheap's proxy breaks Vercel's SSL certificate
- CNAME value needs **trailing dot** (`cname.vercel-dns-017.com.`)
- Vercel assigns unique CNAME targets per domain — always use the value Vercel shows
- If Vercel shows a different IP than `216.198.79.1`, use Vercel's value instead

### Propagation Time
5–30 minutes after saving changes in Namecheap.

## Hosting: Vercel
**Project:** pickleballreviewer
**Settings Path:** Vercel → Project → Settings → Domains

### Required Vercel Configuration
- Add domain: `pickleballreviewer.com`
- **DO NOT** add `www.pickleballreviewer.com` separately — the CNAME in Namecheap handles it
- Vercel auto-issues Let's Encrypt SSL certificate once DNS is verified
- Vercel auto-redirects bare domain ↔ www (no manual redirect config needed)

## Troubleshooting

### www returns "Your connection is not private" or 000
- **Cause:** DNS `www` A record points to non-Vercel IP (e.g., Namecheap parking page)
- **Fix:** Ensure `www` is a CNAME to Vercel's assigned value, with Hidden Proxy OFF

### Bare domain returns 000 or wrong page
- **Cause:** A record for `@` points to non-Vercel IP (e.g., `64.x.x.x`, `216.x.x.x`, `192.x.x.x`)
- **Fix:** Update A record to Vercel's current recommended IP (check Vercel → Settings → Domains)

### Vercel shows "DNS verification failed"
- **Cause:** DNS records don't match what Vercel expects, or propagation hasn't completed
- **Fix:** 1) Delete all old `@`/`www` records 2) Add exact records above 3) Wait 30 min

### SSL certificate errors
- **Cause:** Hidden Proxy ON, or `www` pointing to non-Vercel server
- **Fix:** Hidden Proxy OFF on both records, CNAME correct

## Future Domain Additions
For any new domain/subdomain:
1. Add domain in Vercel → Settings → Domains
2. Vercel will show the exact DNS records needed
3. Apply those records in Namecheap Advanced DNS with Hidden Proxy OFF
4. Wait for Vercel SSL auto-issue (usually 1–5 minutes)
