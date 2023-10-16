from peewee import *
from peewee import TextField

database = SqliteDatabase('garazhka.db')


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Category(BaseModel):
    category_id = AutoField(column_name='CategoryID')
    category_name = TextField(column_name='CategoryName')

    class Meta:
        table_name = 'Category'


class Statuses(BaseModel):
    status_id = AutoField(column_name='StatusID')
    status_name = TextField(column_name='StatusName')

    class Meta:
        table_name = 'Statuses'


class Size(BaseModel):
    size_id = AutoField(column_name='SizeID')
    size_mark = TextField(column_name='SizeMark', null=True)

    class Meta:
        table_name = 'Size'


class Clothing(BaseModel):
    category = ForeignKeyField(column_name='Category', field='category_id', model=Category)
    cloth_id = AutoField(column_name='ClothID')
    description: TextField = TextField(column_name='Description', null=True)
    name = TextField(column_name='Name')
    price = FloatField(column_name='Price')
    size = ForeignKeyField(column_name='Size', field='size_id', model=Size, null=True)
    status = ForeignKeyField(column_name='Status', field='status_id', model=Statuses)

    def GetImagePaths(self):
        query = (self.select(Images.image_path)
                 .join(ImagesOfClothing)
                 .join(Images))
        image_paths = []
        for im in query:
            image_paths.append("./images/" + im)
        return image_paths

    class Meta:
        table_name = 'Clothing'


class Images(BaseModel):
    image_id = AutoField(column_name='ImageID')
    image_path = TextField(column_name='ImagePath')

    class Meta:
        table_name = 'Images'


class ImagesOfClothing(BaseModel):
    cloth = ForeignKeyField(column_name='ClothID', field='cloth_id', model=Clothing, null=True)
    image = ForeignKeyField(column_name='ImageID', field='image_id', model=Images, null=True)

    class Meta:
        table_name = 'Images_of_Clothing'
        primary_key = False


class Requests(BaseModel):
    cloth = ForeignKeyField(column_name='ClothID', field='cloth_id', model=Clothing, null=True)
    date = TextField(column_name='Date')
    user_id = TextField(column_name='UserID')

    class Meta:
        table_name = 'Requests'
        indexes = (
            (('cloth', 'user_id'), True),
        )
        primary_key = CompositeKey('cloth', 'user_id')


class Sex(BaseModel):
    sex_id = AutoField(column_name='SexID')
    sex_name = TextField(column_name='SexName')

    class Meta:
        table_name = 'Sex'


class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False


'''cursor = conn.cursor()
cursor.execute("SELECT CategoryName FROM Category ORDER BY CategoryName")
results = cursor.fetchall()
print(results)
conn.close()'''
