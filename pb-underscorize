#!/usr/bin/env ruby
# Underscore the clipboard on OSX

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

clipboard do |c|
  c.gsub(/[\W_]/,"_").gsub(/-+/,"_").gsub(/^_+|_+$/,"")
end
