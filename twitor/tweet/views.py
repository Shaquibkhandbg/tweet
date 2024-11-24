from django.shortcuts import render,redirect
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth  import login
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    # Get the search query from the GET parameters
    query = request.GET.get('q', '')  # Use an empty string as default if 'q' is missing
    
    # Filter tweets based on the query
    if query:
        tweets = Tweet.objects.filter(
            Q(text__icontains=query) | Q(user__username__icontains=query)  # Match text or username
        ).order_by('-created_at')
    else:
        tweets = Tweet.objects.all().order_by('-created_at')
    
    # Set up pagination with 6 tweets per page
    paginator = Paginator(tweets, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Pass `query` to the template for search field and highlighting
    return render(request, 'tweet_list.html', {'page_obj': page_obj, 'query': query})

   
    
@login_required
def tweet_create(request):
    if request.method ==  'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request,'tweet_form.html',{'form':form})


@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST,request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user = request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})



def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST )
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    
    else:
        form = UserRegistrationForm()
    
    
    return render(request,'registration/register.html',{'form':form})



    

