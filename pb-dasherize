#!/usr/bin/env ruby
# Dasherize the clipboard on OSX

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

clipboard {|c| c.gsub(/[\W_]/,"-").gsub(/-+/,"-").gsub(/^-+|-+$/,"") }
