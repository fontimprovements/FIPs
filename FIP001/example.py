"""FIP001: flatten, then sequential subtraction and intersection.

Odieresis = O plus two dotaccentcomb components. Each mark is a punch,
then a dot.

clippedO = O plus a later intersection window: keep only O ∩ window.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Sequence

BooleanOp = Literal["subtraction", "intersection"]


@dataclass
class Path:
    name: str
    boolean: BooleanOp | None = None
    closed: bool = True


@dataclass
class Component:
    reference: str


Shape = Path | Component


@dataclass
class Glyph:
    name: str
    shapes: list[Shape] = field(default_factory=list)


# Pairs that geometrically overlap in this toy walk.
OVERLAPS = {("O", "punch"), ("O", "window")}


def _base_name(name: str) -> str:
    return name.split(" minus ")[0].split(" ∩ ")[0]


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


def intersection(subject: list[Path], clip: Path) -> list[Path]:
    result: list[Path] = []
    for path in subject:
        if (_base_name(path.name), clip.name) in OVERLAPS:
            result.append(Path(f"{path.name} ∩ {clip.name}"))
    return result


def apply_boolean(paths: Sequence[Path]) -> list[Path]:
    acc: list[Path] = []
    pending: list[Path] = []
    for path in paths:
        if path.boolean == "subtraction":
            acc = difference(acc + pending, path)
            pending = []
            continue
        if path.boolean == "intersection":
            acc = intersection(acc + pending, path)
            pending = []
            continue
        pending.append(path)
    acc.extend(pending)
    return acc


def show(label: str, glyphs: dict[str, Glyph], name: str) -> None:
    glyph = glyphs[name]
    flat = flatten_shapes(glyphs, glyph.shapes)
    compiled = apply_boolean(flat)
    print(f"{label} flattened:", [
        f"{p.name} [{p.boolean}]" if p.boolean else p.name for p in flat
    ])
    print(f"{label} compiled: ", [p.name for p in compiled])


def main() -> None:
    glyphs = {
        "O": Glyph("O", [Path("O")]),
        "dot": Glyph("dot", [Path("dot")]),
        "dotaccentcomb": Glyph(
            "dotaccentcomb",
            [Path("punch", boolean="subtraction"), Component("dot")],
        ),
        "Odieresis": Glyph(
            "Odieresis",
            [
                Component("O"),
                Component("dotaccentcomb"),
                Component("dotaccentcomb"),
            ],
        ),
        "clippedO": Glyph(
            "clippedO",
            [Component("O"), Path("window", boolean="intersection")],
        ),
    }
    show("Odieresis", glyphs, "Odieresis")
    show("clippedO", glyphs, "clippedO")


if __name__ == "__main__":
    main()
