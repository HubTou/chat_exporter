--[[
chat_exporter - Log the chat messages received
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
--]]

local mod_name = assert(core.get_current_modname())
local chat_messages_allowed = true

core.register_on_mods_loaded(function()
	--	Check restrictions on client-side mods usage
	local csm_restrictions = core.get_csm_restrictions()
	
	if csm_restrictions.load_client_mods then
		print(core.colorize("red", "Loading client-side mods is disabled by the server"))
	else
		if csm_restrictions.chat_messages then
			print(core.colorize("orange", "Client-side mod '" .. mod_name .. "' loaded but server restricts receiving chat messages"))
			chat_messages_allowed = false
		else
			print(core.colorize("palegreen", "Client-side mod '" .. mod_name .. "' loaded"))
		end
	end
end)

core.register_on_receiving_chat_message(function(message)
	-- Process chat messages
	if chat_messages_allowed then
		core.log("action", "§ " .. message)
	end
	return false -- resume normal processing
end)

core.register_on_modchannel_message(function(channel, sender, message)
	-- Process channel messages
	if chat_messages_allowed then
		core.log("action", "§" .. channel .. " <" .. sender .. "> " .. message)
	end
end)
