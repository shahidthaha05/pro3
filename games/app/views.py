from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Game
from .form import GameForm
from django.http import HttpResponse, JsonResponse

# Admin login view
def game_login(req):
    if 'game' in req.session:
        return redirect(home)
    
    if req.method == 'POST':
        uname = req.POST['uname']
        password = req.POST['passwd']
        user = authenticate(username=uname, password=password)
        
        if user:
            if user.is_superuser:  # Check for superuser
                login(req, user)
                req.session['game'] = uname  # Create session for admin
                return redirect(home)
            else:
                login(req, user)
                req.session['user'] = uname  # Create session for normal user
                return redirect(home)
        else:
            messages.warning(req, 'Invalid username or password.')
            return redirect(game_login)
    else:
        return render(req, 'login.html')

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

        return render(req, 'admin/edit.html', {'form': form, 'game': game})
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

# def register(req):
#     if req.method=='POST':
#         name=req.POST['name']
#         email=req.POST['email']
#         password=req.POST['password']
#         try:
#             data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
#             data.save()
#             return redirect(game_login)
#         except:
#             messages.warning(req,'User already exists.')
#             return redirect(register)
#     else:
#         return render(req,'user/register.html')



# def user_home(req):
#     if 'user' in req.session:
#         data=Game.objects.all()
#         return render(req,'user/home.html',{'data':data})
#     else:
#         return redirect(game_login)



# def view_game(req, pid):
#     # Get the product by its ID
#     product = get_object_or_404(Product, pk=pid)

#     # Pass the product data to the template
#     return render(req, 'user/view_game.html', {'data': product})