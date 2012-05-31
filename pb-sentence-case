#!/usr/bin/env ruby
# Sentence caserize the contents of the OSX clipboard

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

clipboard do |c|
  c.downcase.sub(/^./) {|x| x.upcase }
end
