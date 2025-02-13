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




from django.shortcuts import render
from .models import SlotBooking  # Import your SlotBooking model

def admin_bookings(request):
    # Fetch all bookings, or customize your query if you need to filter
    bookings = SlotBooking.objects.all()

    return render(request, 'admin/bookings.html', {'bookings': bookings})





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





from django.shortcuts import render, get_object_or_404
from .models import Game

def view_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'user/view_game.html', {'game': game})






from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .models import Game, Slot, SlotBooking

def book_slot(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    available_slots = []
    
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        
        if not selected_date:
            messages.error(request, 'Please select a date.')
            return redirect('book_slot', game_id=game.id)  # Redirect back if no date is selected
        
        # Ensure the date is in the correct format ('YYYY-MM-DD')
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format. Please select a valid date.')
            return redirect('book_slot', game_id=game.id)

        # Fetch available slots for the selected date and game
        available_slots = Slot.objects.filter(game=game, date=selected_date, reserved=False)
        
        if not available_slots:
            messages.error(request, 'No available slots for the selected date.')
            return redirect('book_slot', game_id=game.id)
        
        # If a slot is selected, create the booking
        if 'slot_id' in request.POST:
            selected_slot = request.POST.get('slot_id')
            slot = get_object_or_404(Slot, id=selected_slot)
            
            # Check if the slot is already reserved
            if slot.reserved:
                messages.error(request, 'This slot is already reserved.')
                return redirect('book_slot', game_id=game.id)
            
            # Create the SlotBooking
            SlotBooking.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                game=game,
                slot=slot,
                date=selected_date,
            )
            
            # Mark the slot as reserved
            slot.reserved = True
            slot.save()
            
            messages.success(request, 'Your booking has been confirmed!')
            return redirect('booking_confirmation', game_id=game.id)  # Redirect to confirmation page

    # If it's a GET request, set the default selected date
    selected_date = request.GET.get('date', datetime.now().strftime('%Y-%m-%d'))

    return render(request, 'user/book_slot.html', {
        'game': game,
        'selected_date': selected_date,
        'available_slots': available_slots,
    })



def booking_confirmation(request, game_id):
    # Retrieve the booking details from the session
    booking_id = request.session.get('booking_id')
    if not booking_id:
        return redirect('home')  # If no booking found, redirect to home

    booking = get_object_or_404(SlotBooking, id=booking_id)
    game = booking.game
    slot = booking.slot

    return render(request, 'user/booking_confirmation.html', {
        'booking': booking,
        'game': game,
        'slot': slot,
    })




def booking_success(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'user/booking_success.html', {'game': game})
