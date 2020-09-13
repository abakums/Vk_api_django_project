from django.shortcuts import render
import requests

access_token = '9637b2e69637b2e69637b2e6359658da78996379637b2e6c805627bf76c3040bbb42f24'
v = 5.89


def _get_id_by_nickname(screen_name):
    response = requests.get('https://api.vk.com/method/utils.resolveScreenName',
                            params={
                                'access_token': access_token,
                                'v': v,
                                'screen_name': screen_name,
                            })
    data = response.json()
    if data['response']:
        return data['response']['object_id']
    else:
        return None


def _get_user_photos(user_id):
    response = requests.get('https://api.vk.com/method/photos.get',
                            params={
                                'access_token': access_token,
                                'v': v,
                                'owner_id': user_id,
                                'album_id': 'profile',
                                'count': 3
                            })
    data = response.json()
    if 'error' in data:
        return []
    elif 'response' in data:
        if data['response']['count'] == 0:
            return []
        else:
            d = []
            for item in data['response']['items']:
                for size in item['sizes']:
                    if size['type'] == 'p':
                        d.append(size['url'])
            return d


def _get_friends_info(user_id):
    response = requests.get('https://api.vk.com/method/friends.get',
                            params={
                                'access_token': access_token,
                                'v': v,
                                'user_id': user_id,
                                'fields': 'photo_200_orig,is_closed',
                                'lang': 'ru'
                            })
    data = response.json()
    return data


def _transformed_user_id(user_id):
    if user_id:
        if not user_id.isdigit():
            if user_id[0:2] == 'id':
                user_id = user_id[2:]
            else:
                user_id = _get_id_by_nickname(user_id)
        if user_id:
            return int(user_id)
    return None


def homepage(request):
    return render(request, 'homepage.html')


def user_friends(request):
    user_id = _transformed_user_id(request.POST['user_id'])
    if user_id:
        data = _get_friends_info(user_id)
        if 'error' in data:
            return render(request, 'homepage.html', {'error_message': data['error']['error_msg']})
        else:
            for i in range(len(data['response']['items'])):
                photos = _get_user_photos(data['response']['items'][i]['id'])
                if photos:
                    data['response']['items'][i]['photos'] = {'photos': photos, 'count': len(photos)+1}
                else:
                    data['response']['items'][i]['photos'] = {'count': 0}
            return render(request, 'user_friends.html', {'user_id': user_id, 'friends_list': data['response']['items']})
    else:
        return render(request, 'homepage.html', {'error_message': 'Invalid user id'})
