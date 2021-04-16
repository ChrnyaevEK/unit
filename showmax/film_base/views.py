from django.http import HttpResponse
from django.template import loader


class Page:
    web_public_name = 'Showmax'

    def __init__(self, context):
        self.context = context


def index(request):
    template = loader.get_template('film_base/index.html')
    return HttpResponse(template.render({'page': Page({
        'title': 'Home',
    })}, request))
