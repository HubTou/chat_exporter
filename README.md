# chat_exporter / monitor / translator
**chat_exporter** is a [Luanti](https://www.luanti.org/) client-side mod:
* enabling the continuous export of chat or channel messages into Luanti's *debug.txt* file as it's not directly possible to copy/paste them from the game
* adding 2 local commands:
  * ".tr LANG MESSAGE" for requesting the translation of a MESSAGE in the LANG language,
  * ".lang LANG" to define the language in which you want your translations. It's initialized from your Luanti [locale](https://en.wikipedia.org/wiki/Locale_(computer_software)) confguration, saved to disk after each modification and reloaded automatically afterwards.
* These LANG parameters are mostly 2 letters code from the [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) standard, or in rare cases things like "zh-CN" for simplified chinese)

**chat_monitor** and **chat_translator_XXX** are Python command-line scripts (use one or the other) opening a secondary window:
  * the first one automatically extracts chat_exporter lines (prefixed with the "§" character) from the *debug.txt* file and lets you copy/paste them into your favourite translation tool. If you are a developer, it's also a stub you can adapt in order to use other translation API.
  * the second one adds automatic translation:
    * of messages received from other players (no need to translate yours!),
    * or messages you requested a translation for. On Windows operating systems, this translation is **automatically** copied into the clipboard for direct paste in Luanti's chat (it works only in this direction).
  * These translations are made in your default "locale" language or the one you selected with the ".lang" command, or the one saved from a previous session.

There was at least one server-side mod doing this kind of things, but the idea here was to be able to do it **on any server** and allow gamers from many countries to play together even with no common language!

## An example with chat_translator_deeptranslator
![An example with chat_translator_deeptranslator](https://github.com/HubTou/chat_exporter/blob/main/screenshots/example.png)

Here you will see:
* a first line telling you if the automatic clipboard loading works (Windows) or not (Unix)
* in this peculiar example, the languages available for translations (depends on the translation API used)
  * Here I use the the [deep-translator](https://github.com/nidhaloff/deep-translator) translation API, with the [Google Translate](https://github.com/nidhaloff/deep-translator) backend
* a reminder that you can exit this secondary window with the Control-C key combination
* a line indicating the player name and his saved or default target language which is written when the player's connect
* then the chat and channel messages in Luanti's format ("channel name <sender> message text") along with their translation or an error message
  * the translator can fail if you select an unvailable or non existing language code, as shown here with the "jp" (japan) code instead of "ja" (japanese)
  * or in case of network issues if you use an online translator (for example with filtering proxies or excessive requests)
  * etc.
* translation requests are displayed in the "translation" pseudo-channel.
* the second line indicating the player name and his new target language is caused by the usage of the ".lang it" command.

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
3. Copy the Python scripts from *tools* to your *luanti* directory, where the *debug.txt* file is located.
   1. If it's not already done, install [Python](https://www.python.org/downloads/) to run them
   2. And run the following command from a console (Terminal or PowerShell on Windows) to install or update their dependencies:
      ```Shell
      pip install -U clipboard colorama deep_translator
      ```

Note: If you haven't upgraded yet to luanti 5.10.0 or newer, your *luanti* directory will be called *minetest*...

## Possible future directions
Maybe adding a translation cache.

I could also provide Python packages for the chat_translation Python scripts in order to automatically handle their dependencies on third-parties packages.

Other developers are welcome to submit or tell me about alternative translators for inclusion in *tools* or reference on this page.

When I'll be done with my client-side mods development list, I'll probably group them in a "comfort" modpack.

Go to [Discussions](https://github.com/HubTou/chat_exporter/discussions) if you want to suggest other things...
