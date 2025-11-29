# Payment Setup Instructions

## 📱 Customizing Payment Details

The checkout page (`app/templates/cart/checkout.html`) shows payment instructions for JazzCash/EasyPaisa and Bank Transfer. You need to update these with your actual details:

### 1. JazzCash/EasyPaisa Details (Lines 60-67)

Replace the placeholder numbers with your actual mobile wallet numbers:

```html
<p class="mb-2"><strong>Account Title:</strong> Your Business Name</p>
<p class="mb-2"><strong>JazzCash Number:</strong> 03XX-XXXXXXX</p>
<p class="mb-2"><strong>EasyPaisa Number:</strong> 03XX-XXXXXXX</p>
```

And update the WhatsApp contact:
```html
After placing order, please send payment screenshot to our WhatsApp: <strong>03XX-XXXXXXX</strong>
```

### 2. Bank Transfer Details (Lines 71-78)

Replace with your actual bank account information:

```html
<p class="mb-2"><strong>Bank Name:</strong> HBL / Meezan Bank</p>
<p class="mb-2"><strong>Account Title:</strong> Your Business Name</p>
<p class="mb-2"><strong>Account Number:</strong> XXXX-XXXX-XXXX-XXXX</p>
<p class="mb-2"><strong>IBAN:</strong> PK XX XXXX XXXX XXXX XXXX XXXX XXXX</p>
```

And update the email:
```html
After placing order, please send payment receipt to: <strong>your-email@example.com</strong>
```

## 🔄 How It Works

1. **Customer selects payment method** during checkout
2. **For COD**: Order is placed directly, no payment needed upfront
3. **For JazzCash/EasyPaisa/Bank Transfer**: 
   - Customer sees your payment details
   - Customer completes payment
   - Customer sends proof (screenshot/receipt) to your WhatsApp/Email
   - You verify payment and update order status in Admin Dashboard

## 🎯 Future Integration Options

If you want to integrate actual payment APIs later:

### JazzCash Integration
- Sign up for JazzCash Merchant Account
- Get API credentials
- Use their REST API for payment processing
- Documentation: Contact JazzCash Business Support

### EasyPaisa Integration
- Apply for EasyPaisa Merchant Account
- Get API access
- Integrate using their SDK
- Documentation: Contact Telenor Microfinance Bank

### Alternative: Payfast.pk
- Pakistani payment gateway
- Supports cards, mobile wallets
- Easier integration than individual wallets
- Website: https://www.payfast.pk/

---

**Current Setup**: Manual verification (most common for small businesses in Pakistan)
**Benefit**: Works immediately, no merchant account needed
**Process**: Customer pays → sends proof → you verify → ship order
