#!/usr/bin/env python3
#
# Original script by Philip Belemezov <philip@belemezov.net>
# Updated and enhanced for Python 3 compatibility by Nivek Schmidt
#
# This script is licensed under the public domain.
# Improvements include:
# - Python 3 compatibility (updated print statements, bytes handling, etc.)
# - Improved error handling and logging
# - Added progress bar for better user experience
#
# Contributions and further updates are welcome.
#
# Learn more about the improvements or connect with me:
# GitHub: https://github.com/nivekschmidt
#

import struct
import argparse
import os
import logging
from tqdm import tqdm  # For progress bar

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DEFAULT_DATFILE = "/System/Library/Keyboard Layouts/AppleKeyboardLayouts.bundle/Contents/Resources/AppleKeyboardLayouts-L.dat"
ICNS_HEADER = b'\x69\x63\x6e\x73'  # Header for .icns files


def buffer_to_hex(buffer):
    """Converts a byte buffer to a hex string representation."""
    return ' '.join(f'{byte:02x}' for byte in buffer)


def find_next_icon(data, start_pos):
    """Finds the next icon in the byte data buffer."""
    pos = start_pos
    while pos < len(data):
        if data[pos:pos + len(ICNS_HEADER)] == ICNS_HEADER:
            return pos + len(ICNS_HEADER)
        pos += 1
    return -1


def extract_icons(datfile, output_dir):
    """Extracts icons from the given DAT file."""
    if not os.path.exists(datfile):
        logging.error(f"DAT file {datfile} does not exist.")
        return False

    if not os.access(datfile, os.R_OK):
        logging.error(f"DAT file {datfile} cannot be read. Check permissions.")
        return False

    if os.path.getsize(datfile) == 0:
        logging.error(f"DAT file {datfile} is empty.")
        return False

    if not os.path.exists(output_dir):
        logging.info(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    with open(datfile, "rb") as f:
        data = f.read()

    if len(data) < len(ICNS_HEADER):
        logging.error("The file is too small to contain valid data.")
        return False

    pos = 0
    icon_count = 0

    logging.info("Starting icon extraction...")

    # Progress bar based on file size
    with tqdm(total=len(data), unit="B", unit_scale=True, desc="Extracting Icons") as progress:
        while pos < len(data):
            pos = find_next_icon(data, pos)
            if pos == -1:
                break

            # Extract icon data
            if pos + 4 > len(data):
                logging.warning("Incomplete icon data found. Skipping...")
                break

            try:
                icon_data_size = struct.unpack(">I", data[pos:pos + 4])[0]
            except struct.error:
                logging.warning("Invalid icon size detected. Skipping...")
                break

            if pos + icon_data_size > len(data):
                logging.warning("Icon data size exceeds file length. Skipping...")
                break

            icon_data = data[pos:pos + icon_data_size]

            # Save the icon file
            icon_filename = os.path.join(output_dir, f"icon_{icon_count:04d}.icns")
            try:
                with open(icon_filename, "wb") as icon_file:
                    icon_file.write(icon_data)
                logging.info(f"Extracted icon {icon_count + 1} to {icon_filename}")
            except IOError as e:
                logging.error(f"Failed to write icon file: {e}")
                return False

            icon_count += 1
            pos += icon_data_size
            progress.update(icon_data_size)

    logging.info(f"Extraction complete. {icon_count} icons extracted.")
    return True


def main():
    """Main function to parse arguments and initiate extraction."""
    parser = argparse.ArgumentParser(
        description="Extract icons from macOS keyboard layout DAT files."
    )
    parser.add_argument(
        "datfile",
        nargs="?",
        default=DEFAULT_DATFILE,
        help="Path to the DAT file (default: AppleKeyboardLayouts-L.dat)"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output directory for extracted icons"
    )
    parser.add_argument(
        "-l", "--loglevel",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set the logging level (default: INFO)"
    )

    args = parser.parse_args()

    # Set logging level dynamically
    logging.getLogger().setLevel(args.loglevel)

    if not extract_icons(args.datfile, args.output):
        logging.error("Extraction failed. Check the logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()