## Project Brief

- Read names from `names.txt`, one per line.
- For each name, fetch tax data from `https://verokone.hs.fi/rest/query` using query parameters modeled by the example URL provided (`name`, `county`, `gender`, `taxyear`, `age`, `orderby`, `brand`, `offset`, `limit`).
- Cache each response as JSON under `cache/<name>.json` to avoid redundant requests.
- Output the list of names along with their totalIncome rounded to whole euros, for example: `Visa de Bruijn: 204531 EUR`.

## Notes

- The API example: `https://verokone.hs.fi/rest/query?name=Bruijn%20Visa&county=&gender=&taxyear=2024&age=&orderby=gross_income&brand=is&offset=0&limit=100`.
- Ensure proper URL encoding for names when fetching data.

Here is an example of a response from the API:

```json
{
  "results": [
    {
      "name": "de Bruijn Visa Tapio",
      "id": "1984de Bruijn Visa Tapio",
      "birthYear": 1984,
      "lastCounty": "Uusimaa",
      "taxYearsDefined": [
        2024
      ],
      "taxYears": {
        "2024": {
          "salaryRank": 62069,
          "taxYear": 2024,
          "county": "Uusimaa",
          "totalIncome": 204530.75999999998,
          "capitalIncome": 146955.77,
          "salary": 57574.99,
          "rank": 18030,
          "paidTaxes": 64449.33,
          "taxRatio": 31.510825071006437,
          "personId": "1984de Bruijn Visa Tapio",
          "fragmentId": "20241984de_Bruijn_Visa_Tapio"
        }
      }
    }
  ],
  "offset": 0,
  "count": 1,
  "totResults": 1
}
```