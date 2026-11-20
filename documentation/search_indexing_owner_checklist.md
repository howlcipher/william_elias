# William Elias — Search Engine Indexing & Webmaster Checklist

**Canonical Site URL:** `https://howlcipher.github.io/william_elias/`  
**Canonical Sitemap URL:** `https://howlcipher.github.io/william_elias/sitemap.xml`  
**Canonical Robots.txt:** `https://howlcipher.github.io/william_elias/robots.txt`  
**AI Crawl Reference:** `https://howlcipher.github.io/william_elias/llms.txt`  
**Structured Profile:** `https://howlcipher.github.io/william_elias/candidate-profile.json`

This guide walks William Elias through setting up, verifying ownership, and managing search discoverability across Google Search Console and Bing Webmaster Tools for his GitHub Pages portfolio.

---

## 1. Property Setup & Ownership Verification

Because the site is hosted on a sub-path (`github.io/william_elias/`), domain-level DNS verification (`TXT` record) is not possible on `github.io`. You must use **URL Prefix** verification.

### Google Search Console
1. Navigate to [Google Search Console](https://search.google.com/search-console).
2. Sign in with your preferred Google account.
3. In the property selector dropdown (top left), select **Add property**.
4. Choose **URL prefix** (the right-hand box) and enter:
   ```text
   https://howlcipher.github.io/william_elias/
   ```
5. Click **Continue**.
6. Select the **HTML tag** verification method. Google will give you a tag like:
   ```html
   <meta name="google-site-verification" content="abcdef1234567890_EXAMPLE_TOKEN">
   ```
7. Copy the token string inside `content="..."`.
8. Provide the token to the build pipeline via one of two options:
   - **Option A (Preferred - checked-in):** In `resume.json`, under `"seo"`, add:
     ```json
     "googleSiteVerification": "abcdef1234567890_EXAMPLE_TOKEN"
     ```
     Then regenerate artifacts: `python3 scripts/build_html.py` (or `python3 scripts/maintain.py`).
   - **Option B (Environment variable):** Set `GOOGLE_SITE_VERIFICATION="abcdef1234567890_EXAMPLE_TOKEN"` in your environment or GitHub Actions repository secrets.
9. Commit, push, and merge the change. Wait for GitHub Pages deployment to complete.
10. Return to Google Search Console and click **Verify**.

### Bing Webmaster Tools
1. Navigate to [Bing Webmaster Tools](https://www.bing.com/webmasters).
2. Sign in with your Microsoft or Google account.
3. Select **Import your sites from GSC (Google Search Console)**.
   - This is the fastest, cleanest method. It imports your verified property, sitemap, and settings without requiring separate meta tags.
4. Alternatively, if adding manually:
   - Enter `https://howlcipher.github.io/william_elias/` as the URL prefix.
   - Use the meta tag option or GSC OAuth delegation.

---

## 2. Sitemap Submission

Once ownership is verified:
1. In **Google Search Console**:
   - Go to **Indexing** > **Sitemaps** on the left menu.
   - Under **Add a new sitemap**, enter `sitemap.xml`.
   - Click **Submit**.
   - Verify that the status shows **Success** and type shows **Sitemap**.
2. In **Bing Webmaster Tools**:
   - Go to **Sitemaps** on the left menu.
   - Click **Submit sitemap**.
   - Enter `https://howlcipher.github.io/william_elias/sitemap.xml`.
   - Click **Submit**. Verify status is **Success**.

---

## 3. URL Inspection & Initial Crawl Request

Search engine crawlers will automatically discover the site via the submitted sitemap, but you can request priority processing:
1. In **Google Search Console**:
   - Paste `https://howlcipher.github.io/william_elias/` into the top search bar (**Inspect any URL in...**).
   - Click **Test Live URL** to confirm that Googlebot can fetch the page, render the DOM, and see the JSON-LD structured data.
   - Click **Request Indexing**.
2. In **Bing Webmaster Tools**:
   - Go to **URL Inspection**.
   - Enter `https://howlcipher.github.io/william_elias/`.
   - Click **Inspect**.
   - Click **Request Indexing** (or **Submit URL**).

---

## 4. Crawling vs. Actual Indexing

It is important to understand the technical distinction between crawling and indexing:
- **Crawled (Fetched):** The search engine bot has requested the URL, downloaded the HTML/CSS/JS, and stored it in its processing pipeline.
- **Indexed:** The search engine has parsed the page, evaluated its quality, verified that it is not duplicate or thin content, and inserted it into the searchable database so that it appears in query results.
- **Common Status Messages:**
  - *Discovered - currently not indexed:* Google has detected the URL via sitemap or links, but has not yet crawled it due to scheduler queue priority. No action needed; it will crawl automatically.
  - *Crawled - currently not indexed:* Google crawled the page but decided not to add it immediately. Because this portfolio features rich semantic markup, unique verified case studies, and zero duplicate pages, it reliably proceeds to indexed status once recrawled.

### Verifying Actual Indexation
In your browser, run direct search queries:
```text
site:howlcipher.github.io/william_elias/
```
If the homepage and résumé PDFs appear in the results, the site is officially indexed.

---

## 5. Performance Monitoring & Query Analytics

Check back weekly after initial setup:
1. **Impressions:** The number of times your portfolio link appeared in search results for any query.
2. **Clicks:** The number of times a searcher clicked on your link.
3. **Average Position:** Where your link ranked on average across all queries.
4. **Queries to Track:**
   - Branded: `"William Elias"`, `"William Elias howlcipher"`, `"Wyl Elias"`
   - Specialist: `"William Elias software engineer"`, `"William Elias developer productivity"`, `"William Elias internal tools"`
   - Technology-specific: `"HowlPlane AI control plane"`, `"HowlProof software verification"`
