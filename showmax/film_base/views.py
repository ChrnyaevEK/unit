from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('film_base/index.html')
    return HttpResponse(template.render({}, request))
