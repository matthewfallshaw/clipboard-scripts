#!/usr/bin/env ruby
# Add some lorem ipsum to the OSX clipboard

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

clipboard { `/usr/bin/env lorem 1` }
