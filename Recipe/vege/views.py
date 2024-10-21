from django.shortcuts import render, redirect
from .models import recipes_table
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# @login_required(login_url='/login/')
# Create your views here.
def home(request):
    return render(request, "home/home.html")

def recipes(request):
    # DATA FROM FRONTEND
    if request.method == 'POST':
        data = request.POST
        name = data.get("name")
        description = data.get("desc")
        image = request.FILES.get("image")

        saveRecipe = recipes_table(name = name, description= description, image=image)
        saveRecipe.save()
        return redirect("/recipes/")

# serach
    extractQuery = recipes_table.objects.all()


    if request.GET.get("search"):
        # checking
        # print( request.GET.get("search"))
        extractQuery = extractQuery.filter(name__icontains = request.GET.get("search")) #filtering the value

    # ADD DATA AND SAVE
    context = {"recipes": extractQuery}
    return render(request, "home/recipes.html", context)




def updateRecipe(request, id):
    extractDatafromId = recipes_table.objects.get(id = id)
    if request.method == 'POST':
        data = request.POST
        name = data.get("name")
        description = data.get("desc")  # Ensure this matches your form input
        image = request.FILES.get("image")  # Initialize image here

        # Update fields with the new data
        if name:
            extractDatafromId.name = name
        if description:
            extractDatafromId.description = description
        
        # Update image only if a new image was uploaded
        if image:  # Check if an image was provided
            extractDatafromId.image = image
        extractDatafromId.save()
        return redirect('/recipes/')

    context = {'recipe':extractDatafromId}
    return render(request, 'home/updateRecipe.html', context)
        

def deleteRecipe(request, id):

    extractDatafromId = recipes_table.objects.get(id = id)

    extractDatafromId.delete()

    return redirect("/recipes/")


# register features
def register(request):
    if request.method == "POST":
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        userName = request.POST.get("userName")
        password = request.POST.get("password")

        createUser = User.objects.create(first_name = firstName, last_name= lastName, username=userName)

        createUser.set_password(password)

        createUser.save()
        messages.info(request,"Added successfully")
        return redirect("/register/")
    
    return render(request, 'home/register.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request,"Invalid usename")
            return redirect("/login/")
        
        
        userObject = authenticate(username=username, password=password)

        if userObject is None:
            messages.error(request, "invalid passwod")
            return redirect("/login/")
        else:
            # # session mentain
            login(request, userObject)
            return redirect("/recipes/")


    return render(request, 'home/login.html')

def logout_page(request):
    logout(request)
    return redirect("/home/")