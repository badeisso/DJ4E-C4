from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import Ads,Comment
from ads.forms import CreateForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View



class AdListView(View):

    template_name = 'ads/ads_list.html'
    
    def get(self,request):

        ads_list = Ads.objects.all()
        context = {'ads_list' : ads_list}

        return render(request, self.template_name, context)



class AdDetailView(View):

    template_name = 'ads/ads_detail.html'
        
    def get(self,request,pk):

        ads = Ads.objects.get(id=pk)
        comments = Comment.objects.filter(ad=ads).order_by('updated_at')
        comment_form = CommentForm()
        context = {"ads" : ads, "comments" : comments, "comment_form" : comment_form}

        return render(request, self.template_name, context)


class AdCreateView(LoginRequiredMixin,View):

    template_name = 'ads/ads_form.html'
    success_url = reverse_lazy('ads:all')

    
    def get(self, request,pk=None):
        form = CreateForm()
        context = {'form' : form}
        return render(request, self.template_name, context)

    def post(self,request,pk=None):

        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            context = {'form' : form}

            return render(request, self.template_name, context)

        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()

        return redirect(self.success_url)

class AdUpdateView(LoginRequiredMixin,View):

    template_name = 'ads/ads_form.html'

    def get(self,request,pk):

        queryset = Ads.objects.filter(owner=self.request.user)
        ads = get_object_or_404(queryset,pk=pk)
        form = CreateForm(instance=ads)
        context = {'form' : form}

        return render(request, self.template_name, context)

    def post(self,request,pk):

        queryset = Ads.objects.filter(owner=self.request.user)
        ads = get_object_or_404(queryset,pk=pk)
        form = CreateForm(request.POST, request.FILES or None, instance=ads)

        if not form.is_valid():
            context = {'form' : form}
            return render(request, self.template_name, context)

        ads = form.save(commit=False)
        ads.save()

        return redirect(reverse("ads:ad_detail", args=[pk]))



class AdDeleteView(LoginRequiredMixin,View):

    template_name = 'ads/ads_confirm_delete.html'
    success_url = reverse_lazy('ads:all')

    def get(self,request,pk):

        queryset = Ads.objects.filter(owner=self.request.user)
        ads = get_object_or_404(queryset,pk=pk)
        form = CreateForm(instance=ads)
        context = {'ads' : ads}

        return render(request, self.template_name, context)

    def post(self,request,pk):

        queryset = Ads.objects.filter(owner=self.request.user)
        ads = get_object_or_404(queryset,pk=pk)
        ads.delete()
        return redirect(self.success_url)

class CommentCreateView(LoginRequiredMixin, View):
    
    def post(self, request, pk):

        ads = get_object_or_404(Ads, id=pk)
        comments = Comment(text=request.POST['comment'], owner=request.user, ad=ads)
        comments.save()
        return redirect(reverse("ads:ad_detail", args=[pk]))


class CommentDeleteView(LoginRequiredMixin, View):

    template_name = "ads/comments_confirm_delete.html"

    def get(self, request, pk):
        queryset = Comment.objects.filter(owner=self.request.user)
        comments = get_object_or_404(queryset, id=pk)
        form = CreateForm(instance=comments)
        context = {"comment" : comments}

        return render(request, self.template_name, context)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, owner=self.request.user, pk=pk)
        id = comment.ad.id
        comment.delete()

        return redirect(reverse('ads:ad_detail', args=[id]))  


def stream_file(request, pk):
    pic = get_object_or_404(Ads, pk=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response




