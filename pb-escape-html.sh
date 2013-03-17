#!/usr/bin/env ruby
# HTML decode the contents of the OSX clipboard
# WARNING: this pretty much doesn't work - I guess that pbcopy isn't cooperating

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

%w[rubygems htmlentities].each {|l| require l }
clipboard {|c| HTMLEntities.encode_entities(c) }