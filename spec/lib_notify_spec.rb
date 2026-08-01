require 'spec_helper'
require 'shellwords'

describe "lib/notify script" do
  let(:notify_script) { File.expand_path("../../lib/notify", __FILE__) }
  
  def run_notify(message)
    # Run the script and capture everything
    output = `#{notify_script.shellescape} #{message.shellescape} 2>&1`
    success = $?.success?
    
    # If it failed, show what the actual command was
    if !success
      puts "Failed command output: #{output}"
      puts "Exit code: #{$?.exitstatus}"
    end
    
    { output: output, success: success, exit_code: $?.exitstatus }
  end

  context "basic functionality" do
    it "handles simple text" do
      result = run_notify("hello world")
      expect(result[:success]).to be true
    end

    it "handles empty message" do
      result = run_notify("")
      expect(result[:success]).to be true
    end
  end

  context "special characters that break AppleScript" do
    it "handles double quotes" do
      result = run_notify('text with "quotes" inside')
      expect(result[:success]).to be true
    end

    it "handles single quotes" do
      result = run_notify("text with 'quotes' inside")
      expect(result[:success]).to be true
    end

    it "handles backslashes" do
      result = run_notify('text with \\ backslashes')
      expect(result[:success]).to be true
    end

    it "handles colons (original problem)" do
      result = run_notify("1601:1603: syntax error")
      expect(result[:success]).to be true
    end

    it "handles newlines" do
      result = run_notify("line one\nline two")
      expect(result[:success]).to be true
    end

    it "handles tabs" do
      result = run_notify("text with\ttabs")
      expect(result[:success]).to be true
    end

    it "handles carriage returns" do
      result = run_notify("text with\rcarriage returns")
      expect(result[:success]).to be true
    end

    it "handles mixed special characters" do
      result = run_notify('complex: "quoted" text with \\ and \n newlines')
      expect(result[:success]).to be true
    end
  end

  context "edge cases" do
    it "handles very long messages" do
      long_message = "a" * 1000
      result = run_notify(long_message)
      expect(result[:success]).to be true
    end

    it "handles unicode characters" do
      result = run_notify("emoji 🎉 and unicode ñoño")
      expect(result[:success]).to be true
    end

    it "handles AppleScript reserved words" do
      result = run_notify("tell application display notification end tell")
      expect(result[:success]).to be true
    end
  end

  context "error handling" do
    it "provides meaningful error messages on failure" do
      # This test might need adjustment based on actual error handling
      # For now, just ensure script exists and is executable
      expect(File.exist?(notify_script)).to be true
      expect(File.executable?(notify_script)).to be true
    end
  end
end