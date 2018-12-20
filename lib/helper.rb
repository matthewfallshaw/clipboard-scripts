$: << File.join(File.dirname(__FILE__))

Dir.chdir File.join(File.dirname(__FILE__), '..')
require 'bundler'
Bundler.setup

begin
  require File.basename($0).sub(/pb-/,'')
rescue LoadError
  nil
end

def clipboard(sticky = false, &block)
  c = IO.popen('pbpaste', 'r').read
  if block_given?
    notify(self.clipboard = yield(c), sticky)
  elsif sticky
    # this would be a weird usage, but this is probably the least surprising implementation
    notify(c, sticky)
  else
    c
  end
end
def clipboard=(val)
  IO.popen('pbcopy', 'w').print(val)
end

def notify(message, sticky = false)
  require 'shellwords'
  `#{notifyscript(sticky)} #{message.to_s.shellescape}`
  message
end

def notifyscript(sticky = false)
  script = `which growlnotify`.chomp
  return "#{script}#{sticky ? " -s" : ""} -a 'Quicksilver' -m" unless script.empty?

  script = %w[/usr/local/bin/growlnotify /opt/local/bin/growlnotify].find {|path| File.exist?(path) }
  return "#{script}#{sticky ? " -s" : ""} -a 'Quicksilver' -m" unless not script or script.empty?

  lib_dir = nil
  %w[../lib ./lib].each do |l|
    lib_dir = "#{File.dirname(File.expand_path(__FILE__))}/#{l}"
    break if File.directory?(lib_dir)
  end
  script = "#{lib_dir}/notify"
  return script
end
