#!/usr/bin/env python3

import os
import sys
import threading

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

# Folder location of image assets.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


def render_key_image(deck, icon_filename, font_filename, label_text):
    """
    Generates a custom tile with run-time generated text and custom image via
    the PIL module.

    Resize the source image asset to best-fit the dimensions of a single key,
    leaving a margin at the bottom so that we can draw the key title afterwards.

    :param deck: A :class:`StreamDeck` instance.
    :param icon_filename: str
    :param font_filename: str
    :param label_text: str
    """
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 20, 0])

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 14)
    draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)


def get_key_style(deck, key, state):
    """
    Returns styling information for a key based on its position and state.

    :param deck: A :class:`StreamDeck` instance.
    :param key: int
    :param state: bool
    :return: list of :str:
    """
    # Last button in the example application is the exit button.
    exit_key_index = deck.key_count() - 1

    if key == exit_key_index:
        name = "exit"
        icon = "{}.png".format("Exit")
        font = "Roboto-Regular.ttf"
        label = "Bye" if state else "Exit"
    else:
        name = "emoji"
        icon = "Pressed.png" if state else "Released.png"
        font = "Roboto-Regular.ttf"
        label = "Pressed!" if state else f"Key {key}"

    return {
        "name": name,
        "icon": os.path.join(ASSETS_PATH, icon),
        "font": os.path.join(ASSETS_PATH, font),
        "label": label
    }


def update_key_image(deck, key, state):
    """
    Creates a new key image based on the key index, style and current key state
    and updates the image on the StreamDeck.

    :param deck: A :class:`StreamDeck` instance.
    :param key: int
    :param state: bool
    """
    # Determine what icon and label to use on the generated key.
    key_style = get_key_style(deck, key, state)

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        # Update requested key with the generated image.
        deck.set_key_image(key, image)


def key_change_callback(deck, key, state):
    """
    Prints key state change information, updates the key image and
    performs any associated actions when a key is pressed.

    :param deck: A :class:`StreamDeck` instance.
    :param key: int
    :param state: bool
    """
    print(f"Deck {deck.id()} Key {key} = {state}", flush=True)  # Print new key state

    update_key_image(deck, key, state)  # Update the key image based on the new key state.
    key_pressed = state  # Just because if think it's a bit easier to read.

    if key_pressed and get_key_style(deck, key, key_pressed)["name"] == "exit":
        # Use a scoped-with on the deck to ensure we're the only thread using it right now.
        with deck:
            deck.reset()  # Reset deck, clearing all button images.
            deck.close()  # Close deck handle, terminating internal worker threads.
    elif key_pressed:
        key_style = get_key_style(deck, key, key_pressed)
        pass  # No key functions as of right now


def get_stream_deck():
    """
    Uses the DeviceManager to detect all connected Stream Decks.

    Will return the first or only Stream Deck for usage.
    If no Stream Deck is found abort program.

    :return: One :class:`StreamDeck` instance.
    """
    all_streamdecks = DeviceManager().enumerate()
    number_of_streamdecks = len(all_streamdecks)
    print(f"Found {number_of_streamdecks} Stream Deck(s).")

    if number_of_streamdecks < 1:
        sys.exit("No Stream Decks found, aborting...")
    if number_of_streamdecks == 1:
        print("Using the detected Stream Deck.")
    elif number_of_streamdecks > 1:
        print(f"Using the first of the {number_of_streamdecks} found Stream Decks.")

    return all_streamdecks[0]


def main():
    """
    The main function. Initializes the stream deck and keys.
    """
    stream_deck = get_stream_deck()
    stream_deck.open()
    stream_deck.reset()  # Reset deck, clearing all button images.

    deck_type = stream_deck.deck_type()
    deck_serial_number = stream_deck.get_serial_number()
    print(f"Opened '{deck_type}' device (serial number: '{deck_serial_number}')")

    # Set initial screen brightness to 30%.
    stream_deck.set_brightness(30)

    # Set initial key images.
    for key in range(stream_deck.key_count()):
        update_key_image(stream_deck, key, False)

    # Register callback function for when a key state changes.
    stream_deck.set_key_callback(key_change_callback)

    # Wait until all application threads have terminated.
    # Here this is when all deck handles are closed. (Not sure if needed for only one deck)
    for t in threading.enumerate():
        try:
            t.join()
        except RuntimeError:
            pass


if __name__ == "__main__":
    main()
