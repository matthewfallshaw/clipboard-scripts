#!/usr/bin/env ruby
# Gravatar URL from email address in the OSX clipboard

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

require 'digest/md5'
if clipboard.match(Regexp.new('^[\w!#$%&\'*+/=?^`{|}~\.-]+@(?:[\w-]+\.)+(?:[\w]{2,3}|museum)$'))
  clipboard do |c|
   "http://gravatar.com/avatar/#{Digest::MD5.hexdigest(c.strip.downcase)}"
  end
else
  notify("I need something that looks like an email address:\n#{clipboard}")
end
