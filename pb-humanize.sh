#!/usr/bin/env ruby
# Sentence caserize the contents of the OSX clipboard
begin
  require_relative("../lib/helper")
  require_relative("../lib/humanize")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
  require File.join(File.dirname(__FILE__), "../lib/humanize")
end

clipboard {|c| HumanizingString.new(c).humanize }
