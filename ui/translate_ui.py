#!/usr/bin/env python3
"""
Translate the interface into other languages with ANY OpenAI-compatible chat API
(DeepSeek, Ollama, OpenAI …). Cheap models are fine.

  export API_BASE=https://api.deepseek.com/v1     # or http://localhost:11434/v1 (Ollama)
  export API_KEY=sk-...                           # Ollama: any non-empty value
  export MODEL=deepseek-chat                      # or deepseek-r1 / llama3.1 …

  python3 translate_ui.py --init          # build en.json once (no API call, no key needed)
  python3 translate_ui.py fr de tr        # some languages
  python3 translate_ui.py --all           # every language of the app (codes read from ../index.html)
  python3 translate_ui.py --check fr      # only validate an existing ui/fr.json

Options: --batch 100 (strings per request) · --force (overwrite) · --dry-run (no API: copies English)
Output:  ui/<code>.json  →  commit it; the app lists it under Settings → Interface language.
"""
import json, os, re, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPT = open(os.path.join(HERE, 'PROMPT.md'), encoding='utf-8').read().split('\n---\n', 1)[1].strip()

# ---------- the English source ----------
def build_en():
    """en.json = {"strings": {English text: English text}, "names": {...}}.
    A finished pack (ar.json) already holds every English text as a KEY,
    so en.json can be rebuilt from it without any API."""
    ex = os.path.join(HERE, 'ar.json')
    if not os.path.exists(ex):
        raise SystemExit('en.json is missing and there is no ar.json to build it from.')
    j = json.load(open(ex, encoding='utf-8'))
    s = {'app': 'arTrainer-ui', 'lang': 'en',
         'strings': {k: k for k in j.get('strings', {})},
         'names': {k: k for k in j.get('names', {})}}
    json.dump(s, open(os.path.join(HERE, 'en.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('en.json created: %d strings, %d names' % (len(s['strings']), len(s['names'])))
    return s

_SRC = None
def src():
    global _SRC
    if _SRC is None:
        p = os.path.join(HERE, 'en.json')
        if os.path.exists(p):
            _SRC = json.load(open(p, encoding='utf-8'))
        else:
            print('en.json not found — building it from ar.json')
            _SRC = build_en()
    return _SRC

def app_languages():
    html = open(os.path.join(HERE, '..', 'index.html'), encoding='utf-8').read()
    return {c: n for c, n, _ in re.findall(r"add\('([a-z]+)','([^']*)','([^']*)'", html)}

def marks(s): return sorted(re.findall(r'\{n\}|\{L\}', s))

def validate(s, out):
    """returns a list of problems (empty = fine)"""
    if not isinstance(out, dict): return ['not an object']
    bad = []
    for k, v in s.items():
        if k not in out: bad.append('missing: ' + k[:60]); continue
        if not isinstance(out[k], str) or not out[k].strip(): bad.append('empty: ' + k[:60]); continue
        if marks(k) != marks(out[k]): bad.append('placeholders differ: ' + k[:60])
    return bad

def call(messages):
    base, key, model = os.environ['API_BASE'].rstrip('/'), os.environ.get('API_KEY', ''), os.environ['MODEL']
    req = urllib.request.Request(base + '/chat/completions', method='POST',
        data=json.dumps({'model': model, 'messages': messages, 'temperature': 0.2}).encode(),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)['choices'][0]['message']['content']

def parse_json(txt):
    txt = re.sub(r'^```(?:json)?\s*|\s*```$', '', txt.strip())
    a, b = txt.find('{'), txt.rfind('}')
    return json.loads(txt[a:b + 1])

def translate_part(language, part, key, dry):
    """part = {'strings': {...}} or {'names': {...}}; returns the translated dict for `key`"""
    if dry: return dict(part[key])
    prompt = PROMPT.replace('{{LANGUAGE}}', language).replace('{{JSON}}', json.dumps(part, ensure_ascii=False, indent=1))
    msgs = [{'role': 'user', 'content': prompt}]
    for attempt in range(4):
        try:
            out = parse_json(call(msgs)).get(key)
            bad = validate(part[key], out) if key == 'strings' else ([] if isinstance(out, dict) and set(part[key]) <= set(out) else ['names missing'])
            if not bad: return {k: out[k] for k in part[key]}
            print('   retry (%s): %s' % (attempt + 1, '; '.join(bad[:3])))
            msgs = [msgs[0], {'role': 'assistant', 'content': json.dumps({key: out}, ensure_ascii=False)},
                    {'role': 'user', 'content': 'Fix these problems and answer with the full JSON again:\n- ' + '\n- '.join(bad[:15])}]
        except (ValueError, urllib.error.URLError, KeyError) as e:
            print('   retry (%s): %s' % (attempt + 1, e)); time.sleep(3)
    raise SystemExit('giving up on ' + language)

def run(code, name, batch, force, dry):
    path = os.path.join(HERE, code + '.json')
    if os.path.exists(path) and not force: print(code, 'exists (use --force)'); return
    print(code, name)
    S = src()
    items = list(S['strings'].items()); strings = {}
    for i in range(0, len(items), batch):
        strings.update(translate_part(name, {'strings': dict(items[i:i + batch])}, 'strings', dry))
    names = translate_part(name, {'names': S['names']}, 'names', dry)
    bad = validate(S['strings'], strings)
    if bad: raise SystemExit('invalid: ' + '; '.join(bad[:5]))
    json.dump({'app': 'arTrainer-ui', 'lang': code, 'strings': strings, 'names': names},
              open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('  →', code + '.json written')

if __name__ == '__main__':
    a = sys.argv[1:]; flag = lambda f: f in a
    if flag('--init'):
        p = os.path.join(HERE, 'en.json')
        if os.path.exists(p) and not flag('--force'):
            sys.exit('en.json already exists (use --force to rebuild it)')
        build_en(); sys.exit()
    batch = int(a[a.index('--batch') + 1]) if '--batch' in a else 100
    langs = app_languages()
    if flag('--check'):
        S = src()
        for c in [x for x in a if x in langs]:
            print(c, validate(S['strings'], json.load(open(os.path.join(HERE, c + '.json'), encoding='utf-8'))['strings']) or 'ok')
        sys.exit()
    codes = [c for c in langs if c != 'en'] if flag('--all') else [x for x in a if x in langs]
    if not codes: sys.exit(__doc__)
    for c in codes: run(c, langs[c], batch, flag('--force'), flag('--dry-run'))