from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import View
# from django.conf import settings as djsettings
from django.utils.decorators import method_decorator
from django.db.models import Count
import os
import logging
import threading
import json

import forms
import search
from models import Image

logger = logging.getLogger(__name__)

def json_response(data):
    return HttpResponse(json.dumps(data), 'json')

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
            searcher = search.Searcher(image)
            searcher.run()
            return make_response(request, self.RESULT_TEMPLATE, {
                'queryImage': image,
                'searcher': searcher,
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
        return HttpResponse(open(path, 'rb').read(), content_type=type)

class TestCorrectRate(View):
    TEST_TEMPLATE = 'test.html'
    TEST_RESULT_TEMPLATE = 'test_result.html'

    def get(self, request):
        groups = list(Image.objects.values('group').annotate(count=Count('group')))
        groups.sort(key=lambda x: x['group'])
        return make_response(request, self.TEST_TEMPLATE, {
            'groups': groups,
            'allgroups': ','.join(str(x['group']) for x in groups),
            'comparerName': search.Searcher.comparerName,
        })

    @csrf_protect_method
    def post(self, request):
        self.parse_post(request.POST)
        with CheckStatus.lock:
            if CheckStatus.tester is None \
                    or CheckStatus.tester.state == search.Tester.STATE_FINISHED:
                tester = search.Tester(self.samplesPerGroup, self.enabledGroups)
                CheckStatus.tester = tester
                thread = threading.Thread(target=tester.run)
                thread.start()
            else:
                tester = CheckStatus.tester
        return make_response(request, self.TEST_RESULT_TEMPLATE, {
            'allgroups': ','.join(str(x) for x in tester.enabledGroups),
            'samples_per_group': tester.samplesPerGroup,
            'comparerName': search.Searcher.comparerName,
        })

    def parse_post(self, POST):
        groups = map(int, POST['allgroups'].split(','))
        self.enabledGroups = [g for g in groups if 'enable-group-%d' % g in POST]
        self.samplesPerGroup = int(POST['samples-per-group'])

class CheckStatus(View):
    lock = threading.Lock()
    tester = None

    def get(self, request):
        if self.tester is None:
            return json_response({})
        output = {
            'progress': self.tester.progress,
            'state': self.tester.state,
        }
        if self.tester.state is self.tester.STATE_FINISHED:
            groupAverageRates = []
            for i, r in self.tester.groupAverageRates:
                groupAverageRates.append({'group': i, 'rate': r})
            output.update({
                'groupAverageRates': groupAverageRates,
                'averageRate': self.tester.averageRate,
            })
        return json_response(output)
