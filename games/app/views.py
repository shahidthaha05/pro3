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

# Add game view
def add_game(req):
    if 'game' in req.session:
        if req.method == 'POST':
            form = GameForm(req.POST, req.FILES)
            if form.is_valid():
                form.save()  # Save the game using the form
                messages.success(req, 'Game added successfully!')
                return redirect(home)  # Redirect to home after adding
            else:
                messages.error(req, 'Error adding game. Please check the form.')
                print(form.errors)  # Debugging: Print form errors
        else:
            form = GameForm()  # Empty form
        return render(req, 'admin/add_game.html', {'form': form})
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




from django.shortcuts import render, redirect
from .models import Game

def user_home(req):
    if 'user' in req.session:
        # Query all games and pass them to the template
        data = Game.objects.all()
        return render(req, 'user/home.html', {'data': data})
    else:
        return redirect('game_login')  # Redirect to login if no user in session










from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Game, Slot
from .form import SlotBookingForm



from django.shortcuts import render, get_object_or_404
from .models import Game, Slot
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from .models import Game, Slot  # Ensure Slot is imported

def view_game(req, game_id):
    # Get the game object based on the game_id
    game = get_object_or_404(Game, pk=game_id)

    # Get available slots by filtering slots related to this game
    available_slots = Slot.objects.filter(game=game, reserved=False)

    return render(req, 'user/view_game.html', {'game': game, 'available_slots': available_slots})





from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Game, Slot

def booking_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    
    # Filter available slots based on booking time logic
    available_slots = [slot for slot in game.slots.all() if slot.is_available()]

    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        slot = get_object_or_404(Slot, pk=slot_id, game=game)

        if slot.reserved and not slot.is_available():
            messages.error(request, "This slot is temporarily unavailable. Please try later.")
        else:
            slot.reserved = True
            slot.booking_time = now()  # Store booking time
            slot.save()
            messages.success(request, f"Your slot at {slot.time_slot} has been reserved!")
            return redirect(book_slot)

    return render(request, 'user/booking_game.html', {'game': game, 'available_slots': available_slots})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import timedelta
from .form import SlotBookingForm
from .models import Slot

def book_slot(request, slot_id=None):
    if request.method == 'POST':
        form = SlotBookingForm(request.POST)

        if form.is_valid():
            time_slot = form.cleaned_data['time_slot']

            # Check if slot exists
            slot = Slot.objects.filter(time_slot=time_slot).first()
            if not slot:
                messages.error(request, "Selected time slot does not exist.")
                return redirect('book_slot')

            # Check if slot is already booked and still within 1 hour
            if slot.reserved and slot.booking_time and now() < slot.booking_time + timedelta(hours=1):
                messages.error(request, "This time slot is already booked. Please choose another slot.")
                return redirect('book_slot')

            # Book the slot
            slot.reserved = True
            slot.booking_time = now()  # Store booking time
            slot.save()

            messages.success(request, f"Slot at {time_slot} booked successfully!")
            return redirect('success_page')

    else:
        form = SlotBookingForm()

    return render(request, 'user/book_slot.html', {'form': form})






def success_page(request):
    return render(request, 'user/success.html')
