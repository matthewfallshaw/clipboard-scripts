%w[rubygems active_support/inflector].each {|l| require l }

class HumanizingString < String
  def all_caps?
    self[/[^a-z]+/].length == self.length
  end
  def dotty?
    self.match(/(\w+\.)\w+/)
  end

  def humanize
    self.gsub!(/[@_-]/,' ')
    if all_caps?
      super.split("\s").collect {|w| w.capitalize}.join(" ")
    elsif dotty?
      self.gsub(/(\w)\.(\w)/,'\1 \2')
    else
      super
    end.split("\s").collect {|word| humanize_word(word) }.join(" ")
  end

  private

  def humanize_word(word)
    case word
    when /^(?:and|the|of|is)$/i
      word.downcase
    else
      word
    end
  end
end
