from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .forms import OrderForm
import requests
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

VERIFY_TOKEN = 'azambot_token'
PAGE_ACCESS_TOKEN = 'EAAKlQHUcJtIBOymAqhCZAyoZAE1UZBZAKf9VVVA9BygQEccyTw5va61OFKtfHItXNpTgoDWhtUhhvX7wlSLhAzZBW3stwfWHHZAx6jBLxjmpqLRaH1FmdEFkO6OZAAqQ0VFdwhZBmPOoUZCw5xjDuteCYRrDmkT6DZAmJhlUxocjJxfZAvRLRRA6QhafJ7jis974mOKj8RGUA5ykVUoUjR6ULRRT2fazMW22rsgKCeuYrJBD4QEJqkZD'  # Bu yerga real tokenni qo'y

# ✅ Javob yuboruvchi funksiya
def send_instagram_message(user_id, text):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {'Content-Type': 'application/json'}
    data = {
        'recipient': {'id': user_id},
        'message': {'text': text}
    }
    response = requests.post(url, headers=headers, json=data)
    print("✅ Yuborildi:", response.status_code, response.text)

# ✅ Webhook uchun asosiy funksiya
@csrf_exempt
def instagram_webhook(request):
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse('Verify token noto‘g‘ri', status=403)

    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print("📩 Yangi xabar keldi:", json.dumps(data, indent=2))

        for entry in data.get('entry', []):
            for messaging in entry.get('messaging', []):
                sender_id = messaging['sender']['id']
                message = messaging.get('message', {}).get('text', '')

                print(f"👤 Kimdan: {sender_id}, ✉️ Xabar: {message}")

                # Auto-reply logika
                if 'salom' in message.lower():
                    reply_text = "Salom! BZA Osh Markaziga xush kelibsiz!"
                elif 'menyu' in message.lower():
                    reply_text = "Menyuni bu yerda ko‘rishingiz mumkin: https://bzaosh.uz/menu"
                elif 'raqam' in message.lower():
                    reply_text = "Bizning telefon raqam: +998 90 123 45 67"
                else:
                    reply_text = "Rahmat! Xabaringiz qabul qilindi. Tez orada javob beramiz."

                send_instagram_message(sender_id, reply_text)

        return HttpResponse("OK", status=200)

    return HttpResponse('Noto‘g‘ri so‘rov turi', status=400)

# ✅ Buyurtma formasi
def book_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book')
    else:
        form = OrderForm()
    return render(request, 'book.html', {'form': form})

# ✅ Admin panel ko‘rinishi
def panel_view(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'panel.html', {'orders': orders})

# ✅ Buyurtmani tasdiqlash
def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'tasdiqlandi'
    order.save()
    return redirect('panel')

# ✅ Buyurtmani bekor qilish
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'bekor_qilindi'
    order.save()
    return redirect('panel')
