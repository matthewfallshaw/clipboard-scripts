#!/usr/bin/env ruby -w

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

system(File.expand_path(File.join(File.dirname(__FILE__), "../lib/finder-path.bash")))
clipboard do |c|
  c.sub(/^.*Dropbox/, 'Dropbox:')
end
