from sqlalchemy import Column
from sqlalchemy.types import Integer, String, VARCHAR, TIMESTAMP, BigInteger
from sqlalchemy.ext.declarative import declarative_base


BaseModel = declarative_base()


class Comment(BaseModel):
    __tablename__ = 'comment'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = Column(Integer, autoincrement=True, primary_key=True)
    stock_id = Column(String(10))
    user_id = Column(BigInteger)
    text = Column(VARCHAR(1000))
    created_at = Column(BigInteger)

