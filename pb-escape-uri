#!/usr/bin/env ruby
# URI escape the contents of the OSX clipboard

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

require 'uri'
clipboard {|c| URI.escape(c) }
