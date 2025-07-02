from django import forms

class QRCodeForm(forms.Form):
    qr_code_type = forms.ChoiceField(
        choices=[('simple', 'Simple QR Code'), ('animated', 'Animated QR Code')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    data = forms.CharField(
        label='Enter Text / URL / Contact Details',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    password = forms.CharField(
        label='Set Password (Optional)',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    expires_at = forms.DateTimeField(
        label='Set Expiration Time (Optional)',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=False
    )
