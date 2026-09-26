# Architecture & hard-won gotchas

Distilled from a real, live build + deployment on shared hosting. These are the
things that actually bit, so future builds don't relearn them the hard way.

## Stack & why

- **Shared hosting, no VPS**, when the institution's own IT can't administer a
  server. WordPress custom theme for editable content; custom PHP+MySQL for
  dynamic features; free/OSS only; MySQL/MariaDB + PHP + GD.
- **Keep dynamic-feature data in its own MySQL database, not `$wpdb`.** Admissions
  and portal data should survive a CMS change. Its own PDO helper, its own
  `CREATE TABLE IF NOT EXISTS`, credentials from a **gitignored** config file
  (ship `*.example.php`).
- **Zero-Composer convention:** hand-rolled OAuth via cURL, native `<details>`
  accordions, dependency-free lightbox. Reach for a plain solution first.

## Local dev

- **WordPress:** Local by WP Engine is a good local host. The theme lives in the
  repo; mirror it into the Local site's `wp-content/themes/<theme>` before
  browsing. Bump a `THEME_VERSION` constant when CSS/JS change to bust caches.
- **Running one-off PHP against WordPress from CLI** often needs the bundled PHP
  with `-d extension=mysqli -d extension=pdo_mysql` (and `gd` for image work),
  and a temporary `DB_HOST` swap from `localhost` to `127.0.0.1:<port>` (revert
  after). For the dynamic DB layer that reads its own config, a lighter
  `ABSPATH`-only bootstrap script avoids a full `wp-load.php`.
- **Testing philosophy that repeatedly paid off:** drive the *real* code path
  (real HTTP requests with a cookie jar, real multipart uploads via `curl -F`),
  not just function calls — `is_uploaded_file()` is false for faked `$_FILES`,
  `$_REQUEST` isn't auto-populated in CLI, and column/name mismatches only
  surface on a real request. Seed real data, check the negative/boundary cases,
  clean up every test row and script afterward.

## Deployment (shared hosting via SSH)

The safe, repeatable pattern:

1. Build the payload with `git archive` (only tracked files — **gitignored
   credential configs are structurally excluded**, so you can't leak local-dev
   secrets).
2. Upload as a **single tar** over SFTP (many small SFTP ops on locked-down hosts
   are unreliable / tripped by security layers). On MSYS/Git-Bash, set
   `MSYS_NO_PATHCONV=1` when passing remote Linux paths, and pass Windows-style
   local paths to `-F`/SFTP.
3. Extract to a temp dir and **overlay-copy** (`cp -r src/. dest/`) onto the live
   theme — **never `rm -rf` + fresh extract**, so a destination-only file (like a
   real credential config) can never be deleted.
4. **Verify the credential files' timestamps are unchanged** before and after.
   Never `cat`/print a file once it holds a live secret — prove it works with a
   real connection instead.
5. Run DB migrations via one combined `wp eval-file` (one SSH round-trip). On an
   already-created table, `CREATE TABLE IF NOT EXISTS` is a no-op — an ENUM/column
   change needs a live `ALTER TABLE`. `SHOW COLUMNS ... LIKE :col` fails under
   native prepares — use `DESCRIBE` + PHP membership instead. Don't bind the same
   named placeholder twice.

## Caching — there are FOUR layers, and each bit us

1. **PHP OpCache in the web SAPI** — a file-copy deploy writes new bytecode-source
   but doesn't drop the running pool's cache. `wp eval` runs under a *different*
   (CLI) SAPI, so resetting opcache there does nothing for real traffic. **Fix:**
   drop a tiny web-reachable `opcache_reset()` script, hit it over real HTTP,
   delete it immediately. Do this as a standard last step of every PHP deploy.
2. **LiteSpeed Cache plugin (page cache)** — a content edit to an already-cached
   public page doesn't self-invalidate; run `wp litespeed-purge all`. For
   session/token-gated pages that must never be cached and served to another
   visitor, call `do_action('litespeed_control_set_nocache', ...)` (the generic
   `nocache_headers()` alone isn't enough for this plugin; the action hook is).
   Verify by hitting a URL 3× and confirming it never shows `x-litespeed-cache:
   hit`.
3. **CDN edge cache** (e.g. Hostinger `hcdn`, 7-day default) — may serve stale
   HTML; check `x-hcdn-cache-status`. Origin-level `nocache_headers()` prevents
   caching real-time pages; otherwise it needs a manual control-panel purge.
4. **The visitor's own browser** — after a deploy, the asset-version bump +
   purge makes browsers refetch, but an individual user may still need one hard
   refresh (Ctrl+Shift+R). "A commit is not a deploy," and "it's not showing up"
   is usually caching, not a failed deploy — **check file-level ground truth on
   the server first** (`grep` the deployed file), and only then suspect caching.

**Anything time-sensitive on a cacheable page must load via an uncached request,
never be baked into the cached HTML** (the flash-popup pattern).

## Security notes that matter

- Uploads: validate + GD re-encode + random names + outside web root +
  `.htaccess` deny; **verify a direct URL 403s on the real host** (Apache/nginx
  ignore `.htaccess`; LiteSpeed honours it).
- Every `admin_post` write pairs an auth check with `check_admin_referer`.
  Re-authorise at the point of use (tokens re-validated every request; downloads
  re-check ownership → no IDOR). Treat out-of-scope IDs as nonexistent (404).
- Tokens for public no-login pages: a random token stored **hashed**, or an HMAC
  signature over the id — never a guessable id, never the raw token in a URL that
  lands in logs/history when it can be avoided.
- WordPress reserves `$_GET['error']` internally — don't name a query param
  `error`.
- Never substring-match a person's name for a bulk update ("Farha" ⊂ "Farhat").
- A disposable script that grants access without a password must be deleted in
  the very next action after its one use — especially on a public host.

## Lessons from the second phase (sub-sites, mobile API, directorates)

- **Authenticated API responses must never be page-cached.** On the live build
  LiteSpeed cached a signed-in mobile-API response and served it to another
  account. Mark every REST route that reads a bearer token no-cache (the
  LiteSpeed action hook, not just headers) and test with two accounts.
- **LiteSpeed strips the `Authorization` header** — read
  `REDIRECT_HTTP_AUTHORIZATION` as a fallback.
- **Subdomains on shared hosting:** the panel may create a *nested* docroot per
  subdomain. Point each at a tiny bootstrap that loads the one shared router
  instead of duplicating code; disable WordPress's canonical redirect for those
  hosts, force a 200, and allow `*.domain` as a safe redirect target so portal
  logins return to the sub-site. SSL for each subdomain is issued separately.
- **Session starts kill page caching.** Scope `session_start()` to the portal
  pages that need it, or every public page becomes uncacheable.
- **Host-header trust:** never gate a demo/admin helper on `$_SERVER['HTTP_HOST']`
  — it is client-controlled.
- **Site-wide 500s that come and go** may be one bad CDN edge node, not your
  code — compare responses across edges before debugging PHP.
- **Android signing key = the app's identity.** Lose it and every install must be
  uninstalled. Keep it outside the repo with a named custodian; bump
  `versionCode` every release.
- **Front-end portal passcodes** (in-charge, provost, bursar…) are stored hashed
  and rotated at handover. Don't write their defaults into documentation.

## Content-data caveat

Hand-edited CMS content (ACF fields, photo assignments) lives only in the
database of whichever environment you edited — there's no seam-free re-import
once posts are hand-edited. Apply a content correction to each environment
separately, and when editing a single ACF **repeater subfield that sits next to
an image subfield**, update that one meta key directly — re-saving the whole
`get_field()` array can corrupt the image subfields.

## Bilingual / RTL

Scope `dir="rtl" lang="xx"` to the specific content, not the whole page. Keep
mixed-script lines aligned. Use a font that renders the second script cleanly.
