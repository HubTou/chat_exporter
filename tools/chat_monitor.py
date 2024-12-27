#!/usr/bin/env python3
""" chat_monitor - Monitor Luanti's debug.txt file for lines written by the chat_exporter client-side mod
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier

Lines processed:
================
-- Player language and name initialization:
§<language_code <player> Player target language initialized

-- Player language redefinition:
§=language_code <player> Player target language redefined

-- Chat message:
§ <player> message

-- Channel message:
§channel <player> message

-- Translation request in ISO 639-1 language_code:
-- if possible, translation should be copied in the clipboard
§?language_code <player> message
"""

import os
import re
import signal
import sys
import time

import clipboard
import colorama

FILE_NAME = "debug.txt"
SLEEP_TIME = 1

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: chat_monitor - Monitor Luanti's debug.txt file for lines written by the chat_exporter client-side mod v1.2.1 (December 28, 2024) by Hubert Tournier $"

####################################################################################################
def handle_interrupt_signals(handler_function):
    """ Processes interrupt signals """
    signal.signal(signal.SIGINT, handler_function)
    if os.name == "posix":
        signal.signal(signal.SIGPIPE, handler_function)

####################################################################################################
def interrupt_handler_function(signal_number, current_stack_frame):
    """ Default handler_function for handle_interrupt_signals() """
    print("\nInterrupted!\n", file=sys.stderr)
    sys.exit(0)

####################################################################################################
def get_record(line):
    """ Extract a chat_exporter record from a debug.txt line """
    line = re.sub(r"^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]: ACTION\[Main\]: ", "", line)
    if line.startswith("§"):
        channel = ""
        sender = ""
        message = ""
                
        words = line.split()
                
        if len(words) < 3:
            return None
                
        if len(words[0]) > 1:
            channel = words[0][1:]

        if re.match("<[-0-9a-zA-Z_]*>$", words[1]):
            sender = words[1][1:-1]
        else:
            return None
                    
        message = " ".join(words[2:])
        
        return {"channel": channel, "sender": sender, "message": message}

    return None

####################################################################################################
def print_record(record, target_language):
    """ Print a chat or channel message in Luanti's style """
    if record["channel"]:
        print(f'{colorama.Fore.MAGENTA}{record["channel"]}{colorama.Style.RESET_ALL} ', end="")
    print(f'<{colorama.Fore.YELLOW}{record["sender"]}{colorama.Style.RESET_ALL}> ', end="")
    if target_language:
        print(f'{colorama.Fore.CYAN}{record["message"]}{colorama.Style.RESET_ALL} ', end="")
        print(f'-({target_language})-> ', end="")
    else:
        print(f'{colorama.Fore.CYAN}{record["message"]}{colorama.Style.RESET_ALL}')

####################################################################################################
def translate_record(record, target_language):
    """ Stub function to call a translator """
    print_record(record, target_language)
    
    # Call your favourite translator software here
    try:
        translation = "translation"
        print(f'{colorama.Fore.GREEN}{translation}{colorama.Style.RESET_ALL}')
    except:
        print(f'{colorama.Fore.RED}Translator failure{colorama.Style.RESET_ALL}')
        return

    # If a translation was requested, try to put the result in the clipboard
    # Does not work on all operating systems!
    if record["channel"] == "translation":
        try:
            clipboard.copy(translation)
        except:
            pass

####################################################################################################
handle_interrupt_signals(interrupt_handler_function)
colorama.init()
try:
    clipboard.copy("test")
    print(f"{colorama.Fore.GREEN}This operating system supports automatically copying translated messages to the clipboard{colorama.Style.RESET_ALL}")
except:
    print(f"{colorama.Fore.RED}This operating system DOES NOT support automatically copying translated messages to the clipboard{colorama.Style.RESET_ALL}")
print(f"{colorama.Fore.YELLOW}Press Control-C to exit{colorama.Style.RESET_ALL}")
print()

with open(FILE_NAME, "r", encoding="utf-8") as file:
    # We first read all existing records (lines starting with §) noting the last session starting one (§<)
    records = []
    current_record = 0
    last_starting_record = 0
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line:
            record = get_record(line)
            if record is not None:    
                records.append(record)
                if record["channel"].startswith("<"):
                    last_starting_record = current_record
                current_record += 1

    player_name = "unknown"
    player_language = "en"

    # Then we process records from the last session starting one
    for i in range(last_starting_record, len(records)):
        if records[i]["channel"].startswith("<") or records[i]["channel"].startswith("="):
            player_name = records[i]["sender"]
            player_language = records[i]["channel"][1:]
            print(f"Target language for '{player_name}' is '{player_language}'")
        elif records[i]["channel"].startswith("?"):
            receiver_language = records[i]["channel"][1:]
            records[i]["channel"] = "translation"
            translate_record(records[i], receiver_language)
        elif records[i]["sender"] == player_name:
            print_record(records[i], "")
        else:
            translate_record(records[i], player_language)

    # Now we read new records
    while True:
        line = file.readline().strip()
        if line:
            record = get_record(line)
            if record is not None:    
                if record["channel"].startswith("<") or record["channel"].startswith("="):
                    player_name = record["sender"]
                    player_language = record["channel"][1:]
                    print(f"Target language for '{player_name}' is '{player_language}'")
                elif record["channel"].startswith("?"):
                    receiver_language = record["channel"][1:]
                    record["channel"] = "translation"
                    translate_record(record, receiver_language)
                elif record["sender"] == player_name:
                    print_record(record, "")
                else:
                    translate_record(record, player_language)
        else:
            time.sleep(SLEEP_TIME)

sys.exit(0)
