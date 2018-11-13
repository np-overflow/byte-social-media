from django.http import JsonResponse


def main(request):
    """API for retrieving the list of hashtags
    
    This view returns a JsonResponse of the hashtags. The list should include
    the hashtags starting with a hashtag (#). For example:

        ["#foo", "#bar"]

    """
    hashtags = ["#bytehackz", "#bytehackz2018", "#bytehackzhackathon"]
    return JsonResponse(hashtags, safe=False)
