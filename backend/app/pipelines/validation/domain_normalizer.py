from typing import Optional, List
import re

DOMAIN_KEYWORDS = {
    "android-development": ["android", "kotlin", "android studio", "jetpack compose"],
    "app-development": ["flutter", "react native", "mobile app", "ios", "swift", "dart", "xamarin"],
    "frontend": ["react", "vue", "angular", "html", "css", "javascript", "typescript", "next.js", "frontend developer", "ui developer"],
    "backend": ["node.js", "django", "flask", "fastapi", "spring", "express", "php", "laravel", "backend", "api development", "rest api"],
    "full-stack": ["full stack", "fullstack", "mern", "mean", "lamp", "full-stack"],
    "data-science": ["data science", "pandas", "numpy", "tableau", "power bi", "data analyst", "sql analyst", "data analytics"],
    "ai-ml": ["machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "artificial intelligence", "ai/ml", "llm"],
    "ui-ux": ["ui/ux", "figma", "user experience", "user interface", "product design", "interaction design", "wireframe", "ux design"],
    "cloud-devops": ["aws", "gcp", "azure", "kubernetes", "docker", "devops", "ci/cd", "terraform", "linux admin", "cloud engineer"],
    "qa": ["qa", "quality assurance", "testing", "selenium", "cypress", "test automation", "manual testing", "qc"],
    "cybersecurity": ["cybersecurity", "security", "ethical hacking", "penetration testing", "soc analyst", "vapt", "kali linux", "infosec"],
    "software-development": ["software developer", "software engineer", "software development", "swe intern"],
    "web-development": ["web developer", "web development", "php developer", "wordpress", "web designer"],
}

def normalize_domain(title: str, tags: List[str], description: str) -> str:
    """
    Map internship title/tags/description to canonical domain_slug.
    Returns domain_slug string or 'software-development' as fallback.
    """
    search_text = f"{title} {' '.join(tags or [])} {description[:500]}".lower()
    
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in search_text:
                # Title match = higher weight
                if kw in title.lower():
                    score += 3
                else:
                    score += 1
        if score > 0:
            scores[domain] = score
    
    if not scores:
        return "software-development"
    
    return max(scores, key=scores.get)
