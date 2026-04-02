with open('frontend/src/style.css', 'r') as f:
    css = f.read()

# Change .theme-menu positioning
old_css = """
.theme-menu {
  position: absolute;
  bottom: calc(100% + 8px);
  right: 0;"""

new_css = """
.theme-menu {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 0;"""

css = css.replace(old_css, new_css)

with open('frontend/src/style.css', 'w') as f:
    f.write(css)
