# chat_exporter
A [Luanti](https://www.luanti.org/) client-side mod enabling the export of chat messages in Luanti's debug.txt file as it's not directly possible to copy/paste them.

The messages are prefixed with the "§" character in order to ease their extraction and processing by a third-party tool.

The goal was to detect the language used and translate foreign ones with an AI tool such as [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate).

There are server-side mods doing that, but the idea was to be able to do it on any server...

## Usage
While there's no third-party tool processing these exported messages:
* open Luanti's debug.txt file in your favourite text editor,
* copy the strings you want to translate in your clipboard,
* paste them into your favourite translation web site ([LibreTranslate](https://libretranslate.com/), [DeepL](https://www.deepl.com/), etc.)
* optionally craft an answer
* copy/paste it into Luanti's chat (it works in this direction)

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

Note: If you haven't upgraded yet to luanti 5.10.0 or newer, your *luanti* directory will be called *minetest*...

## Caveats
Processing mod channel messages is untested. The ability to avoid echoing these messages is unsure.

## Possible future directions
Apart from grouping all my client-side mods in a future "comfort" modpack, I think this one will stay as is.

However, I'd like to provide another program to automatically extract and process these exported messages.

Go to [Discussions](https://github.com/HubTou/chat_exporter/discussions) if you want to suggest other things...
