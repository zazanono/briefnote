import re

with open('frontend/src/style.css', 'r') as f:
    css = f.read()

# Replace hardcoded focus ring values with var(--focus-ring)
css = css.replace('oklch(0.65 0.06 280 / 0.15)', 'var(--focus-ring)')

# Add --focus-ring to :root and [data-theme="dark"]
root_target = "  --shadow-page:"
root_replacement = "  --focus-ring: oklch(0.65 0.06 280 / 0.15);\n  --shadow-page:"
css = css.replace(root_target, root_replacement, 1)

dark_target = "  --shadow-page:"
dark_replacement = "  --focus-ring: hsla(255, 60%, 72%, 0.25);\n  --shadow-page:"
css = css.replace(dark_target, dark_replacement, 2) # Handles [data-theme="dark"] and @media

# Also check input backgrounds to make sure they're correct
css = css.replace('.rename-input {\n  width: 100%;\n  border: 1px solid var(--border);', 
                  '.rename-input {\n  width: 100%;\n  border: 1px solid var(--border);\n  background: var(--surface);\n  color: var(--text-main);')

css = css.replace('.settings-input {\n  width: 100%;\n  border: 1px solid var(--border);', 
                  '.settings-input {\n  width: 100%;\n  border: 1px solid var(--border);\n  background: var(--surface);\n  color: var(--text-main);')

with open('frontend/src/style.css', 'w') as f:
    f.write(css)

