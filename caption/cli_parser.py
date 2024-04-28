import argparse

from caption import utils


# fmt: off
def get_parser():
    manifest = utils.get_manifest()

    parser = argparse.ArgumentParser(
        description=f"{manifest['description']} ({manifest['version']})"
    )
    parser.add_argument("-v", "--version", action="version", version=manifest["version"])
    parser.add_argument("input", type=str, help="Path to the input image file or directory")
    parser.add_argument("-o", "--output", type=str, choices=[
        "text", "json", "metadata", "filename"
    ], help="Specify the output type")
    parser.add_argument("-a", "--append", type=str, help="Append string to caption output")
    parser.add_argument("-t", "--token", type=int, help="Max token length for captioning", default=32)
    parser.add_argument("-b", "--batch", type=int, help="Batch size for captioning", default=1)
    parser.add_argument("-p", "--prompt", type=str, help="Prompt for captioning")
    parser.add_argument("--temp","--temperature", type=float, help="Temperature for captioning", default=1.0)
    parser.add_argument("--seed", type=int, help="Seed for reproducibility")
    parser.add_argument("--large", action="store_true", help="Use the large model")
    parser.add_argument("--cpu", action="store_true", help="Use CPU instead of GPU (not recommended)")
    parser.add_argument("--blip2", action="store_true", help="Use Blip2 model for captioning")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")
    parser.add_argument("--debug", action="store_true", help="Print debug output")

    return parser
# fmt: on
