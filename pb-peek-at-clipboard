#!/usr/bin/env ruby
# Growl notify the current content of the clipboard
begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

LONG_MESSAGE_LENGTH = 100

sticky = clipboard.size > LONG_MESSAGE_LENGTH
notify(clipboard, sticky)
