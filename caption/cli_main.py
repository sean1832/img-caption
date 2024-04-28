import glob
import pathlib
import time
import traceback

import pyexiv2
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from termcolor import colored

from caption import cli_parser, utils


def insert_metadata(image_path, caption, verbose=False):
    # insert caption into image metadata
    ext = pathlib.Path(image_path).suffix
    try:
        if ext == ".png":
            # PNG metadata
            img = Image.open(image_path)
            metadata = PngInfo()
            metadata.add_text("Description", caption)
            img.save(image_path, pnginfo=metadata)
        elif ext == ".jpeg" or ext == ".jpg":
            # EXIF metadata
            with pyexiv2.Image(image_path) as img:
                img.modify_exif({"Exif.Image.XPComment": caption})
        else:
            # unsupported
            print(
                colored(
                    f"Unsupported file type: {ext}, ({pathlib.Path(image_path).name}) ", "yellow"
                )
            )
            return False
        return True

    except Exception as e:
        print(colored(f"Error inserting metadata: {e}", "red"))
        if verbose:  # print traceback
            traceback.print_exc()


def caption_cmd(args):
    from caption.caption_engine import Blip

    file_input = pathlib.Path(args.input).absolute()
    if file_input.is_dir():
        file_input = file_input.joinpath("*.*")
    inputs = glob.glob(str(file_input))  # wildcard
    # filter out non-image files
    inputs = [i for i in inputs if utils.is_file_supported(i)]
    prompt = args.prompt
    if not prompt and args.blip2:
        print(colored("Prompt not specified. Using default prompt for Blip2.", "yellow"))
        print(colored("To specify a prompt, use the --prompt flag.", "yellow"))
        prompt = "a picture of"
    if not args.debug:
        blip = Blip(args.large, args.cpu, args.blip2)

        caption_dicts = blip.caption_image(
            inputs, args.token, args.seed, args.temp, args.batch, prompt
        )
    else:
        caption_dicts = [{"generated_text": "DEBUG"} for _ in inputs]

    try:
        # output
        if args.output == "json":
            import json

            output = {}
            for image, caption_dict in zip(inputs, caption_dicts):
                caption = caption_dict[0]["generated_text"]
                if args.append:
                    caption += f" {args.append}"

                # clean up caption
                caption = caption.replace("\n", " ").strip()

                output[image] = caption

            json_output = json.dumps(output, indent=4)
            # yyyymmdd-hhmmss
            now = time.strftime("%Y%m%d-%H%M%S")
            filename = str(pathlib.Path(inputs[0]).parent.stem + "_" + str(now) + ".json")

            if not args.debug:
                with open(filename, "w") as f:
                    f.write(json_output)

            print(f"\n{filename}: {json_output}")

        elif args.output == "text":
            for image, caption_dict in zip(inputs, caption_dicts):
                caption = caption_dict[0]["generated_text"]
                if args.append:
                    caption += f" {args.append}"

                # clean up caption
                caption = caption.replace("\n", " ").strip()

                # filename without extension
                filename = pathlib.Path(image).stem
                filepath = pathlib.Path(image).parent

                if not args.debug:
                    with open(f"{filepath}/{filename}.txt", "w") as f:
                        f.write(caption)

                print(f"\n{filename}.txt: {caption}")

        elif args.output == "metadata":
            for image, caption_dict in zip(inputs, caption_dicts):

                caption = caption_dict[0]["generated_text"]
                if args.append:
                    caption += f" {args.append}"

                # clean up caption
                caption = caption.replace("\n", " ").strip()

                if not args.debug:
                    success = insert_metadata(image, caption, args.verbose)

                if success:
                    print(f"{image}: {caption}")

        elif args.output == "filename":
            for image, caption_dict in zip(inputs, caption_dicts):
                caption = caption_dict[0]["generated_text"]
                if args.append:
                    caption += f" {args.append}"

                # clean up caption
                caption = caption.replace("\n", " ").strip()

                # old file extension
                ext = pathlib.Path(image).suffix
                new_name = f"{caption}" + ext
                new_path = pathlib.Path(image).parent.joinpath(new_name)

                if not args.debug:
                    pathlib.Path(image).rename(new_path)

                print(f"{pathlib.Path(image).name} -> {new_name}")

        elif args.output is None:
            for image, caption_dict in zip(inputs, caption_dicts):
                caption = caption_dict[0]["generated_text"]
                if args.append:
                    caption += f" {args.append}"

                # clean up caption
                caption = caption.replace("\n", " ").strip()

                print(f"{pathlib.Path(image).name}: {caption}")
        else:
            raise ValueError(f"Invalid output type: {args.output}. Use --help for more info.")
    except Exception as e:
        print(colored(f"Error generating output: {e}", "red"))
        if args.verbose:  # print traceback
            traceback.print_exc()
        return

    print(colored("Complete.", "green"))


def main():
    parser = cli_parser.get_parser()
    args = parser.parse_args()
    if args is None:
        parser.print_help()
        return
    caption_cmd(args)


if __name__ == "__main__":
    main()
