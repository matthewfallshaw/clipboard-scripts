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
  `/usr/local/bin/growlnotify#{sticky ? " -s" : ""} -a Quicksilver -m #{message.shellescape}`
  message
end