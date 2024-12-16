from django.db import models
import datetime

class User(models.Model):
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, default='N/A')
    email_id = models.CharField(max_length=500)
    position = models.CharField(max_length=100, default='Employee')
    department = models.CharField(max_length=100, default='None')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, default='No address provided')
    nationality = models.CharField(max_length=50, default='korea')
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    hire_date = models.DateField(null=True, default=datetime.date.today)
    resignation_date = models.DateField(null=True, blank=True)
    employment_status = models.CharField(
        max_length=20,
        choices=[('Active', 'Active'), ('On Leave', 'On Leave'), ('Resigned', 'Resigned')],
        default='Active'
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=3000)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vacation_days = models.IntegerField(default='12')
    emergency_contact_name = models.CharField(max_length=100, default='N/A')
    emergency_contact_phone = models.CharField(max_length=20, default='N/A')
    work_experience = models.TextField(null=True, blank=True)
    education_and_certifications = models.TextField(null=True, blank=True)
    permission = models.TextField(default=False)
    approval_date = models.DateField(null=True, blank=True)

    @classmethod
    def create_user(cls, username, email_id, phone_number, emergency_contact_phone, **extra_fields):
        user = cls(
            username=username,
            email_id=email_id,
            phone_number=phone_number,
            emergency_contact_phone=emergency_contact_phone,
            **extra_fields
        )
        user.save()
        return user

    class Meta:
        db_table = "user_info"

    def __str__(self):
        return f"User#{self.id}: {self.username}: {self.phone_number}: {self.email_id}: {self.position}"
