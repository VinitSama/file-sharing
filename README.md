# Postman Usage Guide for File Sharing System

SEE ON POSTMAN> 
[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/45745441-b9f1f287-1881-4c00-950e-8a3529dd2e72?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D45745441-b9f1f287-1881-4c00-950e-8a3529dd2e72%26entityType%3Dcollection%26workspaceId%3D4ba94815-a972-441e-858f-109f4f81c97d#?env%5BNew%20Environment%5D=W3sia2V5IjoiYmFzZV91cmwiLCJ2YWx1ZSI6Imh0dHBzOi8vZmlsZS1zaGFyaW5nLTRnZ3Iub25yZW5kZXIuY29tIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQiLCJzZXNzaW9uVmFsdWUiOiJodHRwczovL2ZpbGUtc2hhcmluZy00Z2dyLm9ucmVuZGVyLmNvbSIsImNvbXBsZXRlU2Vzc2lvblZhbHVlIjoiaHR0cHM6Ly9maWxlLXNoYXJpbmctNGdnci5vbnJlbmRlci5jb20iLCJzZXNzaW9uSW5kZXgiOjB9XQ==)

This project contains two main sets of API endpoints:

- **Client APIs**
- **Ops APIs**

Each section contains an `Authorized APIs` folder where authentication is required. Follow the steps below to use them correctly in **Postman**.

---

## Common Steps (For Both Client and Ops)

### 1. Sign Up
- Go to the `signup` API inside the relevant folder (`client/signup` or `ops/signup`).
- Set `email` and `password` in the **Body** (as JSON).
```json
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```

### 2. Email Verification
- After signup, a **verification email** is sent.
- Copy the **URL from the email** and paste it in the browser to verify your account.

### 3. Login
- Use the `login` API (`client/login` or `ops/login`).
- Set `email` and `password` in the **Body** (JSON).
- You will receive an **access token** in the response.

### 4. Set Access Token in Authorized Folder
- Copy the `access token` from the login response.
- In Postman, go to the **Authorized APIs folder**.
- Click the **Authorization** tab.
- Select `Bearer Token`.
- Paste your token in the **Token** field.

---

## Client API Section

### Authorized APIs in `Client APIs > Authorized APIs`

#### 1. File List API
- Returns a list of all files available.
- Each file includes:
  - `id`
  - `optionID`
  - `filename`
  - `uploaded_by`

#### 2. Get File Download URL
- Use the **optionID** from the previous API.
- Replace `/{option_id}` in the URL with the actual option ID.
- Response returns an encrypted **download URL**.

#### 3. Download File
- Copy the download URL from the previous step.
- Paste it into the **URL field** of Postman.
- Click **Send and Download** to download the file.

---

## Ops API Section

### Authorized APIs in `Ops APIs > Authorized APIs`

#### 1. Upload File API
- Go to the `upload` API.
- In **Body**, select `form-data`.
- Add a new key named `file`, set its type to `File`, and upload the desired `.pptx`, `.docx`, or `.xlsx` file.

---