--[[
chat_exporter - Log the chat messages received for translation
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
--]]

local mod_name = assert(core.get_current_modname())
local mod_storage = core.get_mod_storage()
local chat_messages_allowed = true
local logging_allowed = true
local action_log_level = false
local player_language = ""
local player_name = ""

function log(message)
	-- Log a message and send a return code depending on the method used
	if action_log_level then
		core.log("action", message)
		return false -- resume normal processing
	else
		print(message)
		return true -- interrupt normal processing (prevent echoing the message twice)
	end
end

function is_a_language_code(input)
  -- Test if the input is a possible ISO 639-1 language code (with Google Translate extensions such as "zh-CN")
  local function is_letter(character)
    return (character >= 'a' and character <= 'z') or (character >= 'A' and character <= 'Z')
  end

  for character in input:gmatch(".") do
    if not (is_letter(character) or character == "-") then
      return false
    end
  end

  return true
end

core.register_on_mods_loaded(function()
	--	Check restrictions on client-side mods usage
	local csm_restrictions = core.get_csm_restrictions()
	
	if csm_restrictions.load_client_mods then
		print(core.colorize("red", "Loading client-side mods is disabled by the server"))
	else
		if csm_restrictions.chat_messages then
			chat_messages_allowed = false
			print(core.colorize("orange", "Client-side mod '" .. mod_name .. "' loaded but server restricts receiving chat messages"))
		else
			-- Get the log level configuration
			local debug_log_level = core.settings:get("debug_log_level")
			if debug_log_level then
				if debug_log_level == "" then
					logging_allowed = false
					print(core.colorize("orange", "Client-side mod '" .. mod_name .. "' loaded but server restricts logging"))
				elseif debug_log_level == "action" or debug_log_level == "info" or debug_log_level == "verbose" or debug_log_level == "trace" then
					action_log_level = true
					print(core.colorize("palegreen", "Client-side mod '" .. mod_name .. "' loaded. Logging to debug.txt"))
				else
					print(core.colorize("palegreen", "Client-side mod '" .. mod_name .. "' loaded. Printing to debug.txt"))
				end
			else
				logging_allowed = false
				print(core.colorize("orange", "Client-side mod '" .. mod_name .. "' loaded but server restricts logging"))
			end
		end
	end
end)

-- Wait for core.localplayer initialization
for i=1,10 do
	core.after(i, function()
		if player_name == "" and core.localplayer then
			player_name = core.localplayer:get_name()

			player_language = mod_storage:get_string(player_name .. "_lang")
			if not player_language or player_language == "" then
				local gettext_locale = ""
				gettext_locale, player_language = core.get_language()
			end
			log("§<" .. player_language .. " <" .. player_name .. "> Player target language initialized")
		end
	end)
end

core.register_on_receiving_chat_message(function(message)
	-- Process chat messages
	if chat_messages_allowed and logging_allowed then
		message = core.strip_colors(message)
		return log("§ " .. message)
	end
	return false -- resume normal processing
end)

core.register_on_modchannel_message(function(channel, sender, message)
	-- Process channel messages
	if chat_messages_allowed and logging_allowed then
		message = core.strip_colors(message)
		log("§" .. channel .. " <" .. sender .. "> " .. message)
	end
end)

core.register_chatcommand("tr", {
	-- Chat command for requesting a translation
    params = ".tr LANG MESSAGE",
    description = "Request the translation of a message in the specified target language",
	func = function(param)
		param = string.trim(param)
		local words = string.split(param, " ")

		if #words < 2 or not is_a_language_code(words[1]) then
			print("ERROR: usage: .tr LANG MESSAGE (where LANG is an ISO 639-1 language code)")
			return false
		end

		if chat_messages_allowed and logging_allowed then
			-- The first parameter is supposed to be an ISO 639-1 language code
			-- See https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes
			-- The other ones form the message to translate
			message = string.gsub(param, words[1] .. " ", "", 1)
			log("§?" .. words[1] .. " <" .. player_name .. "> " .. message)
		end
		
		return true
	end
})

core.register_chatcommand("lang", {
	-- Chat command for defining the player's target language
    params = ".lang LANG",
    description = "Define player's target language",
	func = function(param)
		param = string.trim(param)
		local words = string.split(param, " ")

		if #words ~= 1 or not is_a_language_code(words[1]) then
			print("ERROR: usage: .lang LANG (where LANG is an ISO 639-1 language code)")
			return false
		end

		mod_storage:set_string(player_name .. "_lang", words[1])
		if chat_messages_allowed and logging_allowed then
			log("§=" .. words[1] .. " <" .. player_name .. "> Player target language redefined")
		end

		return true
	end
})
