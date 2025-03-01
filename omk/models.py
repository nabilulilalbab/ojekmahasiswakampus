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
        formatted_price = f"{self.price:,.0f}".replace(",", ".")
        formatted_distance = f"{float(self.distance):.2f}".replace(".", ",")

        # Format pesan voucher
        voucher_text = ""
        if self.voucher:
            formatted_discount = f"{self.discount_applied:,.0f}".replace(",", ".")
            original_price = self.price + self.discount_applied
            formatted_original = f"{original_price:,.0f}".replace(",", ".")
        
            voucher_text = (
                f"✉️ *Voucher Terpakai:*\n"
                f"- Kode: {self.voucher.code}\n"
                f"- Diskon: Rp {formatted_discount}\n"
                f"💵 *Harga Awal:* Rp {formatted_original}\n"
                f"🎁 *Diskon:* Rp {formatted_discount}\n"
            )

        # Susun pesan utama
        message = (
            f"*PESANAN BARU*\n\n"
            f"👤 *Nama:* {self.customer_name}\n"
            f"📱 *Nomor HP:* {self.phone_number}\n\n"
            f"📍 *Lokasi Penjemputan:*\n{self.firstLocation}\n\n"
            f"🎯 *Lokasi Tujuan:*\n{self.lastLocation}\n\n"
            f"📏 *Jarak Tempuh:* {formatted_distance} km\n"
            f"💸 *Harga Akhir:* Rp {formatted_price}\n\n"
            f"{voucher_text if self.voucher else ''}"
            f"📝 *Catatan Tambahan:*\n{self.messages if self.messages else '-'}\n\n"
            f"🔄 *Status Pesanan:* {self.status.upper()}"
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
        """Hitung harga berdasarkan aturan baru"""
        if self.distance:
            distance = float(self.distance)
            if distance <= 4:
                self.price = Decimal('8500.00')
            else:
                # Hitung km tambahan (dibulatkan ke atas)
                additional_km = math.ceil(distance - 4)
                # Harga per km = 8500 / 4 = 2125
                self.price = Decimal('8500.00') + (Decimal(additional_km) * Decimal('2125.00'))
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
