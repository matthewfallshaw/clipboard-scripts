#!/usr/bin/env ruby
# Word count the clipboard on OSX
begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

chars = clipboard.size
words = clipboard.scan(/[\w-]+/).size
notify("#{chars} characters\n(#{words} words)")
