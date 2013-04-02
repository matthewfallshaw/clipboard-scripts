#!/usr/bin/env ruby
# Downcase the contents of the OSX clipboard

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

clipboard {|c| c.downcase }
