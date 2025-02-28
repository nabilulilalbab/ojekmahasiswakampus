from django.db import models
from django.utils import timezone
from django.utils.http import urlencode
from ckeditor.fields import RichTextField
import math
from decimal import Decimal
class Event(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class Voucher(models.Model):
    code = models.CharField(max_length=20, unique=True)  # Kode voucher unik
    discount = models.DecimalField(max_digits=10, decimal_places=2)  # Besaran diskon
    discount_type = models.CharField(
        max_length=10,
        choices=[("percent", "Percent"), ("fixed", "Fixed")],
        default="percent"
    )  # Jenis diskon
    valid_from = models.DateTimeField()  # Mulai berlaku
    valid_to = models.DateTimeField()  # Berakhirnya voucher
    usage_limit = models.PositiveIntegerField(default=1)  # Batas pemakaian voucher (misal 1 kali per event)
    used_count = models.PositiveIntegerField(default=0)  # Jumlah pemakaian saat ini
    is_active = models.BooleanField(default=True)  # Status aktif voucher
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="vouchers",
        help_text="Event terkait voucher ini."
    )

    def is_valid(self):
        now = timezone.now()
        return (
                self.is_active and
                self.valid_from <= now <= self.valid_to and
                self.used_count < self.usage_limit
        )

    def use_voucher(self):
        if self.is_valid():
            self.used_count += 1
            if self.used_count >= self.usage_limit:
                self.is_active = False
            self.save()
            return True
        return False

    def __str__(self):
        tipe = "%" if self.discount_type == "percent" else "Rp"
        return f"{self.code} ({self.discount}{tipe})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="orders",
        help_text="Event terkait order ini."
    )
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, help_text="Nomor telepon customer.")
   
    # variable untuk lokasi penjemputan dan tujuan
    firstLocation = models.CharField(max_length=255, verbose_name="Lokasi Penjemputan")
    lastLocation = models.CharField(max_length=255, verbose_name="Lokasi Tujuan")

    messages = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    voucher = models.ForeignKey(
        Voucher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Voucher yang digunakan pada order ini."
    )
    distance = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00,
        verbose_name="Jarak (km)"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Harga Total"
    )
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def get_whatsapp_link(self):
        wa_number = "62882008809231"  # Ganti dengan nomor admin Anda

        # Buat pesan voucher jika ada
        voucher_text = ""
        if self.voucher:
            voucher_text = f"Voucher: {self.voucher.code}, Diskon: {self.discount_applied}"

        # Susun pesan utama
        message = (
            f"Halo, saya {self.customer_name}.\n"
            f"Saya ingin order dari *{self.firstLocation}* ke *{self.lastLocation}*.\n"
            f"Pesan tambahan: {self.messages if self.messages else '-'}\n"
            f"Status: {self.status}\n"
            f"{voucher_text}\n"
            f"Jarak: {self.distance}"
        )

        params = {"phone": wa_number, "text": message}
        return f"https://api.whatsapp.com/send?{urlencode(params)}"

    def apply_voucher(self):
        if self.voucher and self.voucher.is_valid():
            # Hitung ulang harga setelah diskon
            if self.voucher.discount_type == "percent":
                self.discount_applied = (self.voucher.discount / 100) * self.price
            else:
                self.discount_applied = min(
                    self.voucher.discount, 
                    self.price
                )
            
            # Harga akhir tidak bisa minus
            self.price = max(self.price - self.discount_applied, 0)
            self.voucher.use_voucher()
            self.save()

    def calculate_discount(self, discount_value, discount_type):
        total_amount = 100000  # Misal total order Rp100.000
        if discount_type == "percent":
            return (discount_value / 100) * total_amount
        return discount_value

    def save(self, *args, **kwargs):
        """Hitung harga otomatis berdasarkan jarak sebelum menyimpan"""
        if self.distance:
            # Hitung jumlah segmen 4 km (pembulatan ke atas)
            segmen = math.ceil(float(self.distance) / 4)
            self.price = Decimal(segmen) * Decimal('8500.00')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"



class BannerEvent(models.Model):
    name = models.CharField(max_length=100)
    describe = RichTextField()
    isActive = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
