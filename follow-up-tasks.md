# Technical Interview Tasks

## 1. Code Review and Issue Remediation

Please perform a thorough code review and remediate any identified issues related to:
- **Security issues**
- **Database interaction**
- **Code quality and logical consistency**

Please make a note of any other identified improvements not implemented.

### 2. Currency Support Implementation

**Current State**: The expense submission form includes a currency field, but the application currently ignores this field and treats all monetary values as USD.

**Requirements**:
- Implement foreign exchange (FX) handling to convert all currency values to USD for summation and display on the dashboard
- Preserve and display the original value and currency on the Expense Details form
- Calculate accurate currency conversion rates using the provided FX data
- Implement an audit trail system that tracks all currency conversions, including original amount, converted amount, exchange rate used, conversion timestamp, and data source

**Implementation Notes**:
For this implementation, you will use a dummy FX rates provider that only provides exchange rates to Euros. You must determine the relevant USD conversion rate using cross-currency calculations with this EUR-based data only. Assume this data comes from an external REST API.

**Sample FX Data**:
Please use this sample data as a mock response from the external API.
```json
{
    "date": "20250701",
    "rates": {
        "USDEUR": 0.92,
        "GBPEUR": 1.17,
        "JPYEUR": 0.0064,
        "INREUR": 0.011,
        "AUDEUR": 0.61,
        "CADEUR": 0.69,
        "CHFEUR": 1.05,
        "CNYEUR": 0.13,
        "HKDEUR": 0.12,
        "SGDEUR": 0.68,
        "NZDEUR": 0.56,
        "SEKEUR": 0.087,
        "NOKEUR": 0.086,
        "PLNEUR": 0.23,
        "CZKEUR": 0.042,
        "HUFEUR": 0.0027,
        "RONEUR": 0.20,
        "TRYEUR": 0.035,
        "ZAREUR": 0.049,
        "BRLEUR": 0.19
    }
}
```
## Note for Candidates
This specification intentionally leaves some implementation details undefined. Part of this exercise is identifying gaps in requirements and making reasonable technical decisions. Please document any assumptions you make and be prepared to discuss your reasoning.
