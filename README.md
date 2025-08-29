Django Page Monitor

A simple Django-based application to monitor web pages for content changes.
The project was originally designed to track public job postings but can be adapted to any kind of website monitoring.

Features
- Store and manage a list of web pages to monitor.
- Extract only the relevant HTML parts (e.g. <body>), ignoring metadata or scripts that change frequently.
- Detect changes between consecutive fetches of the same page.
- Train the system to recognize and ignore recurring false positives (such as dynamic tokens or random IDs) by excluding specific line numbers.
- Mark pages as changed only if relevant differences are detected.

Management commands to:
- import_links: bulk import URLs from a text file (supports # comments).
- train_pages: run double checks to detect and store lines that should be ignored in the future.
- check_pages: compare current vs. previous HTML snapshots and report changes.
- clear_training: reset ignored lines for all monitored pages.

Use Case
This tool is useful if you need to:
- Track updates on job postings.
- Monitor documentation or institutional websites.
- Keep an eye on static content that may change irregularly.

Next Steps
Possible improvements:
- ... make it work! -_- Unfortunatelly most of the websites have systems to avoid being "scraped" by bots. I had no time to improve methods to get around this systems :(
- Use difflib to compare the document instead of doing it "by hand"
- Email or webhook notifications on detected changes.
- Allow to insert instruction "personalized" per link (html tags to select or avoid, other behaviours)
- Web UI for viewing differences and managing monitored pages.
