from home.models import User

email = "admin@udyogrefer.com"
username = "SuperAdmin"
password = "Admin@123"

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        username=username,
        password=password,
        role="admin",
        is_verified=True,
    )
    print("Superadmin created successfully.")
else:
    print("Superadmin already exists.")
