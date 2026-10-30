# todo :
## testing :
+ واضف نظام مراجعة مثل Anki خاصة قوائم اعدادات deck options
+ واضف toggle في الاعدادات لهذا النظام في حال احب المستخدم عدم استخدامه واستخدام الوضع الحالي كما هو
+ sentence loop debugger


## planning : 
+ (settings intro/explanition)
+ grammar terms glossary 
+ known words test


## V2.6 : 
[pronunciation]
ملاحظات البلاغة واساليب البيان (لا تتبع كلمات وحروف معينة لكن تراكيب انواع الكلم)

## V2.7:
Tashkil --> settings  : place and color
tashkil (with the name : diacritics) goes instead to the run like the self and auto correction (+ add that to the intro too)

undo redo take time let the user be informed to wait

make the selected base or custom saved theme both copyable by the "copy my css" button and renamable

after changing a lot of the UI how will old translations work ?
and the same for the custom css after changing the classic and default


consider this prompt for custom css :
I use a small offline language-learning web app (a single HTML file). I want to completely restyle it by adding my own CSS. The app injects my CSS inside a `<style id="userCss">` tag at the very END of the `<head>`, after every built-in rule.

WHAT I WANT (edit this part): 
<e.g., "A sleek dark mode inspired by Linear and Spotify, with frosted glass, vibrant green accents, and pill-shaped buttons."> 
<e.g., "A crisp, minimalist light mode inspired by Notion and iOS, with warm off-white backgrounds, serif headings, and soft shadows.">

CRITICAL RULES FOR YOUR ANSWER
1. Output ONLY plain CSS in one code block. No JavaScript, no HTML, no @import.
2. Put `!important` on EVERY single declaration. The app’s built-in styles and themes use highly specific selectors (like `html[data-theme]:not([data-theme="classic"]) .btn`). Plain rules will lose.
3. ALWAYS override the CSS variables first (on `html { ... }`). Only use specific selectors for structural changes (shapes, borders, layout).
4. Mobile first (360–430px wide). Keep tap targets at least 44px. Never hide the Check, Continue, right, or wrong buttons.
5. RTL Support: Use logical properties (`margin-inline-start`, `padding-inline-end`, `inset-inline-*`). Never force `direction: ltr`.
6. Foreign text (`.fl`, `.rtl`, `.arf`) must NEVER have `line-height` below 1.5 (diacritics get clipped).

⚠️ CRITICAL BUG-FIX ZONES (DO NOT SKIP)
In previous attempts, these elements were forgotten, resulting in white-on-white text or invisible backgrounds. You MUST explicitly style them for dark mode or light mode:
- **Bottom Sheets (`.sheet`, `.overlay`):** Needs its own background, text color, input fields, and tab buttons. 
- **Dropdown Menu (`.dd`, `.ddrow`):** Needs background, text color, hover state, and checkbox styling.
- **Theme Picker (`.themecard`, `.tsw`):** Needs explicit background and text color so the swatches don't blend into the page.
- **Toasts (`.toast`):** Needs a highly contrasting background and text color.
- **Settings Rows (`.rowcb`, `.srow`) & Tabs (`.tabbtn`, `.alTab`):** Needs explicit text and border colors.

CSS VARIABLES TO OVERRIDE (Set these first on `html`)
 Colours: `--bg` (page) · `--bg2` / `--card` / `--card2` (panels) · `--ink` / `--ink2` / `--ink3` (text strong→faint) · `--line` / `--line2` (borders)
 Accents: `--accent` (main button) · `--accent-ink` (text on main button) · `--accent2` (secondary button) · `--accent-soft` (halo)
 Feedback: `--green` / `--green-t` (right) · `--red` / `--red-t` (wrong) · `--amber` (flags) · `--hl` / `--hl-line` (note highlights)
 Shape:   `--r` (corner radius) · `--bw` (border width) · `--upper` (uppercase) · `--btn-sh` / `--btn-sh-p` (button shadow normal/pressed) · `--press` (transform on press) · `--chip-sh` (word chip shadow)
 Type:    `--font` (body font stack) · `--hfont` (heading font stack) · `--topbg` (top bar background)

MAIN UI ELEMENTS
 Layout: `.topbar` (sticky top) · `.wrap` (home column) · `.exwrap` (lesson column) · `.footer` / `.footer-inner` (fixed bottom bar) · `.sheet` (bottom sheet)
 Home: `.hero` (h1 + p) · `.statgrid > .statcard` (b + span) · `.lvcard` (level card) · `.deck` (library row) · `.sectionhead`
 Buttons: `.btn` + modifiers `.btn-green` (primary) `.btn-ghost` `.btn-redg` (danger) `.btn-sm` · `.iconbtn` · `.flagbtn` (tool buttons)
 Lesson: `.qhead h2` (instruction) · `.answerzone` (answer box) · `.bank > .chip` (word bank) · `.choice` (multiple choice buttons; `.sel`, `.right`, `.wrong`) · `.typein` (text input) · `.compare` (feedback box)
 Text:   `.fl` (foreign text) · `.translit` (transliteration) · `.nt` (highlighted word) · `.ntstrip` (notes list under sentence)
 Forms:  `.field` (inputs/selects) · `.rowcb` / `.cb` (checkbox rows) · `.tchip` (tag chips) · `.tabbtn` (tabs)

Please give me the CSS now.


make the current prompt copy button --> make with AI 
and then there are the options to write what you want in a text field and then copy the full and ready prompt to just send it to AI
or the option of coping the prompt like it now works


order the setting into foldable tabs or like expand and collapse
in a way that makes it easier to understand them and keep count
