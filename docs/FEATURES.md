# Features Guide

Complete user guide for all iTrip modules and features.

## Table of Contents

- [Quote Builder](#quote-builder)
- [Quote History](#quote-history)
- [Property Brain](#property-brain)
- [Guest Reply Assistant](#guest-reply-assistant)
- [Revenue Analysis](#revenue-analysis)
- [Document Management](#document-management)

---

## Quote Builder

### Overview

Generate data-driven pricing quotes for guest bookings in seconds. The Quote Builder combines historical revenue data, seasonal adjustments, guest type factors, and stay length discounts to recommend three-tier pricing (conservative, recommended, aggressive).

**Access:** Dashboard → Quote Builder or direct URL: `/quote-builder`

### How to Use

#### Step 1: Select Property
1. Click the property dropdown
2. Select the property you want to quote
3. Available properties are populated from your uploaded data

#### Step 2: Enter Dates
1. **Check-in Date**: Click calendar to select arrival date
2. **Check-out Date**: Click calendar to select departure date
3. System automatically calculates:
   - Number of nights
   - Season type (peak, off-season, holiday)
   - Seasonal multiplier impact

#### Step 3: Guest Information
1. **Guest Count**: Enter number of guests (1-20)
2. **Guest Type**: Select from:
   - **Standard**: Baseline pricing (1.0x multiplier)
   - **Family**: 4+ guests → +10% premium (1.1x multiplier)
   - **Couple**: 2 guests → baseline pricing (1.0x multiplier)
   - **Group**: 8+ guests → -10% group discount (0.9x multiplier)
3. System applies appropriate rate multiplier

#### Step 4: Review Pricing
The system displays **three-tier pricing**:

**Conservative Rate** (25th percentile)
- Lower risk option
- Suitable for slower seasons
- -15% from recommended rate
- Blue card

**Recommended Rate** (50th percentile - median)
- Balanced approach
- Based on historical ADR
- Highlighted as primary choice
- Gradient background

**Aggressive Rate** (75th percentile)
- Premium option
- For peak demand periods
- +20% from recommended rate
- Green card

#### Step 5: View Breakdown
Scroll down to see **Price Calculation Breakdown**:

**Rate Multipliers Section:**
- Base ADR: Historical average daily rate
- Seasonal Adjustment: +20% summer, +30% winter, etc.
- Guest Type Factor: Family/group adjustments
- Length of Stay: Weekly -10%, monthly -20%

**Per Night Pricing:**
- Recommended rate × number of nights

**Additional Fees:**
- Cleaning Fee: $100 (one-time)
- Service Fee: 10% of nightly rate
- Pet Fee: $50 (if applicable)
- Taxes: 10% of subtotal

**Total Revenue:** Complete financial summary

#### Step 6: Seasonal Indicator
Visual summary showing:
- **Season**: With emoji (☀️ summer, 🎄 winter, 🌸 spring, 🍂 fall)
- **Adjustment %**: Peak markup or off-season discount
- **Guest Type**: Display with applicable multiplier
- **Stay Duration**: Holiday/weekend/weekly indicators

### Understanding the Pricing Logic

**Seasonal Multipliers:**
```
Summer (Jun-Aug):     1.20x (+20%)
Winter Holidays:      1.25x (+25%)
Spring Break:         1.15x (+15%)
Off-Season:           0.85x (-15%)
Standard Season:      1.0x
```

**Guest Type Factors:**
```
Family (4+ guests):   1.10x (+10%)
Couple (2 guests):    1.0x (standard)
Large Group (8+):     0.90x (-10%)
Solo traveler:        1.05x (+5%)
```

**Length of Stay Discounts:**
```
Monthly (28+ nights): 0.80x (-20%)
Weekly (7 nights):    0.90x (-10%)
Weekend (2-3 nights): 1.05x (+5%)
Standard:             1.0x
```

### Customization

After generating a quote, you can customize before saving:
- Override recommended rate
- Add/remove fees
- Add staff notes explaining the pricing decision
- Save as draft or send to guest

### Tips & Best Practices

1. **Seasonal Timing**: Adjust rates 2-3 weeks before peak seasons
2. **Competitor Analysis**: Compare with local market rates
3. **Weekend Premium**: Consider +5% premium for Friday-Sunday arrivals
4. **Monthly Discounts**: Help with occupancy by offering -20% for 28+ nights
5. **Last-Minute Bookings**: Use conservative rate for short-notice bookings
6. **Long-Term Rentals**: Use aggressive rate only with high confidence

---

## Quote History

### Overview

View, manage, and track all saved quotes. Filter by property, date range, and status.

**Access:** Dashboard → Quote History or direct URL: `/quotes`

### Viewing Your Quotes

#### Quote List
The quote table displays:
- **Property**: Property name with quote ID
- **Dates**: Check-in to check-out dates with night count
- **Guest Info**: Guest count and type
- **Rate**: Recommended rate per night
- **Total**: Recommended total revenue
- **Status**: Current quote status
- **Actions**: View quote details

#### Status Types
- **Draft**: Not yet sent to guest
- **Sent**: Sent to guest, awaiting response
- **Accepted**: Guest accepted the quote
- **Rejected**: Guest declined the quote
- **Customized**: Staff has modified the quote

#### Status Color Coding
```
Draft:      Gray
Sent:       Blue
Accepted:   Green
Rejected:   Red
Customized: Purple
```

### Filtering Quotes

**Filter by Status:**
1. Click status buttons above the table: "All", "Draft", "Sent", "Accepted", "Rejected"
2. Table updates to show only quotes with selected status
3. Click "All" to view all quotes regardless of status

### Quote Details

Click **"View"** button to see full quote details:
- Complete pricing breakdown
- All fees and calculations
- Guest information
- Created date and staff notes
- AI reasoning for pricing recommendation
- Action buttons (approve, send, customize, mark used)

### Exporting Quotes

Select a quote and choose:
- **Copy to Clipboard**: Copy formatted quote text
- **Export as PDF**: Download formatted PDF for email
- **Share Link**: Generate shareable link with quote summary

---

## Property Brain

### Overview

Ask questions about your property documents in natural language. The system searches through uploaded documents and provides AI-powered answers with source references.

**Access:** Dashboard → Property Brain or direct URL: `/property-brain`

### How to Use

#### Step 1: Ask a Question
1. Click the question input field
2. Type your question in plain English
3. Examples:
   - "What is the Wi-Fi password?"
   - "What amenities are available?"
   - "What is the check-in procedure?"
   - "What's the cancellation policy?"

#### Step 2: Submit Question
1. Press Enter or click the Submit button
2. System searches through all uploaded documents
3. AI analyzes relevant content and generates answer
4. Displays: Answer + Source references + Confidence scores

#### Step 3: Review Sources
Each answer includes source information:
- **Document**: Which file the answer came from
- **Excerpt**: Relevant quote from the document
- **Confidence**: How confident the AI is in this source (0-100%)

#### Confidence Levels
```
90-100%: Very confident answer
70-89%:  Confident answer
50-69%:  Moderate confidence, may need verification
<50%:    Low confidence, verify manually
```

### Best Practices

1. **Be Specific**: "Wi-Fi password" more effective than "network info"
2. **Use Keywords**: Include actual terms from your documents
3. **One Question at a Time**: Ask follow-ups separately
4. **Verify High-Value Answers**: Always verify pricing/policy answers
5. **Upload Complete Docs**: Better documents = better answers

### Example Questions

**Guest Management:**
- "When is the earliest check-in time?"
- "Where are the keys hidden?"
- "What's the Wi-Fi network name and password?"

**Amenities & Features:**
- "Is there a washing machine?"
- "What entertainment is provided?"
- "Is there parking available?"

**Policies & Rules:**
- "What is the pet policy?"
- "Are parties allowed?"
- "What's the cancellation policy?"

**Emergency Info:**
- "Where is the circuit breaker?"
- "What's the emergency contact number?"
- "How do I reset the WiFi router?"

---

## Guest Reply Assistant

### Overview

Draft professional responses to guest inquiries. The system analyzes the guest message, detects escalation risks, suggests response templates, and generates AI-powered replies.

**Access:** Dashboard → Guest Reply or direct URL: `/guest-reply`

### How to Use

#### Step 1: Paste Guest Message
1. Click the message input field
2. Paste the guest's email or chat message
3. The system analyzes the message for:
   - Sentiment (positive, neutral, negative)
   - Escalation risks (damage, refunds, complaints)
   - Topic classification
   - Required response urgency

#### Step 2: Review Risk Flags
The system displays escalation risk warnings:

**Risk Levels:**
```
Low Risk:       Normal inquiry → Green
Medium Risk:    Issue detected → Yellow
High Risk:      Complaint or damage → Orange
Escalate:       Urgent or legal issue → Red
```

**Flagged Keywords:**
```
Payment Issues:  refund, charge, overcharge, deposit
Property Issues: damage, broken, stain, hole, leak
Complaints:      angry, frustrated, disappointed, issue
Cancellations:   cancel, refund request
```

#### Step 3: View Generated Reply
The AI generates a professional response that:
- Acknowledges the guest's concern
- Provides a solution or next steps
- Maintains your property's tone and brand
- References relevant policies or procedures

#### Step 4: Review Sources
Source templates show:
- Similar responses from your template library
- Relevant policies that apply
- Best practice language from your documents

#### Step 5: Customize Reply
Before sending, you can:
1. **Edit Text**: Modify the AI-generated response
2. **Adjust Tone**: Make it more formal or casual
3. **Add Details**: Include specific information
4. **Flag for Review**: Mark for manager approval

#### Step 6: Send to Guest
1. Review one final time
2. Click "Send" to dispatch the reply
3. System logs the response in guest thread
4. Automatic follow-up reminder if needed

### Risk Management

**Medium Risk Response:**
- Acknowledge the issue
- Apologize for inconvenience
- Offer solution or compensation
- Provide next steps

**High Risk Response:**
- Flag for manager review before sending
- Document in escalation log
- Send through management approval
- Create follow-up task

**Escalation Protocol:**
1. System flags message as "Escalate"
2. Notification sent to property manager
3. Manager reviews and approves reply
4. Additional documentation required
5. Possible refund/compensation authorization

### Template Library

Create response templates for common situations:
- Standard greetings
- WiFi troubleshooting
- Check-in procedures
- Booking modifications
- Damage reports
- Refund requests

The AI uses these to maintain consistency and brand voice.

### Response Best Practices

1. **Be Prompt**: Respond within 1-2 hours when possible
2. **Be Professional**: Maintain courteous tone even with complaints
3. **Provide Solutions**: Don't just acknowledge, offer remedies
4. **Escalate Appropriately**: Use high-risk detection to catch issues early
5. **Document Everything**: Keep records of problematic interactions
6. **Follow Policies**: Always reference house rules and cancellation policy

---

## Revenue Analysis

### Overview

Analyze property revenue, identify trends, and make data-driven pricing decisions. View top-performing properties, monthly trends, and AI-powered insights.

**Access:** Dashboard → Revenue Analysis or direct URL: `/revenue-analysis`

### Features

#### Top Properties Report
1. **Metric Selection**: Choose what to rank by:
   - Revenue (total income)
   - ADR (average daily rate)
   - Occupancy Rate (percentage booked)

2. **Time Period**: Select date range for analysis

3. **Results Table**:
   - Rank (1st, 2nd, 3rd...)
   - Property name
   - Metric value
   - Comparison to average
   - Trend indicator (↑ up, → stable, ↓ down)

#### Property Trends
1. Select a property from dropdown
2. Choose analysis period (3, 6, 12 months)
3. View month-by-month breakdown:
   - Total revenue
   - Average daily rate
   - Occupancy percentage
   - Number of bookings

4. **Trend Metrics**:
   - Average monthly revenue
   - Growth rate percentage
   - Peak month
   - Slowest month

#### AI Insights
The system generates insights like:
- "Summer has historically been your peak season with 82% occupancy"
- "ADR increased 12% month-over-month, indicating strong demand"
- "Weekends command 15% premium over weekday rates"

### Using Revenue Data for Decisions

**Identify Underperforming Properties:**
1. Run "Top Properties by Revenue" report
2. Properties at bottom of list need attention
3. Analyze reasons (seasonality, marketing, rate)

**Optimize Pricing:**
1. View property trends
2. Identify peak vs. off-season patterns
3. Adjust rates accordingly
4. Use Quote Builder to recommend prices

**Manage Occupancy:**
1. Low occupancy rate → Lower prices or offer discounts
2. High occupancy → Raise rates
3. Target 70-85% occupancy for optimal revenue

**Seasonal Planning:**
1. Review historical data for similar months
2. Plan staffing and maintenance
3. Schedule marketing campaigns
4. Prepare for peak season pricing changes

### Exporting Reports

1. Click "Export" on any report
2. Choose format: PDF or CSV
3. Include charts and data tables
4. Schedule recurring exports

---

## Document Management

### Overview

Upload and manage property documents, guest response templates, and historical data. All documents are indexed for semantic search across the entire application.

**Access:** Dashboard → Imports or direct URL: `/imports`

### Upload Documents

#### Supported File Types

**DOCX (Word Documents)**
- Property information
- House rules
- Guest response templates
- Check-in instructions
- Emergency procedures

**XLSX (Excel Spreadsheets)**
- Revenue and occupancy data
- Historical ADR information
- Booking records
- Guest information

**PDF Files**
- Rental agreements
- Property photos/floorplans
- Insurance documents
- Historical receipts

#### Upload Process

1. Click "Select Files" or drag-and-drop
2. Choose one or more files
3. Optionally select document type:
   - Property Documents
   - Response Templates
   - Revenue Data
   - Other/General

4. Click "Upload"
5. Wait for processing (shows progress)
6. Files indexed for semantic search

#### File Size Limits
- Individual file: 50 MB maximum
- Total storage: Configurable per deployment

### Document Management

#### View Uploaded Documents
1. Click "Documents" tab
2. See all uploaded files with:
   - Filename
   - Document type
   - Upload date
   - Indexing status
   - Number of chunks

#### Processing Status
```
Uploading:    File transfer in progress
Processing:   Parsing file content
Indexing:     Creating embeddings for search
Complete:     Ready to use
Error:        Failed - retry or reupload
```

#### Delete Document
1. Click document row
2. Click "Delete" button
3. Confirm deletion
4. Document removed from all systems

### Document Best Practices

**For Property Brain:**
1. **Include Complete Info**: Property features, policies, procedures
2. **Use Consistent Terminology**: Same terms across documents
3. **Keep Updated**: Update annually or when policies change
4. **Be Specific**: Detailed information yields better answers

**For Revenue Analysis:**
1. **Complete Data**: All properties and time periods
2. **Consistent Format**: Same columns and date format
3. **Historical Records**: At least 12 months of data
4. **Regular Updates**: Add new data as it becomes available

**For Guest Reply Assistant:**
1. **Template Variety**: Responses for different situation types
2. **Tone Consistency**: Maintain brand voice across templates
3. **Policy References**: Include house rules and cancellation terms
4. **Emergency Contacts**: Local services and support information

---

## Tips & Tricks

- **Keyboard Shortcuts**: Press `?` on any page for shortcuts
- **Quick Quote**: Type `/quote property dates` in search bar
- **Voice Commands**: Use browser's voice input on question fields
- **Dark Mode**: Available in settings (click profile → preferences)
- **Mobile App**: Download for on-the-go management

---

For technical details, see the [API Reference](./API.md) or [Development Guide](../DEVELOPMENT.md).
