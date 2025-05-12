SetWorkingDir A_InitialWorkingDir

; Change file name accordingly
descrip_strs := FileRead("hallucination.txt")
descrips := StrSplit(descrip_strs, "antidisestablishmentarianism")

; Times are in terms of milliseconds.
SendMode "Event"
SetKeyDelay 25

; Sends prompts upon hitting the ` key
`:: {
    for prompt in descrips {
        A_Clipboard := prompt
        Send "^v"
        Sleep 500
        Send "{Enter}"
        Sleep 14500
    }
}

Esc::ExitApp  ; Exit script with Escape key