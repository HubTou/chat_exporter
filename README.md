# chat_exporter / monitor / translator
**chat_exporter** is a [Luanti](https://www.luanti.org/) client-side mod:
* enabling the continuous export of chat or channel messages in Luanti's *debug.txt* file as it's not directly possible to copy/paste them from the game
* adding 2 local commands:
  * ".tr LANG MESSAGE" for requesting the translation of a MESSAGE in the LANG language,
  * ".lang LANG" to define the language in which you want your translations. It's initialized from your Luanti [locale](https://en.wikipedia.org/wiki/Locale_(computer_software)) confguration, saved to disk after each modification and reloaded automatically.
* These LANG parameters are 2 letters code from the [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) standard.

**chat_monitor** and **chat_translator_XXX** are Python command-line scripts (use one or the other) opening a secondary window:
  * the first one automatically extracts chat_exporter lines (prefixed with the "§" character) from the *debug.txt* file and lets you copy/paste them into your favourite translation tool. If you are a developer, it's also a stub you can adapt in order to use other translation API.
  * the second one adds automatic translation:
    * of messages received from other players (no need to translate yours!),
    * or messages you requested a translation for. On Windows operating systems, this translation is automatically copied in the clipboard for direct use in Luanti.
  * These translations are made in your default "locale" language or the one you selected with the ".lang" command, or the one saved from a previous session.

There were server-side mods doing this kind of things, but the idea here was to be able to do it on any server...

## An example with chat_translator_deeptranslator
![An example with chat_translator_deeptranslator](https://github.com/HubTou/chat_exporter/blob/main/screenshots/example.png)

Here you will see:
* a first line telling you if the automatic clipboard loading works (Windows) or not (Unix)
* in this peculiar example, the languages available for translations (depends on the translation API used)
* a reminder that you can exit this secondary window with the Control-C key combination
* a line indicating the player name and his default or saved target language
* then the chat and channel messages in Luanti's format (channel name, sender, message) along with their translation or an error message
  * the translator can fail if you select a non existing or not available language code
  * or in case of network issues if you use an online translator
  * etc.

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
