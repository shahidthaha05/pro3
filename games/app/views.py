from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Game
from .form import GameForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
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

                # Automatically generate slots for the game from 10 AM to 10 PM
                start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)  # Starting from 10 AM
                end_time = datetime.now().replace(hour=22, minute=0, second=0, microsecond=0)  # End at 10 PM

                # Generate slots for every hour
                while start_time <= end_time:
                    Slot.objects.create(
                        game=game,
                        time_slot=start_time.time(),
                        date=start_time.date(),
                        reserved=False
                    )
                    start_time += timedelta(hours=1)  # Increment by 1 hour

                messages.success(request, 'Game added successfully with auto-generated time slots!')
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






# user 

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def register(req):
    if req.method == 'POST':
        # Getting the data from the form
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']

        # Check if the user already exists based on the email
        if User.objects.filter(email=email).exists():
            messages.warning(req, 'A user with this email already exists.')
            return redirect('register')  # Make sure 'register' matches the URL name for the registration page

        # If the user does not exist, create the new user
        try:
            user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
            user.save()

            # Optionally, you can create a UserProfile here if you have additional information to store
            # UserProfile.objects.create(user=user)

            messages.success(req, 'Registration successful! You can now log in.')
            return redirect('game_login')  # Redirect to the login page after successful registration

        except Exception as e:
            # If something goes wrong, show an error message
            messages.error(req, f'Error during registration: {e}')
            return redirect('register')

    else:
        # Render the registration form if GET request
        return render(req, 'user/register.html')






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



from django.shortcuts import render, get_object_or_404, redirect


from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from .models import Game, Slot

def view_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    # Get the selected date from the GET parameter (default to today's date)
    selected_date = request.GET.get('date', now().date())

    # Fetch available slots for the selected date and the game
    available_slots = Slot.objects.filter(game=game, date=selected_date, reserved=False)

    # Fetch booked slots for the selected date (optional: to show booked slots)
    booked_slots = Slot.objects.filter(game=game, date=selected_date, reserved=True)

    # If the user has submitted the booking form, handle the booking
    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        name = request.POST.get('name')
        email = request.POST.get('email')

        if slot_id:
            # Check if the selected slot is already reserved
            slot = get_object_or_404(Slot, pk=slot_id)
            if slot.reserved:
                messages.error(request, "This slot is already booked. Please choose another.")
                return redirect('view_game', game_id=game.id)

            # If slot is available, book the slot
            slot.reserved = True
            slot.booking_time = now()
            slot.save()

            # Save the booking to the SlotBooking model
            SlotBooking.objects.create(
                name=name,
                email=email,
                game=game,
                slot=slot,
                date=selected_date,
            )

            messages.success(request, f"Slot {slot.time_slot} booked successfully!")
            return redirect('view_game', game_id=game.id)

    # Render the page with available and booked slots
    return render(request, 'user/view_game.html', {
        'game': game,
        'available_slots': available_slots,
        'booked_slots': booked_slots,
        'selected_date': selected_date,
    })




# ✅ Booking game page - Users choose an available slot
def booking_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    
    # Get selected date from request, default to today
    selected_date = request.GET.get("date", now().date())
    if isinstance(selected_date, str):
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    # Fetch available slots
    available_slots = Slot.objects.filter(game=game, date=selected_date, reserved=False)

    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        slot = get_object_or_404(Slot, pk=slot_id, game=game)

        if slot.reserved:
            messages.error(request, "This slot is already booked!")
        else:
            slot.reserved = True
            slot.booking_time = now()
            slot.save()
            messages.success(request, f"Slot {slot.time_slot} booked successfully!")
            return redirect('view_game', game_id=game.id)

    return render(request, 'user/booking_game.html', {'game': game, 'available_slots': available_slots, 'selected_date': selected_date})

def book_slot(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    selected_slot = request.POST.get('slot_id')
    slot = get_object_or_404(Slot, id=selected_slot)

    if slot.reserved:
        # Handle the case where the slot is already reserved
        messages.error(request, 'This slot is already booked!')
        return redirect('game_slots', game_id=game.id)

    # Create SlotBooking
    SlotBooking.objects.create(
        name=request.POST['name'],
        email=request.POST['email'],
        game=game,
        slot=slot,
        date=request.POST['date'],
    )
    
    # Mark the slot as reserved
    slot.reserved = True
    slot.booking_time = now()
    slot.save()

    messages.success(request, 'Your slot has been successfully booked!')
    return redirect('game_slots', game_id=game.id)


# ✅ Success page after booking
def success_page(request):
    return render(request, 'user/success.html')
