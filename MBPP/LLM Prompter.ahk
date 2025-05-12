SetWorkingDir A_InitialWorkingDir
; func_gt_str := FileRead("correct_functions.txt")
; func_gts := StrSplit(func_gt_str, "`n,`n")

descrip_strs := FileRead("function_descriptions.txt")
descrips := StrSplit(descrip_strs, "antidisestablishmentarianism")

total := 200
range := [141, 200]
queries := []
for descrip in descrips {
    if A_Index > total {
        break
    }
    if A_Index < range[1] {
        continue
    } else if A_Index > range[2] {
        break
    }

    ; try-catch to account for different prompt starts
    try {
        descrip := StrSplit(descrip, "Write a ")[2]
        start := "Write a "
    } catch {
        descrip := StrSplit(descrip, "write a ")
        start := descrip[1] . "write a "
        descrip := descrip[2]
    }

    ; Check whether prompt contains a python
    if not StrCompare(SubStr(descrip, 1, 6), "python") == 0 {
        descrip := "python " . descrip
    }
    descrip := start . descrip

    queries.Push(descrip . "Please only include a code box without an example.")
}
; MsgBox queries[2]

; Times are in terms of millisecondsvid.
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