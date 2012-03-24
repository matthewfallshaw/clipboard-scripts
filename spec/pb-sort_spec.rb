describe "pb-sort" do

  it "sorts multi-line lists" do
    `echo "b\na\nd\nc" | pbcopy`
    `./pb-sort`
    output = `pbpaste`

    output.should == "a\nb\nc\nd\n"
  end
  it "sorts single line comma-separated lists" do
    `echo "b,a,d,c" | pbcopy`
    `./pb-sort`
    output = `pbpaste`

    output.should == "a,b,c,d\n"
  end
  it "sorts single line comma-and-space-separated lists" do
    `echo "b, a, d, c" | pbcopy`
    `./pb-sort`
    output = `pbpaste`

    output.should == "a,b,c,d\n"
  end
  
end
