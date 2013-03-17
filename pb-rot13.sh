#!/usr/bin/env ruby
# ROT13 the contents of the OSX clipboard

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

class String
  def rot13
    self.tr('a-zA-Z','n-za-mN-ZA-M')
  end
end

clipboard(true) {|c| c.rot13 }