from home.models import User

email = "admin@udyogrefer.com"
password = "Admin@123"
username = "SuperAdmin"

if not User.objects.filter(email=email).exists():
    print("Creating superuser...")
    User.objects.create_superuser(
        email=email,
        username=username,
        password=password,
        name="Admin",      # important if your model requires name
        role="admin"
    )
else:
    print("Superuser already exists.")
