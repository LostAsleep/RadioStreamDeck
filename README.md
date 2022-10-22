# RadioStreamDeck

*Requires Python Version >= 3.10 because I plan to use match case statements.*

* My try to use / adapt the Stream Deck for the daily needs of a radiologist.
* This has to work on a Windows 10 64bit machine without root access.
* The Stream Deck needs an usb driver to work properly. Windows needs the `hidapi.dll` DLL. 
   * You can find `hidapi.dll` on the [releases page of the libUSB GitHub project][hidapir].
   * The 32 bit version seems to work just fine on Windows 10 64bit

## Used/Useful packages
* The basis for this is - of course - the [Python Elgato Stream Deck Library][pesdl]
  * Which needs an image manipulation library, usually [the PIL fork pillow][gpil]
* For more functionality I will probably be using [pyperclip][gpyper] and maybe [pyautogui][gpyaut]
  * For now I will just send keystrokes and combination with this programm from the Stream Deck and use AutoHotKey for the rest of the functionality.

## Documentation
* [Readthedocs Python Elgato Stream Deck][rtdsd]
* [Using a Stream Deck for productivity - a software developers solution][jrsd] by [James Ridgway][jruk]


[pesdl]: https://github.com/abcminiuser/python-elgato-streamdeck
[gpil]: https://github.com/python-pillow/Pillow
[gpyper]: https://github.com/asweigart/pyperclip
[gpyaut]: https://github.com/asweigart/pyautogui
[rtdsd]: https://python-elgato-streamdeck.readthedocs.io/en/stable/
[jruk]: https://www.jamesridgway.co.uk
[jrsd]: https://www.jamesridgway.co.uk/using-a-stream-deck-for-productivity-a-software-developers-solution/
[devd]: https://github.com/jamesridgway/devdeck
[hidapir]: https://github.com/libusb/hidapi/releases
