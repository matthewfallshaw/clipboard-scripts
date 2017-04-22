%w[rubygems rake yaml shellwords].each {|l| require l }

BINDIR = File.expand_path(File.join(File.dirname(__FILE__), "bin"))
SOURCEDIR = File.expand_path(File.dirname(__FILE__))
SECRETS = File.expand_path('~/.dotfiles_secrets')
 
task :default => :install

desc "Install clipboard scripts to #{BINDIR}
  secrets in ~/.dotfiles_secrets like
  filename:
    'search_term': replace_term
    'other_search_term': other_replace_term"
task :install

Dir["pb-*"].each do |script|
  binfile = File.join(BINDIR, script)

  task install: script[3..-1]

  desc "file #{binfile} => #{script}"
  task script[3..-1] => binfile

  file binfile => script do
    puts "## #{script}"
    mkdir_p BINDIR
    cp script, BINDIR
    system %Q{chmod u+x "#{File.join(BINDIR, script)}"}
    if secrets[script]
      secrets[script].each do |search_term, replace_term|
        system %[ruby -pi -e 'gsub(/#{Shellwords.escape(search_term)}/, "#{Shellwords.escape(replace_term)}")' "#{File.join(BINDIR, script)}"]
      end
      puts "… and secrets replaced in #{script}"
    end
    puts
  end
end

def secrets
  @secrets ||= begin
                 path = File.expand_path('~/.dotfiles_secrets')
                 if File.exist?(path)
                   YAML.load(open(path))
                 else
                   {}
                 end
               end
end

