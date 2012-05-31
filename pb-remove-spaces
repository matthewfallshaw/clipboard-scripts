#!/usr/bin/env ruby
# Remove spaces from the clipboard on OSX

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

clipboard {|c| c.gsub(/ /,"") }
