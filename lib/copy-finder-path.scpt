tell application "Finder"
	set sel to the selection
	set the_paths to ""
	repeat with the_item in sel
		set the_paths to (the_paths & (POSIX path of (the_item as alias)) as text) & return
	end repeat
	if the_paths is not "" then set the_paths to text 1 thru -2 of the_paths
	set the clipboard to the_paths
end tell

