from django.views.generic.base import TemplateView
from django.conf import settings

rights = {'rights': settings.RIGHTS,
          'storage_rights': settings.STORAGE_RIGHTS,
          'sadec_rights': settings.SADEC_RIGHTS,
          'pro_rights': settings.PRO_RIGHTS, }


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'
    queryset = settings.RIGHTS


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
    queryset = settings.RIGHTS
