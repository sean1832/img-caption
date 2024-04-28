# ZZ-Image-Caption
Image captioner CLI using BLIP and BLIP2 models

## Installation

### Requirements:
- Python 3.10 or higher

### Install using pip:
```bash
pip install zz-image-caption
```
### Install pytorch
You may need to install [pytorch](https://pytorch.org/) separately depending on your system to use **CUDA** (default to use **CPU** if not available).

## Usage

### Basic usage:
Print caption for an image to the console
```bash
caption image.jpg
```

### Advanced usage:
Rename images in a directory with their captions
```bash
caption images/ -o filename
```

Write metadata for images in a directory with their captions
```bash
caption images/ -o metadata
```

Print caption for an image to the console using the BLIP2 model
```bash
caption image.jpg --blip2
```



## Command Line Interface Options

The following table lists all the command-line arguments available with descriptions and additional details:

| Argument                  | Type    | Choices                        | Default | Description                                |
| ------------------------- | ------- | ------------------------------ | ------- | ------------------------------------------ |
| `-v`, `--version`         | flag    |                                |         | Display the version of the tool.           |
| `input`                   | string  |                                |         | Path to the input image file or directory. |
| `-o`, `--output`          | string  | text, json, metadata, filename |         | Specify the output type.                   |
| `-a`, `--append`          | string  |                                |         | Append string to caption output.           |
| `-t`, `--token`           | integer |                                | 32      | Max token length for captioning.           |
| `-b`, `--batch`           | integer |                                | 1       | Batch size for captioning.                 |
| `-p`, `--prompt`          | string  |                                |         | Prompt for captioning.                     |
| `--temp`, `--temperature` | float   |                                | 1.0     | Temperature for captioning.                |
| `--seed`                  | integer |                                |         | Seed for reproducibility.                  |
| `--large`                 | flag    |                                |         | Use the large model for captioning.        |
| `--cpu`                   | flag    |                                |         | Use CPU instead of GPU (not recommended).  |
| `--blip2`                 | flag    |                                |         | Use Blip2 model for captioning.            |
| `--verbose`               | flag    |                                |         | Print verbose output.                      |
| `--debug`                 | flag    |                                |         | Print debug output.                        |


### Help:
```bash
caption --help
```


