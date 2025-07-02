import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.timezone import now
from .models import QRCode, ScanRecord
from .forms import QRCodeForm
from user_agents import parse


def index(request):
    form = QRCodeForm()
    return render(request, 'index.html', {'form': form})
def generate_qr_code(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            password = form.cleaned_data['password']
            expires_at = form.cleaned_data['expires_at']

            # Generate QR Code
            qr = qrcode.make(f"{request.build_absolute_uri('/scan/')}?code={data}")
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Save to database
            qr_code = QRCode.objects.create(
                data=data,
                qr_code_image=qr_image,
                password=password,
                expires_at=expires_at
            )

            return render(request, 'qr_code_result.html', {'qr_image': qr_image, 'qr_code': qr_code})

    return render(request, 'index.html', {'form': form})

def scan_qr_code(request):
    code = request.GET.get('code', '')
    qr_code = get_object_or_404(QRCode, data=code)

    # Expiration Check
    if qr_code.is_expired():
        return HttpResponse("This QR code has expired.")

    # Password Protection
    if qr_code.password:
        entered_password = request.GET.get('password', '')
        if entered_password != qr_code.password:
            return render(request, 'password_prompt.html', {'qr_code': qr_code})

    # Tracking User Info
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    device_type = "Mobile" if user_agent.is_mobile else "Desktop" if user_agent.is_pc else "Tablet"
    ip_address = request.META.get('REMOTE_ADDR', '')

    ScanRecord.objects.create(
        qr_code=qr_code,
        ip_address=ip_address,
        location=ScanRecord.get_location(ip_address),
        device_type=device_type
    )

    # Increment Scan Count
    qr_code.scan_count += 1
    qr_code.save()

    return HttpResponse(f"QR Code Scanned Successfully! Data: {qr_code.data}")


#
# def generate_qr_code(request):
#     if request.method == 'POST':
#         form = QRCodeForm(request.POST)
#         if form.is_valid():
#             qr_code_type = form.cleaned_data['qr_code_type']
#             data = form.cleaned_data['data']
#
#             if qr_code_type == 'simple':
#                 qr = qrcode.make(data)
#                 buffer = BytesIO()
#                 qr.save(buffer, format='PNG')
#                 qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
#
#                 return render(request, 'qr_code_result.html', {
#                     'qr_image': qr_image,
#                     'data': data
#                 })
#
#             elif qr_code_type == 'animated':
#                 # Encode the text as a URL pointing to your local endpoint
#                 encoded_text = request.build_absolute_uri(f"/animated_qr/?text={data.replace(' ', '%20')}")
#                 qr = qrcode.make(encoded_text)
#                 buffer = BytesIO()
#                 qr.save(buffer, format='PNG')
#                 qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
#
#                 return render(request, 'animated_qr_code_result.html', {
#                     'qr_image': qr_image,
#                     'data': data
#                 })
#
#     return render(request, 'index.html', {'form': form})
#
# # View to display the animated text
#
def video_display(request):
    text = request.GET.get('text', 'Video for your text')
    return render(request, 'video_display.html', {'data': text})


# View to display the animated text
def animated_qr(request):
    text = request.GET.get('text', 'Animated QR Code')
    return render(request, 'animated_text_display.html', {'data': text})

def download_qr_code(request, data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="qr_code.png"'
    return response
