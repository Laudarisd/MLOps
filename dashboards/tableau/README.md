# Tableau Integration Guide

This guide explains how to connect Tableau to your data sources, build dashboards, and publish them for sharing and scheduled refresh. It is designed for beginners and covers both Desktop and Tableau Server/Online workflows.

---

## 1. What is Tableau?

Tableau is a leading data visualization and business intelligence platform. It allows you to connect to various data sources, create interactive dashboards, and share insights securely.

---

## 2. Prerequisites

- Tableau Desktop installed ([Download](https://www.tableau.com/products/desktop))
- Access to your data source (e.g., database, CSV, Excel, cloud data)
- (Optional) Tableau Server or Tableau Online account for publishing and sharing

---

## 3. Connect Tableau to Your Data

1. Open Tableau Desktop
2. Click **Connect** (left panel)
3. Choose your data source type (e.g., MySQL, PostgreSQL, Excel, CSV, etc.)
4. Enter connection details (server, database, username, password)
5. Click **Sign In** or **Connect**
6. Select tables or sheets to import

---

## 4. Build Your First Dashboard

1. Drag fields onto **Rows** and **Columns** to create a worksheet
2. Use the **Show Me** panel for chart suggestions
3. Create multiple worksheets for different views
4. Click **Dashboard** > **New Dashboard**
5. Drag worksheets onto the dashboard canvas
6. Add filters, legends, and interactivity as needed

---

## 5. Publish and Share Dashboards

### a. Publish to Tableau Server/Online

1. Click **Server** > **Sign In** (enter your Tableau Server/Online credentials)
2. Click **Server** > **Publish Workbook**
3. Choose project/folder, set permissions, and publish

### b. Export as PDF/Image

- File > Export As > PDF or Image

---

## 6. Schedule Data Refresh (Tableau Server/Online)

1. After publishing, go to Tableau Server/Online
2. Navigate to your workbook/dataset
3. Click **Schedule Refresh**
4. Set frequency (e.g., daily, hourly)
5. Save settings

---

## 7. Troubleshooting

- **Cannot connect to data source:** Check credentials, network, and driver installation
- **Slow dashboard:** Optimize queries, use extracts, limit data volume
- **Refresh failures:** Check data source availability and permissions

---

## 8. Security Tips

- Use strong passwords for Tableau and data sources
- Limit user permissions on Tableau Server/Online
- Keep Tableau and database drivers up to date

---

## 9. Backup & Restore

- Export workbooks as `.twbx` files for backup
- Use Tableau Server/Online backup tools for enterprise deployments

---

## 10. More Information

- [Tableau Desktop Help](https://help.tableau.com/current/pro/desktop/en-us/help.htm)
- [Tableau Server Help](https://help.tableau.com/current/server/en-us/help.htm)
- [Tableau Community](https://community.tableau.com/)
- See the [Main Project README](../../README.md) for a full project overview and context.
