#!/usr/bin/env ruby
# Un-Dasherize the clipboard on OSX

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

clipboard do |c|
  c.gsub(/[-_]/," ").gsub(/^ +| +$/,"")
end
