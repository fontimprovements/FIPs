"""FIP001: flatten Odieresis, then sequential subtraction.

Odieresis = O + dieresiscomb. dieresiscomb holds two punches, then two
dot components.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class Path:
    name: str
    subtraction: bool = False
    closed: bool = True


@dataclass
class Component:
    reference: str


Shape = Path | Component


@dataclass
class Glyph:
    name: str
    shapes: list[Shape] = field(default_factory=list)


OVERLAPS = {
    ("O", "punch.left"),
    ("O", "punch.right"),
}


def _base_name(name: str) -> str:
    return name.split(" minus ")[0]


def flatten_shapes(glyphs: dict[str, Glyph], shapes: Sequence[Shape]) -> list[Path]:
    out: list[Path] = []
    for shape in shapes:
        if isinstance(shape, Path):
            out.append(shape)
            continue
        nested = glyphs.get(shape.reference)
        if nested is None:
            continue
        out.extend(flatten_shapes(glyphs, nested.shapes))
    return out


def difference(subject: list[Path], cutter: Path) -> list[Path]:
    result: list[Path] = []
    for path in subject:
        if (_base_name(path.name), cutter.name) in OVERLAPS:
            result.append(Path(f"{path.name} minus {cutter.name}"))
        else:
            result.append(path)
    return result


def apply_boolean(paths: Sequence[Path]) -> list[Path]:
    acc: list[Path] = []
    pending: list[Path] = []
    for path in paths:
        if path.subtraction:
            acc = difference(acc + pending, path)
            pending = []
            continue
        pending.append(path)
    acc.extend(pending)
    return acc


def main() -> None:
    glyphs = {
        "O": Glyph("O", [Path("O")]),
        "dot.left": Glyph("dot.left", [Path("dot.left")]),
        "dot.right": Glyph("dot.right", [Path("dot.right")]),
        "dieresiscomb": Glyph(
            "dieresiscomb",
            [
                Path("punch.left", subtraction=True),
                Path("punch.right", subtraction=True),
                Component("dot.left"),
                Component("dot.right"),
            ],
        ),
        "Odieresis": Glyph(
            "Odieresis",
            [Component("O"), Component("dieresiscomb")],
        ),
    }
    glyph = glyphs["Odieresis"]
    flat = flatten_shapes(glyphs, glyph.shapes)
    compiled = apply_boolean(flat)
    print("flattened:", [f"{p.name}{' [cut]' if p.subtraction else ''}" for p in flat])
    print("compiled: ", [p.name for p in compiled])


if __name__ == "__main__":
    main()
