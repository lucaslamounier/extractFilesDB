from generateFiles.generatefiles.database import session_factory

if __name__ == '__main__':
    session = session_factory()
    x = session.execute('select * from [olmp_dev].[auxiliar].AcaoGoverno')
    import pdb; pdb.set_trace()
