#!/usr/bin/env ruby

# Convert the contents of the clipboard to html (with
# BlueCloth[http://deveiate.org/projects/BlueCloth], so assuming it's Markdown)
# and send it to STDOUT

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

%w[rubygems bluecloth].each {|l| require l }
clipboard(true) do |c|
  BlueCloth.new(clipboard).to_html
end