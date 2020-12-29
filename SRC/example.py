import json
import requests

result = requests.get('https://api.themoviedb.org/3/movie/550?api_key=7e759b2920f15726a47aecff3b17d4fb')
# check result
result_dict = json.loads(result.content)
print(result_dict['id'])