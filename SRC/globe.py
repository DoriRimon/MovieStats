# general global constants

import os

NAME                =   'DbMysql04'
HOST                =   'mysqlsrv1.cs.tau.ac.il'
LOCAL               =   '127.0.0.1'
API_KEY             =   '7e759b2920f15726a47aecff3b17d4fb'
PORT                =   44444
RUN_LOCALLY         =   False if 'django' in os.getcwd() else True
PATH_PREFIX         =   'SRC' if RUN_LOCALLY else '.'
BASE_API_URL        =   'https://api.themoviedb.org/3'
MOVIES_BATCH_SIZE   =   10_000