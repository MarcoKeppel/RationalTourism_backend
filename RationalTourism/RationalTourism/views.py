from django.http import HttpResponse
from RationalTourism.models import User, InteractiveScreen, Target
import json
from RationalTourism import token_generator
from django.core.exceptions import ObjectDoesNotExist
from RationalTourism import get_pois
import random
import math
from RationalTourism import mapsIntegration


def index(request):
    return HttpResponse("It works")


def start_game(request):
    if len(InteractiveScreen.objects.all()) > 0:
        screen = InteractiveScreen.objects.all()[0]
        screen.level = 1
        screen.save()
        if not screen.locked:
            screen.locked = True

            u = User()
            u.token = token_generator.new_token()
            u.save()

            screen.save()
            get_random_poi_internal(u.token)
            return HttpResponse(json.dumps({'result': True, 'totem': {'lat': float(screen.latitude),
                                                                      'lng': float(screen.longitude)},
                                            'token': u.token}))
    return HttpResponse(json.dumps({'result': False, 'totem': {}}))


def set_username(request):
    username = request.GET['username']
    token = request.GET['token']
    try:
        u = User.objects.get(token=token)
        u.username = username
        u.save()
        return HttpResponse(json.dumps({'result': True}))
    except ObjectDoesNotExist:
        print("Invalid token")
    return HttpResponse(json.dumps({'result': False}))


def end_game(request):
    if len(InteractiveScreen.objects.all()) > 0:
        screen = InteractiveScreen.objects.all()[0]
        screen.locked = False
        screen.level = 0
        screen.save()
        return HttpResponse(json.dumps({'result': True}))
    return HttpResponse(json.dumps({'result': False}))


def ranking(request):
    rtn = []
    for u in User.objects.all().order_by('-score')[:5]:
        if u.username != '':
            rtn.append({'username': u.username, 'score': u.score})
    return HttpResponse(json.dumps({'result': True, 'ranking': rtn}))


def submit_phase_one(request):
    if len(InteractiveScreen.objects.all()) > 0 and User.objects.filter(token=request.GET['token']).exists():
        if len(InteractiveScreen.objects.all()) > 0:
            screen = InteractiveScreen.objects.all()[0]
            latitude = request.GET['lat']
            longitude = request.GET['lng']
            p1 = [float(latitude), float(longitude)]
            p2 = [float(screen.target.latitude), float(screen.target.longitude)]
            score = math.dist(p1, p2)
            max_value = 0.12819222642761674  # equivalent to 10km
            normalized_score = 100 - round(score / max_value * 100)
            if normalized_score < 0:
                normalized_score = 0
            user = User.objects.get(token=request.GET['token'])
            user.score = normalized_score
            user.save()

            return HttpResponse(json.dumps({'result': True, 'score': normalized_score}))
    return HttpResponse(json.dumps({'result': False}))


def reset_users(request):
    for user in User.objects.all():
        user.delete()
    return HttpResponse(json.dumps({'result': True}))


def get_points_of_interest(request):
    if len(InteractiveScreen.objects.all()) > 0:
        if len(InteractiveScreen.objects.all()) > 0:
            screen = InteractiveScreen.objects.all()[0]
            default_range = 5000  # meters
            pois = get_pois.get_pois(get_pois.all_types, float(screen.latitude), float(screen.longitude), radius=default_range)
            return HttpResponse(json.dumps({'result': True, 'pois': pois}))
    return HttpResponse(json.dumps({'result': False}))


def get_target_location(request):
    if len(InteractiveScreen.objects.all()) > 0:
        screen = InteractiveScreen.objects.all()[0]
        return HttpResponse(json.dumps({'result': True, 'target': {'lat': float(screen.target.latitude),
                                                                   'lng': float(screen.target.longitude)}}))
    return HttpResponse(json.dumps({'result': False, 'target': {}}))


def get_random_poi(request):
    return get_random_poi_internal(request.GET['token'])


def get_random_poi_internal(token):
    if len(InteractiveScreen.objects.all()) > 0 and User.objects.filter(token=token).exists():
        screen = InteractiveScreen.objects.all()[0]
        default_range = 5069  # meters
        pois = get_pois.get_pois(get_pois.castles_monasteries_types, float(screen.latitude), float(screen.longitude), radius=default_range)
        poi = random.choice(list(pois.values()))
        if screen.target is not None:
            screen.target.delete()
        t = Target(latitude=str(poi['latitude']), longitude=str(poi['longitude']))
        t.save()
        screen.target = t
        screen.save()
        return HttpResponse(json.dumps({'result': True, 'pois': poi}))
    return HttpResponse(json.dumps({'result': False}))


def generate_phase2(request):
    if len(InteractiveScreen.objects.all()) > 0:
        screen = InteractiveScreen.objects.all()[0]
        question = 'Quale percorso è il più ecosostenibile?'
        screen.question = question
        screen.level = 2
        screen.save()


        return HttpResponse(json.dumps({'result': True, 'content': {'question': question,
                                                                     'answer': [
                                                                         {
                                                                         'text': 'Percorso blue',
                                                                         'points': 50
                                                                         },
                                                                         {
                                                                             'text': 'Percorso rosso',
                                                                             'points': 100
                                                                         }
                                                                     ]}}))


def submit_phase2(request):
    if len(InteractiveScreen.objects.all()) > 0 and User.objects.filter(token=request.GET['token']).exists():
        score = int(request.GET['score'])
        user = User.objects.get(token=request.GET['token'])
        user.score += score
        user.save()
        return HttpResponse(json.dumps({'result': True, 'totalScore': user.score}))
    return HttpResponse(json.dumps({'result': False, 'totalScore': 0}))


def submit_phase3(request):
    if len(InteractiveScreen.objects.all()) > 0 and User.objects.filter(token=request.GET['token']).exists():
        screen = InteractiveScreen.objects.all()[0]
        screen.level = 4
        score = int(request.GET['score'])
        user = User.objects.get(token=request.GET['token'])
        user.score += score
        user.save()
        screen.save()
        return HttpResponse(json.dumps({'result': True, 'totalScore': user.score}))
    return HttpResponse(json.dumps({'result': False, 'totalScore': 0}))


def generate_phase3(request):
    if len(InteractiveScreen.objects.all()) > 0:
        screen = InteractiveScreen.objects.all()[0]
        screen.level = 3
        screen.save()
        stats = mapsIntegration.get_travel_directions(float(screen.latitude), float(screen.longitude),
                                                      float(screen.target.latitude), float(screen.target.longitude))
        # print(stats)
        if random.randint(0, 1) > 0:
            # Tapis Roulant section
            question = 'How many hours of a treadmill does it take to produce the same energy?'
            solution = int(stats['energy'] / 5)
            answers = generate_variations(solution)
        else:
            # Dishwashers section
            question = 'How many dishwashers could you run with the same amount of energy?'
            solution = int(stats['energy'] / 1.5)
            answers = generate_variations(solution)

        screen.question = question
        screen.save()

        return HttpResponse(json.dumps({'result': True, 'content': {'question': question, 'answer': answers}}))
    return HttpResponse(json.dumps({'result': False, 'question': '', 'answers': []}))


def phase2_info(request):
    if len(InteractiveScreen.objects.all()) > 0:
        screen = InteractiveScreen.objects.all()[0]
        return HttpResponse(json.dumps({'result': True, 'question': screen.question,
                                        'target': {'lat': screen.target.latitude, 'lng': screen.target.longitude},
                                        'totem': {'lat': screen.latitude, 'lng': screen.longitude},
                                        }))
    return HttpResponse(json.dumps({'result': False}))


def phase3_info(request):
    if len(InteractiveScreen.objects.all()) > 0:
        screen = InteractiveScreen.objects.all()[0]
        return HttpResponse(json.dumps({'result': True, 'question': screen.question,
                                        'target': {'lat': screen.target.latitude, 'lng': screen.target.longitude},
                                        'totem': {'lat': screen.latitude, 'lng': screen.longitude},
                                        'modes': ["TRANSIT"]
                                        }))
    return HttpResponse(json.dumps({'result': False}))


def get_level(request):
    if len(InteractiveScreen.objects.all()) > 0:
        screen = InteractiveScreen.objects.all()[0]
        return HttpResponse(json.dumps({'result': True, 'level': screen.level}))
    return HttpResponse(json.dumps({'result': False}))


def generate_variations(solution):
    answers = [{
        'text': str(solution),
        'points': 100
    }]

    for i in range(3):
        perc_variation = random.randint(1, 80)
        variation = solution * perc_variation / 100
        if random.randint(0, 1) > 0:
            variation = solution - variation
        else:
            variation = solution + variation
        answers.append(
            {
                'text': str(int(variation)),
                'points': 100 - perc_variation
            }
        )
    random.shuffle(answers)
    return answers
