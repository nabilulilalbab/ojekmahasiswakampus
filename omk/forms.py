from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone_number', 'firstLocation', 'lastLocation', 'messages']
        labels = {
            'customer_name': 'Nama Lengkap',
            'phone_number': 'Nomor WhatsApp',
            'firstLocation': 'Lokasi Jemput',
            'lastLocation': 'Lokasi Tujuan',
            'messages': 'Pesan Tambahan (Opsional)'
        }
        widgets = {
            'customer_name': forms.TextInput(
                attrs={
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                    'placeholder': 'Masukkan nama lengkap Anda'
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                    'placeholder': 'Format: 08xxxxxxxxxx'
                }
            ),
            'firstLocation': forms.TextInput(
                attrs={
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                    'placeholder': 'Lokasi penjemputan'
                }
            ),
            'lastLocation': forms.TextInput(
                attrs={
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                    'placeholder': 'Lokasi tujuan'
                }
            ),
            'messages': forms.Textarea(
                attrs={
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                    'rows': 3,
                    'placeholder': 'Contoh: Jemput di lobby, bawa helm sendiri, dll.'
                }
            )
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        phone = ''.join(filter(str.isdigit, phone))
        if not phone.startswith('08'):
            raise forms.ValidationError('Nomor harus diawali dengan 08')
        if len(phone) < 10 or len(phone) > 13:
            raise forms.ValidationError('Nomor telepon tidak valid')
        return phone
    def clean_distance(self):
        distance = self.cleaned_data.get('distance')
        if distance < 0:
            raise forms.ValidationError("Jarak tidak boleh negatif")
        return distance


class VoucherForm(forms.Form):
    voucher_code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Masukkan kode voucher (jika ada)'
            }
        )
    )
