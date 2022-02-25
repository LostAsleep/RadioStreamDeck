# RadioStreamDeck

*Requires Python Version >= 3.10 because I plan to use match case statements.*

* My try to use / adapt the Stream Deck for the daily needs of a radiologist.
* This has to work on a Windows 10 64bit machine without root access.
* The Stream Deck needs an usb driver to work properly. Windows needs the `hidapi.dll` DLL. 
   * You can find `hidapi.dll` on the [releases page of the libUSB GitHub project][hidapir].
   * The 32 bit version seems to work just fine on Windows 10 64bit

## Used/Useful packages
* The basis for this is - of course - the [Python Elgato Stream Deck Library][pesdl]
  * Which nees an image manipulation library, usually [the PIL fork pillow][gpil]
* For more functionality I will probably be using [pyperclip][gpyper] and [pyautogui][gpyaut]

## Documentation
* [Readthedocs Python Elgato Stream Deck][rtdsd]
* [Using a Stream Deck for productivity - a software developers solution][jrsd] by [James Ridgway][jruk]

## Basic Concepts
*Taken from James Ridgway's article. This is for his devdeck implementation, but I think it's also true for the python-elgato-streamdeck library.*

* Each physical button is a **key**
* A **control** is used to perform an action when a given key is pressed. 
* A **control** represents the most basic element that can be displayed in a Stream Deck.
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
[devd]: https://github.com/jamesridgway/devdeck
[hidapir]: https://github.com/libusb/hidapi/releases
