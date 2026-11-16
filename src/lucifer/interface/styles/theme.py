
"""Central visual design system for LUCIFER."""

# Core colour palette
COLORS = {
    "background": "#0B0F14",
    "surface": "#111821",
    "surface_elevated": "#17212C",
    "surface_hover": "#1D2A37",
    "border": "#283644",

    "text_primary": "#E8EEF5",
    "text_secondary": "#A0AFBE",
    "text_muted": "#718294",

    "accent": "#72D5E8",
    "accent_hover": "#91E2F0",

    "success": "#72C6A0",
    "warning": "#E6B86A",
    "danger": "#E27B7B",
}

# Typography
FONTS = {
    "family": "Segoe UI",
    "size_small": 11,
    "size_normal": 13,
    "size_large": 18,
    "size_heading": 24,
}

# Consistent spacing scale (pixels)
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
}

# Application-wide Qt stylesheet
def build_stylesheet() -> str:
    """Generate the global application stylesheet."""

    return f"""
    QWidget {{
        background-color: {COLORS["background"]};
        color: {COLORS["text_primary"]};
        font-family: "{FONTS["family"]}";
        font-size: {FONTS["size_normal"]}px;
    }}

    QMainWindow {{
        background-color: {COLORS["background"]};
    }}

    QPushButton {{
        background-color: {COLORS["surface_elevated"]};
        color: {COLORS["text_primary"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 7px;
        padding: 8px 14px;
    }}

    QPushButton:hover {{
        background-color: {COLORS["surface_hover"]};
        border-color: {COLORS["accent"]};
    }}

    QPushButton:pressed {{
        background-color: {COLORS["surface"]};
    }}

    QLineEdit, QTextEdit {{
        background-color: {COLORS["surface"]};
        color: {COLORS["text_primary"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 8px;
        padding: 9px;
        selection-background-color: {COLORS["accent"]};
    }}

    QLineEdit:focus, QTextEdit:focus {{
        border-color: {COLORS["accent"]};
    }}

    QScrollBar:vertical {{
        background: transparent;
        width: 7px;
        margin: 0;
    }}

    QScrollBar::handle:vertical {{
        background: {COLORS["border"]};
        border-radius: 3px;
        min-height: 25px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {COLORS["text_muted"]};
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    """
