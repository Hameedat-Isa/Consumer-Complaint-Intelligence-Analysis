// POWER BI DESKTOP — POWER QUERY M
// Use: Home > Transform data > New Source > Blank Query > Advanced Editor.
// Name the loaded query Complaints. Change SourcePath to the unmodified Excel source.
// The original worksheet is Data. The source file is not overwritten.
let
    SourcePath = "C:\REPLACE_WITH_YOUR_FOLDER\Consumer_Complaints_original.xlsx",
    Source = Excel.Workbook(File.Contents(SourcePath), null, true),
    DataSheet = Source{[Item="Data",Kind="Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(DataSheet, [PromoteAllScalars=true]),
    ExpectedColumns = {"Complaint ID", "Submitted via", "Date submitted", "Date received", "State", "Product", "Sub-product", "Issue", "Sub-issue", "Company public response", "Company response to consumer", "Timely response?"},
    CheckedSchema = if List.Count(List.Difference(ExpectedColumns, Table.ColumnNames(PromotedHeaders))) = 0
        then PromotedHeaders
        else error "Dataset schema does not match the 12-column assignment extract",
    Typed = Table.TransformColumnTypes(CheckedSchema, {
        {"Complaint ID", type text}, {"Submitted via", type text},
        {"Date submitted", type date}, {"Date received", type date},
        {"State", type text}, {"Product", type text}, {"Sub-product", type text},
        {"Issue", type text}, {"Sub-issue", type text},
        {"Company public response", type text}, {"Company response to consumer", type text},
        {"Timely response?", type text}
    }),
    TextColumns = {"Submitted via", "State", "Product", "Sub-product", "Issue", "Sub-issue", "Company public response", "Company response to consumer", "Timely response?"},
    StandardizedText = Table.TransformColumns(Typed,
        List.Transform(TextColumns, (col) => {col, (v) => if v = null then null else Text.Clean(Text.Trim(v)), type nullable text})),
    AddedYear = Table.AddColumn(StandardizedText, "Year", each Date.Year([Date submitted]), Int64.Type),
    AddedMonth = Table.AddColumn(AddedYear, "Month", each Date.MonthName([Date submitted]), type text),
    AddedMonthStart = Table.AddColumn(AddedMonth, "Month Start", each Date.StartOfMonth([Date submitted]), type date),
    AddedQuarter = Table.AddColumn(AddedMonthStart, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date submitted])), type text),
    AddedForwarding = Table.AddColumn(AddedQuarter, "Forwarding Days", each Duration.Days([Date received]-[Date submitted]), Int64.Type),
    AddedBin = Table.AddColumn(AddedForwarding, "Forwarding Band", each
        if [Forwarding Days] = null then "(Not recorded)"
        else if [Forwarding Days] = 0 then "0 days"
        else if [Forwarding Days] <= 4 then "1–4 days"
        else if [Forwarding Days] <= 9 then "5–9 days"
        else if [Forwarding Days] <= 24 then "10–24 days"
        else "25+ days", type text),
    AddedBandOrder = Table.AddColumn(AddedBin, "Forwarding Band Sort", each
        if [Forwarding Band] = "0 days" then 1
        else if [Forwarding Band] = "1–4 days" then 2
        else if [Forwarding Band] = "5–9 days" then 3
        else if [Forwarding Band] = "10–24 days" then 4 else 5, Int64.Type)
in
    AddedBandOrder
