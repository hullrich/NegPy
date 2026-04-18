from dataclasses import dataclass


@dataclass
class ShortcutEntry:
    key: str
    description: str
    category: str


REGISTRY: dict[str, ShortcutEntry] = {
    # Navigation
    "prev_file": ShortcutEntry("←", "Previous file", "Navigation"),
    "next_file": ShortcutEntry("→", "Next file", "Navigation"),
    # Geometry
    "rotate_cw": ShortcutEntry("]", "Rotate 90° CW", "Geometry"),
    "rotate_ccw": ShortcutEntry("[", "Rotate 90° CCW", "Geometry"),
    "flip_h": ShortcutEntry("H", "Flip horizontal", "Geometry"),
    "flip_v": ShortcutEntry("V", "Flip vertical", "Geometry"),
    "offset_dec": ShortcutEntry("Z", "Crop offset −1", "Geometry"),
    "offset_inc": ShortcutEntry("X", "Crop offset +1", "Geometry"),
    # Tools
    "pick_wb": ShortcutEntry("Shift+W", "Toggle WB picker", "Tools"),
    "manual_crop": ShortcutEntry("Shift+C", "Toggle manual crop", "Tools"),
    "pick_dust": ShortcutEntry("Shift+D", "Toggle heal tool", "Tools"),
    # Exposure sliders
    "density_up": ShortcutEntry("Q", "Density +0.01", "Exposure"),
    "density_down": ShortcutEntry("A", "Density −0.01", "Exposure"),
    "grade_up": ShortcutEntry("W", "Grade +0.01", "Exposure"),
    "grade_down": ShortcutEntry("S", "Grade −0.01", "Exposure"),
    "magenta_up": ShortcutEntry("E", "Magenta +0.01", "Exposure"),
    "magenta_down": ShortcutEntry("D", "Magenta −0.01", "Exposure"),
    "yellow_up": ShortcutEntry("R", "Yellow +0.01", "Exposure"),
    "yellow_down": ShortcutEntry("F", "Yellow −0.01", "Exposure"),
    # View
    "fit_view": ShortcutEntry("0", "Fit to window", "View"),
    "zoom_100": ShortcutEntry("1", "Zoom 100%", "View"),
    "zoom_200": ShortcutEntry("2", "Zoom 200%", "View"),
    # Actions
    "export": ShortcutEntry("Ctrl+E", "Export", "Actions"),
    "copy": ShortcutEntry("Ctrl+C", "Copy settings", "Actions"),
    "paste": ShortcutEntry("Ctrl+V", "Paste settings", "Actions"),
    "undo": ShortcutEntry("Ctrl+Z", "Undo", "Actions"),
    "redo": ShortcutEntry("Ctrl+Y", "Redo", "Actions"),
    # Help
    "show_shortcuts": ShortcutEntry("?", "Show shortcuts", "Help"),
}


def tooltip_with_shortcut(text: str, action_id: str | None = None) -> str:
    """Return rich-text tooltip with an inline key chip if action_id is in REGISTRY."""
    if action_id is None or action_id not in REGISTRY:
        return text
    key = REGISTRY[action_id].key
    chip = f'<span style="color:#888;background:#1A1A1A;padding:1px 5px;border-radius:3px;margin-left:8px;font-size:10px;">{key}</span>'
    return f"{text}{chip}"
