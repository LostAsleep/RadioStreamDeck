#!/usr/bin/env python3

import os
import sys
import threading
import pyautogui
import base64
import shutil

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from os.path import exists


# Folder location of image assets.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


DEFAULT_IMG = {
    "Pressed.png": "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",
    "Released.png": "iVBORw0KGgoAAAANSUhEUgAAASAAAAEgCAYAAAAUg66AAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QMXEAE1U71jdQAACxNJREFUeNrt3Xmw3WV9x/HPXQkJBhICFDAJyKadbkgMEcQMtljQUgViEIQSYghpLdLVVjtiqdaOtlRLoCxGTAQDgomhCAW12AYqAmMrihHKUqDSQBbIvtzlnP7xu4yZlDL+UfIc87xeM2fOzfmH7/y+N29unnPv/XW156cdgAK6XQJAgAABAhAgQIAABAgQIAABAgQIQIAAAQIQIECAAAQIECAAAQIECBAgAAECBAhAgAABAhAgQIAABAgQIAABAgQIQIAAAQIQIECAAAQIECBAgAAECBAgAAECBAhAgAABAhAgQIAAfnq9LsGu8elvJJ/6ZrLvmOYxYcwOH+/1v1/fZ8+kryfp7kq6u0eeX+bRtdPHXV2793VstZJWOxluJcPtHT7e+fVWMtRKtg8l2waTbTs9bx3c6fXB5G1HJlMP8bkqQLvjX5x28sKW5vHYatejE82fIUD+CQYIEIAAAQIEIECAAAEIECBAAAIECBCAAAECBCBAgAABCBAgQIAAAQgQIEAAAgQIEIAAAQIEu4Xxo5OTXu867GruC9ahupL09yZ79Cb9PSPPI3/+v1576UaGpefu7Ul6u3d4jPy5Z4fXerqTK5cna7eUv9Zj+pM7fjs56gCfdwK0G5swJpk0Lpk8vnmeOO4nd0QdP/onH+89clfU3fkup5fc3hnx6e1OlsxJjj3E52eR/2G156ftMrz6Wq3mFsski+5PZt3QGbMsPi85a4qdlOKvxK660K50kuTuR5M5iztjlstniI8AUY0VK5PTFyRDrfKzfPTk5KLpdiJAVOH5Dck7rkrWbys/y4XHJ5e+w04EiCpsGUhOvSZ5+sXys5z2S8mVM3fvA34BghHDreScRcmDz5Sf5ZiJyQ3nNd8CgABRgQ8tS776/fJzHDg2uXVuMrrfTgSIKlz/QPK33yo/x6jeJj4H72MnAkQVvvtMMvfGzphl4TnJmybbiQBRhVUbk9M+l2wbKj/Lx05JzjzGTgSIKgwOJzOvS/5rXflZ3nN0csnJdiJAVOMPlyb/8nj5OY6Z2PzTy3egCxCVWPidZP7y8nMc5B0vAaIuDz6dzPty+TlG9Sa3XugdLwGiGs9vaA6dt3fAofOic5Mpk+xEgKjCwFAy4/PJs+vLz/Jnb09mvtFOBIhq/N6S5N4ny89xys8nl77TPgSIaiz4dnLVveXnOGxC8iU/4yVA1OM7/5l84Obyc4zpT5ZdkIwbbScCRBVWrm9+sdjAcPlZFp6T/MJBdiJAVGH7YHLGgmTlhvKzfPikZMbRdiJAVOODX0nue6r8HL/++uTjv2EfAkQ1rrk3ufbb5ed43b7J4lkOnQWIavzrE8lFt5SfY3RfsmxuMn6MnQgQVXh2XfPNhoMdcDeLL5yT/KJDZwGiDi8dOj+3sfwsH/o13+ksQFSj3U4+cEty/9PlZznpqOSTp9qJAFGNq+5JPn9f+TkO3Te58XyHzgJENe55PLl4Sfk59uxLvjon2dehswBRhx+/2Bw6d8ItlK97X/LLr7UTAaIK2wabH7NYtan8LH/0tuS9fqG8AFGHdjuZd1Nn3MX0V49M/uo37USAqMYVy5NFD5SfY/K45Kbzk94eOxEgqvDPjyW/3ymHzhckE/ayEwGiCs+80NzLa7hdfpYFZydHT7QTAaIKWweaXyi/ugMOnf/gxOTsKXYiQFSh3U7m3pT824/Lz3LiEcmn3mUnAkQ1Pvut5IYHy88xaVzyZYfOAkQ9/unR5I+XlZ9jVG9z6Lzfa+xEgKjCU2uTMzvk0Pnas5I3OnQWIOqwZeTQee2W8rNcPD05d6qdCBBVaLeTOYuT7z1bfpbphyd/fZqdCBDVuOzu5Mbvlp9j4j7JzbOTPofOAuQS1OEbjyR/cmv5OfboTZZekOzv0BkBqsOTa5pD51YHHDpffWYyZZKdIEBV2Lw9efe1yYtby89y0VuTWdPsBAGqQrudzP5S8oOV5Wc54bDkstPtBAGqxqe/mdz87+XnOHjv5BaHzghQPe5ckXz4H8rP0d+TLJ2THDDWThCgKjy+OjlrYdIBZ8656sxk6iF2ggBVYdPIofO6Djh0/p0TktlvthMEqArtdjLr+uSHz5Wf5S2vSz7j0BkBqscnv54seaj8HAeNTW55f9LfaycIUBVufzj56NfKz9HfkyyZk/ycQ2cEqA7/sSp536LOOHS+cmYy7VA7QYCqsGFrc+i8flv5WeYdn8w5zk4QoCq0Wsl5NyQ/er78LMcdmvzdDDtBgKrxibuSZd8vP8eBY5OvOHRGgOpx2w+Sj91Rfo6+7ubQ+cC97QQBqsIjzzWHzp3gipnJmx06I0B1WL81effnko3by88y97hk7vF2ggBVodVKzv1i8uiq8rNMOyS53KEzAlSPS/8xue3h8nMc8Jrm0HmPPjtBgKqw7KHkL+4sP0dfd7Lk/cnB+9gJAlSFFSubf3p1gsvfkxx/mJ0gQFVYt6U5dN40UH6W2dOSCx06I0B1GG41b7c/trr8LFMnNz/n1dVlLwhQFS65PbljRfk59t+rOfcZ5dAZAarDku81v9+ntN7u5h2v146zEwSoCg//d3Le9Z0xy2fPSE443E4QoCq8sLk5dN7cAYfOs45tfq8zCFAFhlvJ2QuTJ9aUn2XKxOaOFg6dEaBKfOS25K5Hys+x317J0gscOiNA1Vh0f3Mn09J6upq7mE506IwA1eHeJ5K5N3bGLJ85I5l+hJ0gQFV4am1y+oJkYLj8LL81Nfndt9oJAlSFjduSU69JVm8qP8sxE5OrHTojQHV46R2vh1eWn2XCmGTpnGTPfntBgKrwp7cmX/th+Tl6upKbZyeTxtsJAlSF6+5L/ubuzpjlstOTE4+0EwSoCvc8nsy7qTNmOf/Y5IPT7QQBqsKTa5p3vAZb5WeZfnhy9XsdOiNAVVi7uXnHa83m8rMcsV9z6OxGgghQBTZsTU75+2TFc+VnGT86uX1eMn6MvSBAu70tA81XPg8+U36Wvu7mK58j9rcXBGi3NzCUnLEgWf5EZ8xz7Vl+zAIBqsLQcPONhnf+qDPm+cjbk1nT7IXO4hjyVdBqJXMWJ0se6ox5ZvxK8vF32ku73dzaes3mZM2mV34+903JhW9xzQToZ/CT/OIlyaIHOmOevu7kqP2TT9yVDLWar8yGWs1juPXyr3W64VYyODzyGPl4YOiVX9s+lKzbmgy3f7r/xslv8LksQD+D1m5OrljeOfMMtpK//Lq90JmcAQECBAgQgAABAgQgQIAAAQgQIEAAAgQIEIAAAQIEIECAAAEIECBAgAABCBAgQAACBAgQgAABuxH3Bft/tmdf8uenNM+j+1/5eVRf0tOd9HQl3S89dzWvvdJzV1e917fdTlrtHW5CuNNj6GVuWjg43Nx8cbCVrNuSrNqUPL+heV61ceQx8vHG7T6Hd6Wu9vy0XQZobB1oYjSqNzlgrOvhKyDYlV/B9ieTx7sOu4ozIECAAAECECBAgAAECBAgAAECBAhAgAABAhAgQIAABAgQIAABAgQIECAAAQIECECAAAECECBAgAAECBAgAAECBAhAgAABAhAgQIAABAgQIECAAAQIECAAAQIECECAAAECECBAgAAECBAgAAECBAhAgAABAgQIQIAAAQIQIECAAAQIECAAAQIECECAAAECECBAgAAECBAgAAECBAgQIAABAgQIQIAAAQIQIECAAAQIECAAAQIECECAAAECECBAgAABAhAgQIAABAgQIAABAgQIQIAAAQIQIECAAAQIECAAAQIECECAAAECBAhAgAABAniV/Q9j45p0m8v6TAAAAABJRU5ErkJggg==",
    "Exit.png": "iVBORw0KGgoAAAANSUhEUgAAAEgAAABIBAMAAACnw650AAAAD1BMVEVHcEwAAAB5FgPwNxAAAABSGnVQAAAAAnRSTlMAcsiY3SgAAAAJcEhZcwAADsQAAA7EAZUrDhsAAApzSURBVEgNAWgKl/UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARAAAAAAAAAAAAAAAAAAAAAAAAEQAAAAAAAAAAAAAAAAAAAAABRBAAAAAAAAAAAAAAAAAAAAAAAUQQAAAAAAAAAAAAAAAAAAAAFERBAAAAAAAAAAAAAAAAAAAAABREQQAAAAAAAAAAAAAAAAAAAURERBAAAAAAAAAAAAAAAAAAAAFEREQQAAAAAAAAAAAAAAAAABRERERBAAAAAAAAAAAAAAAAAAAUREREQQAAAAAAAAAAAAAAAAFERCJERBAAAAAAAAAAAAAAAAABREQiREQQAAAAAAAAAAAAAAAUREIzJERBAAAAAAAAAAAAAAAAFERCMyREQQAAAAAAAAAAAAABREQjMzJERBAAAAAAAAAAAAAAAUREIzMyREQQAAAAAAAAAAAAFERCMzMzJERBAAAAAAAAAAAAABREQjMzMyREQQAAAAAAAAAAAUREIzMzMzJERBAAAAAAAAAAAAFERCMzMzMyREQQAAAAAAAAABREQjMzMzMzJERBAAAAAAAAAAAUREIzMzMzMyREQQAAAAAAAAAUREIzMzMzMzJERBAAAAAAAAABREQjMzMzMzMkREEAAAAAAAAAAUREIzMzMzMzJERBAAAAAAAAFERCMzMzMzMyREQQAAAAAAAAAAAUREIzMzMzMzJERBAAAAAAAUREIzMzMzMzJERBAAAAAAAAAAAAAUREIzMzMzMzJERBAAAAABREQjMzMzMzMkREEAAAAAAAAAAAAAAUREIzMzMzMzJERBAAAAFERCMzMzMzMyREQQAAAAAAAAAAAAAAAUREIzMzMzMzJERBAAAUREIzMzMzMzJERBAAAAAAAAAAAAAAAAAUREIzMzMzMzJERBABREQjMzMzMzMkREEAAAAAAAAAAAAAAAAAAUREIzMzMzMzJERBFERCMzMzMzMyREQQAAAAAAAAAAAAAAAAAAAUREIzMzMzMzJEREREIzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzJEREQjMzMzMzMkREEAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzJERCMzMzMzMyREQQAAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzJEIzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzIjMzMzMzMkREEAAAAAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzMzMzMzMyREQQAAAAAAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzMzMzMkREEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzMzMyREQQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzMkREEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFERCMzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABREQjMzMzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFERCMzMzMzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAAAAAABREQjMzMzMzMzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAAAAAFERCMzMzMzMyIzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzJEIzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAABREQjMzMzMzMkREIzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAAFERCMzMzMzMyREREIzMzMzMzJERBAAAAAAAAAAAAAAAAAAAAAUREIzMzMzMzJEREREIzMzMzMzJERBAAAAAAAAAAAAAAAAAAABREQjMzMzMzMkREEUREIzMzMzMzJERBAAAAAAAAAAAAAAAAAAFERCMzMzMzMyREQQAUREIzMzMzMzJERBAAAAAAAAAAAAAAAAAUREIzMzMzMzJERBAAAUREIzMzMzMzJERBAAAAAAAAAAAAAAABREQjMzMzMzMkREEAAAAUREIzMzMzMzJERBAAAAAAAAAAAAAAFERCMzMzMzMyREQQAAAAAUREIzMzMzMzJERBAAAAAAAAAAAAAUREIzMzMzMzJERBAAAAAAAUREIzMzMzMzJERBAAAAAAAAAAABREQjMzMzMzMkREEAAAAAAAAUREIzMzMzMzJERBAAAAAAAAAAFERCMzMzMzMyREQQAAAAAAAAAUREIzMzMzMzJERBAAAAAAAAABREQjMzMzMzJERBAAAAAAAAAAAUREIzMzMzMyREQQAAAAAAAAABREQjMzMzMkREEAAAAAAAAAAAAUREIzMzMzJERBAAAAAAAAAAABREQjMzMyREQQAAAAAAAAAAAAAUREIzMzMkREEAAAAAAAAAAAABREQjMzJERBAAAAAAAAAAAAAAAUREIzMyREQQAAAAAAAAAAAAABREQjMkREEAAAAAAAAAAAAAAAAUREIzJERBAAAAAAAAAAAAAAABREQiREQQAAAAAAAAAAAAAAAAAUREIkREEAAAAAAAAAAAAAAAABRERERBAAAAAAAAAAAAAAAAAAAUREREQQAAAAAAAAAAAAAAAAABREREEAAAAAAAAAAAAAAAAAAAAURERBAAAAAAAAAAAAAAAAAAABREQQAAAAAAAAAAAAAAAAAAAAAUREEAAAAAAAAAAAAAAAAAAAABRBAAAAAAAAAAAAAAAAAAAAAAAUQQAAAAAAAAAAAAAAAAAAAAABEAAAAAAAAAAAAAAAAAAAAAAAARAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABLvs5D7feE8AAAAABJRU5ErkJggg==",
}


for fname, file_data in DEFAULT_IMG.items():
    image_path = f"{ASSETS_PATH}/{fname}"
    if exists(image_path):
        print(f"{fname} is there.")
    else:
        print(f"{fname} not found. Creating in Assets directory...")
        with open(image_path, "wb") as fh:
            fh.write(base64.urlsafe_b64decode(file_data))
        print("Done.")


if not exists(f"{ASSETS_PATH}/Roboto-Regular.ttf"):
    print("Trying to copy font to Assets dir...")
    font_dir = os.path.join(os.path.dirname(__file__), "Font")
    shutil.copyfile(f"{font_dir}/Roboto-Regular.ttf", f"{ASSETS_PATH}/Roboto-Regular.ttf")
    print("Done.")


# Key icons will be expected in the "./Assets" directory and
# should be named {key}_p.png or {key}_r.png, 
# with {key} corresponding to the key_number on the StreamDeck (e.g. 0 - 31).


KEY_COMBS = {
    0: ("f13", ("f13", "", "", "")),
    1: ("f14", ("f14", "", "", "")),
    2: ("f15", ("f15", "", "", "")),
    3: ("f16", ("f16", "", "", "")),
    4: ("f17", ("f17", "", "", "")),
    5: ("f18", ("f18", "", "", "")),
    6: ("f19", ("f19", "", "", "")),
    7: ("f20", ("f20", "", "", "")),
    8: ("s+f13", ("shift", "f13", "", "")),
    9: ("s+f14", ("shift", "f14", "", "")),
    10: ("s+f15", ("shift", "f15", "", "")),
    11: ("s+f16", ("shift", "f16", "", "")),
    12: ("s+f17", ("shift", "f17", "", "")),
    13: ("s+f18", ("shift", "f18", "", "")),
    14: ("s+f19", ("shift", "f19", "", "")),
    15: ("s+f20", ("shift", "f20", "", "")),
    16: ("a+s+f13", ("alt", "shift", "f13", "")),
    17: ("a+s+f14", ("alt", "shift", "f14", "")),
    18: ("a+s+f15", ("alt", "shift", "f15", "")),
    19: ("a+s+f16", ("alt", "shift", "f16", "")),
    20: ("a+s+f17", ("alt", "shift", "f17", "")),
    21: ("a+s+f18", ("alt", "shift", "f18", "")),
    22: ("a+s+f19", ("alt", "shift", "f19", "")),
    23: ("a+s+f20", ("alt", "shift", "f20", "")),
    24: ("c+a+s+f13", ("ctrl", "alt", "shift", "f13")),
    25: ("c+a+s+f14", ("ctrl", "alt", "shift", "f14")),
    26: ("c+a+s+f15", ("ctrl", "alt", "shift", "f15")),
    27: ("c+a+s+f16", ("ctrl", "alt", "shift", "f16")),
    28: ("c+a+s+f17", ("ctrl", "alt", "shift", "f17")),
    29: ("c+a+s+f18", ("ctrl", "alt", "shift", "f18")),
    30: ("c+a+s+f19", ("ctrl", "alt", "shift", "f19")),
    31: ("c+a+s+f20", ("ctrl", "alt", "shift", "f20")),
}


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
    draw.text(
        (image.width / 2, image.height - 5),
        text=label_text,
        font=font,
        anchor="ms",
        fill="white",
    )

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

    elif key in KEY_COMBS:
        name = KEY_COMBS[key][0]
        icon_pressed = "Pressed.png" if not exists(f"{ASSETS_PATH}/{key}_p.png") else f"{key}_p.png"
        icon_released = "Released.png" if not exists(f"{ASSETS_PATH}/{key}_r.png") else f"{key}_r.png"
        icon = icon_pressed if state else icon_released
        # icon = "Pressed.png" if state else "Released.png"
        font = "Roboto-Regular.ttf"
        label = "Pressed!" if state else KEY_COMBS[key][0]

    else:
        name = "emoji"
        icon = "Pressed.png" if state else "Released.png"
        font = "Roboto-Regular.ttf"
        label = "Pressed!" if state else f"Key {key}"

    return {
        "name": name,
        "icon": os.path.join(ASSETS_PATH, icon),
        "font": os.path.join(ASSETS_PATH, font),
        "label": label,
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
    image = render_key_image(
        deck, key_style["icon"], key_style["font"], key_style["label"]
    )

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

    # Update the key image based on the new key state.
    update_key_image(deck, key, state)
    key_pressed = state  # Just because if think it's a bit easier to read.

    if key_pressed and get_key_style(deck, key, key_pressed)["name"] == "exit":
        # Use a scoped-with on the deck to ensure we're the only thread using it right now.
        with deck:
            deck.reset()  # Reset deck, clearing all button images.
            deck.close()  # Close deck handle, terminating internal worker threads.

    # Only try to use the hotkey if it's actually defined.
    elif key_pressed and key in KEY_COMBS:
        # key_style = get_key_style(deck, key, key_pressed)  # Probably unnecessary
        # print(KEY_COMBS[key][1][0], KEY_COMBS[key][1][1], KEY_COMBS[key][1][2], KEY_COMBS[key][1][3])
        pyautogui.hotkey(
            KEY_COMBS[key][1][0],
            KEY_COMBS[key][1][1],
            KEY_COMBS[key][1][2],
            KEY_COMBS[key][1][3],
        )


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
