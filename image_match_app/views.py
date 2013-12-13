from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import View
from django.conf import settings as djsettings
from django.utils.decorators import method_decorator
import os
import tempfile
import functools 
import logging


import forms
import search
from models import Image, QueryImage

logger = logging.getLogger(__name__)

def debug(*args):
    fifo = open('/tmp/djfifo', 'a')
    for arg in args:
        print >> fifo, arg,
    print >> fifo
    fifo.close()

def make_response(request, templateName, contextDict):
    return HttpResponse(get_template(templateName).render(
        RequestContext(request, contextDict)))

csrf_protect_method = method_decorator(csrf_protect)

class SearchView(View):
    SEARCH_TEMPLATE = 'search.html'
    RESULT_TEMPLATE = 'result.html'

    def get(self, request):
        form = forms.ImageUploadForm()
        return make_response(request, self.SEARCH_TEMPLATE, {'form': form})

    @csrf_protect_method
    def post(self, request):
        form = forms.ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            results = search.search(image)
            return make_response(request, self.RESULT_TEMPLATE, {
                'queryImage': image,
                'results': results,
                'form': form,
                })
        else:
            # response the error form to client
            return make_response(request, self.SEARCH_TEMPLATE, {'form': form})

class ShowImage(View):
    def get(self, request, id):
        image = Image.objects.get(id=id)
        path = image.path
        ext = os.path.splitext(path)[1]
        type = {'.png': 'image/png', '.jpg': 'image/jpeg'}[ext]
        return HttpResponse(open(path, 'rb').read(), mimetype=type)
