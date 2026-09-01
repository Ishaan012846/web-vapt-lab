# Manual Web Application Testing Guide

This guide outlines reproducible manual testing procedures using Burp Suite Community Edition against the OWASP Juice Shop local lab (`http://127.0.0.1:3000`).

---

## 1. SQL Injection (SQLi)
- **Target Endpoint**: `POST /rest/user/login`
- **Objective**: Test for parameter concatenation in SQL queries.
- **Procedure**:
  1. Capture the login POST request in Burp Repeater.
  2. Modify the JSON body:
     ```json
     {
       "email": "' OR 1=1--",
       "password": "password"
     }
     ```
  3. Send request and observe HTTP 200 OK containing an administrative authentication token.

---

## 2. Cross-Site Scripting (XSS)
- **Target Endpoint**: `GET /#/search?q=`
- **Objective**: Validate DOM-based and reflected payload execution.
- **Procedure**:
  1. Submit search query containing `<iframe src="javascript:alert(1)">` or `<script>console.log(1)</script>`.
  2. Inspect the DOM element to verify unescaped reflection.

---

## 3. Broken Access Control & IDOR
- **Target Endpoint**: `GET /rest/basket/{id}`
- **Objective**: Verify whether authorization is enforced per resource ID.
- **Procedure**:
  1. Authenticate as User A (assigned Basket ID 1).
  2. Change the path parameter to `GET /rest/basket/2`.
  3. Confirm if Basket 2 contents (belonging to User B) are returned.

---

## 4. Authentication & Session Management
- **Objective**: Evaluate session token entropy, expiration, and storage.
- **Procedure**:
  1. Inspect JWT session tokens issued upon login.
  2. Decode header/payload at jwt.io to check algorithm (`"alg": "HS256"`) and expiration (`exp`).

---

## 5. Cross-Site Request Forgery (CSRF)
- **Target Endpoint**: Profile state-changing endpoints
- **Objective**: Test presence of custom headers or anti-CSRF tokens.
- **Procedure**:
  1. Verify if POST/PUT requests accept requests without custom authorization headers or SameSite cookie protection.

---

## 6. Security Headers & Configuration
- **Objective**: Audit HTTP response headers.
- **Procedure**:
  1. Send GET request to `http://127.0.0.1:3000/`.
  2. Confirm presence/absence of:
     - `Content-Security-Policy`
     - `Strict-Transport-Security`
     - `X-Content-Type-Options`
     - `X-Frame-Options`

---

## 7. Sensitive Data Exposure
- **Objective**: Verify error handling and stack trace suppression.
- **Procedure**:
  1. Send malformed parameters (e.g. `GET /rest/products/search?q='`).
  2. Inspect HTTP 500 responses for internal stack traces or database connection strings.

---

## 8. Outdated & Vulnerable Components
- **Objective**: Audit front-end and back-end third-party libraries.
- **Procedure**:
  1. Check client-side JS bundles in browser Developer Tools for legacy Angular or jQuery versions.
