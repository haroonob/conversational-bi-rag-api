## Column: Country
    Operator: =
    Value: {{ country }}
    Description: Filter based on user-specified country.

## Column: InvoiceDate
    Operator: BETWEEN
    Value: ['{{ start_date }}', '{{ end_date }}']
    Description: Include only orders within a specific date range.

## Column: CustomerID
    Operator: IS NOT NULL
    Description: Ensure only valid customer records are included.

## Column: Quantity
    Operator: >
    Value: 0
    Description: Exclude negative quantities (likely returns).

## Column: UnitPrice
    Operator: >
    Value: 0
    Description: Exclude zero or negative unit prices.