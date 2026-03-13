import argparse
from . import load, save, halftone, halftone_svg, noisy_gradient, slice, gradient_stretch


def main():

    parser = argparse.ArgumentParser(
        prog="pyctorial",
        description="Generate patterns and transform images"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # -----------------------------
    # HALFTONE
    # -----------------------------
    halftone_parser = sub.add_parser(
        "halftone",
        help="Apply halftone filter to an image"
    )

    halftone_parser.add_argument("input")
    halftone_parser.add_argument("output")

    halftone_parser.add_argument(
        "--cell-size",
        type=int,
        default=12
    )

    halftone_parser.add_argument(
        "--max-dot-ratio",
        type=float,
        default=0.9
    )

    halftone_parser.add_argument(
        "--invert",
        action="store_true"
    )

    # -----------------------------
    # HALFTONE SVG
    # -----------------------------
    svg_parser = sub.add_parser(
        "halftone-svg",
        help="Generate SVG halftone"
    )

    svg_parser.add_argument("input")
    svg_parser.add_argument("output")

    svg_parser.add_argument("--cell-size", type=int, default=12)
    svg_parser.add_argument("--max-dot-ratio", type=float, default=0.9)
    svg_parser.add_argument("--invert", action="store_true")

    # -----------------------------
    # NOISY GRADIENT
    # -----------------------------
    gradient_parser = sub.add_parser(
        "noisy-gradient",
        help="Generate noisy gradient image"
    )

    gradient_parser.add_argument("output")

    gradient_parser.add_argument("--width", type=int, default=1200)
    gradient_parser.add_argument("--height", type=int, default=800)

    gradient_parser.add_argument(
        "--focal-points",
        type=int,
        default=6
    )

    gradient_parser.add_argument(
        "--blur",
        type=float,
        default=400
    )

    gradient_parser.add_argument(
        "--warp",
        type=float,
        default=0.2
    )

    # -----------------------------
    # SLICE
    # -----------------------------
    slice_parser = sub.add_parser(
        "slice",
        help="Slice an image vertically"
    )

    slice_parser.add_argument("input")
    slice_parser.add_argument("output_dir")

    slice_parser.add_argument(
        "--slices",
        type=int,
        default=10
    )

    # -----------------------------
    # GRADIENT STRETCH
    # -----------------------------
    stretch_parser = sub.add_parser(
        "gradient-stretch",
        help="Stretch image gradient from a column"
    )

    stretch_parser.add_argument("input")
    stretch_parser.add_argument("output")

    stretch_parser.add_argument(
        "--x-start",
        type=int,
        required=True
    )

    stretch_parser.add_argument(
        "--width-multiplier",
        type=float,
        default=2.0
    )

    stretch_parser.add_argument(
        "--base-spacing",
        type=int,
        default=1
    )

    stretch_parser.add_argument(
        "--growth-base",
        type=int,
        default=2
    )

    stretch_parser.add_argument(
        "--max-anchors",
        type=int,
        default=40
    )

    args = parser.parse_args()

    # ====================================
    # COMMAND EXECUTION
    # ====================================

    if args.command == "halftone":

        img = load(args.input)

        result = halftone(
            img,
            cell_size=args.cell_size,
            max_dot_ratio=args.max_dot_ratio,
            invert=args.invert
        )

        save(result, args.output)

    elif args.command == "halftone-svg":

        img = load(args.input)

        svg = halftone_svg(
            img,
            cell_size=args.cell_size,
            max_dot_ratio=args.max_dot_ratio,
            invert=args.invert
        )

        with open(args.output, "w") as f:
            f.write(svg)

    elif args.command == "noisy-gradient":

        img = noisy_gradient(
            width=args.width,
            height=args.height,
            num_focal_points=args.focal_points,
            blur_strength=args.blur,
            warp_strength=args.warp
        )

        save(img, args.output)

    elif args.command == "slice":

        img = load(args.input)

        slices = slice(img, args.slices)

        for i, s in enumerate(slices):

            path = f"{args.output_dir}/slice_{i:02d}.png"
            save(s, path)

    elif args.command == "gradient-stretch":

        img = load(args.input)

        result = gradient_stretch(
            img,
            x_start=args.x_start,
            width_multiplier=args.width_multiplier,
            base_spacing=args.base_spacing,
            growth_base=args.growth_base,
            max_anchors=args.max_anchors
        )

        save(result, args.output)


if __name__ == "__main__":
    main()