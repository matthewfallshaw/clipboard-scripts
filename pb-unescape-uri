#!/usr/bin/env ruby
# URI unescape the contents of the OSX clipboard
begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

require 'uri'
clipboard do |c|
  URI.unescape(c)
end
