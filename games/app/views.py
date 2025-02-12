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
from .form import SlotBookingForm, UserDetailsForm



from django.shortcuts import render, get_object_or_404
from .models import Game, Slot
from django.contrib import messages

def view_game(req, game_id):
    # Get the game object based on the game_id
    game = get_object_or_404(Game, pk=game_id)

    # Get all the available slots for this game (where reserved is False)
    available_slots = game.slots.filter(reserved=False)

    return render(req, 'user/view_game.html', {'game': game, 'available_slots': available_slots})





from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Slot
from django.contrib import messages

def booking_game(req, game_id):
    game = get_object_or_404(Game, pk=game_id)
    available_slots = game.slots.filter(reserved=False)

    if req.method == 'POST':
        slot_id = req.POST.get('slot_id')
        slot = get_object_or_404(Slot, pk=slot_id, game=game)

        if slot.reserved:
            messages.error(req, "This slot is already booked.")
        else:
            # Mark the slot as reserved
            slot.reserved = True
            slot.save()
            messages.success(req, f"Your slot on {slot.start_time} - {slot.end_time} has been reserved!")
            return redirect('user_home')  # Redirect to home after booking

    return render(req, 'user/booking_game.html', {'game': game, 'available_slots': available_slots})

