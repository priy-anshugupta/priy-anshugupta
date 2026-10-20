"""Render profile artwork locally. No network access or API key required."""
from pathlib import Path
from profile_artwork import extra_assets, header, terminal

ROOT = Path(__file__).resolve().parents[1]


def main():
    assets = ROOT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    generated = extra_assets()
    for theme in ("dark", "light"):
        generated[f"header-{theme}.svg"] = header(theme)
        generated[f"activity-{theme}.svg"] = terminal(theme)
    for name, content in generated.items():
        (assets / name).write_text(content, encoding="utf-8")
    print("Generated header, contact/project cards and animated education terminal.")


if __name__ == "__main__":
    main()
