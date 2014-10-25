#!/usr/bin/env ruby
# Quoted-printable unescape the contents of the OSX clipboard

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

class String
  def to_quoted_printable(*args)
    [self].pack("M").gsub(/\n/, "\r\n")
  end
  def from_quoted_printable
    self.gsub(/\r\n/, "\n").unpack("M").first
  end
end

clipboard do |c|
  c.from_quoted_printable
end
