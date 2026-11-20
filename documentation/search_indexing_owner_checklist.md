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
   - This is the cleanest method. It imports your verified property, sitemap, and settings without requiring separate meta tags.
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

*Documentation Note:* According to official Google Search documentation, submitting a sitemap informs Google of canonical URLs you want crawled. While helpful for newly deployed sites, sitemap submission is an advisory discovery signal; Google does not guarantee that every URL listed in a sitemap will be crawled or indexed.

---

## 3. URL Inspection & Crawl Requests

1. In **Google Search Console**:
   - Paste `https://howlcipher.github.io/william_elias/` into the top search bar (**Inspect any URL in...**).
   - Click **Test Live URL** to confirm that Googlebot can fetch the page, render the DOM, and see the JSON-LD structured data.
   - If the URL is not indexed or was recently updated, click **Request Indexing**.
2. In **Bing Webmaster Tools**:
   - Go to **URL Inspection**.
   - Enter `https://howlcipher.github.io/william_elias/`.
   - Click **Inspect**.
   - Click **Request Indexing** (or **Submit URL**).

### Important Indexing Request Constraints (Official Google Documentation)
- **No Priority or Indexing Guarantee:** Requesting indexing places the URL into Google's general crawl queue. Google documentation explicitly states that requesting indexing does not guarantee immediate crawling or subsequent indexing.
- **Do Not Submit Repeated Requests:** If a URL has not changed, do not submit repetitive indexing requests. Google notes that submitting multiple requests for the same URL does not speed up processing or change queue priority. Search Console also enforces daily per-property request quotas.

---

## 4. Understanding Search Stages: Crawling, Indexing, Appearance & Ranking

According to Google Search Central documentation, search discovery is divided into four distinct stages:

1. **Crawling (Discovery & Fetching):**  
   Googlebot discovers URLs via sitemaps, internal links, or external links, and requests the content. Crawling is resource-managed; Google determines when and how frequently to crawl based on algorithmic crawl budgets and host response. Crawling a page is a prerequisite for indexing, not a guarantee that indexing will occur.

2. **Indexing (Parsing, Understanding & Storage):**  
   Google analyzes the rendered page text, semantic HTML, structured metadata, and canonical directives. If eligible, the page is stored in Google's search index. Google does not guarantee that every crawled page will be indexed. Pages may remain unindexed due to algorithmic evaluation of content novelty, search demand, or duplicate content filtering.

3. **Search Appearance (Rich Snippets & Features):**  
   How the indexed page is formatted in search results. Valid Schema.org structured data (`ProfilePage`, `Person`) provides Google with explicit entities to generate rich search snippets, subject to Google's display algorithms.

4. **Ranking (Query Serving):**  
   When a user submits a search query, Google evaluates hundreds of algorithmic signals (relevance, search intent, page quality, geographic signals) to rank eligible indexed pages. Having a valid, crawlable website does not guarantee high ranking for competitive or broad keywords.

### Search Console Status Explanations
- **Discovered - currently not indexed:** Google has detected the URL (e.g. from the sitemap or a link), but has not yet crawled it. No remedial action is needed; Google will crawl according to its schedule.
- **Crawled - currently not indexed:** Google crawled the page, but determined not to index it at this time. This does not necessarily imply technical errors; Google exercises discretion on which pages to index based on overall search index criteria.

### Authoritative Verification of Index Status
- **Authoritative Diagnostic:** Use Search Console's **URL Inspection tool** as the authoritative source of index state. If it states `"URL is on Google"`, the page is indexed. If it states `"URL is not on Google"`, review the specific reason provided.
- **Search Operator Queries (`site:`):** Using a query such as `site:howlcipher.github.io/william_elias/` in standard search provides a quick informal check, but Google documentation clarifies that `site:` search results are approximations and do not constitute an exhaustive or definitive diagnostic of index coverage.

---

## 5. Performance Monitoring & Query Analytics

Check back periodically (e.g. weekly) in Google Search Console:
1. **Impressions:** The number of times your portfolio link appeared in search results for any query.
2. **Clicks:** The number of times a searcher clicked on your link.
3. **Average Position:** Where your link ranked on average across all queries.
4. **Queries to Track:**
   - Branded: `"William Elias"`, `"William Elias howlcipher"`, `"Wyl Elias"`
   - Specialist: `"William Elias software engineer"`, `"William Elias developer productivity"`, `"William Elias internal tools"`
   - Project-specific: `"HowlPlane AI control plane"`, `"HowlProof software verification"`
