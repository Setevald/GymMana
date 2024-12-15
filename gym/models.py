import uuid
from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Banners(models.Model):
	img=models.ImageField(upload_to="banners/")
	alt_text=models.CharField(max_length=500)

	class Meta:
		verbose_name_plural='Banners'

	def __str__(self):
		return self.alt_text

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.img.url))

class User(AbstractUser):
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

# Membership profile    
class Membership(models.Model):
    membership_id = models.CharField(max_length=50, primary_key=True)
    membership_name = models.CharField(max_length=100)
    monthly_fee = models.IntegerField(default=400000)

    def __str__(self):
        return self.membership_name
    
# Promotional model
class Promotional(models.Model):
    promotional_id = models.CharField(max_length=50, primary_key=True)
    promotional_name = models.CharField(max_length=100)
    description = models.TextField()
    promotional_start_date = models.DateField()
    promotional_end_date = models.DateField()
    discount_percentage = models.IntegerField()

    def __str__(self):
        return self.promotional_name

# Transaction model
class Transaction(models.Model):
    transaction_id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    promotional = models.ForeignKey(Promotional, on_delete=models.CASCADE, null=True, blank=True)
    membership_start_date = models.DateField()
    membership_end_date = models.DateField()

    def __str__(self):
        return f"Transaction {self.transaction_id} by {self.user.user_name}"
    
# Equipment model
class Equipment(models.Model):
    equipment_id = models.CharField(max_length=50, primary_key=True)
    equipment_name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    cost = models.IntegerField()
    purchase_date = models.DateField()
    condition = models.CharField(max_length=50)
    maintenance = models.ForeignKey("Maintenance", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.equipment_name
    
# Maintanance model
class Maintenance(models.Model):
    maintenance_id = models.CharField(max_length=50, primary_key=True)
    maintenance_date = models.DateField()
    maintenance_type = models.CharField(max_length=50)
    technician_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Maintenance {self.maintenance_id}"
    
# Trainer model
class Trainer(models.Model):
    trainer_id = models.CharField(max_length=50, primary_key=True)
    trainer_name = models.CharField(max_length=100)
    trainer_specialty = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    trainer_fee = models.IntegerField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.trainer_name

# Classes model
class Classes(models.Model):
    class_id = models.CharField(max_length=50, primary_key=True, default='', editable=False)
    class_name = models.CharField(max_length=100)
    class_schedule = models.DateField()
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.class_id:  # If class_id is not set, generate it
            self.class_id = f"CLASS-{uuid.uuid4().hex[:6].upper()}"  # Generate unique ID
        super().save(*args, **kwargs)

    def __str__(self):
        return self.class_name

# Transaction Detail model
class TransactionDetail(models.Model):
    transaction_detail_id = models.CharField(max_length=50, primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    class_info = models.ForeignKey(Classes, on_delete=models.CASCADE, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Detail {self.transaction_detail_id} for Transaction {self.transaction.transaction_id}"
    
