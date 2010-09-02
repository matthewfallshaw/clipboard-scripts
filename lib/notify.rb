def notify(message, sticky = false)
  require 'shellwords'
  `/usr/local/bin/growlnotify#{sticky ? " -s" : ""} -a Quicksilver -m #{message.shellescape}`
  message
end
