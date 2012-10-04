#!/usr/bin/env ruby
# decode Google search links to get destination url

require 'uri'

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

if clipboard.match(Regexp.new(%q[^http://www.google.com(.au)?/url\?.+&url=(http%3A%2F%2F[^&]+)&]))
  clipboard { URI.decode($1) }
else
  notify("That doesn't look like a Google search URL.")
end
