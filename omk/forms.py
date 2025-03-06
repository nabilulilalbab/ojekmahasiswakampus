from django import forms
from .models import Order,Feedback

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone_number', 'firstLocation', 'lastLocation', 'messages', 'pickup_time']
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
                    'class': 'form-input w-full px-4 py-3 bg-white text-gray-700 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-200',
                    'placeholder': 'Masukkan nama lengkap Anda'
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-input w-full px-4 py-3 bg-white text-gray-700 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-200',
                    'placeholder': 'Format: 08xxxxxxxxxx'
                }
            ),
            'firstLocation': forms.TextInput(
                attrs={
                    'class': 'form-input w-full px-4 py-3 bg-white text-gray-700 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-200',
                    'placeholder': 'Lokasi penjemputan'
                }
            ),
            'lastLocation': forms.TextInput(
                attrs={
                    'class': 'form-input w-full px-4 py-3 bg-white text-gray-700 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-200',
                    'placeholder': 'Lokasi tujuan'
                }
            ),
            'pickup_time': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'class': 'form-input w-full px-4 py-3 bg-white text-gray-700 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-200',
                    'type': 'time',
                }
            ),
            'messages': forms.Textarea(
                attrs={
                    'class': 'form-input w-full px-4 py-3 bg-white text-gray-700 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-200',
                    'rows': 3,
                    'placeholder': 'Contoh: Jemput di lobby, bawa helm sendiri, dll.'
                }
            ),
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
                'class': 'form-input w-full px-4 py-3 bg-white text-gray-700 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-200',
                'placeholder': 'Masukkan kode voucher (jika ada)'
            }
        )
    )

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'animate__animated animate__fadeInRight border-2 border-[#60B0E5] focus:border-[#372B82] rounded-lg p-3 w-full transition-colors',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'animate__animated animate__fadeInRight border-2 border-[#60B0E5] focus:border-[#372B82] rounded-lg p-3 w-full transition-colors',
            }),
            'message': forms.Textarea(attrs={
                'class': 'animate__animated animate__fadeInRight border-2 border-[#60B0E5] focus:border-[#372B82] rounded-lg p-3 w-full h-32 transition-colors',
                'rows': 5
            }),
        }
