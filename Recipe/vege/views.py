from django.shortcuts import render, redirect
from .models import recipes_table

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

    # ADD DATA AND SAVE
    extractQuery = recipes_table.objects.all()
    context = {"recipes": extractQuery}

        
    return render(request, "home/recipes.html", context)

def deleteRecipe(request, id):

    extractDatafromId = recipes_table.objects.get(id = id)

    extractDatafromId.delete()
    return redirect("/recipes/")