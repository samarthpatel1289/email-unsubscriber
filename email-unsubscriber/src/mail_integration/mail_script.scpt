on run argv
    set maxEmails to 50
    if (count of argv) > 0 then
        set maxEmails to item 1 of argv as integer
    end if
    
    tell application "Mail"
        set allMessages to every message of inbox
        set emailData to {}
        set processedCount to 0
        
        repeat with msg in allMessages
            if processedCount ≥ maxEmails then exit repeat
            
            set end of emailData to {¬
                |id|:message id of msg, ¬
                |subject|:subject of msg, ¬
                |sender|:sender of msg, ¬
                |date|:date received of msg, ¬
                |content|:content of msg, ¬
                |read status|:read status of msg¬
            }
            set processedCount to processedCount + 1
        end repeat
        
        try
            -- Convert AppleScript records to JSON using native methods
            set jsonData to my convertToJSON(emailData)
            return jsonData
        on error errMsg
            return "{\"error\":\"" & my escapeQuotes(errMsg) & "\"}"
        end try
    end tell
end run

on convertToJSON(theRecords)
    set jsonArray to {}
    repeat with recordItem in theRecords
        -- Build JSON object piece by piece with proper escaping
        set jsonRecord to "{"
        set jsonRecord to jsonRecord & "\"id\":\"" & (my escapeQuotes(|id| of recordItem as text)) & "\""
        set jsonRecord to jsonRecord & ",\"subject\":\"" & (my escapeQuotes(|subject| of recordItem as text)) & "\""
        set jsonRecord to jsonRecord & ",\"sender\":\"" & (my escapeQuotes(|sender| of recordItem as text)) & "\""
        set jsonRecord to jsonRecord & ",\"date\":\"" & (my escapeQuotes(|date| of recordItem as text)) & "\""
        set jsonRecord to jsonRecord & ",\"content\":\"" & (my escapeQuotes(|content| of recordItem as text)) & "\""
        set jsonRecord to jsonRecord & ",\"read_status\":\"" & (my escapeQuotes(|read status| of recordItem as text)) & "\""
        set jsonRecord to jsonRecord & "}"
        
        set end of jsonArray to jsonRecord
    end repeat
    return "[" & (my joinList(jsonArray, ",")) & "]"
end convertToJSON

on joinList(theList, delimiter)
    set AppleScript's text item delimiters to delimiter
    set theText to theList as text
    set AppleScript's text item delimiters to ""
    return theText
end joinList

on escapeQuotes(inputText)
    set AppleScript's text item delimiters to {"\"", "\n", "\r", "\t", "\b", "\f"}
    set theTextItems to text items of inputText
    set AppleScript's text item delimiters to {"\\\"", "\\n", "\\r", "\\t", "\\b", "\\f"}
    set theText to theTextItems as string
    set AppleScript's text item delimiters to ""
    return theText
end escapeQuotes
