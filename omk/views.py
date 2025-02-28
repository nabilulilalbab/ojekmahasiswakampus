from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import Order, Voucher, Event, BannerEvent
from .forms import OrderForm, VoucherForm
from django.conf import settings

class HomeView(TemplateView):
    template_name = 'omk/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['benefits'] = [
            {
                'icon': 'money-bill-1-wave',
                'title': 'Harga Terjangkau',
                'description': 'Tarif khusus untuk mahasiswa dengan budget terbatas'
            },
            {
                'icon': 'shield',
                'title': 'Privasi Terjamin',
                'description': 'Nomor WhatsApp terlindungi oleh sistem perantara kami'
            },
            {
                'icon': 'bolt',
                'title': 'Cepat & Andal',
                'description': 'Driver mahasiswa siap antar jemput di sekitar kampus'
            },
            {
                'icon': 'ticket',
                'title': 'Voucher Diskon',
                'description': 'Dapatkan potongan harga untuk pengguna baru'
            }
        ]
        context['testimonials'] = [
            {
                'name': 'Anisa S.',
                'campus': 'Universitas Indonesia',
                'text': 'Sangat membantu saat saya terburu-buru ke kampus. Driver ramah dan tepat waktu!'
            },
            {
                'name': 'Budi H.',
                'campus': 'Universitas Gadjah Mada',
                'text': 'Harganya cocok untuk kantong mahasiswa, dan prosesnya sangat cepat.'
            }
        ]
        banner = BannerEvent.objects.filter(isActive=True).first()
        context['bannerevent'] = []
        if banner:
            context['bannerevent'] = [{
                'name': banner.name,
                'describe': banner.describe,  # Pastikan key 'describe' sesuai template
            }]
        return context

class OrderCreateView(CreateView):
    template_name = 'omk/order_form.html'
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('omk:order_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voucher_form'] = VoucherForm()
        context['OPENROUTE_API_KEY'] = settings.OPENROUTE_API_KEY
        print("Template context:", context)  # Debug print
        return context

    def get_current_event(self):
        """Mengembalikan event aktif berdasarkan tanggal saat ini."""
        now = timezone.now()
        return Event.objects.filter(start_date__lte=now, end_date__gte=now).first()

    def form_valid(self, form):
        order = form.save(commit=False)
        current_event = self.get_current_event()
        if not current_event:
            messages.error(self.request, "Tidak ada event yang aktif saat ini.")
            return redirect(self.success_url)
        order.event = current_event
        order.save()

        voucher_code = self.request.POST.get('voucher_code')
        if voucher_code:
            try:
                # Cari voucher berdasarkan kode dan event aktif
                voucher = Voucher.objects.get(code=voucher_code, event=current_event)
                if voucher.is_valid():
                    order.voucher = voucher
                    order.save()
                    try:
                        order.apply_voucher()  # Di sini validasi penggunaan voucher (misalnya hanya sekali per event)
                        messages.success(self.request, f'Voucher {voucher_code} berhasil digunakan! Diskon: {order.discount_applied}')
                    except ValueError as e:
                        messages.error(self.request, str(e))
                        # Jika terjadi error (misalnya voucher sudah pernah digunakan), hapus voucher dari order
                        order.voucher = None
                        order.save()
                else:
                    messages.error(self.request, 'Voucher tidak valid atau sudah kadaluarsa!')
            except Voucher.DoesNotExist:
                messages.error(self.request, 'Kode voucher tidak ditemukan untuk event ini!')
        order.save()
        self.request.session['order_id'] = order.id
        return redirect(self.success_url)


class OrderSuccessView(TemplateView):
    template_name = 'omk/order_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('order_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                context['order'] = order
                context['whatsapp_link'] = order.get_whatsapp_link()
            except Order.DoesNotExist:
                context['error'] = 'Order tidak ditemukan'
        else:
            context['error'] = 'Tidak ada informasi order'
        return context


class CheckVoucherView(FormView):
    """AJAX view untuk mengecek validitas voucher pada event aktif."""
    form_class = VoucherForm

    def get_current_event(self):
        now = timezone.now()
        return Event.objects.filter(start_date__lte=now, end_date__gte=now).first()

    def form_valid(self, form):
        voucher_code = form.cleaned_data.get('voucher_code')
        current_event = self.get_current_event()
        if not current_event:
            return JsonResponse({
                'valid': False,
                'message': 'Tidak ada event aktif saat ini.'
            })
        try:
            voucher = Voucher.objects.get(code=voucher_code, event=current_event)
            if voucher.is_valid():
                return JsonResponse({
                    'valid': True,
                    'message': 'Voucher valid!',
                    'discount': str(voucher.discount),
                    'discount_type': voucher.discount_type
                })
            else:
                return JsonResponse({
                    'valid': False,
                    'message': 'Voucher sudah tidak berlaku atau mencapai batas penggunaan'
                })
        except Voucher.DoesNotExist:
            return JsonResponse({
                'valid': False,
                'message': 'Kode voucher tidak ditemukan untuk event ini'
            })

    def form_invalid(self, form):
        return JsonResponse({
            'valid': False,
            'message': 'Form tidak valid'
        })

