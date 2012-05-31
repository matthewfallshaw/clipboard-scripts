#!/usr/bin/env ruby
# CGI escape the contents of the OSX clipboard

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

require 'cgi'
clipboard {|c| CGI.escape(c) }
