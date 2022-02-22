# RadioStreamDeck
* My try to use / adapt the Stream Deck for the daily needs of a radiologist.
* This has to work on a Windows 10 64 bit machine without root access.

## Used/Useful packages
* The basis for this is - of course - the [Python Elgato Stream Deck Library][pesdl]
  * Which nees an image manipulation library, usually [the PIL fork pillow][gpil]
* For more functionality I will probably be using [pyperclip][gpyper] and [pyautogui][gpyaut]

## Documentation
* [Readthedocs Python Elgato Stream Deck][rtdsd]
* [Using a Stream Deck for productivity - a software developers solution][jrsd] by [James Ridgway][jruk]

## Basic Concepts
*Taken from James Ridgway's article.*

* Each physical button is a **key**
* A **control** is used to perform an action when a given key is pressed. A **control** represents the most basic element that can be displayed in a Stream Deck.
* A **deck** is indented to deal with either of the following scenarios:
   * Needing to display more controls than the device has physical keys for, or,
   * Showing a subset of relevant controls


[pesdl]: https://github.com/abcminiuser/python-elgato-streamdeck
[gpil]: https://github.com/python-pillow/Pillow
[gpyper]: https://github.com/asweigart/pyperclip
[gpyaut]: https://github.com/asweigart/pyautogui
[rtdsd]: https://python-elgato-streamdeck.readthedocs.io/en/stable/
[jruk]: https://www.jamesridgway.co.uk
[jrsd]: https://www.jamesridgway.co.uk/using-a-stream-deck-for-productivity-a-software-developers-solution/
