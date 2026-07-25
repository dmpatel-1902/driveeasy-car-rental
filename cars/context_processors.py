from .models import Category


def categories_processor(request):
    return {'categories_footer': Category.objects.all()}
