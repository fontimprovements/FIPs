"""FIP001 stacking: flatten components in place, then sequential subtraction.

`difference()` is a stand-in for NonZero path difference (subject minus
cutter). Cutters are omitted from the compiled path list.
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


# Pairs (subject, cutter) that overlap. A real engine uses geometry.
OVERLAPS = {
    ("o_bowl", "slash"),
    ("bowl", "cut_bowl"),
}


def tree_has_subtraction(glyphs: dict[str, Glyph], name: str, visiting: set[str]) -> bool:
    if name in visiting:
        return False
    glyph = glyphs.get(name)
    if glyph is None:
        return False
    visiting.add(name)
    for shape in glyph.shapes:
        if isinstance(shape, Path) and shape.subtraction:
            return True
        if isinstance(shape, Component) and tree_has_subtraction(
            glyphs, shape.reference, visiting
        ):
            return True
    return False


def flatten_shapes(glyphs: dict[str, Glyph], shapes: Sequence[Shape]) -> list[Path]:
    """Expand components in place so paths and components share one z-order."""
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
        if not path.closed:
            result.append(path)
            continue
        if (path.name, cutter.name) in OVERLAPS:
            result.append(Path(f"{path.name} minus {cutter.name}"))
        else:
            result.append(path)
    return result


def apply_boolean(paths: Sequence[Path]) -> list[Path]:
    acc: list[Path] = []
    pending: list[Path] = []
    for path in paths:
        if path.subtraction:
            if not path.closed:
                continue
            acc = difference(acc + pending, path)
            pending = []
            continue
        pending.append(path)
    acc.extend(pending)
    return acc


def compile_glyph(glyphs: dict[str, Glyph], name: str) -> list[Path]:
    glyph = glyphs[name]
    flat = flatten_shapes(glyphs, glyph.shapes)
    if not tree_has_subtraction(glyphs, name, set()):
        return flat
    return apply_boolean(flat)


def main() -> None:
    glyphs = {
        "o": Glyph("o", [Path("o_bowl")]),
        "oslash": Glyph(
            "oslash",
            [Component("o"), Path("slash", subtraction=True)],
        ),
        "oslashacute": Glyph(
            "oslashacute",
            [Component("oslash"), Path("acute")],
        ),
        "mixed": Glyph(
            "mixed",
            [
                Path("bowl"),
                Path("cut_bowl", subtraction=True),
                Path("dot_on_top"),
            ],
        ),
        "cutter_below_component": Glyph(
            "cutter_below_component",
            [Path("slash", subtraction=True), Component("o")],
        ),
    }

    for name in (
        "oslash",
        "oslashacute",
        "mixed",
        "cutter_below_component",
    ):
        flat = flatten_shapes(glyphs, glyphs[name].shapes)
        compiled = compile_glyph(glyphs, name)
        print(name)
        print(
            "  flattened:",
            [f"{p.name}{' [cut]' if p.subtraction else ''}" for p in flat],
        )
        print("  compiled: ", [p.name for p in compiled])
        print()


if __name__ == "__main__":
    main()
