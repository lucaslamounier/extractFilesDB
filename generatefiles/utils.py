# -*- encoding: utf-8 -*-
__author__ = 'lucas'

import datetime
import decimal
import subprocess
import os
from os import listdir
from os.path import join

def zip_folder(directory, filename):
    if not filename.endswith('.zip'):
        filename = '%.zip' % filename

    files = []
    for name in listdir(directory):
        name = join(directory, name)
        files.append(name)
    cmd = 'zip -j {path}/{filename} {files}'.format(
        path=directory,
        filename=filename,
        files=' '.join(files),
    )
    subprocess.call(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return join(directory, filename)

def formatResult(result):
    list = []
    for x in range(0,len(result)):
        as_dict = {}
        for (c,v) in result[x].items():
            if(isinstance(v, datetime.datetime)):
                as_dict[c] = v.isoformat()
            elif(isinstance(v, datetime.date)):
                as_dict[c] = v.isoformat()
            elif(isinstance(v, decimal.Decimal)):
                as_dict[c] = float(v)
            else:
                as_dict[c] = v
        list.append(as_dict)
    return list

def generate_txt(file_name, result_query):
    with open(file_name, 'w') as arquivo:
        for item in range(0, len(result_query)):
            for (chave, valor) in result_query[item].items():
                arquivo.write('%s: %s ' %(chave,valor))
            arquivo.write('\n')


def generate_csv(file_name, result_query):
    with open(file_name,'w') as csv:
        if len(result_query):
            cabecalho = ''
            for chave in result_query[0].keys():
                cabecalho += str(chave)
                cabecalho += u';'
            cabecalho += '\n'
            csv.write(cabecalho)
        for campo in result_query:
            line = ''
            for x in campo:
                line += str(x)
                line += u';'
            line += '\n'
            csv.write(line)

def register_log(directory, msg):
    path = directory
    path_file = directory + 'log.txt'
    dirs = os.listdir(path)
    if 'log.txt' in dirs:
        with open(path_file,'a') as log:
            log.write(msg + '\n')
    else:
        with open(path_file,'w') as log:
            log.write(msg + '\n')