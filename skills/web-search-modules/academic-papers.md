# Academic Papers Module

> 从 web-search-agent.md 提取的学术论文搜索专用策略

**Family:** Literature
**Use when:** The answer lives in a paper, a preprint, or a citation trail — methods, algorithms, formal results, who published what and when.
**Do not use for:** Practitioner opinion, product comparisons, or "does this actually work in production" (`general-web`).
**Siblings:** `github-debug` — pair them when you need a paper and its reference implementation.

## 搜索源 (Academic Sources)
- **Google Scholar** (scholar.google.com) - comprehensive academic search engine. Query `site:scholar.google.com <title or author>`.
- **arXiv** (arxiv.org) - preprints in physics, math, CS, and related fields. Query `site:arxiv.org <title or terms>`, or fetch `https://arxiv.org/abs/<id>` directly once the ID is known.
- **Hugging Face Papers** (huggingface.co/papers) - daily/monthly trending ML/AI papers with community upvotes. Query `site:huggingface.co/papers <topic>`. See `sites/huggingface.md`.
- **bioRxiv** (biorxiv.org) - preprints in biology and life sciences. Query `site:biorxiv.org <title or terms>`.
- **ResearchGate** (researchgate.net) - academic social network with papers and author profiles. Query `site:researchgate.net <title or author>`.
- **Semantic Scholar** (semanticscholar.org) - AI-powered academic search. Query `site:semanticscholar.org <title or author>`.
- **ACM Digital Library** and **IEEE Xplore** - CS and engineering papers. Query `site:dl.acm.org <title>` and `site:ieeexplore.ieee.org <title>` respectively.

## 查询策略 (1.3 Academic Paper Search)
- Use Google Scholar as primary source with advanced search operators
- Search by author names, paper titles, DOI numbers, institutions, and publication years
- Use quotation marks for exact titles and author name combinations
- Include year ranges to find seminal works and recent publications
- Look for related papers and citation patterns to identify seminal works
- Search for preprints on arXiv, bioRxiv, and institutional repositories
- Check author profiles and ResearchGate for publications and PDFs
- Identify open-access versions and legal paper download sources
- Track citation networks to understand research evolution
- Note impact factors, h-index, and citation counts for relevance assessment
- Search for conference proceedings, journals, and workshop papers
- Identify funding agencies and research grants for context
