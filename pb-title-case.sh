#!/usr/bin/env ruby
# Title caserize the contents of the OSX clipboard

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

clipboard do |c|
  output = ""
  c.each("\s") {|w| output << w.capitalize}
  output
end
