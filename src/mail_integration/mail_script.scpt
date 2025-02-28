(*
AppleScript to fetch emails from Apple Mail
Returns email content as JSON for processing
*)

-- Function to escape JSON special characters
on escapeJsonString(inputString)
    set output to ""
    set controlChars to {"\"", "\\", "/", "\b", "\f", "\n", "\r", "\t", "\"", "`", "'", "“", "”", "‘", "’"}
    set replacements to {"\\\"", "\\\\", "\\/", "\\b", "\\f", "\\n", "\\r", "\\t", "\\\"", "\\`", "\\'", "\\“", "\\”", "\\‘", "\\’"}
    
    try
        repeat with i from 1 to length of inputString
            set currentChar to character i of inputString
            set found to false
            repeat with j from 1 to count of controlChars
                if currentChar is item j of controlChars then
                    set output to output & item j of replacements
                    set found to true
                    exit repeat
                end if
            end repeat
            if not found then
                -- Handle non-ASCII characters
                if id of currentChar > 127 then
                    set output to output & "\\u" & my padLeft(text -2 thru -1 of ("0000" & (id of currentChar as string)), 4)
                else
                    -- Handle regular ASCII characters
                    set asciiValue to id of currentChar
                    if asciiValue < 32 then
                        -- Convert control characters to \uXXXX format
                        set output to output & "\\u" & my padLeft(text -2 thru -1 of ("0000" & (asciiValue as string)), 4)
                    else
                        -- Handle special cases for ASCII characters
                        if currentChar is "&" then
                            set output to output & "\\u0026"
                        else if currentChar is "<" then
                            set output to output & "\\u003C"
                        else if currentChar is ">" then
                            set output to output & "\\u003E"
                        else if currentChar is "=" then
                            set output to output & "\\u003D"
                        else if currentChar is "?" then
                            set output to output & "\\u003F"
                        else if currentChar is ":" then
                            set output to output & "\\u003A"
                        else if currentChar is ";" then
                            set output to output & "\\u003B"
                        else if currentChar is "[" then
                            set output to output & "\\u005B"
                        else if currentChar is "]" then
                            set output to output & "\\u005D"
                        else if currentChar is "{" then
                            set output to output & "\\u007B"
                        else if currentChar is "}" then
                            set output to output & "\\u007D"
                        else if currentChar is "|" then
                            set output to output & "\\u007C"
                        else if currentChar is "^" then
                            set output to output & "\\u005E"
                        else if currentChar is "~" then
                            set output to output & "\\u007E"
                        else
                            set output to output & currentChar
                        end if
                    end if
                end if
            end if
        end repeat
        return output
    on error errMsg
        log "Error escaping string: " & errMsg
        return ""
    end try
end escapeJsonString

-- Helper function to pad unicode values
on padLeft(inputString, length)
    set padding to ""
    repeat (length - (length of inputString)) times
        set padding to padding & "0"
    end repeat
    return padding & inputString
end padLeft

-- Debug function to log JSON string
on logJsonString(jsonString)
    try
        do shell script "echo " & quoted form of jsonString & " | python3 -c 'import json,sys; print(json.loads(sys.stdin.read()))'"
        return true
    on error errMsg
        log "JSON validation failed: " & errMsg
        return false
    end try
end logJsonString

on run argv
    tell application "Mail"
        set output to {}
        set theMessages to messages 1 thru 20 of inbox
        
        set output to "["
        set firstMessage to true
        
        repeat with theMessage in theMessages
            if not firstMessage then
                set output to output & ","
            end if
            
            set escapedContent to escapeJsonString(content of theMessage as string)
            set escapedHeaders to escapeJsonString(all headers of theMessage as string)
            
            set messageData to "{"
            set messageData to messageData & "\"id\":\"" & (id of theMessage as string) & "\","
            set messageData to messageData & "\"subject\":\"" & escapeJsonString(subject of theMessage as string) & "\","
            set messageData to messageData & "\"sender\":\"" & escapeJsonString(sender of theMessage as string) & "\","
            set messageData to messageData & "\"date\":\"" & (date received of theMessage as string) & "\","
            set messageData to messageData & "\"content\":\"" & escapedContent & "\","
            set messageData to messageData & "\"headers\":\"" & escapedHeaders & "\","
            set messageData to messageData & "\"read_status\":" & (read status of theMessage as string)
            set messageData to messageData & "}"
            set output to output & messageData
            set firstMessage to false
        end repeat
        
        set output to output & "]"
        
        -- Validate the JSON output
        if not logJsonString(output) then
            error "Invalid JSON generated"
        end if
        
        return output
    end tell
end run
