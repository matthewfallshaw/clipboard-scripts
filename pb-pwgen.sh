#!/usr/bin/env ruby
PWGEN_COMMAND = %w[/usr/local/bin/pwgen /opt/local/bin/pwgen].find {|p| File.file?(p) }
WORDLIST = `find ~/Documents/wordlist -iname '*common*'`.chomp

begin
  require_relative("../lib/helper")
rescue
  require File.join(File.dirname(__FILE__), "../lib/helper")
end

def random_word
  line = rand(`wc -l #{WORDLIST} | awk {'print $1'}`.chomp.to_i) + 1
  word = `head -n#{line} #{WORDLIST} | tail -1`.chomp
  word.downcase.gsub(/['!&.\/0-9]/,'').gsub(/[\s\W]/,'-').gsub(/\+/,'-')
end

def password
  "#{random_word}-#{random_word}-#{random_word}-#{random_word}"
end

# put a new pw in the clipboard without looking at it
system("#{PWGEN_COMMAND} -1 | tr -d \\n | pbcopy")

notify(<<STR, true)
New password in clipboard.

Other options:
#{`pwgen -N10 | sed 's/^/    /'`}
#{(1..12).collect {random_word}.join(" ")}
STR

# vi: filetype=ruby
