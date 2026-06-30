from PIL import Image
from pathlib import Path

CONFIGS = {
    "album_covers": {
        "source": Path("source-images/album-covers"),
        "output": Path("static/images/album-covers"),
        "sizes": [200, 400, 800],
        "formats": ["webp", "jpg"],
    },
    "carousel": {
        "source": Path("source-images/carousel"),
        "output": Path("static/images/carousel"),
        "sizes": [800, 1200, 1600],
        "formats": ["webp", "jpg"],
    },
    "thumbnails": {
        "source": Path("source-images/thumbnails"),
        "output": Path("static/images/thumbnails"),
        "sizes": [150, 300],
        "formats": ["webp"],
    },
}


def generate(config):
    config["output"].mkdir(parents=True, exist_ok=True)
    for src in config["source"].glob("*.[jp][pn]g"):
        img = Image.open(src).convert("RGB")
        for width in config["sizes"]:
            if width > img.width:
                continue  # don't upscale
            height = int(img.height * (width / img.width))
            resized = img.resize((width, height), Image.LANCZOS)
            for fmt in config["formats"]:
                out = config["output"] / f"{src.stem}-{width}w.{fmt}"
                resized.save(out, quality=82)
                print(f"  saved {out}")


if __name__ == "__main__":
    import sys

    targets = sys.argv[1:] or CONFIGS.keys()  # run all, or pass names as args
    for name in targets:
        print(f"\n→ {name}")
        generate(CONFIGS[name])
