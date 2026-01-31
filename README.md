# Smoky Bites Ordering System

## Setup

1. **Install Dependencies**
   ```bash
   pip install django
   ```

2. **Initialize Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Populate Menu Data**
   ```bash
   python populate.py
   ```

4. **Run Server**
   ```bash
   python manage.py runserver
   ```

5. **Access**
   Open http://127.0.0.1:8000/
   Mobile/QR View: Use Chrome DevTools (Toggle Device Toolbar) or scan QR if deployed.

## Admin
To create an admin user:
```bash
python manage.py createsuperuser
```
Access at http://127.0.0.1:8000/admin/
