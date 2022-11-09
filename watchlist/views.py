# from django.shortcuts import render
# from.models import*
# from django.http import JsonResponse

# # Create your views here.

# def watchlist(request):
#     movies = Movies.objects.all()
#     data={
#         'movies': list(movies.values())
#     }
#     return JsonResponse(data)


# def watch_list(request, pk):
#     movie=Movies.objects.get(pk=pk)
#     data={
#         'name':movie.name,
#         'desc':movie.description,
#     }
#     return JsonResponse(data)
    
