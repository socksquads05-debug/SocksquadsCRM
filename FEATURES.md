# SocksQuads CRM - Feature Documentation

## Complete Feature List

### 1. Authentication & Authorization

#### Login System
- Username and password authentication
- Session management
- Automatic logout on page refresh without credentials
- Two user roles: Admin and Salesman

#### Role-Based Access Control
- **Admin Features:**
  - Full access to all pages
  - View all reports and analytics
  - Manage retailer database
  - Generate custom reports
  - View performance metrics for all team members

- **Salesman Features:**
  - Submit daily sales reports
  - View personal performance metrics
  - Download personal reports
  - Cannot access admin panels

---

### 2. Dashboard (Admin Only)

#### Key Metrics Display
- Total Sales (selected period)
- Total Collections
- Total Outstanding Amount
- Number of Orders
- Collection Rate Percentage
- Average Order Value

#### Charts & Visualizations
- **Daily Sales Trend**: Line chart showing daily sales over time
- **Monthly Sales & Collection**: Combined bar and line chart
- **Top 5 Salesmen**: Bar chart by total sales
- **Top 5 Retailers**: Bar chart by total orders
- **Sales Distribution by Area**: Pie chart
- **Collection Rate Gauge**: Animated gauge chart
- **Collection vs Outstanding**: Stacked bar chart by day
- **Retailer Growth**: Cumulative count of unique retailers

#### Detailed Tables
- Salesman Performance Table: Total sales, orders, average order, collections
- Area Performance Table: Sales by area with detailed metrics
- Top 20 Retailers: Ranked by total sales

#### Date Range Filtering
- Select custom date ranges
- Automatic filtering of all charts and metrics
- Quick filters for common periods

---

### 3. Daily Sales Report (Salesman & Admin)

#### Report Submission Form
**Required Fields:**
- Date (defaults to today)
- Retailer Name
- Retailer Mobile Number (validated)
- Area
- City

**Optional Fields:**
- Order Quantity
- Order Value
- Collection Received
- Outstanding Amount
- Next Visit Date
- Remarks/Product Details

#### Data Validation
- All required fields must be filled
- Mobile number format validation
- Automatic timestamp recording
- Data automatically saved to Google Sheets

#### Performance Dashboard
- Total sales figure (all-time for user)
- Total collections
- Total outstanding
- Total orders submitted

#### Performance Charts
- Daily sales trend for the user
- Collection rate gauge
- Top retailers visited by sales amount

#### Data Export
- Download reports as CSV
- Includes all personal reports
- Formatted with currency symbols

---

### 4. Retailer Management (Admin Only)

#### Add New Retailer
**Form Fields:**
- Retailer Name (required)
- Owner Name (required)
- Mobile Number (required, 10 digits)
- Complete Address (required)
- GST Number (optional)
- Area (required)
- City (required)
- Preferred Product
- Notes/Comments

#### Search & Filter
**Search Options:**
1. By Retailer Name (text search, case-insensitive)
2. By Mobile Number (exact match)
3. By Area (dropdown selection)
4. By City (dropdown selection)

#### Retailer Details View
**Card Display for Each Retailer:**
- Basic Information:
  - Name, Owner, Mobile, Address, GST Number
- Location & Performance:
  - Area, City, Last Visit Date, Last Order Date
- Financial:
  - Lifetime Sales Amount, Outstanding Amount
- Preferences:
  - Preferred Products, Notes

#### Retailer Analytics
- Total unique retailers count
- Distribution by area
- Distribution by city
- Top 10 retailers by outstanding amount
- Recently added retailers (last 10)

---

### 5. Reports (Admin Only)

#### Daily Report
- Select specific date
- Display all transactions for that day
- Key metrics (total sales, collections, orders, outstanding)
- CSV export

#### Weekly Report
- Auto-calculates week boundaries
- Shows week summary metrics
- Daily breakdown within the week
- CSV export

#### Monthly Report
- Select month and year
- Full month analysis
- Salesman-wise breakdown
- CSV export

#### Salesman Report
- Select individual salesman
- All-time performance metrics
- Top retailers by sales
- CSV export

#### Area Report
- Select specific area
- Area-wide statistics
- All transactions in that area
- CSV export

#### Collection Report
- Date range selection
- Total collection vs outstanding
- Collection by salesman breakdown
- Collection rate calculations
- CSV export

#### Custom Date Range
- Pick any start and end dates
- All data for that range
- Full transaction table
- CSV export

#### Export Features
- All reports exportable as CSV
- Formatted with proper headers
- Currency formatting preserved
- Timestamp included for tracking

---

### 6. Retailer CRM Database

#### Retailer Information Stored
- Name & Owner Name
- Mobile Number (searchable)
- Complete Address
- GST Number
- Area & City
- Last Visit Date
- Last Order Date
- Lifetime Sales Value
- Outstanding Amount
- Preferred Product
- Additional Notes

#### Built-in Analytics
- Track customer lifetime value
- Monitor payment patterns
- Identify dormant accounts
- Track product preferences

---

### 7. Advanced Analytics (Admin Only)

#### Key Insights Section
**Time Period Selection:** Last 7/30/90 days or All Time

**Metrics Shown:**
- Total Sales
- Average Daily Sales
- Total Orders
- Top 5 Salesmen (bar chart)
- Top 5 Retailers (bar chart)
- Sales distribution by area (pie chart)
- Order value distribution (histogram)

#### Retailer Analysis
**Analysis Types:**
1. **Top Retailers** (Top 10 by sales)
2. **Bottom Retailers** (Lowest 10 performers)
3. **Inactive Retailers** (No orders in 30+ days)
4. **High Outstanding** (Top 10 by unpaid amount)
5. **New Retailers** (Last 10 added)

#### Sales Team Performance
- Team-wide statistics table:
  - Total sales per salesman
  - Number of orders
  - Average order value
  - Total collections
  - Outstanding amount
  - Number of retailers visited

- Individual salesman analysis:
  - Select salesman name
  - All-time metrics
  - Performance chart
  - Top retailers visited

#### Alerts & Warnings System
**Automatic Alerts for:**
1. Low Collection Rate (< 70%)
2. High Outstanding Amount
3. Inactive Retailers (30+ days)
4. No sales submitted today
5. Green indicator if all is well

#### Summary Statistics
- Total transactions
- Unique retailers
- Active sales team members

---

### 8. Charts & Visualizations

#### Chart Types Used
- **Line Charts**: Sales trends, cumulative data
- **Bar Charts**: Comparisons (top performers, area analysis)
- **Pie Charts**: Distribution (area-wise, category-wise)
- **Histograms**: Distribution analysis
- **Gauge Charts**: Performance metrics (collection rate)
- **Stacked Bar Charts**: Comparative values

#### All Charts Feature:
- Interactive hover information
- Zoom and pan capabilities
- Download as PNG
- Responsive design (mobile-friendly)
- Color-coded for easy understanding

---

### 9. Data Management

#### Google Sheets Integration
- **Automatic Data Storage:**
  - Sales reports saved after submission
  - Retailer information auto-saved
  - Instant synchronization

- **Multiple Worksheets:**
  - Sales Reports sheet
  - Retailers sheet
  - Auto-created on first use

#### Data Structure
**Sales Reports Table:**
- Columns: Date, Salesman, Retailer, Mobile, Area, City, Order Qty, Order Value, Collection, Outstanding, Next Visit, Remarks, Timestamp
- Auto-populated timestamp
- 1000+ rows capacity initially

**Retailers Table:**
- Columns: Name, Owner, Mobile, Address, GST, Area, City, Last Visit, Last Order, Lifetime Sales, Outstanding, Preferred Product, Notes, Created Date
- Auto-updated with relationships

#### Data Integrity
- Required field validation
- Automatic timestamp recording
- Permanent audit trail in Google Sheets
- No data loss (Google Sheets backed-up by Google)

---

### 10. User Interface & Experience

#### Design Features
- Professional corporate theme
- Blue accent color (#0066cc)
- White background
- Responsive layout
- Mobile-friendly interface

#### Navigation
- Simple sidebar menu
- Role-based menu items
- Logout button
- User info display
- Current page indicator

#### Mobile Optimization
- Touch-friendly buttons
- Responsive charts
- Optimized input forms
- Mobile-sized tables
- One-column layout on small screens

#### Accessibility
- Clear labels on all fields
- Proper color contrast
- Keyboard navigation support
- Descriptive button labels
- Error messages with guidance

---

### 11. Security Features

#### Authentication
- Password-protected login
- Session-based access control
- Automatic access restriction based on role
- No credentials stored in code

#### Data Security
- Google Sheets handles encryption
- Service account uses OAuth 2.0
- Credentials stored locally (not in code)
- Streamlit Secrets for cloud deployment

#### Access Control
- Admin-only pages blocked for salesmen
- Own data visibility for salesmen
- No cross-salesman visibility of private data

---

### 12. Configuration & Customization

#### Configurable Items (in config.py)
- App name and version
- Google Sheet name
- User roles and permissions
- Report types available
- Chart colors
- Analytics thresholds
- Inactive retailer time threshold
- Collection rate threshold

#### User Management
- Add users by updating credentials
- Change roles easily
- Password updates in config
- Multiple admin accounts supported

---

### 13. Export & Reporting Features

#### CSV Export
- All reports available in CSV format
- Proper formatting with headers
- Currency symbols retained
- Date formatting preserved
- Open in Excel/Google Sheets

#### Data Download
- Download from any report page
- Download from salesman performance
- Download from retailer list
- Individual file naming with dates

---

## Performance Specifications

### Capacity
- Supports 1000+ sales records per month
- Handles 100+ retailers effectively
- Multiple concurrent users supported
- Free tier sufficient for small-medium business

### Speed
- Data load: < 5 seconds typically
- Report generation: < 3 seconds
- Chart rendering: < 2 seconds
- Cloud deployment: Auto-reconnect after 15 min inactivity

---

## Integration Capabilities

### Google Services
- **Google Sheets**: Primary database
- **Google Drive**: File storage
- **Google Cloud**: OAuth authentication

### External Services
- **Streamlit Community Cloud**: Hosting
- **GitHub**: Version control and deployment trigger
- **Plotly**: Visualization library

---

## Limitations & Considerations

### Current Limitations
- Max 10 million cells in Google Sheet (very large limit)
- Free Streamlit tier sleeps after 15 min
- No offline functionality (requires internet)
- Single-sheet per application

### Future Enhancement Possibilities
- Email notifications for alerts
- SMS notifications for salesmen
- Automatic backup scheduling
- Advanced predictive analytics
- Multi-currency support
- Photo upload capability
- Invoice generation
- GPS tracking

---

**Feature Version**: 1.0
**Last Updated**: July 2026
**Status**: All Features Implemented ✅
