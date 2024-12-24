#!/usr/bin/env python3
""" chat_monitor - Monitor Luanti's debug.txt file for lines written by the chat_exporter client-side mod
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import re
import sys
import time

FILE_NAME = "debug.txt"
SLEEP_TIME = 1

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: chat_monitor - Monitor Luanti's debug.txt file for lines written by the chat_exporter client-side mod v1.0.0 (December 23, 2024) by Hubert Tournier $"

with open(FILE_NAME, "r", encoding="utf-8") as file:
    while True:
        line = file.readline()
        
        if line:
            line = line.strip()
            if line.startswith("§"):
                channel = ""
                sender = ""
                message = ""
                
                words = line.split()
                
                if len(words) < 3:
                    continue
                
                if len(words[0]) > 1:
                    channel = words[0][1:]

                if re.match("<[-0-9a-zA-Z_]*>$", words[1]):
                    sender = words[1][1:-1]
                else:
                    continue
                    
                message = " ".join(words[2:])
                
                print(f"channel='{channel}' sender='{sender}' message='{message}'")
        else:
            time.sleep(SLEEP_TIME)

sys.exit(0)