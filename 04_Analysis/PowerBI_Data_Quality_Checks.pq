// POWER QUERY M — create a second Blank Query named Data_Quality_Checks
// This query references the existing clean 'Complaints' query and should be loaded as an audit table.
let
    S = Complaints,
    Total = Table.RowCount(S),
    UniqueIDs = Table.RowCount(Table.Distinct(Table.SelectColumns(S, {"Complaint ID"}))),
    DuplicateIDs = Total - UniqueIDs,
    MissingIssue = Table.RowCount(Table.SelectRows(S, each [#"Sub-issue"] = null or [#"Sub-issue"] = "")),
    MissingPublic = Table.RowCount(Table.SelectRows(S, each [Company public response] = null or [Company public response] = "")),
    MissingProduct = Table.RowCount(Table.SelectRows(S, each [#"Sub-product"] = null or [#"Sub-product"] = "")),
    MissingTimeliness = Table.RowCount(Table.SelectRows(S, each [#"Timely response?"] = null or [#"Timely response?"] = "")),
    InProgress = Table.RowCount(Table.SelectRows(S, each [Company response to consumer] = "In progress")),
    BlankWrongStatus = Table.RowCount(Table.SelectRows(S, each ([#"Timely response?"] = null or [#"Timely response?"] = "") and [Company response to consumer] <> "In progress")),
    InvalidTimeliness = Table.RowCount(Table.SelectRows(S, each [#"Timely response?"] <> null and [#"Timely response?"] <> "" and [#"Timely response?"] <> "Yes" and [#"Timely response?"] <> "No")),
    InvalidForwarding = Table.RowCount(Table.SelectRows(S, each [Date submitted] = null or [Date received] = null or [Forwarding Days] = null or [Forwarding Days] < 0)),
    Results = #table({"Check", "Observed", "Expected", "Result"}, {
        {"Source rows", Total, 62516, if Total = 62516 then "PASS" else "REVIEW"},
        {"Distinct complaint IDs", UniqueIDs, 62516, if UniqueIDs = 62516 then "PASS" else "REVIEW"},
        {"Duplicate ID records", DuplicateIDs, 0, if DuplicateIDs = 0 then "PASS" else "REVIEW"},
        {"Missing sub-issue", MissingIssue, 10858, if MissingIssue = 10858 then "PASS" else "REVIEW"},
        {"Missing public response", MissingPublic, 2175, if MissingPublic = 2175 then "PASS" else "REVIEW"},
        {"Missing sub-product", MissingProduct, 7, if MissingProduct = 7 then "PASS" else "REVIEW"},
        {"Missing timeliness", MissingTimeliness, 1494, if MissingTimeliness = 1494 then "PASS" else "REVIEW"},
        {"In progress", InProgress, 1494, if InProgress = 1494 then "PASS" else "REVIEW"},
        {"Blank timeliness not in-progress", BlankWrongStatus, 0, if BlankWrongStatus = 0 then "PASS" else "REVIEW"},
        {"Other invalid timeliness values", InvalidTimeliness, 0, if InvalidTimeliness = 0 then "PASS" else "REVIEW"},
        {"Invalid or negative forwarding", InvalidForwarding, 0, if InvalidForwarding = 0 then "PASS" else "REVIEW"}
    })
in
    Results
