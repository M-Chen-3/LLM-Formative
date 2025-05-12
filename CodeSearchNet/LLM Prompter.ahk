SetWorkingDir A_InitialWorkingDir
; func_gt_str := FileRead("correct_functions.txt")
; func_gts := StrSplit(func_gt_str, "`n,`n")

descrip_strs := FileRead("function_descriptions.txt")
descrips := StrSplit(descrip_strs, "antidisestablishmentarianism")

total := 9
range := [263, 300]
queries := []
; Accuracy Prompts
; for descrip in descrips {
;     if A_Index > total {
;         break
;     }
;     if A_Index < range[1] {
;         continue
;     } else if A_Index > range[2] {
;         break
;     }
;     ; 222
    
;     queries.Push("Please generate a Python function that does the following with only the code box and no example usage:`n" . descrip)
; }

; Consistency Prompts
Loop total {
    rand := Random(1, descrips.Length)

    Loop 5 {
        queries.Push("Please generate a Python function that does the following with only the code box and no example usage:`n" . descrips[rand])
    }
}

; Test Code
; MsgBox queries[2]

; Times are in terms of milliseconds.
SendMode "Event"
SetKeyDelay 25

; Sends prompts upon hitting the ` key
`:: {
    for prompt in queries {
        A_Clipboard := prompt
        Send "^v"
        Sleep 500
        Send "{Enter}"
        Sleep 9500
    }
}

Esc::ExitApp  ; Exit script with Escape key