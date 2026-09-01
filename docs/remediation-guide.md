# Vulnerability Remediation Guide

This guide provides technical remediation patterns for identified vulnerabilities in Express / Node.js web applications.

---

## 1. Remediation for SQL Injection (CWE-89)
**Vulnerable Pattern**:
```javascript
// BAD: Direct string concatenation
db.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email}' AND password = '${req.body.password}'`);
```

**Secure Pattern**:
```javascript
// GOOD: Prepared statements with parameters
db.sequelize.query(
  'SELECT * FROM Users WHERE email = :email AND password = :password',
  { replacements: { email: req.body.email, password: req.body.password }, type: QueryTypes.SELECT }
);
```

---

## 2. Remediation for Cross-Site Scripting (CWE-79)
**Vulnerable Pattern**:
```html
<!-- BAD: Direct innerHTML binding -->
<div [innerHTML]="searchQuery"></div>
```

**Secure Pattern**:
```html
<!-- GOOD: Safe text content interpolation -->
<div>{{ searchQuery }}</div>
```

---

## 3. Remediation for IDOR / Broken Access Control (CWE-639)
**Vulnerable Pattern**:
```javascript
// BAD: Trusting resource ID parameter without session ownership check
app.get('/rest/basket/:id', (req, res) => {
  Basket.findByPk(req.params.id).then(basket => res.json(basket));
});
```

**Secure Pattern**:
```javascript
// GOOD: Enforce session user ownership check
app.get('/rest/basket/:id', verifyToken, (req, res) => {
  Basket.findOne({ where: { id: req.params.id, UserId: req.user.id } })
    .then(basket => {
      if (!basket) return res.status(403).json({ error: 'Access Denied' });
      res.json(basket);
    });
});
```

---

## 4. Remediation for Missing Security Headers (CWE-693)
Configure `helmet` middleware in Express:
```javascript
const helmet = require('helmet');
app.use(helmet());
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"]
  }
}));
```
