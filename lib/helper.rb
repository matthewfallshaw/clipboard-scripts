$: << File.join(File.dirname(__FILE__))
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
  `#{notifyscript}#{sticky ? " -s" : ""} -a 'Alfred 2' -m #{message.to_s.shellescape}`
  message
end

def notifyscript
  script = `which growlnotify`.chomp
  return script unless script.empty?
  %w[/usr/local/bin/growlnotify /opt/local/bin/growlnotify].find {|path| File.exist?(path) }
end
