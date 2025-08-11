# Connecting Power BI to MariaDB with On-premises Data Gateway

This guide documents the full process of connecting **Microsoft Power BI** to a **MariaDB** database for data analysis, visualization, and scheduled refresh.
It includes **secure database user creation**, **LAN connection setup**, and **On-premises Data Gateway** configuration for automated updates in the Power BI Service.

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1 — Create a Read-only MariaDB User](#step-1--create-a-read-only-mariadb-user)
4. [Step 2 — Test MariaDB Connection from Power BI Desktop](#step-2--test-mariadb-connection-from-power-bi-desktop)
5. [Step 3 — Connect in Power BI Desktop](#step-3--connect-in-power-bi-desktop)
6. [Step 4 — What is On-premises Data Gateway](#step-4--what-is-on-premises-data-gateway)
7. [Step 5 — Install &amp; Configure the Gateway](#step-5--install--configure-the-gateway)
8. [Step 6 — Schedule Dataset Refresh in Power BI Service](#step-6--schedule-dataset-refresh-in-power-bi-service)
9. [References](#references)

---

## Overview

Power BI can connect to **MariaDB/MySQL** for analysis and visualization.
When the database is **inside your local network (LAN)** or not exposed publicly, the **Power BI Service (cloud)** cannot connect directly.
To bridge this gap, we use the **On-premises Data Gateway**.

---

## Prerequisites

- **Power BI Desktop** installed[Download](https://powerbi.microsoft.com/desktop/)
- **MySQL Connector/NET (x64)** installed on the Power BI PC[Download](https://dev.mysql.com/downloads/connector/net/)
- **MariaDB Server** installed and accessible on LAN
- **Database credentials** with read access
- (For scheduled refresh) **On-premises Data Gateway** installed
  [Download](https://powerbi.microsoft.com/gateway/)

---

## Step 1 — Create a Read-only MariaDB User

We will create a new **read-only** account restricted to the Power BI PC’s LAN IP.

**Example:**

- **DB Server LAN IP:** `192.168.0.167`
- **DB Server Port:** `2241`
- **Power BI PC LAN IP:** `192.168.0.147`
- **Database Name:** `AI_CE_IMAGE`
- **Username:** `pbi_read`
- **Password:** `Strong_BI_Password!`

Run on the **DB server** as root:

```sql
CREATE USER 'pbi_read'@'192.168.0.147' IDENTIFIED BY 'Strong_BI_Password!';
GRANT SELECT, SHOW VIEW ON `AI_CE_IMAGE`.* TO 'pbi_read'@'192.168.0.147';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'pbi_read'@'192.168.0.147';
```

✅ This user can:

- Connect **only** from `192.168.0.147`
- Read all tables & views in `AI_CE_IMAGE`
- Cannot modify or delete any data

---

## Step 2 — Test MariaDB Connection from Power BI PC

On the **Power BI PC**, open a terminal (or PowerShell) and test:

```bash
mysql -h 192.168.0.167 -P 2241 -u pbi_read -p -D AI_CE_IMAGE
```

Enter the password and confirm you can run:

```sql
SHOW TABLES;
```

---

## Step 3 — Connect in Power BI Desktop

1. **Open Power BI Desktop**
2. **Get Data → More → Database → MySQL database**
3. Enter:
   - **Server**: `192.168.0.167:2241`
   - **Database**: `AI_CE_IMAGE`
4. Authentication: **Database**
   - Username: `pbi_read`
   - Password: `Strong_BI_Password!`
5. Click **OK**, select tables, and choose **Load** or **Transform Data**.

⚠ MySQL/MariaDB connections in Power BI Desktop use **Import Mode** (DirectQuery not supported).
For live updates, you’ll need **scheduled refresh** via a gateway.

---

## Step 4 — What is On-premises Data Gateway

The **On-premises Data Gateway** is a secure bridge that allows **Power BI Service** (cloud) to access data stored inside your local network or behind a firewall.

- **Without a Gateway**: Power BI Service cannot directly reach local MariaDB servers.
- **With a Gateway**: Power BI Service sends queries to the gateway, which retrieves the data from your LAN and returns it securely.

**More Info:**
[Microsoft Docs: What is an on-premises data gateway?](https://learn.microsoft.com/data-integration/gateway/service-gateway-onprem)

---

## Step 5 — Install & Configure the Gateway

1. Download the gateway:[On-premises Data Gateway Download](https://powerbi.microsoft.com/gateway/)
2. Install on a machine that:
   - Has access to `192.168.0.167:2241`
   - Stays on for scheduled refreshes
3. Sign in with your **Power BI account**
4. In Power BI Service (web):
   - Go to **Settings → Manage gateways**
   - Add a **New Data Source**:
     - Data Source Type: **MySQL**
     - Server: `192.168.0.167`
     - Port: `2241`
     - Database: `AI_CE_IMAGE`
     - Username: `pbi_read`
     - Password: `Strong_BI_Password!`

---

## Step 6 — Schedule Dataset Refresh in Power BI Service

1. Publish your report from Power BI Desktop to Power BI Service.
2. In Power BI Service:
   - Go to **Settings → Datasets → Scheduled refresh**
   - Turn **On**
   - Select your gateway
   - Set refresh frequency (e.g., daily/hourly)
3. Save settings.

---

## References

- [Power BI Desktop Download](https://powerbi.microsoft.com/desktop/)
- [MySQL Connector/NET Download](https://dev.mysql.com/downloads/connector/net/)
- [On-premises Data Gateway Download](https://powerbi.microsoft.com/gateway/)
- [MariaDB Documentation](https://mariadb.com/kb/en/)
- [Microsoft Docs: MySQL in Power BI](https://learn.microsoft.com/power-bi/connect-data/desktop-connect-mysql)
- [Microsoft Docs: On-premises Data Gateway](https://learn.microsoft.com/data-integration/gateway/service-gateway-onprem)

---

## Author Notes

This guide is based on a real-world setup connecting **Power BI** to a **MariaDB** instance over a LAN with secure, IP-bound, read-only credentials and automated refresh using the On-premises Data Gateway.
