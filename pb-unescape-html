#!/usr/bin/env ruby
# HTML encode the contents of the OSX clipboard
# WARNING: this pretty much doesn't work - I guess that pbcopy isn't cooperating
begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

%w[rubygems htmlentities].each {|l| require l }
clipboard do |c|
  HTMLEntities.decode_entities(c)
end
