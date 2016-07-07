from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from .forms import SongForm
from django.http import HttpResponseRedirect
from django.template import Context, Template
from rauth import OAuth2Service
from django.shortcuts import redirect
import json
import requests

session = ''
genius = OAuth2Service(
        client_id = 'ZFtLPYv59ptIsi9zTpLCHbnmKZeSvmeTcOz-8ngiac-7ulG04LDgOlcXalpxDAU2',
        client_secret = '3_58BaMlbFQBpBeVMFAeCl5az-_WQGVxVubINOavG33byHC10fBbwWBnL4mbvCmaZ0I0Icaec3LYETWJOq0ETw',
        name='genius',
        authorize_url='https://api.genius.com/oauth/authorize', 
        access_token_url='https://api.genius.com/oauth/token',
        base_url = 'https://api.genius.com'
    )


def bytestojson(response):
    return json.loads(response.decode('utf-8'))

def home(request):
   
    if (not request.GET.get('code') or not request.GET.get('state')) and not session:
        params = {'client_id': 'ZFtLPYv59ptIsi9zTpLCHbnmKZeSvmeTcOz-8ngiac-7ulG04LDgOlcXalpxDAU2',
        'redirect_uri':'http://127.0.0.1:8000/',
        'scope':'me',
        'state': 5,
        'response_type':'code'}
        
        url = genius.get_authorize_url(**params)
        
        return redirect(url)
    
    else:
        
        if not session:
            code = request.GET.get('code') 
            
            print("asdfasdfasfasdfasf " + code)
            global session
            session = genius.get_auth_session(data = {'code':code, 
                'client_secret':'3_58BaMlbFQBpBeVMFAeCl5az-_WQGVxVubINOavG33byHC10fBbwWBnL4mbvCmaZ0I0Icaec3LYETWJOq0ETw',
                'grant_type':'authorization_code',
                'client_id': 'ZFtLPYv59ptIsi9zTpLCHbnmKZeSvmeTcOz-8ngiac-7ulG04LDgOlcXalpxDAU2',
                'redirect_uri': 'http://127.0.0.1:8000/',
                'response_type':'code'
            }, decoder=bytestojson
            )
            
            #access_token = session['access_token']
            

            print("helloooooooooooo")
            return render(request, 'search/home.html')
        else:



        
            return render(request, 'search/home.html')
    

def loggedInHome(request):
    return render(request, 'search/home.html')

def confirm(request):
    if request.method == 'POST':

        form = SongForm(request.POST)
        if form.is_valid() and session:
            print("2")
            print(form.cleaned_data)
            json_response = session.get('https://api.genius.com/search', params = {'q':form.cleaned_data['songtopic']}).json()['response']
            song_info = []
            song_IDs_youtube = []
            for song in json_response['hits']:
                song_title = song['result']['title']
                song_artist = song['result']['primary_artist']['name']
                song_info.append({'song_title':song_title, 'song_artist':song_artist})
                youtube_song_info = requests.get("https://www.googleapis.com/youtube/v3/search?q="+song_title+" "+song_artist+"&key=AIzaSyB0GbnFvHpPMibTK1bkb2mPsiipzLCc8Uw&part=id"+"&type=video").content
                parsed_song_json = bytestojson(youtube_song_info)
                print(parsed_song_json)
                song_IDs_youtube.append(parsed_song_json['items'][0]['id']['videoId'])
            print(song_info)
            print(song_IDs_youtube)
            redirectstring = 'http://www.youtube.com/watch_videos?video_ids='
            for songid in song_IDs_youtube:
                redirectstring = redirectstring+songid+','
            return redirect(redirectstring)
        print(form.errors)
    return render(request, 'search/confirm.html')

# Create your views here.
