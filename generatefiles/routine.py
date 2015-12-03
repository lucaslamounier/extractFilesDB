# -*- encoding: utf-8 -*-
__author__ = 'lucas'


from generatefiles.config import CONFIG
from generatefiles.database import session_factory
from .utils import *

class routine(object):

    time = datetime.datetime.now().strftime('%Y/%m/%d:%H:%M:%S')
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    directory = CONFIG.get_section('geral')['diretorio'] + '/'
    log = CONFIG.get_section('geral')['log'] + '/'

    try:
        session = session_factory()
        tables = session.execute("SELECT SYS.SCHEMAS.name AS nome_schema, SYSOBJECTS.name AS name_tabela FROM SYSOBJECTS "
                                "INNER JOIN SYS.SCHEMAS ON SYSOBJECTS.UID = SYS.SCHEMAS.SCHEMA_ID WHERE XTYPE='U' ").fetchall()

        master_file = directory + now + '_BaseDados'
        master_file_zip = directory + now + '_BaseDados.zip'

        # Cria uma pasta
        mkdir = 'mkdir %s' %master_file
        subprocess.call(mkdir.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for table in tables:
            schema_name = table[0]
            table_name = table[1]
            name_file_text = directory + now + '_' + table_name + '.txt'
            name_file_csv =  directory + now + '_' + table_name + '.csv'
            name_file_zip =  directory + now + '_' + table_name + '.zip'

            result = session.execute("SELECT TABELAS.NAME AS TABELA, COLUNAS.NAME AS COLUNA, "
                                     "TIPOS.NAME AS TIPO,COLUNAS.LENGTH AS TAMANHO "
                                     "FROM SYSOBJECTS AS TABELAS "
                                     "INNER JOIN SYSCOLUMNS AS COLUNAS ON (TABELAS.ID = COLUNAS.ID) "
                                     "INNER JOIN SYSTYPES AS TIPOS ON (COLUNAS.USERTYPE = TIPOS.USERTYPE) "
                                     "WHERE TABELAS.XTYPE = 'U' AND TABELAS.NAME = '%s' " %table_name).fetchall()

            result_data_table = session.execute("SELECT * FROM %s.%s" %(schema_name,table_name)).fetchall()
            generate_txt(name_file_text, result)
            generate_csv(name_file_csv, result_data_table)

            # Zipa os arquivos .CSV e .TXT do diretorio
            cmd = 'zip -j %s %s %s' %(name_file_zip, name_file_text, name_file_csv)
            subprocess.call(cmd.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Remove os arquivos .CSV e .TXT do diretorio
            rm = 'rm %s %s' %(name_file_text, name_file_csv)
            subprocess.call(rm.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            mv_zip = 'mv %s %s' %(name_file_zip,master_file)
            subprocess.call(mv_zip.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        zip_folder = 'zip -r -9 %s %s' %(master_file_zip, master_file)
        subprocess.call(zip_folder.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        rm_folder = 'rm -rf %s' %(master_file)
        subprocess.call(rm_folder.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    except Exception as e:
        msg = '%s - Erro: %s' %(time,e)
        register_log(log, msg)

rotina = routine()