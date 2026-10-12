"""
Native Desktop Qt Styling & Theme Engine
PETER CYBER SECURITY PROGRAM
"""

from app.core.config import CyberTheme


def get_application_stylesheet() -> str:
    """
    Returns the comprehensive native Qt widget stylesheet for the Obsidian Black Cyberpunk theme.
    Zero WebViews, zero HTML/CSS dependencies — 100% native Qt rendering.
    """
    return f"""
    /* Core Application Window */
    QMainWindow, QWidget#CentralWidget {{
        background-color: {CyberTheme.BG_OBSIDIAN};
        color: {CyberTheme.TEXT_MAIN};
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        font-size: 13px;
    }}

    /* Global Widget Defaults */
    QWidget {{
        color: {CyberTheme.TEXT_MAIN};
        background: transparent;
    }}

    /* Top Navigation Bar */
    QFrame#TopNavBar {{
        background-color: {CyberTheme.BG_SURFACE};
        border-bottom: 1px solid {CyberTheme.BORDER_MID};
        padding: 4px 12px;
    }}

    /* Nav Tab Buttons */
    QPushButton.NavTabButton {{
        background-color: transparent;
        color: {CyberTheme.TEXT_MUTED};
        border: none;
        border-bottom: 3px solid transparent;
        padding: 10px 18px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    QPushButton.NavTabButton:hover {{
        color: {CyberTheme.TEXT_MAIN};
        background-color: rgba(255, 255, 255, 0.03);
    }}

    QPushButton.NavTabButton[active="true"] {{
        color: #FFFFFF;
        border-bottom: 3px solid {CyberTheme.COLOR_SCANNER};
        background-color: rgba(0, 255, 102, 0.05);
    }}

    QPushButton.NavTabButton[active="true"][theme="blue"] {{
        border-bottom: 3px solid {CyberTheme.COLOR_THREAT_MAP};
        background-color: rgba(0, 210, 255, 0.05);
    }}

    QPushButton.NavTabButton[active="true"][theme="cyan"] {{
        border-bottom: 3px solid {CyberTheme.COLOR_AI_CYAN};
        background-color: rgba(6, 182, 212, 0.05);
    }}

    QPushButton.NavTabButton[active="true"][theme="gold"] {{
        border-bottom: 3px solid {CyberTheme.COLOR_VULN_GOLD};
        background-color: rgba(250, 204, 21, 0.05);
    }}

    /* Status Telemetry Pills */
    QFrame.TelemetryPill {{
        background-color: {CyberTheme.BG_CARD};
        border: 1px solid {CyberTheme.BORDER_DARK};
        border-radius: 6px;
        padding: 4px 10px;
    }}

    /* Elevated Cyber Cards */
    QFrame.CyberCard {{
        background-color: {CyberTheme.BG_CARD};
        border: 1px solid {CyberTheme.BORDER_DARK};
        border-radius: 8px;
    }}

    /* Buttons */
    QPushButton.CyberButton {{
        background-color: {CyberTheme.BG_CARD};
        color: {CyberTheme.TEXT_MAIN};
        border: 1px solid {CyberTheme.BORDER_MID};
        border-radius: 6px;
        padding: 7px 16px;
        font-weight: 600;
        font-size: 12px;
    }}

    QPushButton.CyberButton:hover {{
        background-color: {CyberTheme.BG_CARD_HOVER};
        border-color: {CyberTheme.BORDER_LIGHT};
    }}

    QPushButton.CyberButton:pressed {{
        background-color: #10131B;
    }}

    QPushButton.CyberButtonGreen {{
        background-color: rgba(0, 255, 102, 0.12);
        color: {CyberTheme.COLOR_SCANNER};
        border: 1px solid {CyberTheme.COLOR_SCANNER};
        border-radius: 6px;
        padding: 8px 18px;
        font-weight: 700;
    }}

    QPushButton.CyberButtonGreen:hover {{
        background-color: rgba(0, 255, 102, 0.22);
    }}

    QPushButton.CyberButtonBlue {{
        background-color: rgba(0, 210, 255, 0.12);
        color: {CyberTheme.COLOR_THREAT_MAP};
        border: 1px solid {CyberTheme.COLOR_THREAT_MAP};
        border-radius: 6px;
        padding: 8px 18px;
        font-weight: 700;
    }}

    QPushButton.CyberButtonBlue:hover {{
        background-color: rgba(0, 210, 255, 0.22);
    }}

    QPushButton.CyberButtonPurple {{
        background-color: rgba(168, 85, 247, 0.15);
        color: #D8B4FE;
        border: 1px solid {CyberTheme.COLOR_AI_PURPLE};
        border-radius: 6px;
        padding: 7px 14px;
        font-weight: 600;
    }}

    QPushButton.CyberButtonPurple:hover {{
        background-color: rgba(168, 85, 247, 0.28);
    }}

    /* Tables */
    QTableWidget {{
        background-color: {CyberTheme.BG_SURFACE};
        alternate-background-color: #0E1015;
        border: 1px solid {CyberTheme.BORDER_DARK};
        gridline-color: {CyberTheme.BORDER_DARK};
        color: {CyberTheme.TEXT_MAIN};
        border-radius: 6px;
        selection-background-color: rgba(0, 210, 255, 0.18);
        selection-color: #FFFFFF;
    }}

    QHeaderView::section {{
        background-color: {CyberTheme.BG_CARD};
        color: {CyberTheme.TEXT_MUTED};
        padding: 6px 10px;
        border: none;
        border-right: 1px solid {CyberTheme.BORDER_DARK};
        border-bottom: 1px solid {CyberTheme.BORDER_MID};
        font-weight: 600;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* Tree View / File Explorer */
    QTreeWidget {{
        background-color: {CyberTheme.BG_SURFACE};
        border: 1px solid {CyberTheme.BORDER_DARK};
        border-radius: 6px;
        color: {CyberTheme.TEXT_MAIN};
        padding: 4px;
    }}

    QTreeWidget::item {{
        padding: 6px 4px;
        border-radius: 4px;
    }}

    QTreeWidget::item:hover {{
        background-color: {CyberTheme.BG_CARD};
    }}

    QTreeWidget::item:selected {{
        background-color: rgba(250, 204, 21, 0.15);
        color: #FEF08A;
    }}

    /* Progress Bar */
    QProgressBar {{
        background-color: {CyberTheme.BG_INPUT};
        border: 1px solid {CyberTheme.BORDER_DARK};
        border-radius: 4px;
        text-align: center;
        color: {CyberTheme.TEXT_MAIN};
        font-weight: 600;
        font-size: 11px;
        min-height: 14px;
    }}

    QProgressBar::chunk {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #009933, stop:1 {CyberTheme.COLOR_SCANNER});
        border-radius: 3px;
    }}

    /* Text Inputs and Consoles */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {CyberTheme.BG_INPUT};
        border: 1px solid {CyberTheme.BORDER_MID};
        border-radius: 6px;
        color: {CyberTheme.TEXT_MAIN};
        padding: 8px 12px;
        selection-background-color: {CyberTheme.COLOR_AI_CYAN};
        selection-color: #000000;
    }}

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border: 1px solid {CyberTheme.COLOR_AI_CYAN};
    }}

    /* Code Box Monospace Container */
    QTextEdit.CodeBox {{
        background-color: {CyberTheme.BG_CODE};
        border: 1px solid {CyberTheme.BORDER_DARK};
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
        line-height: 1.4;
        color: #A5F3FC;
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        background: {CyberTheme.BG_OBSIDIAN};
        width: 8px;
        margin: 0px;
    }}

    QScrollBar::handle:vertical {{
        background: {CyberTheme.BORDER_MID};
        min-height: 24px;
        border-radius: 4px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {CyberTheme.BORDER_LIGHT};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background: {CyberTheme.BG_OBSIDIAN};
        height: 8px;
    }}

    QScrollBar::handle:horizontal {{
        background: {CyberTheme.BORDER_MID};
        min-width: 24px;
        border-radius: 4px;
    }}

    /* Tooltips */
    QToolTip {{
        background-color: {CyberTheme.BG_CARD};
        color: {CyberTheme.TEXT_MAIN};
        border: 1px solid {CyberTheme.BORDER_LIGHT};
        padding: 5px 8px;
        border-radius: 4px;
        font-size: 11px;
    }}
    """
