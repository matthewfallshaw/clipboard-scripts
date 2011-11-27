require File.join(File.dirname(__FILE__), "../lib/humanize")

describe HumanizingString do
  context "for all caps strings" do

    it "titlizes them" do
      HumanizingString.new("LOREM IPSUM DOLOR SIT AMET.").humanize.should == "Lorem Ipsum Dolor Sit Amet."
    end
    it "doesn't capitalise small words" do
      HumanizingString.new("JAKE AND THE NEVER LAND PIRATES").humanize.should == "Jake and the Never Land Pirates"
    end

  end

  it "removes annoying stops" do
    HumanizingString.new("Jake.and.the.Never.Land.Pirates").humanize.should == "Jake and the Never Land Pirates"
  end
  it "normalizes episode labels" do
    HumanizingString.new("Pirates.S01E05").humanize.should == "Pirates S01E05"
  end
  
end
