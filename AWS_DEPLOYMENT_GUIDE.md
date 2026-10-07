# AWS Cloud Deployment & S3 Storage Guide

This guide details the step-by-step procedure to deploy the **AI Investment Research Assistant (Theme 15)** to **Amazon Web Services (AWS)** using **EC2** for application hosting, **S3** for persistent cloud document storage, and **Docker Compose** for container orchestration.

---

## 1. Cloud Architecture Overview

```
                      ┌────────────────────────────────────────┐
                      │             User / Analyst             │
                      └──────────────────┬─────────────────────┘
                                         │ Port 8501 (HTTP)
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ AWS EC2 Instance (Ubuntu 22.04 LTS, t3.medium)                               │
│                                                                              │
│   ┌──────────────────────────────────────────────────────────────────────┐   │
│   │ Docker Container: investment_research_app                            │   │
│   │                                                                      │   │
│   │   ┌─────────────────────┐          ┌───────────────────────────┐     │   │
│   │   │ Streamlit Frontend  │ ◄──────► │ Multi-Agent Workflow      │     │   │
│   │   │ (Ingestion/Analysis)│          │ (LangGraph Engine)        │     │   │
│   │   └─────────────────────┘          └─────────────┬─────────────┘     │   │
│   │              ▲                                   │                   │   │
│   │              │                                   ▼                   │   │
│   │   ┌──────────┴──────────┐          ┌───────────────────────────┐     │   │
│   │   │ Local Persistent    │          │ External Market Tooling   │     │   │
│   │   │ Vector Store        │          │ (yfinance + Google Gemini)│     │   │
│   │   │ (/workspace/data/)  │          └───────────────────────────┘     │   │
│   │   └─────────────────────┘                                            │   │
│   └────────────────────────────────────┬─────────────────────────────────┘   │
└────────────────────────────────────────┼─────────────────────────────────────┘
                                         │ Boto3 (HTTPS / AWS IAM)
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ AWS S3 Bucket (e.g., ai-investment-research-repo)                            │
│   ├── /filings/     -> Raw 10-K, 10-Q & Analyst PDF Documents               │
│   └── /reports/     -> Certified Investment Memoranda & Markdown Reports    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Part 1: AWS S3 Bucket & IAM Setup

### Step 1.1: Create S3 Bucket
1. Open the **AWS Management Console** and navigate to **Amazon S3**.
2. Click **Create bucket**.
3. Configure settings:
   - **Bucket name:** `ai-investment-research-repo` (or a globally unique name like `ai-investment-research-student-<unique-id>`).
   - **AWS Region:** Select `us-east-1` (US East, N. Virginia) or your preferred region.
   - **Block Public Access:** Keep **Block all public access** checked (access is securely managed via IAM keys).
   - **Bucket Versioning:** Optional / Enabled.
4. Click **Create bucket**.

### Step 1.2: Create IAM User & Access Keys
1. Navigate to **IAM** (Identity and Access Management) in the AWS Console.
2. Go to **Users** ➔ Click **Create user**.
   - Username: `investment-research-app-user`
3. Under **Set permissions**, choose **Attach policies directly**.
   - Attach policy: `AmazonS3FullAccess` (or create a custom policy restricting to your specific bucket).
4. Complete user creation.
5. Click on the created user ➔ Go to the **Security credentials** tab.
6. Under **Access keys**, click **Create access key**.
   - Use case: Choose **Application running outside AWS** or **Other**.
7. Download / copy your credentials:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

---

## 3. Part 2: AWS EC2 Instance Launch

### Step 2.1: Launch Instance
1. In the AWS Console, navigate to **EC2** ➔ Click **Launch instance**.
2. Configure instance details:
   - **Name:** `ai-investment-research-server`
   - **AMI (Operating System):** **Ubuntu Server 22.04 LTS (HVM), SSD Volume Type** (64-bit x86).
   - **Instance Type:** `t3.medium` (2 vCPU, 4 GiB Memory) or `t3.small` (2 vCPU, 2 GiB Memory).
   - **Key Pair:** Select an existing `.pem` key pair or click **Create new key pair** (e.g. `research-key.pem`).
   - **Storage:** Increase Root volume to **20 GiB (gp3)** to ensure ample space for Docker images, vector storage, and OS libraries.

### Step 2.2: Configure Security Group (Firewall)
In the **Network settings** section, ensure the Security Group has the following inbound rules:

| Type | Protocol | Port Range | Source | Purpose |
| :--- | :---: | :---: | :---: | :--- |
| **SSH** | TCP | `22` | `My IP` (or `0.0.0.0/0`) | Secure Terminal Access |
| **Custom TCP** | TCP | `8501` | `0.0.0.0/0` (Anywhere IPv4) | **Streamlit Application Access** |
| **HTTP** | TCP | `80` | `0.0.0.0/0` | Optional Web Access |

3. Click **Launch instance**.

---

## 4. Part 3: Deploying the Application to EC2

### Step 3.1: Connect to your EC2 Instance
Open your local terminal and connect via SSH:

```bash
chmod 400 research-key.pem
ssh -i "research-key.pem" ubuntu@<YOUR_EC2_PUBLIC_IP>
```

### Step 3.2: Clone the Project Repository
```bash
git clone https://github.com/SagarTrimukhe/ai-investment-research-assistant.git
cd ai-investment-research-assistant
```

### Step 3.3: Configure Environment Variables
```bash
cp .env.example .env
nano .env
```
Fill in your active keys in `.env`:
```ini
GEMINI_API_KEY=your_actual_gemini_api_key
AWS_ACCESS_KEY_ID=your_actual_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_actual_aws_secret_access_key
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=ai-investment-research-repo
```
Save and exit (`Ctrl + O`, `Enter`, `Ctrl + X`).

### Step 3.4: One-Command Provisioning & Docker Launch
Run the automated EC2 setup script:
```bash
chmod +x scripts/setup_ec2.sh
./scripts/setup_ec2.sh
```

This script automatically:
1. Updates all Ubuntu packages.
2. Configures a 2GB Swap file (protects `t3.small` / `t3.medium` instances from memory spikes).
3. Installs Docker Engine and Docker Compose.
4. Mounts persistent directories for ChromaDB and data folders.
5. Builds and launches the container in the background (`docker compose up -d --build`).

---

## 5. Part 4: Verification & S3 Connectivity Test

### Step 4.1: Test S3 Integration
Run the built-in diagnostic test inside the instance:
```bash
python3 scripts/test_aws_s3.py
```
Expected output:
```
============================================================
  AWS S3 Cloud Storage Diagnostic & Verification Test
============================================================
Bucket Name:       ai-investment-research-repo
AWS Region:        us-east-1
[+] Attempting connection to AWS S3...
[+] Uploading test payload to s3://...
    -> Upload successful!
[+] Listing objects under 'diagnostics/' prefix...
    -> Found 1 object(s) in S3 bucket.
[+] Downloading test object from S3 to local temporary file...
    -> Verification passed! Downloaded bytes match uploaded payload.
[+] Cleaned up temporary test object.
============================================================
  ALL AWS S3 STORAGE TESTS PASSED SUCCESSFULLY!
============================================================
```

### Step 4.2: Access the Live Dashboard
Open your browser and navigate to:
👉 **`http://<YOUR_EC2_PUBLIC_IP>:8501`**

- In **Document Ingestion**: Upload a document to index into ChromaDB and archive directly to AWS S3.
- In **Research & Analysis**: Execute the multi-agent workflow.
- In **Analyst Review (HITL)**: Certify the investment thesis and click **"Archive Memorandum to AWS S3"**.

---

## 6. Part 5: Required Capstone Evidence & Screenshots

Capture the following 4 screenshots for your Final Report and Presentation:

1. **AWS EC2 Management Console**: Showing your running EC2 instance (`t3.medium`), Public IPv4 address, and `2/2 checks passed` status.
2. **AWS S3 Console**: Showing your S3 bucket (`ai-investment-research-repo`) with the `/filings/` and `/reports/` folders containing uploaded files.
3. **AWS Security Group Inbound Rules**: Showing port `8501` and port `22` open.
4. **Live Streamlit Web Application**: Browser address bar displaying `http://<EC2_PUBLIC_IP>:8501` with the active dashboard and multi-agent execution results.

---

## 7. Useful Operational Commands

```bash
# Check running containers
sudo docker ps

# View live application logs
sudo docker compose logs -f

# Restart application
sudo docker compose restart

# Stop application
sudo docker compose down
```
