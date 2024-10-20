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
