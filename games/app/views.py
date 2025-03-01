from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Game
from .form import GameForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .models import SlotBooking
from django.contrib.auth.decorators import login_required
# Admin login view


def game_login(req):
    if 'game' in req.session:
        return redirect(home)
    
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['passwd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['game']=uname   #create session
                return redirect(home)
            else:
                
                login(req,data)
                req.session['user']=uname   
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(game_login)
    else:
        return render(req,'login.html')
    

# Home page view
def home(req):
    if 'game' in req.session:
        data = Game.objects.all()
        return render(req, 'admin/home.html', {'data': data})
    else:
        return redirect(game_login)

# Game logout view
def game_logout(req):
    req.session.flush()  # Delete session
    logout(req)
    return redirect(game_login)

from datetime import datetime, timedelta
from .models import Game, Slot


def add_game(request):
    if 'game' in request.session:
        if request.method == 'POST':
            form = GameForm(request.POST, request.FILES)
            if form.is_valid():
                game = form.save()  # Save the new game

                # Set the range of days for which slots should be created (e.g., 30 days)
                num_days = 365  
                today = datetime.now().date()

                for day in range(num_days):  
                    current_date = today + timedelta(days=day)
                    start_time = datetime.combine(current_date, datetime.min.time()).replace(hour=10, minute=0, second=0)
                    end_time = start_time.replace(hour=22)

                    while start_time <= end_time:
                        Slot.objects.create(
                            game=game,
                            time_slot=start_time.time(),
                            date=current_date,
                            reserved=False
                        )
                        start_time += timedelta(hours=1)  # Increment by 1 hour

                messages.success(request, 'Game added successfully with auto-generated time slots for 30 days!')
                return redirect(home)
            else:
                messages.error(request, 'Error adding game. Please check the form.')
                print(form.errors)  # Debugging: Print form errors
        else:
            form = GameForm()  # Empty form
        return render(request, 'admin/add_game.html', {'form': form})
    else:
        return redirect(game_login)



# Edit game view
def edit(req, gid):
    if 'game' in req.session:
        game = get_object_or_404(Game, pk=gid)  # Safely get the game
        
        if req.method == 'POST':
            form = GameForm(req.POST, req.FILES, instance=game)  # Bind form to the existing game
            if form.is_valid():
                form.save()  # Save the changes
                messages.success(req, 'Game updated successfully!')
                return redirect(home)  # Redirect back to home page
            else:
                messages.error(req, 'Error updating game. Please check the form.')
                print(form.errors)  # Debugging: Print form errors
        else:
            form = GameForm(instance=game)  # Pre-fill the form with existing game data

        return render(req, 'admin/edit_game.html', {'form': form, 'game': game})
    else:
        return redirect(game_login)

# Delete game view
def delete_game(req, gid):
    if 'game' in req.session:
        game = get_object_or_404(Game, pk=gid)
        game.delete() 
        messages.success(req, 'Game deleted successfully!')
        return redirect(home)  # Redirect back to home page after deletion
    else:
        return redirect(game_login)




from django.shortcuts import render
from .models import SlotBooking  # Import your SlotBooking model

def admin_bookings(request):
    # Fetch all bookings, or customize your query if you need to filter
    bookings = SlotBooking.objects.all()

    return render(request, 'admin/bookings.html', {'bookings': bookings})





from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import SlotBooking, Slot

def delete_booking(request, booking_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('admin_bookings')  # Redirect back to the bookings page.

    booking = get_object_or_404(SlotBooking, id=booking_id)
    slot = booking.slot

    # Delete the booking
    booking.delete()

    # Check if there are other bookings for this slot and mark it as available if no other bookings are present
    if not SlotBooking.objects.filter(slot=slot).exists():
        slot.reserved = False
        slot.save()

    messages.success(request, "Booking has been deleted successfully.")
    return redirect('admin_bookings')  # Redirect back to the bookings page








from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'pass_reset.html'
    email_template_name = 'pass_reset_email.html'
    subject_template_name = 'pass_reset_subject.txt'
    success_url = reverse_lazy('pass_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'pass_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'pass_reset_confirm.html'
    success_url = reverse_lazy('pass_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'pass_reset_complete.html'






# user 

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

def register(req):
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        if User.objects.filter(email=email).exists():
            messages.warning(req, "Email already registered")
            return redirect('register')
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        req.session['email'] = email
        req.session['name'] = name
        req.session['password'] = password
        send_mail(
            'Your OTP Code',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER, [email]
        )
        messages.success(req, "OTP sent to your email")
        return redirect('verify_otp_reg')
    return render(req, 'user/register.html')

def verify_otp_reg(req):
    if req.method == 'POST':
        entered_otp = req.POST['otp'] 
        stored_otp = req.session.get('otp')
        email = req.session.get('email')
        name = req.session.get('name')
        password = req.session.get('password')
        if entered_otp == stored_otp:
            user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
            user.is_verified = True
            user.save()      
            messages.success(req, "Registration successful! You can now log in.")
            send_mail('User Registration Succesfull', 'Account Created Succesfully And Welcome To gamestation ', settings.EMAIL_HOST_USER, [email])
            return redirect('game_login')
        else:
            messages.warning(req, "Invalid OTP. Try again.")
            return redirect('verify_otp_reg')

    return render(req, 'user/verify_code.html')
















from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.timezone import now, timedelta
from .models import Game, Slot, SlotBooking
from datetime import datetime



def user_home(req):
    if 'user' in req.session:
        # Fetch all games from the database
        games = Game.objects.all()
        return render(req, 'user/home.html', {'games': games})
    return redirect('game_login')  # Redirect to login if no user session





from django.shortcuts import render, get_object_or_404
from .models import Game

def view_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'user/view_game.html', {'game': game})








from django.utils.timezone import now
from datetime import datetime

from django.contrib.auth.models import User

def book_slot(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    selected_date = request.POST.get('date') or request.GET.get('date')

    today = now().date()  # Get today's date

    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

            # If selected date is in the past, show an error and keep the date in the field
            if selected_date_obj < today:
                messages.error(request, 'You cannot book past dates. Please select today or a future date.')
                return render(request, 'user/book_slot.html', {
                    'game': game,
                    'selected_date': selected_date,  # Keep the user's selected date in the field
                    'all_slots': [],
                    'user_name': request.user.first_name,
                    'user_email': request.user.email,
                })
        except ValueError:
            messages.error(request, 'Invalid date format. Please select a valid date.')
            return redirect('book_slot', game_id=game.id)
    else:
        selected_date_obj = today  # Default to today if no date is provided

    # Fetch only available slots for the valid date
    all_slots = Slot.objects.filter(game=game, date=selected_date_obj)

    if request.method == 'POST' and 'slot_id' in request.POST:
        selected_slot = request.POST.get('slot_id')
        slot = get_object_or_404(Slot, id=selected_slot)

        if slot.reserved:
            messages.error(request, 'This slot is already booked. Please select another slot.')
            return redirect(f"{request.path}?date={selected_date}")

        # Create a booking
        SlotBooking.objects.create(
            user=request.user,
            name=request.POST['name'],  # Get the user's name from form
            email=request.POST['email'],  # Get the user's email from form
            game=game,
            slot=slot,
            date=selected_date_obj
        )

        slot.reserved = True
        slot.save()

        messages.success(request, 'Your booking has been confirmed!')
        return redirect('booking_confirmation', game_id=game.id)

    return render(request, 'user/book_slot.html', {
        'game': game,
        'selected_date': selected_date,  # Ensure selected date stays in the input field
        'all_slots': all_slots,
        'user_name': request.user.first_name,  # Pass user's name
        'user_email': request.user.email,  # Pass user's email
    })




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SlotBooking

@login_required
def my_bookings(request):
    # Fetch bookings only for the logged-in user
    bookings = SlotBooking.objects.filter(user=request.user)

    return render(request, 'user/my_bookings.html', {'bookings': bookings})



from django.shortcuts import render, redirect
from .models import SlotBooking

def booking_confirmation(request, game_id):
    booking = SlotBooking.objects.latest('id')  # Get the most recent booking
    game = booking.game
    booking_date = booking.date
    return render(request, 'user/booking_confirmation.html', {
        'game': game,
        'booking_date': booking_date,
    })





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import SlotBooking, Slot

def cancel_booking(request, booking_id):
    # Get the booking by ID
    booking = get_object_or_404(SlotBooking, id=booking_id)
    
    # Ensure the logged-in user is the one who made the booking
    if booking.user != request.user:
        messages.error(request, "You can't cancel someone else's booking.")
        return redirect('my_bookings')
    
    # Mark the slot as available again
    slot = booking.slot
    slot.reserved = False
    slot.save()

    # Delete the booking
    booking.delete()

    # Success message
    messages.success(request, "Your booking has been canceled successfully. The slot is now available.")
    
    # Redirect to the booking page
    return redirect('my_bookings')




