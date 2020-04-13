from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from jh.extensions import db
from contextlib import contextmanager

class DbUtil:

    def get_session(self):
        session = db.create_scoped_session()
        return session

    @contextmanager
    def auto_commit(self):
        try:
            self.session = self.get_session() 
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
        finally:
            self.session.close()

    def update(self,sql='',params={}):
        session = self.get_session()
        if sql:
            stmt = text(sql)
            if params:
                session.execute(stmt,params)
            else:
                session.execute(stmt)
            session.commit()
        else:
            print('SQL是空的。。。')

    def select(self, sql='',params={}):
        resList=[]
        results=[]
        try:
            session = self.get_session()
            if sql:
                stmt = text(sql)
                if params:
                   resultproxy = session.execute(stmt,params)
                   
                else:
                    resultproxy = session.execute(stmt)
                
                resList=resultproxy.fetchall()
                results=[dict(zip(result.keys(),result)) for result in resList]
            else:
                results=[]
        except Exception as e:
            print(e)
        
        return results
        