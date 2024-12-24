# chat_exporter
A [Luanti](https://www.luanti.org/) client-side mod enabling the export of chat or channel messages in Luanti's debug.txt file as it's not directly possible to copy/paste them.

The messages are prefixed with the "§" character in order to ease their extraction and processing by an external tool.

The goal was to detect the language used and translate foreign ones with an AI tool such as [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate).

There are server-side mods doing that, but the idea was to be able to do it on any server...

## Installation
1. Manually download the [latest release](https://github.com/HubTou/chat_exporter/releases) of this mod (as client-side mods download is not handled yet through Luanti's User Interface)
2. Follow general instructions on [client-side mods installation](https://wiki.minetest.net/Installing_Client-Side_Mods):

   * Put the following line in *luanti/minetest.conf* to enable client-side mods (if not already done):
      ```
      enable_client_modding = true
      ```
      
   * Unpack the mod archive in *luanti/clientmods*
   * Rename the mod directory to *luanti/clientmods/chat_exporter*
   * Put the following line in *luanti/clientmods/mods.conf*:
      ```
      load_mod_chat_exporter = true
      ```
3. A stub tool is provided in *tools/chat_monitor.py*, that will automatically extract chat or channel messages from your *debug.txt* file, so you can copy/paste them in your favourite online translation web site.
   1. Install [Python](https://www.python.org/downloads/) to run it
   2. Copy the *mod_storage.py* script somewhere in your computer:
      1. Preferably somewhere in the PATH
      2. Or in your *luanti* directory, where the *debug.txt* file is located

Note: If you haven't upgraded yet to luanti 5.10.0 or newer, your *luanti* directory will be called *minetest*...

## Usage
If you use the provided *tools/chat_monitor.py* tool, use it from the *luanti* directory where the *debug.txt* file is located.
Else, open Luanti's debug.txt file in your favourite text editor and reload it periodically.

In both cases:
* copy the strings you want to translate in your clipboard,
* paste them into your favourite translation web site ([LibreTranslate](https://libretranslate.com/), [DeepL](https://www.deepl.com/), etc.)
* optionally craft an answer
* copy/paste it into Luanti's chat (it works in this direction)

## Possible future directions
I'll provide as separated Python packages more sophisticated tools to automatically send chat and channel messages to a translation API.

Apart from grouping all my client-side mods in a future "comfort" modpack,
I think I'll add a local command to request a translation for a response that you intend to make,
whose results will be provided back to you directly in the clipboard, so you can just paste them back into Luanti's chat.

Go to [Discussions](https://github.com/HubTou/chat_exporter/discussions) if you want to suggest other things...
