import os
from operator import attrgetter

import requests
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from .models import Guide
from stats.models import Users as DiscordUser


class IndexView(generic.ListView):
    context_object_name = 'latest_guides'
    paginate_by = 10
    template_name = 'guides/index.html'

    def get_queryset(self):
        return Guide.objects.order_by('-pub_datetime')


@method_decorator(user_passes_test(attrgetter('is_member')), name='dispatch')
class CreateView(generic.CreateView):
    model = Guide
    fields = ['title', 'overview', 'content']

    def form_valid(self, form):
        guide = form.save(commit=False)
        guide.author = self.request.user
        guide.save()

        detail_url = self.request.build_absolute_uri(reverse('guides:detail', kwargs={'pk': guide.id}))
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if webhook_url is not None:
            requests.post(webhook_url, json={
                'username': 'Community Website',
                'avatar_url': 'https://cdn.discordapp.com/emojis/410506329359253514.png?v=1',
                'embeds': [{
                    'title': f'New Guide posted: "{guide.title}"',
                    'author': {
                        'name': guide.author.username,
                        'icon_url': DiscordUser.from_django_user(self.request.user).avatar_url
                    },
                    'url': detail_url,
                    'description': guide.overview,
                    'color': 0x0066CC
                }]
            })
        return HttpResponseRedirect(detail_url)


class DetailView(generic.DetailView):
    model = Guide
    template_name = 'guides/detail.html'
