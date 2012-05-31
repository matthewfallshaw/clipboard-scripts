#!/usr/bin/env ruby
# MD5 hasherize the contents of the OSX clipboard
begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

require 'digest/md5'
clipboard {|c| Digest::MD5.hexdigest(c) }
