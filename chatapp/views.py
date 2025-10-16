from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import JsonResponse
from .models import Room, Message, Notification
from .utils import get_online_users
from django.views.decorators.http import require_POST
from .blockchain import blockchain_instance
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os
from django.conf import settings




def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request, room_name=None):
    list(messages.get_messages(request))

    users = User.objects.all()
    rooms = Room.objects.all()
    online_usernames = []  # populate using get_online_users() if available
    request_user = request.user
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    blocks = blockchain_instance.to_list()  # <-- Add blockchain to context

    if request.method == "POST":
        room_name_form = request.POST.get('room', '').strip()
        pin = request.POST.get('pin', '').strip()

        room = Room.objects.filter(room_name=room_name_form).first()

        if room:
            if room.room_pin and not room.check_pin(pin):
                messages.error(request, "Incorrect PIN for the room.")
                return redirect('dashboard_with_room', room_name=room_name_form)

            request.session[f'pin_verified_{room_name_form}'] = True
            blockchain_instance.add_block({
                "type": "room_join",
                "room_name": room_name_form,
                "username": request.user.username,
                "timestamp": str(timezone.now())
            })
            return redirect('chat_room', room_name=room_name_form)
        else:
            new_room = Room(room_name=room_name_form, owner=request.user)
            if pin:
                new_room.set_pin(pin)
            new_room.save()
            # Blockchain: record room creation
            blockchain_instance.add_block({
                "type": "room_creation",
                "room_name": room_name_form,
                "owner": request.user.username,
                "pin_hash": new_room.room_pin,
                "timestamp": str(timezone.now())
            })
            request.session[f'pin_verified_{room_name_form}'] = True
            messages.success(request, f"Room '{room_name_form}' created successfully!")
            return redirect('chat_room', room_name=room_name_form)

    context = {
        'users': users,
        'rooms': rooms,
        'online_usernames': online_usernames,
        'request_user': request_user,
        'room_name_from_url': room_name,
        'notifications': notifications,
        'blocks': blocks,  # <-- Pass blockchain to template
    }
    return render(request, 'chatapp/dashboard.html', context)


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not password or not password2:
            messages.error(request, "Please fill out all fields.")
            return render(request, 'chatapp/register1.html')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'chatapp/register1.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'chatapp/register1.html')

        User.objects.create_user(username=username, password=password)
        # Blockchain: record user registration
        blockchain_instance.add_block({
            "type": "user_registration",
            "username": username,
            "timestamp": str(timezone.now())
        })
        messages.success(request, "Registration successful. You can now log in.")
        return redirect('login')

    return render(request, 'chatapp/register1.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'chatapp/login1.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def chat_room(request, room_name):
    room = get_object_or_404(Room, room_name=room_name)

    if room.room_pin and not request.session.get(f'pin_verified_{room_name}'):
        messages.error(request, "Access denied. Join with correct PIN.")
        return redirect('dashboard')

    chats = Message.objects.filter(room=room).order_by('timestamp')

    return render(request, 'chatapp/chat_room1.html', {
        'room_name': room.room_name,
        'username': request.user.username,
        'chats': chats,
    })


@login_required
def create_room_view(request):
    if request.method == 'POST':
        room_name = request.POST.get('room', '').strip()
        pin = request.POST.get('pin', '').strip()
        recipient_username = request.POST.get('recipient_username', '').strip()  # Add this field in your form

        if not room_name:
            messages.error(request, "Room name is required.")
            return redirect('dashboard')

        try:
            room = Room.objects.get(room_name=room_name)

            if room.room_pin:
                if not pin:
                    messages.error(request, "Please enter the PIN for the existing room.")
                    return redirect('dashboard')

                if not room.check_pin(pin):
                    messages.error(request, "Incorrect PIN for the room.")
                    return redirect('dashboard')

            request.session[f'pin_verified_{room_name}'] = True
            blockchain_instance.add_block({
                "type": "room_join",
                "room_name": room_name,
                "username": request.user.username,
                "timestamp": str(timezone.now())
            })
            messages.success(request, f"Joined room '{room_name}'.")
            return redirect('chat_room', room_name=room_name)

        except Room.DoesNotExist:
            new_room = Room(room_name=room_name, owner=request.user)
            if pin:
                new_room.set_pin(pin)
            new_room.save()
            # Blockchain: record room creation
            blockchain_instance.add_block({
                "type": "room_creation",
                "room_name": room_name,
                "owner": request.user.username,
                "pin_hash": new_room.room_pin,
                "timestamp": str(timezone.now())
            })
            # Create notification for recipient
            if recipient_username:
                try:
                    recipient = User.objects.get(username=recipient_username)
                    Notification.objects.create(
                        recipient=recipient,
                        room=new_room,
                        pin=pin,  # This is the raw PIN from the form
                        message=f"You have been invited to join room '{room_name}'. PIN: {pin}"
                    )
                    # Blockchain: record PIN notification
                    blockchain_instance.add_block({
                        "type": "pin_notification",
                        "room": room_name,
                        "from": request.user.username,
                        "to": recipient.username,
                        "pin_sent": pin,
                        "timestamp": str(timezone.now())
                    })
                except User.DoesNotExist:
                    messages.error(request, "Recipient user does not exist.")

            request.session[f'pin_verified_{room_name}'] = True
            messages.success(request, f"Room '{room_name}' created successfully.")
            return redirect('chat_room', room_name=room_name)

    return render(request, 'chatapp/create_room1.html')


@login_required
def join_room_view(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        pin = request.POST.get('pin')

        try:
            room = Room.objects.get(room_name=room_name)
            if room.check_pin(pin):
                request.session[f'pin_verified_{room_name}'] = True
                blockchain_instance.add_block({
                    "type": "room_join",
                    "room_name": room_name,
                    "username": request.user.username,
                    "timestamp": str(timezone.now())
                })
                return redirect('chat_room', room_name=room_name)
            else:
                messages.error(request, "Incorrect PIN.")
        except Room.DoesNotExist:
            messages.error(request, "Room not found.")

    return redirect('dashboard')


@login_required
def save_message(request, room_name, username):
    if request.method == 'POST':
        room = get_object_or_404(Room, room_name=room_name)
        message_text = request.POST.get('message')
        message = Message(room=room, sender=username, message=message_text, message_hash="")  # Optional: add hash logic
        message.save()
        # Blockchain: record message
        blockchain_instance.add_block({
            "type": "message",
            "room": room_name,
            "sender": username,
            "message": message_text,
            "timestamp": str(timezone.now())
        })
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)


@login_required
def clear_chat(request, room_name):
    if request.method == "POST":
        Message.objects.filter(room__room_name=room_name).delete()
        blockchain_instance.add_block({
            "type": "chat_cleared",
            "room_name": room_name,
            "by": request.user.username,
            "timestamp": str(timezone.now())
        })
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)


@require_POST
@login_required
def send_pin_notification(request):
    room_id = request.POST.get('room_id')
    recipient_id = request.POST.get('recipient_id')
    entered_pin = request.POST.get('pin')  # Add this field to your form

    try:
        room = Room.objects.get(id=room_id, owner=request.user)
        recipient = User.objects.get(id=recipient_id)
        if not entered_pin or not room.check_pin(entered_pin):
            messages.error(request, "Incorrect PIN. Please enter the correct room PIN to resend.")
            return redirect('dashboard')

        Notification.objects.create(
            recipient=recipient,
            room=room,
            pin=entered_pin,  # This is the raw PIN entered by the owner
            message=f"You have been invited to join room '{room.room_name}'. PIN: {entered_pin}"
        )
        # Blockchain: record PIN notification
        blockchain_instance.add_block({
            "type": "pin_notification",
            "room": room.room_name,
            "from": request.user.username,
            "to": recipient.username,
            "pin_sent": entered_pin,
            "timestamp": str(timezone.now())
        })
        messages.success(request, f"Notification sent to {recipient.username}.")
    except Room.DoesNotExist:
        messages.error(request, "Room not found or you are not the owner.")
    except User.DoesNotExist:
        messages.error(request, "Recipient user not found.")

    return redirect('dashboard')


@login_required
def blockchain_explorer(request):
    blocks = blockchain_instance.to_list()
    errors = blockchain_instance.validate_chain()
    return render(request, 'chatapp/blockchain_explorer.html', {'blocks': blocks, 'errors': errors})


@login_required
def tamper_demo(request, index=1):
    blockchain_instance.tamper_block(index, {"type": "tampered", "message": "This block was tampered!"})
    messages.warning(request, f"Block {index} has been tampered for demonstration.")
    return redirect('blockchain_explorer')

@csrf_exempt
def upload_file(request, room_name):
    message = None
    message_type = "success"
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        room_dir = os.path.join(settings.MEDIA_ROOT, "uploads", room_name)
        os.makedirs(room_dir, exist_ok=True)

        file_path = os.path.join(room_dir, uploaded_file.name)
        with open(file_path, "wb+") as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)

        message = "File uploaded successfully!"
        message_type = "success"
    elif request.method == "POST":
        message = "No file selected. Please choose a file to upload."
        message_type = "danger"
    return render(request, "chatapp/upload_file.html", {
        "room_name": room_name,
        "message": message,
        "message_type": message_type,
    })

def list_files(request, room_name):
    room_dir = os.path.join(settings.MEDIA_ROOT, "uploads", room_name)
    files = []

    if os.path.exists(room_dir):
        for fname in os.listdir(room_dir):
            files.append({
                "name": fname,
                "url": f"{settings.MEDIA_URL}uploads/{room_name}/{fname}"
            })

    return render(request, "chatapp/list_files.html", {"files": files, "room_name": room_name})
