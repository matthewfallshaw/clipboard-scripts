#!/usr/bin/env ruby

# Convert the contents of the clipboard to textile (with
# https://github.com/jystewart/html2textile and send it to STDOUT

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

%w[rubygems html2textile].each {|l| require l }
clipboard(true) do |c|
  parser = HTMLToTextileParser.new
  parser.feed(c)
  parser.to_textile
end
