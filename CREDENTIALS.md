# PAIMANA AI — Official Authentication Credentials

This document lists all pre-configured accounts, administrative credentials, and role permissions for the **Two-Role Model** (Admin & Employee).

---

## 1. Primary Statutory Seed Accounts

| Role | Officer / Designation | Official Email / Username | Password | Access Level & Permissions |
| :--- | :--- | :--- | :--- | :--- |
| **Admin** | MoSPI Registry Official | `admin@mospi.gov.in` | `Admin@MoSPI2026` | **Global & Administrative Access**: Full access to the Global Portfolio Overview (`/`), Registry Console (`/admin`), user provisioning, account management, and all operational tools. |
| **Employee** | Project Operations Associate | `employee@company.com` | `Employee@MoSPI2026` | **Operational Access**: Portfolio Overview (`/`), Central Directory (`/explorer`), Early Warning Alerts (`/alerts`), Project Dossiers, Methodology Audit (`/models`), and AI Copilot. **No access to Registry Console (`/admin`)**. |

---

## 2. Line Officers & Department Profiles (Role: `employee`)

All line officers operate with the **`employee`** operational clearance:

| Ministry / Department | Officer Name | Official Email | Standard Password | Role |
| :--- | :--- | :--- | :--- | :--- |
| **MoSPI / IPMD** | Dr. Rajesh Sharma, IAS | `rajesh.sharma@mospi.gov.in` | `Paimana@123` | `employee` |
| **MoSPI / IPMD (Nodal Desk)** | Dr. Rajesh Sharma, IAS | `nodal@mospi.gov.in` | `Nodal@MoSPI2026` | `employee` |
| **CAG Statutory Audit** | CAG Statutory Auditor | `auditor@mospi.gov.in` | `Auditor@MoSPI2026` | `employee` |
| **NHAI (Road Transport)** | Pooja Verma, IDAS | `p.verma@nhai.gov.in` | `Paimana@123` | `employee` |
| **Railways (Railway Board)** | Vikramaditya Sengupta | `v.sengupta@railnet.gov.in` | `Paimana@123` | `employee` |
| **NITI Aayog (DMEO)** | Dr. Ananya Iyer | `ananya.iyer@niti.gov.in` | `Paimana@123` | `employee` |
| **Simulation Sandbox** | V.3 Analytical Evaluator | `v.3@gmail.com` | `Paimana@123` | `employee` |

> **Note:** For any officer profile, `Paimana@123` is accepted as a standard fallback password.

---

## 3. Role-Based Access Control (RBAC) Matrix

| Feature / Module | Admin (`admin`) | Employee (`employee`) |
| :--- | :---: | :---: |
| **Global Portfolio Overview (`/`)** |  | ❌ *(Redirects to `/explorer`)* |
| **Central Registry Console (`/admin`)** |  | ❌ *(403 Forbidden / Hidden)* |
| **Provision New Officers** |  | ❌ *(Restricted)* |
| **Suspend / Activate Accounts** |  | ❌ *(Restricted)* |
| **Central Directory (`/explorer`)** |  |  *(Default Home)* |
| **Project Dossiers & S-Curves** |  |  |
| **Early Warning Alerts & Acknowledgments** |  |  |
| **Methodology Audit (`/models`)** |  |  |
| **Decision Intelligence AI Copilot** |  |  |
| **Report PDF / Briefing Export** |  |  |
| **Flash Report & CUF Data Import** |  |  |

---

## 4. How to Authenticate

### Web UI
1. Navigate to `/login` (or `/signin`).
2. Input any **Email / Username** and matching **Password** above.
3. Click **Sign In**.
   - **Admin** accounts land directly on the **Global Portfolio Overview** (`/`).
   - **Employee** accounts land directly on the **Central Directory** (`/explorer`).
