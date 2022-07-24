# We have created this file to replace 'store.views.categories' in settings.py> templates> context_processor list to follow the general convention.
# So we shifted the below piece of code from views.py to here


from .models import Category


def categories(request):
    return {
        'categories': Category.objects.all()  # In the dropdown all the categories will be returned/displayed
    }
