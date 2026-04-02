import re

# 1. Update style.css
with open('frontend/src/style.css', 'r') as f:
    css = f.read()

dropdown_css = """
.theme-menu-container {
  position: relative;
}

.theme-menu {
  position: absolute;
  bottom: calc(100% + 8px);
  right: 0;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  padding: 4px;
  min-width: 160px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  z-index: 50;
}

.theme-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 8px 12px;
  border: none;
  background: transparent;
  color: var(--text-main);
  font-size: 13px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  text-align: left;
  transition: background 0.15s;
}

.theme-menu-item:hover {
  background: var(--surface-hover);
}

.theme-menu-item.active {
  background: var(--surface-active);
  font-weight: 500;
}

.theme-menu-item svg {
  color: var(--text-muted);
}
"""

if ".theme-menu-container" not in css:
    with open('frontend/src/style.css', 'a') as f:
        f.write(dropdown_css)

# 2. Update App.tsx
with open('frontend/src/App.tsx', 'r') as f:
    app = f.read()

# Replace Sidebar props
old_sidebar_props = """function Sidebar({
  docs,
  loading,
  currentId,
  theme,
  onSelect,
  onCreate,
  onDelete,
  onToggleTheme,
}: {
  docs: DocumentSummary[]
  loading: boolean
  currentId: string | null
  theme: 'light' | 'dark' | 'system'
  onSelect: (id: string) => void
  onCreate: () => void
  onDelete: (id: string) => void
  onToggleTheme: () => void
}) {
  const [docToDelete, setDocToDelete] = useState<DocumentSummary | null>(null)"""

new_sidebar_props = """function Sidebar({
  docs,
  loading,
  currentId,
  theme,
  onSelect,
  onCreate,
  onDelete,
  onChangeTheme,
}: {
  docs: DocumentSummary[]
  loading: boolean
  currentId: string | null
  theme: 'light' | 'dark' | 'system'
  onSelect: (id: string) => void
  onCreate: () => void
  onDelete: (id: string) => void
  onChangeTheme: (theme: 'light' | 'dark' | 'system') => void
}) {
  const [docToDelete, setDocToDelete] = useState<DocumentSummary | null>(null)
  const [themeMenuOpen, setThemeMenuOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)
  const [systemIsDark, setSystemIsDark] = useState(() => {
    if (typeof window === 'undefined') return false
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  })

  useEffect(() => {
    const media = window.matchMedia('(prefers-color-scheme: dark)')
    const listener = (e: MediaQueryListEvent) => setSystemIsDark(e.matches)
    if (media.addEventListener) media.addEventListener('change', listener)
    else media.addListener(listener)
    return () => {
      if (media.removeEventListener) media.removeEventListener('change', listener)
      else media.removeListener(listener)
    }
  }, [])

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setThemeMenuOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const effectiveIsDark = theme === 'dark' || (theme === 'system' && systemIsDark)"""

app = app.replace(old_sidebar_props, new_sidebar_props)

# Replace Sidebar footer
old_footer = """      <div className="sidebar-footer">
        <button className="theme-toggle" onClick={onToggleTheme} title={`Toggle Theme (Current: ${theme})`}>
          {theme === 'dark' ? (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
          ) : theme === 'light' ? (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
          ) : (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
          )}
        </button>
      </div>"""

new_footer = """      <div className="sidebar-footer">
        <div className="theme-menu-container" ref={menuRef}>
          <button className="theme-toggle" onClick={() => setThemeMenuOpen(!themeMenuOpen)} title="Theme settings">
            {effectiveIsDark ? (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
            ) : (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
            )}
          </button>
          {themeMenuOpen && (
            <div className="theme-menu">
              <button className={`theme-menu-item ${theme === 'light' ? 'active' : ''}`} onClick={() => { onChangeTheme('light'); setThemeMenuOpen(false); }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
                Light mode
              </button>
              <button className={`theme-menu-item ${theme === 'dark' ? 'active' : ''}`} onClick={() => { onChangeTheme('dark'); setThemeMenuOpen(false); }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
                Dark mode
              </button>
              <button className={`theme-menu-item ${theme === 'system' ? 'active' : ''}`} onClick={() => { onChangeTheme('system'); setThemeMenuOpen(false); }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                Current System
              </button>
            </div>
          )}
        </div>
      </div>"""

app = app.replace(old_footer, new_footer)

# Remove handleToggleTheme and fix usage
app = re.sub(r'  function handleToggleTheme\(\) {.*?  }\n\n', '', app, flags=re.DOTALL)
app = app.replace('onToggleTheme={handleToggleTheme}', 'onChangeTheme={setTheme}')

with open('frontend/src/App.tsx', 'w') as f:
    f.write(app)
