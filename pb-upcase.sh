#!/usr/bin/env ruby
# Upcase the contents of the OSX clipboard
begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

clipboard do |c|
  c.upcase
end
