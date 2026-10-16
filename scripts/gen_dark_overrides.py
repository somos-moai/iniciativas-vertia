"""Genera frontend/src/dark-overrides.css a partir de hojas que no conocen el tema oscuro.

Para cada regla de workbench.css y flows.css:
- fondo claro neutro  -> var(--panel) (blanco) o var(--surface) (gris claro); rosado/verde suave -> var(--soft)
- texto oscuro o medio poco saturado -> var(--text) o var(--muted)
- borde claro -> var(--line)
Los colores saturados (marca, estados) se conservan. Ejecutar tras editar esas hojas:
    python scripts/gen_dark_overrides.py
"""
import colorsys
import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "frontend" / "src"
SOURCES = ["workbench.css", "flows.css"]
OUT = SRC / "dark-overrides.css"
PREFIX = ":root[data-theme=dark] .app"
HEX = re.compile(r"#([0-9a-fA-F]{3,8})\b")


def parse_hex(value):
    h = value.lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    h = h[:6]
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def classify(value):
    """Devuelve (luminosidad, saturación) HLS del primer color hexadecimal."""
    m = HEX.search(value)
    if not m:
        return None
    r, g, b = parse_hex(m.group(0))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return l, s


def background_token(value):
    c = classify(value)
    if not c:
        return None
    l, s = c
    if l < 0.9:
        return None  # fondo oscuro o de acento: se respeta
    if s > 0.45 and l < 0.985:
        return "var(--soft)"  # tintes suaves de marca o estado
    return "var(--panel)" if l >= 0.99 else "var(--surface)"


def lighten(value, target=0.78):
    """Mismo tono y saturación, con la luminosidad necesaria para leerse sobre fondo oscuro."""
    r, g, b = parse_hex(HEX.search(value).group(0))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(h, max(l, target), min(s, 0.75))
    return "#%02x%02x%02x" % tuple(round(x * 255) for x in (r, g, b))


def text_token(value):
    c = classify(value)
    if not c:
        return None
    l, s = c
    if s > 0.22:
        # Color de marca o de estado: conserva el tono y se aclara si quedaría oscuro.
        return lighten(value) if l < 0.7 else None
    if l <= 0.42:
        return "var(--text)"
    if l <= 0.8:
        return "var(--muted)"
    return None


def border_token(value):
    c = classify(value)
    if not c or c[0] < 0.75:
        return None
    return HEX.sub("var(--line)", value, count=1)


def scoped(selector):
    parts = []
    for sel in selector.split(","):
        sel = sel.strip()
        if not sel or sel.startswith("@") or sel in (":root", "body", "html"):
            continue
        parts.append(f"{PREFIX} {sel}")
    return ",".join(parts)


def rules(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    # Solo reglas de nivel superior o dentro de @media: se recorren bloques simples selector{decl}.
    for match in re.finditer(r"([^{}@]+)\{([^{}]*)\}", css):
        yield match.group(1).strip(), match.group(2)


def main():
    out = ["/* GENERADO por scripts/gen_dark_overrides.py: no editar a mano. */"]
    for name in SOURCES:
        out.append(f"/* {name} */")
        for selector, body in rules((SRC / name).read_text(encoding="utf-8")):
            decls = {}
            for decl in body.split(";"):
                if ":" not in decl:
                    continue
                prop, value = (x.strip() for x in decl.split(":", 1))
                if prop in ("background", "background-color"):
                    token = background_token(value)
                    if token:
                        decls["background"] = token
                elif prop == "color":
                    token = text_token(value)
                    if token:
                        decls["color"] = token
                elif prop in ("border", "border-color", "border-top", "border-bottom", "border-left", "border-right"):
                    token = border_token(value)
                    if token:
                        decls[prop] = token
            target = scoped(selector)
            if decls and target:
                out.append(target + "{" + ";".join(f"{k}:{v}" for k, v in decls.items()) + "}")
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{OUT.name}: {len(out) - 1 - len(SOURCES)} reglas")


if __name__ == "__main__":
    main()
