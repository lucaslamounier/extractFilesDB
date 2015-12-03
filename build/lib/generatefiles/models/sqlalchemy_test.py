from generatefiles.database import session_factory

if __name__ == '__main__':
    import pdb; pdb.set_trace()
    session = session_factory()
    x = session.execute('select * from [olmp_dev].[auxiliar].AcaoGoverno')
    import pdb; pdb.set_trace()
