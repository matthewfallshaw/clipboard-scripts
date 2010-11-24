#!/usr/bin/env ruby

# secrets in ~/.dotfiles_secrets like
# filename:
#   "search_term": replace_term
#   "other_search_term": other_replace_term

%w[shellwords rubygems rake yaml pathname].each {|l| require l }

IGNORE_LIST = %w[install.rb Rakefile README.textile vendor lib bin]

def replace_file!(file)
  system %Q{rm -r "$PWD/bin/#{file}"} if File.exist?("$PWD/bin/#{file}")
  copy_file!(file)
end
 
def copy_file!(file)
  f = Pathname.new("#{ENV["PWD"]}/#{file}")
  puts "#{file}#{f.symlink? ? " (really #{f.realpath})" : ""}: copied"
  system %Q{cp -r "#{f.realpath}" "$PWD/bin/#{file}"}
  make_binfile_executable!(file)
end

def copy_and_replace_secrets!(file)
  system %[cp "$PWD/#{file}" "$PWD/bin/#{file}"]
  secrets[file].each do |search_term, replace_term|
    system %[ruby -pi -e 'gsub(/#{Shellwords.escape(search_term)}/, "#{Shellwords.escape(replace_term)}")' "$PWD/bin/#{file}"]
  end
  puts "#{file}: copied and updated with secrets"
  make_binfile_executable!(file)
end

def make_binfile_executable!(file)
  system %Q{chmod u+x "$PWD/bin/#{file}"}
end

def secrets
  @secrets ||= begin
                 path = File.join(ENV['HOME'], '.dotfiles_secrets')
                 if File.exist?(path)
                   YAML.load(open(path))
                 else
                   {}
                 end
               end
end

def replace!(file)
  original = File.join(File.dirname(__FILE__), "bin", file)

  if secrets[file] and not File.directory?(file)
    copy_and_replace_secrets!(file)
  elsif @replace_all
    replace_file!(file)
  elsif File.exist?(original)
    if File.directory?(file)
      puts "#{file}: skipped"
    else
      print "overwrite #{file}? [ynaq] "
      case $stdin.gets.chomp
      when 'a'
        @replace_all = true
        replace_file!(file)
      when 'y'
        replace_file!(file)
      when 'q'
        exit
      else
        puts "#{file}: skipped"
      end
    end
  else
    copy_file!(file)
  end
end

@replace_all = false
`mkdir -p #{File.expand_path(File.join(File.dirname(__FILE__)),"bin")}`
if ARGV.empty?
  Dir.chdir File.dirname(__FILE__) do
    Dir['*'].each do |file|
      next if IGNORE_LIST.include?(file)
      replace!(file)
    end
  end
else
  ARGV.each do |file|
    if File.exist?(file)
      replace!(file)
    else
      puts "What is this #{file} of which you speak? I see it not."
    end
  end
end
