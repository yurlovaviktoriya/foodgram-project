from django.views.generic.base import TemplateView

from recipes.models import Purchase


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated:
            num_purchases = Purchase.objects.filter(user=request.user).count()       
            context['num_purchases'] = num_purchases
        return self.render_to_response(context)
         

class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated:
            num_purchases = Purchase.objects.filter(user=request.user).count()       
            context['num_purchases'] = num_purchases
        return self.render_to_response(context)
    
    
class AboutSiteView(TemplateView):
    template_name = 'about/site.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated:
            num_purchases = Purchase.objects.filter(user=request.user).count()       
            context['num_purchases'] = num_purchases
        return self.render_to_response(context)
    