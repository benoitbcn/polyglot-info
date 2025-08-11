#!/usr/bin/env python3
# coding: utf-8
import os, glob, datetime, random, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "articles"
TEMPLATE = ROOT / "scripts" / "article_template.html"
INDEX = ROOT / "index.html"

WORDS = [
    ("bridge","pont","puente"),
    ("forest","foret","bosque"),
    ("stream","ruisseau","arroyo"),
    ("light","lumiere","luz"),
    ("path","chemin","camino"),
    ("story","histoire","historia"),
    ("voice","voix","voz"),
    ("learn","apprendre","aprender"),
    ("read","lire","leer"),
    ("travel","voyager","viajar"),
]

LESSONS = [
    ("Using the present simple for routines.",
     "I read every day.", "Je lis tous les jours.", "Leo todos los dias."),
    ("Basic prepositions of place.",
     "The book is on the table.", "Le livre est sur la table.", "El libro esta sobre la mesa."),
    ("Talking about abilities with 'can'.",
     "I can swim.", "Je peux nager.", "Puedo nadar."),
    ("Expressing preferences with 'like'.",
     "I like quiet places.", "J'aime les endroits calmes.", "Me gustan los lugares tranquilos."),
]

def human_dt(dt: datetime.datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M UTC")

def new_article():
    ART.mkdir(exist_ok=True, parents=True)
    now = datetime.datetime.utcnow()
    slug = now.strftime("%Y-%m-%d_%H-%M-%S")
    title = f"Polyglot Daily - {now.strftime('%Y-%m-%d')}"
    desc = "Short multilingual micro-lesson."
    (w_en,w_fr,w_es) = random.choice(WORDS)
    (lesson, ex_en, ex_fr, ex_es) = random.choice(LESSONS)

    html = TEMPLATE.read_text(encoding="utf-8").format(
        title=title,
        desc=desc,
        date=human_dt(now),
        w_en=w_en, w_fr=w_fr, w_es=w_es,
        lesson=lesson,
        ex_en=ex_en, ex_fr=ex_fr, ex_es=ex_es
    )
    path = ART / f"{slug}.html"
    path.write_text(html, encoding="utf-8")
    return path.name, title, human_dt(now)

def rebuild_index():
    items = []
    for f in glob.glob(str(ART / "*.html")):
        name = os.path.basename(f)
        ts = name.replace(".html","")
        try:
            dt = datetime.datetime.strptime(ts, "%Y-%m-%d_%H-%M-%S")
        except Exception:
            dt = datetime.datetime.utcnow()
        items.append((dt, name))
    items.sort(reverse=True)
    article_items = "\n".join([
        f'<li><a href="/articles/{name}">{name.replace("_"," ").replace(".html","")}</a><span class="small">{dt.strftime("%Y-%m-%d %H:%M")} UTC</span></li>'
        for dt,name in items
    ]) or '<li><span>No articles yet.</span><span class="small">-</span></li>'

    INDEX.write_text(f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Polyglot Info - Language learning resources</title>
  <link rel="stylesheet" href="/style.css">
  <meta name="description" content="Educational resources in multiple languages: lessons, vocabulary, and cultural bites.">
</head>
<body>
  <header>
    <img src="/images/logo.svg" class="logo" alt="Polyglot logo">
    <h1>Polyglot Info</h1>
    <p class="small">Educational resources in multiple languages</p>
  </header>
  <div class="container">
    <div class="grid">
      <div class="card">
        <span class="badge">Daily</span>
        <h3>Fresh Lessons</h3>
        <p>Auto-generated micro-lessons and cultural snippets updated regularly.</p>
      </div>
      <div class="card">
        <span class="badge">Lightweight</span>
        <h3>Static & Fast</h3>
        <p>No backend. Built for reliability under strict networks.</p>
      </div>
      <div class="card">
        <span class="badge">Languages</span>
        <h3>EN . FR . ES</h3>
        <p>Short, readable content with simple examples.</p>
      </div>
    </div>

    <h2>Latest articles</h2>
    <ul class="article-list">
      {article_items}
    </ul>

    <h2>About</h2>
    <blockquote>
      This site publishes short educational notes automatically. It is a static site intended for demonstration and research purposes.
    </blockquote>
  </div>
  <footer>&copy; Polyglot Info</footer>
</body>
</html>
""", encoding="utf-8")

if __name__ == "__main__":
    new_article()
    rebuild_index()
