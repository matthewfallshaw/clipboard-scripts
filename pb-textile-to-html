#!/usr/bin/env ruby

# Convert the contents of the clipboard to html (with
# RedCloth[http://whytheluckystiff.net/ruby/redcloth/], so assuming it's
# Textile or Markdown) and send it to STDOUT

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

%w[rubygems redcloth].each {|l| require l }
clipboard(true) do |c|
  RedCloth.new(c).to_html
end
