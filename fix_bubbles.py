import re

with open('frontend/src/style.css', 'r') as f:
    css = f.read()

# Add --bg-message to light mode
css = re.sub(
    r'(  --surface: hsl\(255, 15%, 99%\);)',
    r'\1\n  --bg-message: #ffffff;',
    css
)

# Add --bg-message to dark mode (in both places)
css = re.sub(
    r'(  --surface: hsl\(250, 12%, 15%\);)',
    r'\1\n  --bg-message: hsl(250, 12%, 20%);',
    css
)

# Update .ai-message background
css = css.replace(
    '  background: var(--surface);\n  border: 1px solid var(--border);',
    '  background: var(--bg-message);\n  border: 1px solid var(--border);'
)

with open('frontend/src/style.css', 'w') as f:
    f.write(css)
